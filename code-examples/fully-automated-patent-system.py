# 完全自動化システムの生成プロンプト
<role>
あなたは完全自動化システム開発の専門家で、AIと機械学習に精通しています。
自律的な意思決定と継続的改善を実現するシステム設計を得意としています。
</role>

<context>
完全自動化された特許分析システムを開発する必要があります。
データ収集から分析、品質評価、レポート生成、通知まで、人間の介入なしで動作するシステムが求められています。
</context>

<task>
以下の要件で完全自動化システムを作成してください：

機能要件：
- 自動データ収集
- 自律的分析実行
- 品質評価と改善
- レポート自動生成
- 通知システム
- 継続的学習

技術要件：
- Python 3.8以上
- AI/ML ライブラリ
- 品質評価システム
- 通知機能
- 学習機能

以下の手順で段階的に開発してください：
1. まず、データ収集・分析機能を実装
2. 次に、品質評価システムを実装
3. そして、自律的改善機能を追加
4. 最後に、完全自動化ワークフローを構築
</task>

<output_format>
出力形式：
- モジュラー設計
- 設定可能な品質閾値
- 詳細なログ出力
- 学習機能
- 通知システム
</output_format>

<constraints>
制約：
- 完全自律的な動作
- 継続的な学習と改善
- 品質管理の自動化
- エラー時の自動復旧
</constraints>

# 自動生成されるコード例
class FullyAutomatedPatentSystem:
    def __init__(self):
        self.data_collector = DataCollector()
        self.analyzer = PatentAnalyzer()
        self.report_generator = ReportGenerator()
        self.notification_system = NotificationSystem()
        self.quality_checker = QualityChecker()

    def automated_workflow(self):
        """完全自動化ワークフロー"""
        while True:
            try:
                # 1. データ収集
                new_data = self.data_collector.collect_new_data()

                # 2. 自動分析
                analysis_results = self.analyzer.analyze_all(new_data)

                # 3. 品質チェック
                quality_score = self.quality_checker.check_quality(analysis_results)

                # 4. レポート生成
                if quality_score > 0.8:  # 品質閾値
                    report = self.report_generator.generate_report(analysis_results)

                    # 5. 自動配信
                    self.notification_system.distribute_report(report)

                # 6. 学習・改善
                self.analyzer.learn_from_results(analysis_results, quality_score)

                time.sleep(3600)  # 1時間待機

            except Exception as e:
                self.notification_system.send_error_notification(e)
                time.sleep(300)  # エラー時は5分待機
