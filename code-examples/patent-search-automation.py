# LangChain Agentを使って書き換えた特許検索自動化システム
import os
import schedule
import time
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# --- 1. ツールの定義 ---
@tool
def search_patent_api(keywords: List[str], days_back: int = 7) -> List[Dict[str, Any]]:
    """
    特許データベースAPIを叩いて、指定されたキーワードと期間に一致する特許を検索する。
    これはダミー実装であり、実際には外部APIを呼び出す。
    """
    print(f"--- ツール実行: search_patent_api (キーワード: {keywords}, {days_back}日前から) ---")
    results = [
        {
            "patent_number": f"JP2024-00{i+1}",
            "title": f"{kw}に関する画期的な発明",
            "abstract": f"これは{kw}の分野における重要な進歩です。",
        }
        for i, kw in enumerate(keywords)
    ]
    return results

@tool
def evaluate_patent_importance(patents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    LLMを使って、検索された特許リストの重要度を評価・スコアリングする。
    """
    print(f"--- ツール実行: evaluate_patent_importance ({len(patents)}件) ---")
    for patent in patents:
        patent["importance_score"] = round(7.0 + len(patent["title"]) * 0.1, 1)
        patent["reason"] = "新規性が高く、市場への影響が大きいため。"
    return patents

@tool
def save_to_database(patents: List[Dict[str, Any]]) -> str:
    """
    重要度評価済みの特許リストをデータベースに保存する。
    """
    print(f"--- ツール実行: save_to_database ({len(patents)}件) ---")
    print("以下の特許をDBに保存しました:")
    for p in patents:
        print(f"  - {p['patent_number']} (スコア: {p['importance_score']})")
    return f"{len(patents)}件の特許をデータベースに正常に保存しました。"

# --- 2. エージェントの作成 ---
class PatentSearchAutomationAgent:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        tools = [search_patent_api, evaluate_patent_importance, save_to_database]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは特許検索と分析を自動化するAIエージェントです。与えられたツールを順序立てて使い、タスクを完了させてください。"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def run_task(self, keywords: List[str]):
        """エージェントに検索・分析・保存のタスクを実行させる"""
        prompt = f"""以下のキーワードについて、日次の特許検索自動化タスクを実行してください: {keywords}
        手順は以下の通りです:
        1. `search_patent_api` を使って特許を検索します。
        2. 検索結果を `evaluate_patent_importance` に渡して、各特許の重要度を評価します。
        3. 評価後のリストを `save_to_database` に渡して、結果を保存します。
        """
        result = self.agent_executor.invoke({"input": prompt})
        return result['output']

# --- 3. スケジューリング ---
def job():
    print(f"\n--- 定期実行ジョブ開始: {time.ctime()} ---")
    config = {"search_keywords": ["AI", "machine learning"]} 
    agent = PatentSearchAutomationAgent()
    agent.run_task(config["search_keywords"])
    print(f"--- 定期実行ジョブ終了 ---")

if __name__ == "__main__":
    print("=== LangChain Agentによる特許検索自動化 デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    job() # まずは1回実行
