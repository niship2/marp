# LangGraphを使ってリファクタリングした統合自動化システム
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# --- 1. 状態定義 ---
class PipelineState(TypedDict):
    requirements: str
    system_design: str
    code_files: List[str]
    automation_scripts: List[str]

# --- 2. ダミーのクライアント ---
def dummy_claude_code_client(reqs):
    print("--- ノード: システム設計 (Claude) ---")
    return f"'{reqs}' に基づくシステム設計書"

def dummy_cursor_client(design):
    print("--- ノード: コード生成 (Cursor) ---")
    return ["main.py", "utils.py"]

def dummy_gemini_cli_client(files):
    print("--- ノード: スクリプト生成 (Gemini) ---")
    return ["run.sh", "test.sh"]

def dummy_scheduler(scripts):
    print("--- ノード: タスク登録 (Scheduler) ---")
    print(f"{scripts} をスケジューラーに登録しました。")

# --- 3. ノード関数の定義 ---
def design_system(state: PipelineState):
    design = dummy_claude_code_client(state["requirements"])
    return {"system_design": design}

def generate_code(state: PipelineState):
    files = dummy_cursor_client(state["system_design"])
    return {"code_files": files}

def generate_scripts(state: PipelineState):
    scripts = dummy_gemini_cli_client(state["code_files"])
    return {"automation_scripts": scripts}

def register_tasks(state: PipelineState):
    dummy_scheduler(state["automation_scripts"])
    return {}

# --- 4. グラフの構築 ---
workflow = StateGraph(PipelineState)
workflow.add_node("design_system", design_system)
workflow.add_node("generate_code", generate_code)
workflow.add_node("generate_scripts", generate_scripts)
workflow.add_node("register_tasks", register_tasks)

workflow.set_entry_point("design_system")
workflow.add_edge("design_system", "generate_code")
workflow.add_edge("generate_code", "generate_scripts")
workflow.add_edge("generate_scripts", "register_tasks")
workflow.add_edge("register_tasks", END)

app = workflow.compile()

# --- 5. 実行 ---
if __name__ == "__main__":
    print("=== LangGraphによる統合自動化パイプライン デモンストレーション ===\n")
    
    requirements = "ユーザー認証機能を持つWebアプリケーション"
    inputs = {"requirements": requirements}
    
    final_state = app.invoke(inputs)
    
    print("\n=== パイプライン完了 ===")
    print(f"最終状態: {final_state}")