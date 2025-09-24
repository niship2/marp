# LangChainを使って書き換えた特許文献一括処理システム
import os
import pandas as pd
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda

# --- 1. LLMとパーサーの準備 ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
json_parser = JsonOutputParser()

# --- 2. 分析チェーンの定義 ---
analysis_prompt = ChatPromptTemplate.from_template(
    """あなたは特許分析の専門家です。以下の特許文献のテキストを分析してください。
分析項目は以下の通りです。
1. 主要な技術用語（上位10個）
2. 重要度スコア（1.0〜10.0）
3. スコアの理由

{format_instructions}

特許文献テキスト:
---
{document_text}
---
""").partial(format_instructions=json_parser.get_format_instructions())

def get_text_from_doc(doc):
    return doc.page_content

analysis_chain = (
    {"document_text": RunnableLambda(get_text_from_doc)}
    | analysis_prompt
    | llm
    | json_parser
)

# --- 3. メイン処理クラス ---
class PatentDocumentProcessor:
    def __init__(self, input_directory: str, output_directory: str):
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def process_directory(self) -> List[Dict[str, Any]]:
        """ディレクトリ内の全PDFファイルを一括処理する"""
        print(f"処理対象ディレクトリ: {self.input_directory}")
        loader = DirectoryLoader(
            self.input_directory, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True, use_multithreading=True
        )
        documents = loader.load()
        
        if not documents:
            print("処理対象のPDFファイルが見つかりませんでした。")
            return []
            
        print(f"{len(documents)}個のファイルをロードしました。分析を開始します...")
        results = analysis_chain.with_fallbacks(
            fallbacks=[RunnableLambda(lambda x: {"error": str(x)})]
        ).map(documents)
        
        final_results = []
        for doc, result in zip(documents, results):
            if "error" not in result:
                result['file_name'] = os.path.basename(doc.metadata.get('source', ''))
                final_results.append(result)
            else:
                print(f"ファイル処理エラー: {doc.metadata.get('source', '')} - {result['error']}")

        self.export_to_csv(final_results)
        return final_results

    def export_to_csv(self, results: List[Dict[str, Any]]):
        """結果をCSVファイルに出力する"""
        if not results:
            print("エクスポートする結果がありません。")
            return
            
        output_path = os.path.join(self.output_directory, "patent_analysis_results.csv")
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"分析結果を {output_path} に保存しました。")

# --- 4. 実行 ---
if __name__ == "__main__":
    print("=== LangChainによる特許文献一括処理 デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します.\n")

    input_dir = "./patent_documents_demo"
    output_dir = "./analysis_results_demo"
    os.makedirs(input_dir, exist_ok=True)
    
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(os.path.join(input_dir, "dummy_patent_1.pdf"))
        c.drawString(72, 720, "Invention: AI Drug Discovery System. Abstract: This invention relates to an AI drug discovery system that generates novel compounds using deep learning.")
        c.save()
        print("デモ用のPDFファイルを作成しました。")
    except ImportError:
        print("PDF生成ライブラリ(reportlab)がありません。`pip install reportlab`でインストールしてください。")

    processor = PatentDocumentProcessor(input_directory=input_dir, output_directory=output_dir)
    processor.process_directory()
