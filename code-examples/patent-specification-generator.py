# LangChainを使って書き換えた明細書作成支援システム
import os
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

# --- 1. LLMの準備 ---
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2)

# --- 2. 各セクション生成チェーンの定義 ---
def create_section_chain(section_name: str, instruction: str):
    """各セクションを生成するためのLCELチェーンを作成するヘルパー関数"""
    prompt = ChatPromptTemplate.from_template(
        f"""あなたは特許明細書作成の専門家です。
提供された発明の概要に基づいて、明細書の「{section_name}」のセクションを作成してください。

【指示】
{instruction}

【発明の概要】
{{invention_summary}}
"""
    )
    return prompt | llm | StrOutputParser()

class PatentSpecificationGenerator:
    def __init__(self):
        self.generation_chain = RunnableParallel(
            title=create_section_chain("発明の名称", "発明の核心を捉えた、簡潔で的確な名称を作成してください。"),
            technical_field=create_section_chain("技術分野", "この発明が属する技術分野を具体的に説明してください。"),
            background_art=create_section_chain("背景技術", "この発明に関連する従来の技術（先行技術）とその問題点を説明してください。"),
            problem=create_section_chain("発明が解決しようとする課題", "背景技術の問題点を踏まえ、この発明が具体的に何を解決しようとしているのかを明確に記述してください。"),
            solution=create_section_chain("課題を解決するための手段", "上記の課題を解決するために、この発明がどのような構成や手段を用いているのかを具体的に説明してください。"),
            effects=create_section_chain("発明の効果", "上記の解決手段によって、どのような優れた効果が得られるのかを具体的に記述してください。"),
        )

    def generate_specification_sections(self, invention_summary: str) -> Dict[str, str]:
        """発明の概要から、明細書の主要セクションを並列生成する"""
        print("--- 明細書の各セクションを生成中... ---")
        return self.generation_chain.invoke({"invention_summary": invention_summary})

    def format_specification(self, sections: Dict[str, str]) -> str:
        """生成されたセクションを最終的な明細書のフォーマットに整形する"""
        spec_parts = [
            f"# 【発明の名称】\n{sections['title']}\n",
            f"## 【技術分野】\n{sections['technical_field']}\n",
            f"## 【背景技術】\n{sections['background_art']}\n",
            f"## 【発明が解決しようとする課題】\n{sections['problem']}\n",
            f"## 【課題を解決するための手段】\n{sections['solution']}\n",
            f"## 【発明の効果】\n{sections['effects']}\n",
        ]
        return "\n".join(spec_parts)

# --- 3. 実行 ---
if __name__ == "__main__":
    print("=== LangChainによる明細書作成支援 デモンストレーション ===\n")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        print("警告: OPENAI_API_KEYが設定されていません。ダミーキーを使用します。\n")

    invention_summary = """
    発明のテーマ: スマートフォンを使ったリアルタイム植物病害診断システム
    コア技術:
    - スマートフォンのカメラで撮影した葉の画像を使用する。
    - 軽量なCNNモデルをスマホアプリに搭載し、オフラインで高速に病害を特定する。
    - 診断結果とGPS情報をサーバーに送信し、病害の発生状況を地図上でリアルタイムにマッピングする。
    """

    generator = PatentSpecificationGenerator()
    generated_sections = generator.generate_specification_sections(invention_summary)
    final_specification = generator.format_specification(generated_sections)

    print("\n--- 生成された明細書ドラフト ---")
    print(final_specification)

    with open("generated_specification_draft.md", "w", encoding="utf-8") as f:
        f.write(final_specification)
    print("\n'generated_specification_draft.md' に保存しました。")
