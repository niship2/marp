---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# 5. プログラミングを用いた生成 AI 活用法

---

## 5-1. Agent 構築の基本

#### Agent の構成要素

```python
# 基本的なAgent構造
class PatentAgent:
    def __init__(self):
        self.memory = []
        self.tools = []
        self.model = None

    def execute_task(self, task):
        # タスク実行ロジック
        pass
```

#### 主要機能

- **計画立案**: タスクの分解と実行順序
- **ツール選択**: 適切なツールの選択
- **結果評価**: 実行結果の品質確認

---

## 5-2. LangChain / LangGraph の利用

#### LangChain

```python
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI

# 基本的なチェーン構築
template = "特許調査の結果を分析してください: {input}"
prompt = PromptTemplate(template=template, input_variables=["input"])
chain = LLMChain(llm=OpenAI(), prompt=prompt)
```

#### LangGraph

```python
from langgraph import StateGraph

# ワークフロー定義
workflow = StateGraph(StateType)
workflow.add_node("search", search_patents)
workflow.add_node("analyze", analyze_results)
workflow.add_edge("search", "analyze")
```

---

## 5-3. Google Agent Development Kit の活用

#### 特徴

- **Google AI 統合**: Gemini 等との連携
- **マルチモーダル**: テキスト・画像・音声対応
- **スケーラビリティ**: 大規模システム対応

#### 知財業務での活用

- **文書解析**: 特許明細書の自動解析
- **画像認識**: 図面の理解
- **音声処理**: 会議録音の文字起こし

---

## 5-4. MCP との連携

#### MCP (Model Context Protocol)

- **標準化**: AI ツール間の相互運用性
- **拡張性**: 新機能の容易な追加
- **セキュリティ**: 安全なツール連携

#### 知財業務での活用

- **データベース連携**: 特許情報システム
- **外部 API**: 翻訳・検索サービス
- **内部システム**: 文書管理・ワークフロー
