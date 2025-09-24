# RAG システム実装例

## 概要

LangChain を使用した RAG（Retrieval Augmented Generation）システムの実装例です。

## 基本的な RAG システム

```python
import os
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import chromadb

class PatentRAGSystem:
    def __init__(self, openai_api_key: str):
        """特許RAGシステムの初期化"""
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.1,
            openai_api_key=openai_api_key
        )
        self.vectorstore = None
        self.qa_chain = None

    def load_patent_documents(self, directory_path: str):
        """特許文献の読み込み"""
        # PDFファイルの読み込み
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()

        # テキストの分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        splits = text_splitter.split_documents(documents)

        return splits

    def create_vectorstore(self, documents):
        """ベクトルストアの作成"""
        # Chromaベクトルストアの作成
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory="./patent_chroma_db"
        )

        # QAチェーンの作成
        self._create_qa_chain()

    def _create_qa_chain(self):
        """QAチェーンの作成"""
        # 特許分析用のプロンプトテンプレート
        prompt_template = """
        あなたは特許分析の専門家です。以下の特許文献の情報を基に、質問に回答してください。

        特許文献の情報:
        {context}

        質問: {question}

        回答は以下の形式で提供してください：
        1. 技術的要約
        2. 主要な特徴
        3. 先行技術との違い
        4. 実装可能性
        5. 関連する技術分野

        回答:
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # RetrievalQAチェーンの作成
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            ),
            chain_type_kwargs={"prompt": prompt}
        )

    def search_patents(self, query: str, top_k: int = 5):
        """特許文献の検索"""
        if not self.vectorstore:
            raise ValueError("ベクトルストアが初期化されていません")

        # 類似度検索の実行
        docs = self.vectorstore.similarity_search(query, k=top_k)
        return docs

    def analyze_patent(self, question: str):
        """特許文献の分析"""
        if not self.qa_chain:
            raise ValueError("QAチェーンが初期化されていません")

        # 質問に対する回答を生成
        response = self.qa_chain.run(question)
        return response

    def generate_patent_report(self, technology_domain: str):
        """特許分析レポートの生成"""
        questions = [
            f"{technology_domain}分野の主要な技術動向は何ですか？",
            f"{technology_domain}分野で注目すべき特許はありますか？",
            f"{technology_domain}分野の技術的課題は何ですか？",
            f"{technology_domain}分野の将来展望はどうですか？"
        ]

        report = {
            "technology_domain": technology_domain,
            "analysis_results": []
        }

        for question in questions:
            answer = self.analyze_patent(question)
            report["analysis_results"].append({
                "question": question,
                "answer": answer
            })

        return report
```

## 高度な RAG システム

```python
# 高度な機能を追加したRAGシステム
class AdvancedPatentRAGSystem(PatentRAGSystem):
    def __init__(self, openai_api_key: str):
        super().__init__(openai_api_key)
        self.conversation_memory = []
        self.analysis_history = []

    def add_conversation_memory(self, query: str, response: str):
        """会話履歴の追加"""
        self.conversation_memory.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now()
        })

    def get_contextual_response(self, query: str):
        """文脈を考慮した回答生成"""
        # 過去の会話履歴を含めたコンテキスト作成
        context = self._build_conversation_context()

        # 文脈を考慮した質問の生成
        contextual_query = f"""
        過去の会話履歴:
        {context}

        現在の質問: {query}

        上記の文脈を考慮して回答してください。
        """

        response = self.analyze_patent(contextual_query)
        self.add_conversation_memory(query, response)

        return response

    def _build_conversation_context(self):
        """会話履歴のコンテキスト構築"""
        if not self.conversation_memory:
            return ""

        # 最新の5つの会話を取得
        recent_conversations = self.conversation_memory[-5:]
        context = ""

        for conv in recent_conversations:
            context += f"Q: {conv['query']}\nA: {conv['response']}\n\n"

        return context

    def export_analysis_report(self, format_type: str = "json"):
        """分析レポートのエクスポート"""
        report_data = {
            "conversation_history": self.conversation_memory,
            "analysis_history": self.analysis_history,
            "vectorstore_info": {
                "document_count": len(self.vectorstore.get()["documents"]) if self.vectorstore else 0
            }
        }

        if format_type == "json":
            return json.dumps(report_data, indent=2, default=str)
        elif format_type == "csv":
            # CSV形式でのエクスポート実装
            pass

        return report_data
```

## 使用例

```python
def main():
    # API キーの設定
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # RAGシステムの初期化
    rag_system = PatentRAGSystem(openai_api_key)

    # 特許文献の読み込み
    documents = rag_system.load_patent_documents("./patent_documents")

    # ベクトルストアの作成
    rag_system.create_vectorstore(documents)

    # 特許文献の検索
    search_results = rag_system.search_patents("AI技術の特許", top_k=3)
    print("検索結果:", search_results)

    # 特許文献の分析
    analysis_result = rag_system.analyze_patent("この特許の技術的新規性は何ですか？")
    print("分析結果:", analysis_result)

    # レポートの生成
    report = rag_system.generate_patent_report("人工知能")
    print("レポート:", report)

if __name__ == "__main__":
    main()
```

## 環境構築

```bash
# 必要なライブラリのインストール
pip install langchain langchain-openai openai chromadb faiss-cpu tiktoken

# 環境変数の設定
export OPENAI_API_KEY="your-openai-api-key"
```

## 実行結果の例

```
質問: RAGシステムにおけるベクトルデータベースの役割は何ですか？
回答: RAGシステムにおいて、ベクトルデータベースは外部の知識ベースから関連情報を検索するという中心的な役割を果たします。
これにより、LLMが持つ知識を補強し、ハルシネーションを抑制することができます。

--- 検索された関連チャンク ---
RAGシステムは、外部の知識ベースから関連情報を検索し、その情報を基にLLMが回答を生成する仕組みです。
--------------------
ベクトルデータベースは、この情報検索のステップで中心的な役割を果たします。
--------------------
```

## まとめ

- 今回提示した技術スタックを利用することで、自由に RAG システムを構築可能
- 市販品や RAG システムでは制御できない部分まで制御可能

* **LangChain** が全体のパイプライン（データ読み込み、分割、LLM 連携）を管理。
* **OpenAI Embeddings** がテキストの意味を捉えるためのベクトルを生成。
* **FAISS / Chroma / Pinecone** がベクトルを効率的に保存・検索する。

まずは FAISS や Chroma で小規模なプロトタイプを構築し、その仕組みを理解した上で、要件に応じて Pinecone のようなスケーラブルなソリューションへ移行する。
