# 夜間自動処理システムの生成プロンプト
<role>
あなたは自動化システム開発の専門家で、スケジューリングとバッチ処理に精通しています。
安定した長時間運用とエラーハンドリングの実装を得意としています。
</role>

<context>
夜間の特許分析自動化システムを開発する必要があります。
定期的な特許検索、分析、レポート生成、通知を自動実行するシステムが求められています。
</context>

<task>
以下の要件で夜間自動処理システムを作成してください：

機能要件：
- 定期的な特許検索実行
- 重要度評価と優先順位付け
- 技術動向分析
- レポート自動生成
- 通知システム

技術要件：
- Python 3.8以上
- schedule ライブラリ使用
- ログ機能
- エラーハンドリング
- 通知機能（メール・Slack）

以下の手順で段階的に開発してください：
1. まず、スケジューリング機能を実装
2. 次に、分析エンジンを実装
3. そして、レポート生成機能を追加
4. 最後に、通知・エラーハンドリング機能を実装
</task>

<output_format>
出力形式：
- クラスベースの設計
- 設定可能なスケジュール
- 詳細なログ出力
- エラーハンドリング
- 通知機能
</output_format>

<constraints>
制約：
- 安定した長時間運用
- 適切なエラーハンドリング
- リソース効率の考慮
- セキュリティの確保
</constraints>

# 自動生成されるコード例

import schedule
import time
from datetime import datetime
import logging

class NightlyPatentAnalysis:
    def __init__(self):
        self.logger = self.setup_logging()
        self.analysis_engine = PatentAnalysisEngine()
        self.notification_system = NotificationSystem()

    def setup_schedule(self):
        """スケジュール設定"""
        # 毎日午前2時に実行
        schedule.every().day.at("02:00").do(self.nightly_patent_analysis)

        # 毎週月曜日の午前3時に週次レポート生成
        schedule.every().monday.at("03:00").do(self.weekly_report_generation)

        # 毎月1日の午前4時に月次分析実行
        schedule.every().month.at("04:00").do(self.monthly_analysis)

    def nightly_patent_analysis(self):
        """夜間特許分析"""
        try:
            self.logger.info("夜間特許分析を開始")

            # 1. 新規特許の自動検索
            new_patents = self.analysis_engine.search_new_patents()

            # 2. 重要度評価
            prioritized_patents = self.analysis_engine.evaluate_importance(new_patents)

            # 3. 技術動向分析
            trend_analysis = self.analysis_engine.analyze_trends(prioritized_patents)

            # 4. レポート生成
            report = self.analysis_engine.generate_daily_report(trend_analysis)

            # 5. 通知送信
            self.notification_system.send_daily_report(report)

            self.logger.info("夜間特許分析が完了")

        except Exception as e:
            self.logger.error(f"夜間分析でエラーが発生: {e}")
            self.notification_system.send_error_notification(e)

    def run(self):
        """スケジューラー実行"""
        self.setup_schedule()

        while True:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにチェック

# 実行
if __name__ == "__main__":
    nightly_analysis = NightlyPatentAnalysis()
    nightly_analysis.run()
