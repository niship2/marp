# 特許文献検索・分析システム (LCEL版)
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.docstore.document import Document

class PatentRAGSystem:
    def __init__(self, openai_api_key: str):
        """特許RAGシステムの初期化"""
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.llm = ChatOpenAI(
            model_name="gpt-4-turbo", temperature=0.1, openai_api_key=openai_api_key
        )
        self.vectorstore = None
        self.qa_chain = None

    def load_patent_documents(self, directory_path: str):
        """特許文献の読み込み"""
        loader = DirectoryLoader(
            directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader
        )
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        return text_splitter.split_documents(documents)

    def create_vectorstore(self, documents):
        """ベクトルストアの作成"""
        print("ベクトルストアを作成中...")
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings,
        )
        self._create_lcel_chain()
        print("ベクトルストアとQAチェーンの準備完了。")

    def _create_lcel_chain(self):
        """LCELを使ってQAチェーンを作成"""
        retriever = self.vectorstore.as_retriever()
        
        prompt_template = """あなたは特許分析の専門家です。以下の特許文献の情報を基に、質問に回答してください。

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
        prompt = PromptTemplate.from_template(prompt_template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.qa_chain = (
            { "context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def search_patents(self, query: str, top_k: int = 5):
        """特許文献の検索"""
        if not self.vectorstore:
            raise ValueError("ベクトルストアが初期化されていません")
        return self.vectorstore.similarity_search(query, k=top_k)

    def analyze_patent(self, question: str):
        """特許文献の分析 (LCELのinvokeを使用)"""
        if not self.qa_chain:
            raise ValueError("QAチェーンが初期化されていません")
        return self.qa_chain.invoke(question)

    def generate_patent_report(self, technology_domain: str):
        """特許分析レポートの生成"""
        questions = [
            f"{technology_domain}分野の主要な技術動向は何ですか？",
            f"{technology_domain}分野で注目すべき特許はありますか？",
            f"{technology_domain}分野の技術的課題は何ですか？",
            f"{technology_domain}分野の将来展望はどうですか？",
        ]
        report = {"technology_domain": technology_domain, "analysis_results": []}
        for question in questions:
            answer = self.analyze_patent(question)
            report["analysis_results"].append({"question": question, "answer": answer})
        return report

# 使用例
def main():
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します.\n")
    
    rag_system = PatentRAGSystem(os.getenv("OPENAI_API_KEY"))

    # ダミーの特許文献を作成 (ローカルファイル不要のデモ)
    dummy_docs = [
        Document(page_content="AIを用いた画像認識技術に関する特許。特に、医療画像の診断支援への応用。", metadata={"source": "doc1"}),
        Document(page_content="強化学習に基づくロボット制御技術。工場の組み立てラインでの自律的な作業を可能にする。", metadata={"source": "doc2"}),
    ]
    
    rag_system.create_vectorstore(dummy_docs)

    print("\n--- 検索テスト ---")
    search_results = rag_system.search_patents("AI技術の特許", top_k=1)
    print("検索結果:", search_results)

    print("\n--- 分析テスト ---")
    analysis_result = rag_system.analyze_patent("この特許の技術的新規性は何ですか？")
    print("分析結果:", analysis_result)

if __name__ == "__main__":
    main()