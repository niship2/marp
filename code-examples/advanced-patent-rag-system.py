# langchainを使った高度なRAGシステム
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document

# ベースとなるRAGシステムをインポート
from patent_rag_system import PatentRAGSystem

class AdvancedPatentRAGSystem(PatentRAGSystem):
    """`PatentRAGSystem` を継承し、高度な検索・分析機能を追加したクラス"""

    def __init__(self, openai_api_key: str):
        """高度なRAGシステムの初期化"""
        super().__init__(openai_api_key)
        self.advanced_chain = None
        self._setup_advanced_pipeline()

    def _setup_advanced_pipeline(self):
        """Multi-Query, RAG-Fusion, Rerank を組み込んだ高度なパイプラインを構築"""
        # ダミーの特許ドキュメントを作成 (本来は `load_patent_documents` を使用)
        documents = [
            Document(page_content="AIを用いた画像認識技術に関する特許。特に、医療画像の診断支援への応用。", metadata={"id": "patent_001", "year": 2022}),
            Document(page_content="自然言語処理（NLP）を利用した自動要約システムの特許。長文の技術文書を効率的に要約する。", metadata={"id": "patent_002", "year": 2021}),
            Document(page_content="強化学習に基づくロボット制御技術。工場の組み立てラインでの自律的な作業を可能にする。", metadata={"id": "patent_003", "year": 2023}),
        ]

        # FAISSベクトルストアを作成 (Chromaの代わりにインメモリのFAISSを使用)
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # --- Multi-Query Retriever の実装 ---
        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five
            different versions of the given user question to retrieve relevant documents from
            a vector database. By generating multiple perspectives on the user question, your
            goal is to help the user overcome some of the limitations of distance-based
            similarity search. Provide these alternative questions separated by newlines.
            Original question: {question}""",
        )
        llm_chain = LLMChain(llm=self.llm, prompt=QUERY_PROMPT, output_key="text")
        multi_query_retriever = MultiQueryRetriever(
            retriever=base_retriever, llm_chain=llm_chain
        )

        # --- Rerank (リランキング) の実装 ---
        compressor = FlashrankRerank()
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=multi_query_retriever
        )

        # --- 高度なRAGパイプラインの構築 (LCEL) ---
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = PromptTemplate.from_template(template)

        self.advanced_chain = (
            {"context": compression_retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def analyze_patent(self, question: str):
        """基本的な分析機能を、高度なパイプラインを使ってオーバーライド"""
        if not self.advanced_chain:
            raise ValueError("高度なQAチェーンが初期化されていません")

        print(f"--- 高度な分析を実行中... ---")
        print(f"元のクエリ: {question}\n")

        # パイプラインを実行して回答を取得
        response = self.advanced_chain.invoke(question)
        return response

# 使用例
def main():
    print("=== 高度な特許RAGシステム デモンストレーション ===\n")

    # APIキーが設定されていない場合にダミーキーを設定
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        openai_api_key = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。")
        print("実際の分析を行うには、有効なAPIキーを設定してください。\n")

    # 高度なRAGシステムの初期化
    advanced_rag_system = AdvancedPatentRAGSystem(openai_api_key=openai_api_key)

    # 特許分析の実行 (オーバーライドされた `analyze_patent` が呼ばれる)
    query = "AIを使った自律的な作業に関する技術"
    analysis_result = advanced_rag_system.analyze_patent(query)

    print(f"--- 分析結果 ---\n{analysis_result}\n")
    print("\n=== デモンストレーション完了 ===")

if __name__ == "__main__":
    main()
