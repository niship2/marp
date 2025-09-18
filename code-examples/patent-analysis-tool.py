# Claude Code による特許分析ツールの自動生成
<role>
あなたは特許分析システム開発の専門家で、PythonとAI技術に精通しています。
効率的で保守性の高いコード作成と、特許業務の自動化を得意としています。
</role>

<context>
特許文献の自動分析ツールを開発する必要があります。
特許データベースからの情報取得、技術分類、競合分析、レポート生成を統合したシステムが求められています。
</context>

<task>
以下の要件で特許文献の自動分析ツールを作成してください：

機能要件：
- 特許データベースからの情報取得
- 技術分類の自動化
- 競合分析の実行
- レポート生成機能
- Web インターフェース

以下の手順で段階的に開発してください：
1. まず、データベース連携機能を実装
2. 次に、分析アルゴリズムを実装
3. そして、レポート生成機能を追加
4. 最後に、Web インターフェースを構築
</task>

<output_format>
出力形式：
- クラスベースの設計
- 設定可能なパラメータ
- 詳細なログ出力
- エラーハンドリング
- 拡張性のある構造
</output_format>

<constraints>
制約：
- 保守性の高いコード設計
- 適切なエラーハンドリング
- メモリ効率の考慮
- セキュリティの確保
</constraints>

# 自動生成されるコード例
class PatentAnalysisTool:
    def __init__(self):
        self.api_client = PatentAPIClient()
        self.llm = OpenAI()
        self.vectorstore = Chroma()

    def analyze_patent_landscape(self, technology_domain):
        # 自動生成された分析ロジック
        patents = self.api_client.search_patents(technology_domain)
        analysis = self.perform_analysis(patents)
        report = self.generate_report(analysis)
        return report
