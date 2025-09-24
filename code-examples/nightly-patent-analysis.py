# LangGraphを使ってリファクタリングした夜間バッチ処理システム
import os
import json
import sqlite3
import time
import schedule
import logging
from datetime import datetime, timedelta
from typing import TypedDict, Dict, Any, List, Optional

from langgraph.graph import StateGraph, END

# --- 1. LangGraphの状態定義 ---
class NightlyRunState(TypedDict):
    config: Dict[str, Any]
    run_id: Optional[int]
    task_results: Dict[str, Any]
    overall_status: str
    error_messages: List[str]
    summary: str

# --- 元のクラスのロジックを関数として分割 ---

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{log_dir}/nightly_analysis_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

LOGGER = setup_logging()

def load_config(config_file: str) -> Dict[str, Any]:
    default_config = {
        'analysis_tasks': {
            'patent_search': {'enabled': True},
            'document_processing': {'enabled': True},
            'specification_generation': {'enabled': False}
        }
    }
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            default_config.update(user_config)
    except FileNotFoundError:
        LOGGER.warning(f"設定ファイルが見つかりません: {config_file}。デフォルト設定を使用します。")
    return default_config

# --- 2. ノード関数の定義 ---

def start_run(state: NightlyRunState):
    LOGGER.info("--- ノード: start_run ---")
    # ここでDBに実行開始を記録するなどの処理が入る
    return {"task_results": {}, "overall_status": "running", "error_messages": [], "summary": ""}

def patent_search_node(state: NightlyRunState):
    LOGGER.info("--- ノード: patent_search ---")
    # 本来の処理のダミー
    result = {'status': 'success', 'data': {'new_patents': 5}}
    state['task_results']['patent_search'] = result
    if result['status'] == 'error':
        state['error_messages'].append("Patent search failed.")
    return {"task_results": state['task_results'], "error_messages": state['error_messages']}

def document_processing_node(state: NightlyRunState):
    LOGGER.info("--- ノード: document_processing ---")
    result = {'status': 'success', 'data': {'documents_processed': 10}}
    state['task_results']['document_processing'] = result
    return {"task_results": state['task_results']}

def spec_generation_node(state: NightlyRunState):
    LOGGER.info("--- ノード: spec_generation ---")
    result = {'status': 'success', 'data': {'specifications_generated': 2}}
    state['task_results']['specification_generation'] = result
    return {"task_results": state['task_results']}

def finalize_run(state: NightlyRunState):
    LOGGER.info("--- ノード: finalize_run ---")
    status = 'success' if not state['error_messages'] else 'partial_failure'
    summary = f"実行サマリー: {len(state['task_results'])}個のタスクを実行し、ステータスは {status} です。"
    LOGGER.info(f"最終ステータス: {status}")
    # ここでDB更新や通知送信を行う
    return {"overall_status": status, "summary": summary}

# --- 3. 条件付きエッジの定義 ---
def should_run_search(state: NightlyRunState):
    return "patent_search_node" if state['config']['analysis_tasks']['patent_search']['enabled'] else "document_processing_branch"

def should_run_processing(state: NightlyRunState):
    return "document_processing_node" if state['config']['analysis_tasks']['document_processing']['enabled'] else "spec_generation_branch"

def should_run_spec_gen(state: NightlyRunState):
    return "spec_generation_node" if state['config']['analysis_tasks']['specification_generation']['enabled'] else "finalize_run"

# --- 4. グラフの構築 ---
class NightlyPatentAnalysisWorkflow:
    def __init__(self):
        workflow = StateGraph(NightlyRunState)
        workflow.add_node("start_run", start_run)
        workflow.add_node("patent_search_node", patent_search_node)
        workflow.add_node("document_processing_node", document_processing_node)
        workflow.add_node("spec_generation_node", spec_generation_node)
        workflow.add_node("finalize_run", finalize_run)

        workflow.set_entry_point("start_run")
        workflow.add_conditional_edges("start_run", should_run_search, {
            "patent_search_node": "patent_search_node",
            "document_processing_branch": "document_processing_node" # スキップして次へ
        })
        workflow.add_conditional_edges("patent_search_node", should_run_processing, {
            "document_processing_node": "document_processing_node",
            "spec_generation_branch": "spec_generation_node" # スキップして次へ
        })
        workflow.add_conditional_edges("document_processing_node", should_run_spec_gen, {
            "spec_generation_node": "spec_generation_node",
            "finalize_run": "finalize_run"
        })
        workflow.add_edge("spec_generation_node", "finalize_run")
        workflow.add_edge("finalize_run", END)
        self.app = workflow.compile()

    def run(self, config: Dict[str, Any]):
        initial_state = {"config": config}
        return self.app.invoke(initial_state)

# --- 5. 元のクラスをリファクタリング ---
class NightlyPatentAnalysis:
    def __init__(self, config_file: str = "nightly_config.json"):
        self.config = load_config(config_file)
        self.workflow = NightlyPatentAnalysisWorkflow()

    def run_nightly_analysis(self):
        start_time = datetime.now()
        LOGGER.info(f"夜間分析を開始します (LangGraph版): {start_time}")
        final_state = self.workflow.run(self.config)
        duration = datetime.now() - start_time
        LOGGER.info(f"夜間分析完了: {final_state['overall_status']}, 実行時間: {duration}")
        LOGGER.info(f"サマリー: {final_state['summary']}")

    def start_scheduler(self):
        start_time = self.config.get('schedule', {}).get('start_time', '02:00')
        LOGGER.info(f"スケジューラーを開始します: 毎日{start_time}実行")
        schedule.every().day.at(start_time).do(self.run_nightly_analysis)
        while True:
            schedule.run_pending()
            time.sleep(60)

# --- 実行 ---
if __name__ == "__main__":
    analyzer = NightlyPatentAnalysis()
    LOGGER.info("テスト実行を開始します (1回のみ)")
    analyzer.run_nightly_analysis()
