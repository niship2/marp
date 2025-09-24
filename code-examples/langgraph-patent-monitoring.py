# LangGraphを使用した特許監視ワークフロー（完成版）
import os
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.docstore.document import Document

# --- 0. 環境設定 ---
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# --- 1. LLMの準備 ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# --- 2. 状態の定義 ---
class PatentState(TypedDict):
    keywords: List[str]
    search_results: List[Document]
    analysis_results: Dict
    report: str

# --- 3. ワークフローの各ノード（関数）を定義 ---

def search_patents(state: PatentState):
    """キーワードに基づいて特許を検索する（ダミー実装）"""
    print(f"--- ノード: search_patents ---")
    keywords = state['keywords']
    print(f"検索キーワード: {keywords}")

    # 本来はここで特許データベースAPIを叩いたり、ベクトルストアを検索する
    # ここではデモ用にダミーの検索結果を生成
    results = [
        Document(page_content=f"{kw}に関する新しい技術。効率が20%向上。", metadata={"id": f"patent_{i+1}", "source": "dummy_db"})
        for i, kw in enumerate(keywords)
    ]
    print(f"検索結果: {len(results)}件")
    return {"search_results": results}

def analyze_patents(state: PatentState):
    """検索結果を分析する"""
    print(f"--- ノード: analyze_patents ---")
    search_results = state['search_results']
    if not search_results:
        print("分析対象の検索結果がありません。")
        return {"analysis_results": {"summary": "分析対象なし"}}

    # 検索結果を文字列にフォーマット
    context = "\n\n".join([doc.page_content for doc in search_results])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは特許分析の専門家です。与えられた特許情報のリストから、技術的な新規性、主要な出願人、および潜在的な影響について要約してください。"),
        ("user", "以下の特許情報を分析してください:\n\n{context}")
    ])
    chain = prompt | llm
    analysis = chain.invoke({"context": context}).content
    print("分析が完了しました。")
    return {"analysis_results": {"summary": analysis}}

def generate_report(state: PatentState):
    """分析結果からレポートを生成する"""
    print(f"--- ノード: generate_report ---")
    analysis_summary = state['analysis_results'].get('summary', '要約がありません。')
    keywords = state['keywords']

    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたはシニア特許アナリストです。提供された分析要約を基に、経営層向けの簡潔な週次レポートを作成してください。"),
        ("user", "監視キーワード: {keywords}\n\n分析要約:\n{summary}\n\n上記を基にレポートを作成してください。")
    ])
    chain = prompt | llm
    report = chain.invoke({"keywords": keywords, "summary": analysis_summary}).content
    print("レポートが生成されました。")
    return {"report": report}


# --- 4. ワークフローを構築・コンパイル ---
def create_patent_monitoring_workflow():
    """特許監視ワークフローのグラフを定義し、コンパイルする"""
    workflow = StateGraph(PatentState)

    # ノードの追加
    workflow.add_node("search", search_patents)
    workflow.add_node("analyze", analyze_patents)
    workflow.add_node("report", generate_report)

    # エッジの追加
    workflow.set_entry_point("search")
    workflow.add_edge("search", "analyze")
    workflow.add_edge("analyze", "report")
    workflow.add_edge("report", END)

    return workflow.compile()

# --- 5. ワークフローを実行 ---
if __name__ == "__main__":
    print("=== LangGraphによる特許監視ワークフロー デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    # ワークフローのコンパイル
    app = create_patent_monitoring_workflow()

    # 実行する入力
    inputs = {"keywords": ["量子コンピューティング", "AI創薬"]}

    # ワークフローの実行
    final_state = app.invoke(inputs)

    print("\n\n--- 最終レポート ---")
    print(final_state["report"])