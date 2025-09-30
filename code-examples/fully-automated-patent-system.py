# LangGraphを使ってリファクタリングした自動化システム
import os
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# --- 1. 状態定義 ---
class SystemState(TypedDict):
    new_data: List[str]
    analysis_results: Dict[str, Any]
    quality_score: float
    report: str
    cycle_count: int

# --- 2. ダミーのコンポーネント ---
def dummy_data_collector():
    print("--- ノード: データ収集 ---")
    return ["新しい特許データ1", "新しい特許データ2"]

def dummy_analyzer(data):
    print("--- ノード: 自動分析 ---")
    return {"summary": f"{len(data)}件のデータを分析しました。"}

def dummy_quality_checker(results):
    print("--- ノード: 品質チェック ---")
    score = 0.9  # ダミーのスコア
    print(f"品質スコア: {score}")
    return score

def dummy_report_generator(results):
    print("--- ノード: レポート生成 ---")
    return f"分析レポート: {results['summary']}"

def dummy_notification_system(report):
    print(f"--- ノード: 自動配信 ---")
    print(f"レポートを配信しました: {report}")

def dummy_learning_module(results, score):
    print("--- ノード: 学習・改善 ---")
    print(f"スコア{score}で結果を学習しました。")

# --- 3. ノード関数の定義 ---
def collect_data(state: SystemState):
    return {"new_data": dummy_data_collector()}

def analyze_data(state: SystemState):
    return {"analysis_results": dummy_analyzer(state["new_data"])}

def check_quality(state: SystemState):
    return {"quality_score": dummy_quality_checker(state["analysis_results"])}

def generate_report(state: SystemState):
    return {"report": dummy_report_generator(state["analysis_results"])}

def distribute_report(state: SystemState):
    dummy_notification_system(state["report"])
    return {}

def learn_from_results(state: SystemState):
    dummy_learning_module(state["analysis_results"], state["quality_score"])
    cycle_count = state.get("cycle_count", 0) + 1
    return {"cycle_count": cycle_count}

# --- 4. 条件付きエッジの定義 ---
def decide_to_generate_report(state: SystemState):
    return "generate_report" if state["quality_score"] > 0.8 else "learn_from_results"

def decide_to_continue(state: SystemState):
    # デモのため、3サイクルで終了
    return "collect_data" if state.get("cycle_count", 0) < 3 else END

# --- 5. グラフの構築 ---
workflow = StateGraph(SystemState)
workflow.add_node("collect_data", collect_data)
workflow.add_node("analyze_data", analyze_data)
workflow.add_node("check_quality", check_quality)
workflow.add_node("generate_report", generate_report)
workflow.add_node("distribute_report", distribute_report)
workflow.add_node("learn_from_results", learn_from_results)

workflow.set_entry_point("collect_data")
workflow.add_edge("collect_data", "analyze_data")
workflow.add_edge("analyze_data", "check_quality")
workflow.add_conditional_edges(
    "check_quality",
    decide_to_generate_report,
    {"generate_report": "generate_report", "learn_from_results": "learn_from_results"}
)
workflow.add_edge("generate_report", "distribute_report")
workflow.add_edge("distribute_report", "learn_from_results")
workflow.add_conditional_edges(
    "learn_from_results",
    decide_to_continue,
    {"collect_data": "collect_data", END: END}
)

app = workflow.compile()

# --- 6. 実行 ---
if __name__ == "__main__":
    print("=== LangGraphによる自動化システム デモンストレーション ===\n")
    # 初期状態で起動
    final_state = app.invoke({"cycle_count": 0})
    print("\n=== ワークフロー完了 ===")