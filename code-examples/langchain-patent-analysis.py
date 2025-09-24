# LangChain (LCEL) とメモリ機能を使ったモダンな特許分析システム
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- 1. LLMとプロンプトの準備 ---
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.1)

# プロンプトテンプレートを定義 (メモリ用のプレースホルダーを追加)
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは特許分析の専門家です。"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "以下の特許文献を{analysis_type}の観点から分析してください：\n\n{patent_text}"),
])

# --- 2. メモリの準備 ---
# セッションIDごとにメモリを保持するための辞書
demo_memory = {}

def get_session_history(session_id: str):
    """セッションIDに対応するメモリを取得（なければ新規作成）"""
    if session_id not in demo_memory:
        demo_memory[session_id] = ConversationBufferMemory(
            memory_key="history", return_messages=True
        )
    return demo_memory[session_id]

# --- 3. LCELでチェーンを構築 ---
# 基本的なチェーン
base_chain = prompt | llm | StrOutputParser()

# メモリ機能をラップしたチェーン
# これにより、`invoke`時に`config={"configurable": {"session_id": "..."}}`を指定するだけで
# 自動的に会話履歴がロード＆セーブされる
patent_analysis_chain_with_memory = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="patent_text", # ユーザー入力を示すキー
    history_messages_key="history",   # メモリが格納されるキー
)

# --- 4. 実行 ---
if __name__ == "__main__":
    print("=== LCELによる会話メモリ付き特許分析 デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    patent_document = """
    特許番号: JP2023-12345
    発明の名称: 自己修復機能を持つAIアルゴリズム
    要約: 本発明は、外部からの予期せぬデータ入力や内部状態の変化に対して、
    自律的にその構造を修復し、性能を維持するAIアルゴリズムに関する。
    このアルゴリズムは、特に自動運転車の制御システムにおいて、
    システムの堅牢性を高めることを目的とする。
    """
    
    # セッションIDを定義
    my_session_id = "user123"

    # 1回目の分析
    print("--- 1回目の分析 (新規性) ---")
    response1 = patent_analysis_chain_with_memory.invoke(
        {"analysis_type": "新規性", "patent_text": patent_document},
        config={"configurable": {"session_id": my_session_id}}
    )
    print(response1)

    # 2回目の分析 (同じセッションIDを使用)
    # 1回目の会話内容を覚えている
    print("\n--- 2回目の分析 (市場性) ---")
    response2 = patent_analysis_chain_with_memory.invoke(
        {"analysis_type": "市場性", "patent_text": "前の特許について"}, # "前の特許"で文脈を維持できる
        config={"configurable": {"session_id": my_session_id}}
    )
    print(response2)

    # メモリの内容を確認
    print("\n--- 現在の会話履歴 ---")
    print(get_session_history(my_session_id).chat_memory.messages)