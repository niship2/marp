---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# 6. 生成 AI にすべて任せるアプローチ

---

## 6-1. コーディングアシスタントの活用

#### Claude Code

- **コード生成**: 特許分析ツールの作成
- **デバッグ支援**: エラーの自動修正
- **最適化**: パフォーマンス改善

#### Cursor

- **IDE 統合**: 開発環境での直接支援
- **リアルタイム**: コード作成の即座な支援
- **学習機能**: プロジェクト固有の学習

#### Devin

- **自律開発**: 完全自動のソフトウェア開発
- **要件理解**: 自然言語からの仕様理解
- **継続改善**: フィードバックによる改善

---

## 6-2. GeminiCli について

#### 特徴

- **コマンドライン統合**: ターミナルからの直接利用
- **スクリプト化**: 自動化の容易な実装
- **ファイル操作**: ローカルファイルの直接処理

#### 活用例

```bash
# 特許文献の一括処理
gemini process patents/*.pdf --output analysis/

# 定期レポートの自動生成
gemini generate-report --template weekly --data patents.json
```

---

## 6-3. 寝てる間に進めてもらう

#### 自動化戦略

- **スケジューリング**: 定期的なタスク実行
- **条件分岐**: 状況に応じた処理選択
- **通知機能**: 完了・異常の自動通知

#### 実装例

```python
# 夜間自動処理
@schedule.every().day.at("02:00")
def nightly_patent_analysis():
    # 新規特許の自動分析
    # 競合他社の動向監視
    # レポートの自動生成
    pass
```

#### 注意点

- **品質管理**: 自動処理結果の確認
- **エラーハンドリング**: 異常時の対応
- **セキュリティ**: 機密情報の保護
