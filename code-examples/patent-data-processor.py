# LangChain (LCEL) を使って書き換えた特許データ一括処理システム
import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# --- 0. 環境設定 ---
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# --- 1. ダミーのAPIクライアントとLLMの準備 ---
# 本来のPatentAPIClientの代わりとなるダミー関数
def dummy_get_patent(patent_id: str) -> Dict[str, Any]:
    print(f"ダミーAPI呼び出し: {patent_id} の情報を取得")
    return {
        "id": patent_id,
        "title": f"特許{patent_id}の名称",
        "abstract": f"これは、特許{patent_id}の要約です。AIとデータ処理に関する革新的な内容を含んでいます。",
        "claims": [f"請求項1: {patent_id}を実現するためのシステム。"]
    }

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# --- 2. LCELを使った分析パイプラインの構築 ---

class PatentDataProcessor:
    def __init__(self, openai_api_key: str = None):
        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # --- 分析サブチェーンの定義 ---
        # 1. 技術要素を抽出するチェーン
        extract_prompt = ChatPromptTemplate.from_template(
            "特許データ（特に要約と請求項）から、主要な技術要素を箇条書きで5つ抽出してください。\n\n特許データ:\n{patent_data_str}"
        )
        self.extract_chain = extract_prompt | llm | StrOutputParser()

        # 2. 重要度を評価するチェーン
        importance_prompt = ChatPromptTemplate.from_template(
            "特許データから、その技術の新規性・市場性・影響を考慮し、10段階評価で重要度スコアを付けてください。理由も簡潔に述べてください。JSON形式（例: {{'score': 8, 'reason': '...'}}）で出力してください。\n\n特許データ:\n{patent_data_str}"
        )
        self.importance_chain = importance_prompt | llm | JsonOutputParser()

        # 3. 関連技術を検索するチェーン
        related_prompt = ChatPromptTemplate.from_template(
            "特許データから、関連する可能性のある技術分野やキーワードを3つ挙げてください。\n\n特許データ:\n{patent_data_str}"
        )
        self.related_chain = related_prompt | llm | StrOutputParser()

        # --- メイン分析チェーンの構築 ---
        # RunnableParallelを使って、3つのサブチェーンを並列実行
        self.analysis_chain = RunnableParallel(
            technical_elements=self.extract_chain,
            importance=self.importance_chain,
            related_technologies=self.related_chain,
        )

    def analyze_technology(self, patent_data: Dict[str, Any]) -> Dict[str, Any]:
        """単一の特許データを分析する"""
        # LCELは辞書を直接扱えるが、LLMへの入力は文字列が望ましいので変換
        patent_data_str = f"タイトル: {patent_data['title']}\n要約: {patent_data['abstract']}"
        return self.analysis_chain.invoke({"patent_data_str": patent_data_str})

    def process_patent_data_batch(self, patent_ids: List[str]) -> List[Dict[str, Any]]:
        """
        複数の特許データを一括で処理する
        LCELの .map() を使って、リストの各要素にチェーンを適用する
        """
        print(f"--- {len(patent_ids)}件の特許データを一括処理開始 ---")
        
        # 各IDに対してダミーAPI呼び出しと分析チェーンを連結した処理
        processing_chain = RunnablePassthrough.assign(
            patent_data=lambda x: dummy_get_patent(x["patent_id"])
        ) | RunnablePassthrough.assign(
            analysis=lambda x: self.analyze_technology(x["patent_data"])
        ) | (lambda x: {"patent_id": x["patent_id"], "analysis": x["analysis"]})

        # .map() を使ってリスト内の各IDにチェーンを適用
        results = processing_chain.map([{"patent_id": pid} for pid in patent_ids])
        
        print("--- 全ての処理が完了 ---")
        return results

# --- 3. 実行 ---
if __name__ == "__main__":
    print("=== LCELによる特許データ一括処理 デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    processor = PatentDataProcessor()
    
    patent_ids_to_process = ["JP2023-001", "JP2023-002", "JP2023-003"]
    
    batch_results = processor.process_patent_data_batch(patent_ids_to_process)

    import json
    print("\n--- 最終結果 ---")
    print(json.dumps(batch_results, indent=2, ensure_ascii=False))