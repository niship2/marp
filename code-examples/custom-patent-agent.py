# LangGraph と AutoGen を連携させたAIエージェント
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
import autogen
from langchain_openai import ChatOpenAI

# --- 0. 環境設定 ---
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# --- 1. AutoGen エージェントの設定 ---
# LLMの設定 (AutoGenはデフォルトで `gpt-4` を使おうとするため、モデルを指定)
llm_config = {
    "model": "gpt-4-turbo",
    "api_key": os.environ.get("OPENAI_API_KEY"),
}

# エージェントの定義
researcher = autogen.AssistantAgent(
    name="researcher",
    system_message="あなたは特許調査の専門家です。与えられたテーマについて、関連する特許や技術動向を調査し、要点をまとめてください。",
    llm_config=llm_config,
)
analyst = autogen.AssistantAgent(
    name="analyst",
    system_message="あなたは特許分析の専門家です。調査結果を受け取り、技術の新規性、市場性、競合の観点から詳細な分析レポートを作成してください。最後に'TERMINATE'と述べてください。",
    llm_config=llm_config,
)
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,  # コード実行は不要
    default_auto_reply="分析を続けてください。",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
)

# --- 2. LangGraph の状態定義 ---
class AgentState(TypedDict):
    query: str
    research_result: str

# --- 3. LangGraph のノード定義 ---
def autogen_chat_node(state: AgentState):
    """AutoGenのグループチャットを実行し、結果を返すノード"""
    print("--- AutoGen グループチャット開始 ---")
    query = state["query"]

    groupchat = autogen.GroupChat(
        agents=[user_proxy, researcher, analyst],
        messages=[],
        max_round=10,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # チャットを開始
    user_proxy.initiate_chat(
        manager,
        message=f"以下のテーマについて特許調査と分析を実行してください: {query}"
    )

    # 最後のメッセージ（通常はanalystの最終レポート）を取得
    final_message = groupchat.messages[-1]["content"].replace("TERMINATE", "").strip()
    print("--- AutoGen グループチャット終了 ---")

    return {"research_result": final_message}

# --- 4. グラフの構築とコンパイル ---
workflow = StateGraph(AgentState)
workflow.add_node("autogen_chat", autogen_chat_node)
workflow.set_entry_point("autogen_chat")
workflow.add_edge("autogen_chat", END)
app = workflow.compile()

# --- 5. 実行 ---
if __name__ == "__main__":
    print("=== LangGraphとAutoGenによるカスタム特許エージェント デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    # グラフを実行
    query = "AI創薬における新しいアルゴリズム"
    final_state = app.invoke({"query": query})

    print("\n\n--- 最終分析結果 ---")
    print(final_state["research_result"])