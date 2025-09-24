# LangGraphを使用して書き換えた分散調査システム
import os
from typing import TypedDict, List, Dict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --- 0. 環境設定 ---
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# --- 1. LLMの準備 ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

def create_agent_prompt(system_message: str):
    return ChatPromptTemplate.from_messages([("system", system_message), ("user", "{input}")])

# --- 2. グラフの状態を定義 ---
class AgentState(TypedDict):
    original_query: str
    tasks: Dict[str, str]
    technical_result: str
    legal_result: str
    market_result: str
    competitor_result: str
    final_report: str

# --- 3. 各エージェントとコーディネーターのノードを定義 ---

def coordinator_node(state: AgentState):
    """クエリを分析し、各専門エージェントへのタスクを分配する"""
    print("--- コーディネーター: タスク分配 ---")
    original_query = state["original_query"]
    prompt = create_agent_prompt(
        """あなたは特許調査プロジェクトのマネージャーです。
ユーザーからの調査クエリを分析し、以下の4つの専門エージェントに具体的な調査タスクを割り振ってください。
- technical: 技術的な新規性、実装可能性、技術的課題などを調査
- legal: 特許の有効性、権利範囲、侵害リスクなどを調査
- market: 市場規模、成長性、主要プレイヤー、応用分野などを調査
- competitor: 競合他社の関連特許、開発動向、強み・弱みなどを調査

出力は必ず以下のJSON形式にしてください:
{
  "technical": "（技術エージェントへの指示）",
  "legal": "（法務エージェントへの指示）",
  "market": "（市場エージェントへの指示）",
  "competitor": "（競合エージェントへの指示）"
}"""
    )
    chain = prompt | llm.with_structured_output(Dict[str, str])
    tasks = chain.invoke({"input": original_query})
    print(f"生成されたタスク: {tasks}")
    return {"tasks": tasks}

def technical_agent_node(state: AgentState):
    """技術的な側面から特許を分析する"""
    print("--- 技術エージェント: 分析実行 ---")
    task = state["tasks"]["technical"]
    prompt = create_agent_prompt("あなたは技術分析の専門家です。与えられた指示に基づいて特許の技術的側面を分析し、結果を報告してください。")
    chain = prompt | llm
    result = chain.invoke({"input": task}).content
    print(f"分析結果: {result[:100]}...")
    return {"technical_result": result}

def legal_agent_node(state: AgentState):
    """法的な側面から特許を分析する"""
    print("--- 法務エージェント: 分析実行 ---")
    task = state["tasks"]["legal"]
    prompt = create_agent_prompt("あなたは特許法務の専門家です。与えられた指示に基づいて特許の法的側面を分析し、結果を報告してください。")
    chain = prompt | llm
    result = chain.invoke({"input": task}).content
    print(f"分析結果: {result[:100]}...")
    return {"legal_result": result}

def market_agent_node(state: AgentState):
    """市場性の側面から特許を分析する"""
    print("--- 市場分析エージェント: 分析実行 ---")
    task = state["tasks"]["market"]
    prompt = create_agent_prompt("あなたは市場分析の専門家です。与えられた指示に基づいて特許の市場性を分析し、結果を報告してください。")
    chain = prompt | llm
    result = chain.invoke({"input": task}).content
    print(f"分析結果: {result[:100]}...")
    return {"market_result": result}

def competitor_agent_node(state: AgentState):
    """競合の側面から特許を分析する"""
    print("--- 競合分析エージェント: 分析実行 ---")
    task = state["tasks"]["competitor"]
    prompt = create_agent_prompt("あなたは競合分析の専門家です。与えられた指示に基づいて競合他社の動向を分析し、結果を報告してください。")
    chain = prompt | llm
    result = chain.invoke({"input": task}).content
    print(f"分析結果: {result[:100]}...")
    return {"competitor_result": result}

def integrator_node(state: AgentState):
    """各エージェントの分析結果を統合し、最終レポートを作成する"""
    print("--- インテグレーター: 最終レポート作成 ---")
    prompt_text = f"""あなたは特許コンサルタントのチーフアナリストです。
以下の各専門エージェントからの分析レポートを統合し、包括的で分かりやすい最終調査レポートを作成してください。

元の調査クエリ: {state['original_query']}

--- 技術分析レポート ---
{state['technical_result']}

--- 法務分析レポート ---
{state['legal_result']}

--- 市場分析レポート ---
{state['market_result']}

--- 競合分析レポート ---
{state['competitor_result']}

---
最終レポートを作成してください。
"""
    result = llm.invoke(prompt_text).content
    print("最終レポートが作成されました。")
    return {"final_report": result}


# --- 4. グラフを構築 ---
workflow = StateGraph(AgentState)

workflow.add_node("coordinator", coordinator_node)
workflow.add_node("technical_agent", technical_agent_node)
workflow.add_node("legal_agent", legal_agent_node)
workflow.add_node("market_agent", market_agent_node)
workflow.add_node("competitor_agent", competitor_agent_node)
workflow.add_node("integrator", integrator_node)

workflow.set_entry_point("coordinator")

# コーディネーターから各分析エージェントへタスクを渡す
workflow.add_edge("coordinator", "technical_agent")
workflow.add_edge("coordinator", "legal_agent")
workflow.add_edge("coordinator", "market_agent")
workflow.add_edge("coordinator", "competitor_agent")

# すべての分析エージェントが終わったら統合ノードへ
# LangGraphは、あるノードへの入力が複数ある場合、すべての入力が揃うのを待ってからそのノードを実行します。
workflow.add_edge("technical_agent", "integrator")
workflow.add_edge("legal_agent", "integrator")
workflow.add_edge("market_agent", "integrator")
workflow.add_edge("competitor_agent", "integrator")

workflow.add_edge("integrator", END)

# グラフをコンパイル
app = workflow.compile()

# --- 5. グラフを実行 ---
if __name__ == "__main__":
    print("=== LangGraphによる分散特許調査システム デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    query = "ドローンによる自動配送技術に関する特許ランドスケープ調査"
    inputs = {"original_query": query}

    # ストリーミングで実行過程を表示する場合
    # for s in app.stream(inputs):
    #     print(s)
    #     print("----\n")

    # 最終結果のみを取得する場合
    final_state = app.invoke(inputs)

    print("\n\n--- 最終レポート ---")
    print(final_state["final_report"])