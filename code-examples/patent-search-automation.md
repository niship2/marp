# 特許検索自動化システム

## 概要

定期的な特許検索を自動化し、新規特許の監視を実現するシステムです。

## 要件

- 特許データベース API 連携
- 定期検索の自動実行
- 新規特許の自動抽出・重要度評価
- 結果の自動通知

## 実装例

```python
import requests
import schedule
import time
import sqlite3
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any
import os

class PatentSearchAutomation:
    def __init__(self, config_file: str = "config.json"):
        """特許検索自動化システムの初期化"""
        self.setup_logging()
        self.config = self.load_config(config_file)
        self.db_path = self.config.get('database_path', 'patent_monitor.db')
        self.setup_database()

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('patent_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """設定ファイルの読み込み"""
        default_config = {
            'api_endpoints': {
                'jpo': 'https://www.j-platpat.inpit.go.jp/api/patent',
                'uspto': 'https://developer.uspto.gov/ibd-api/v1/patent'
            },
            'search_keywords': ['AI', 'artificial intelligence', 'machine learning'],
            'search_interval': 'daily',
            'notification': {
                'email': {
                    'enabled': True,
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'recipients': []
                }
            },
            'importance_threshold': 7.0
        }

        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def setup_database(self):
        """データベースの初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patent_number TEXT UNIQUE,
                title TEXT,
                abstract TEXT,
                inventors TEXT,
                assignee TEXT,
                filing_date TEXT,
                publication_date TEXT,
                importance_score REAL,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_keywords TEXT,
                results_count INTEGER,
                new_patents_count INTEGER,
                search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def search_patents(self, keywords: List[str], days_back: int = 7) -> List[Dict[str, Any]]:
        """特許検索の実行"""
        self.logger.info(f"特許検索開始: {keywords}")

        # 実際のAPI呼び出し（例：J-PlatPat API）
        patents = []

        for keyword in keywords:
            try:
                # API呼び出しの例
                params = {
                    'q': keyword,
                    'date_from': (datetime.now() - timedelta(days=days_back)).strftime('%Y%m%d'),
                    'date_to': datetime.now().strftime('%Y%m%d'),
                    'format': 'json'
                }

                # 実際のAPI呼び出しは実装に応じて調整
                # response = requests.get(self.config['api_endpoints']['jpo'], params=params)
                # patents.extend(self.parse_api_response(response.json()))

                # デモ用のダミーデータ
                patents.extend(self.generate_demo_patents(keyword))

            except Exception as e:
                self.logger.error(f"検索エラー {keyword}: {str(e)}")

        return patents

    def generate_demo_patents(self, keyword: str) -> List[Dict[str, Any]]:
        """デモ用の特許データ生成"""
        import random

        demo_patents = []
        for i in range(random.randint(1, 5)):
            patent = {
                'patent_number': f'JP{random.randint(2020000000, 2024999999)}',
                'title': f'{keyword}に関する特許発明 {i+1}',
                'abstract': f'この発明は{keyword}技術に関するもので、従来技術の課題を解決する。',
                'inventors': f'発明者{i+1}',
                'assignee': f'会社{i+1}',
                'filing_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'publication_date': datetime.now().strftime('%Y-%m-%d'),
                'keywords': keyword
            }
            demo_patents.append(patent)

        return demo_patents

    def calculate_importance_score(self, patent: Dict[str, Any]) -> float:
        """重要度スコアの計算"""
        score = 0.0

        # タイトルの重要度
        title = patent.get('title', '').lower()
        for keyword in self.config['search_keywords']:
            if keyword.lower() in title:
                score += 2.0

        # 要約の重要度
        abstract = patent.get('abstract', '').lower()
        for keyword in self.config['search_keywords']:
            score += abstract.count(keyword.lower()) * 0.5

        # 出願日の新しさ
        filing_date = patent.get('filing_date', '')
        if filing_date:
            try:
                filing_dt = datetime.strptime(filing_date, '%Y-%m-%d')
                days_ago = (datetime.now() - filing_dt).days
                if days_ago <= 30:
                    score += 1.0
                elif days_ago <= 90:
                    score += 0.5
            except:
                pass

        return min(score, 10.0)

    def save_patents(self, patents: List[Dict[str, Any]]) -> int:
        """特許データの保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        new_patents_count = 0

        for patent in patents:
            # 重要度スコアの計算
            importance_score = self.calculate_importance_score(patent)
            patent['importance_score'] = importance_score

            try:
                cursor.execute('''
                    INSERT INTO patents
                    (patent_number, title, abstract, inventors, assignee,
                     filing_date, publication_date, importance_score, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patent['patent_number'],
                    patent['title'],
                    patent['abstract'],
                    patent['inventors'],
                    patent['assignee'],
                    patent['filing_date'],
                    patent['publication_date'],
                    importance_score,
                    patent['keywords']
                ))
                new_patents_count += 1

            except sqlite3.IntegrityError:
                # 既存の特許の場合はスキップ
                pass

        conn.commit()
        conn.close()

        return new_patents_count

    def get_high_importance_patents(self, threshold: float = None) -> List[Dict[str, Any]]:
        """高重要度特許の取得"""
        if threshold is None:
            threshold = self.config['importance_threshold']

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM patents
            WHERE importance_score >= ?
            AND created_at >= datetime('now', '-1 day')
            ORDER BY importance_score DESC
        ''', (threshold,))

        columns = [description[0] for description in cursor.description]
        patents = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return patents

    def send_notification(self, patents: List[Dict[str, Any]]):
        """通知の送信"""
        if not patents:
            return

        if not self.config['notification']['email']['enabled']:
            return

        email_config = self.config['notification']['email']

        # メール本文の作成
        subject = f"新規高重要度特許の通知 ({len(patents)}件)"

        body = f"""
新規の高重要度特許が{len(patents)}件見つかりました。

=== 特許一覧 ===
"""

        for i, patent in enumerate(patents, 1):
            body += f"""
{i}. {patent['title']}
   特許番号: {patent['patent_number']}
   出願者: {patent['assignee']}
   重要度スコア: {patent['importance_score']:.1f}
   出願日: {patent['filing_date']}
"""

        body += f"""
詳細はデータベースをご確認ください。
検索日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        # メール送信
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['username']
            msg['To'] = ', '.join(email_config['recipients'])
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])

            text = msg.as_string()
            server.sendmail(email_config['username'], email_config['recipients'], text)
            server.quit()

            self.logger.info(f"通知メールを送信しました: {len(patents)}件")

        except Exception as e:
            self.logger.error(f"メール送信エラー: {str(e)}")

    def run_daily_search(self):
        """日次検索の実行"""
        self.logger.info("日次特許検索を開始します")

        # 検索実行
        patents = self.search_patents(self.config['search_keywords'])

        # データベースに保存
        new_patents_count = self.save_patents(patents)

        # 検索履歴の記録
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO search_history (search_keywords, results_count, new_patents_count)
            VALUES (?, ?, ?)
        ''', (', '.join(self.config['search_keywords']), len(patents), new_patents_count))
        conn.commit()
        conn.close()

        # 高重要度特許の通知
        high_importance_patents = self.get_high_importance_patents()
        if high_importance_patents:
            self.send_notification(high_importance_patents)

        self.logger.info(f"日次検索完了: 総数{len(patents)}件, 新規{new_patents_count}件, 高重要度{len(high_importance_patents)}件")

    def start_monitoring(self):
        """監視の開始"""
        self.logger.info("特許監視システムを開始します")

        # スケジュール設定
        schedule.every().day.at("02:00").do(self.run_daily_search)

        # 初回実行
        self.run_daily_search()

        # スケジュール実行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにチェック

    def generate_report(self, days: int = 7) -> str:
        """レポートの生成"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 統計情報の取得
        cursor.execute('''
            SELECT COUNT(*) FROM patents
            WHERE created_at >= datetime('now', '-{} days')
        '''.format(days))
        total_patents = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*) FROM patents
            WHERE importance_score >= ?
            AND created_at >= datetime('now', '-{} days')
        '''.format(days), (self.config['importance_threshold'],))
        high_importance_count = cursor.fetchone()[0]

        cursor.execute('''
            SELECT AVG(importance_score) FROM patents
            WHERE created_at >= datetime('now', '-{} days')
        '''.format(days))
        avg_score = cursor.fetchone()[0] or 0

        # 上位特許の取得
        cursor.execute('''
            SELECT title, patent_number, importance_score, assignee
            FROM patents
            WHERE created_at >= datetime('now', '-{} days')
            ORDER BY importance_score DESC
            LIMIT 10
        '''.format(days))
        top_patents = cursor.fetchall()

        conn.close()

        # レポート生成
        report = f"""
=== 特許監視レポート ({days}日間) ===
期間: {datetime.now() - timedelta(days=days)} ～ {datetime.now()}

=== 統計情報 ===
総特許数: {total_patents}件
高重要度特許数: {high_importance_count}件
平均重要度スコア: {avg_score:.2f}

=== 重要度スコア上位特許 ===
"""

        for i, (title, patent_number, score, assignee) in enumerate(top_patents, 1):
            report += f"{i}. {title}\n"
            report += f"   特許番号: {patent_number}\n"
            report += f"   出願者: {assignee}\n"
            report += f"   重要度スコア: {score:.1f}\n\n"

        return report

def main():
    """メイン処理"""
    monitor = PatentSearchAutomation()

    # 監視開始
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("監視を停止します")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
```

## 設定ファイル例 (config.json)

```json
{
  "api_endpoints": {
    "jpo": "https://www.j-platpat.inpit.go.jp/api/patent",
    "uspto": "https://developer.uspto.gov/ibd-api/v1/patent"
  },
  "search_keywords": [
    "AI",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network"
  ],
  "search_interval": "daily",
  "importance_threshold": 7.0,
  "database_path": "patent_monitor.db",
  "notification": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your_email@gmail.com",
      "password": "your_app_password",
      "recipients": ["recipient1@example.com", "recipient2@example.com"]
    }
  }
}
```

## 使用方法

```bash
# 必要なライブラリのインストール
pip install requests schedule

# 設定ファイルの作成
cp config.json.example config.json
# config.jsonを編集

# システムの実行
python patent_search_automation.py
```

## 期待される効果

- **24 時間監視**: 継続的な特許監視
- **見落とし防止**: 自動化による確実な検索
- **効率化**: 手動検索の 90%削減
- **重要度判定**: 自動的な優先度評価
