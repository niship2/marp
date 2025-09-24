# LangChain Agentを使用して書き換えた特許調査エージェント
import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# --- 1. ツールの定義 ---
@tool
def patent_search_tool(query: str) -> str:
    """指定されたクエリに関連する特許を検索し、結果のリストを返す。"""
    print(f"--- ツール実行: patent_search_tool (クエリ: {query}) ---")
    return f"'{query}' に関連する特許として、JP2023-001とUS12345が見つかりました。"

@tool
def technical_analysis_tool(patent_ids: List[str]) -> str:
    """特許IDのリストを受け取り、それらの技術的な新規性と課題を分析する。"""
    print(f"--- ツール実行: technical_analysis_tool (ID: {patent_ids}) ---")
    return f"{patent_ids}を分析した結果、主要な技術は自己修復AIであり、計算コストが課題です。"

@tool
def report_generation_tool(analysis_summary: str) -> str:
    """分析サマリーを受け取り、最終的な調査レポートを作成する。"""
    print(f"--- ツール実行: report_generation_tool ---")
    return f"最終レポート:\n{analysis_summary}\n\n結論として、この技術分野は将来性が高いと評価されます。"

# --- 2. エージェントの作成 ---
class PatentResearchAgent:
    def __init__(self):
        # os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        tools = [patent_search_tool, technical_analysis_tool, report_generation_tool]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは特許調査を専門とするAIアシスタントです。与えられたツールを段階的に使って、ユーザーの依頼を達成してください。"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def research_patent(self, query: str):
        """特許調査エージェントを実行する"""
        print("--- エージェント実行開始 ---")
        result = self.agent_executor.invoke({"input": query})
        print("--- エージェント実行終了 ---")
        return result['output']

# --- 3. 実行 ---
if __name__ == "__main__":
    print("=== LangChain Agentによる特許調査 デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    agent = PatentResearchAgent()
    report = agent.research_patent("自己修復AIに関する特許動向を調査し、レポートを作成してください。")
    
    print("\n\n--- 最終生成物 ---")
    print(report)