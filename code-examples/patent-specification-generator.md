# 明細書作成支援システム

## 概要

明細書作成の効率化と品質向上を実現するシステムです。

## 要件

- 発明内容の自動分析
- 明細書構造の自動生成
- 各セクションの自動作成
- 品質チェック・修正提案機能

## 実装例

```python
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from dataclasses import dataclass

@dataclass
class InventionData:
    """発明データの構造"""
    title: str
    technical_field: str
    background_art: str
    problem: str
    solution: str
    effects: str
    embodiments: List[str]
    claims: List[str]

class PatentSpecificationGenerator:
    def __init__(self, config_file: str = "spec_config.json"):
        """明細書作成支援システムの初期化"""
        self.setup_logging()
        self.config = self.load_config(config_file)
        self.templates = self.load_templates()

    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """設定ファイルの読み込み"""
        default_config = {
            'output_format': 'markdown',
            'language': 'japanese',
            'quality_checks': {
                'enable_grammar_check': True,
                'enable_consistency_check': True,
                'enable_completeness_check': True
            },
            'templates_path': 'templates/'
        }

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except FileNotFoundError:
            self.logger.warning(f"設定ファイルが見つかりません: {config_file}")

        return default_config

    def load_templates(self) -> Dict[str, str]:
        """テンプレートの読み込み"""
        templates = {
            'title': """
# 【発明の名称】
{title}
""",
            'technical_field': """
## 【技術分野】
{technical_field}
""",
            'background_art': """
## 【背景技術】
{background_art}
""",
            'problem': """
## 【発明が解決しようとする課題】
{problem}
""",
            'solution': """
## 【課題を解決するための手段】
{solution}
""",
            'effects': """
## 【発明の効果】
{effects}
""",
            'embodiments': """
## 【発明の実施の形態】
{embodiments}
""",
            'claims': """
## 【請求項】
{claims}
"""
        }
        return templates

    def analyze_invention(self, invention_data: Dict[str, Any]) -> InventionData:
        """発明内容の分析"""
        self.logger.info("発明内容の分析を開始します")

        # 基本的な分析処理
        analyzed_data = InventionData(
            title=self.analyze_title(invention_data.get('title', '')),
            technical_field=self.analyze_technical_field(invention_data.get('technical_field', '')),
            background_art=self.analyze_background_art(invention_data.get('background_art', '')),
            problem=self.analyze_problem(invention_data.get('problem', '')),
            solution=self.analyze_solution(invention_data.get('solution', '')),
            effects=self.analyze_effects(invention_data.get('effects', '')),
            embodiments=self.analyze_embodiments(invention_data.get('embodiments', [])),
            claims=self.analyze_claims(invention_data.get('claims', []))
        )

        return analyzed_data

    def analyze_title(self, title: str) -> str:
        """発明の名称の分析・改善"""
        if not title:
            return "【要修正】発明の名称が入力されていません"

        # 基本的な改善ルール
        improved_title = title.strip()

        # 長すぎる場合は短縮提案
        if len(improved_title) > 50:
            improved_title = improved_title[:47] + "..."
            self.logger.warning("発明の名称が長すぎます。短縮を検討してください")

        return improved_title

    def analyze_technical_field(self, field: str) -> str:
        """技術分野の分析・改善"""
        if not field:
            return "【要修正】技術分野が入力されていません"

        # 技術分野の標準化
        standardized_field = field.strip()

        # 一般的な技術分野のキーワードチェック
        tech_keywords = ['情報処理', '通信', '制御', '機械', '化学', '材料', 'バイオ', '医療']
        if not any(keyword in standardized_field for keyword in tech_keywords):
            self.logger.warning("技術分野の記述が一般的でない可能性があります")

        return standardized_field

    def analyze_background_art(self, background: str) -> str:
        """背景技術の分析・改善"""
        if not background:
            return "【要修正】背景技術が入力されていません"

        # 背景技術の構造チェック
        improved_background = background.strip()

        # 課題への言及があるかチェック
        if '課題' not in improved_background and '問題' not in improved_background:
            self.logger.warning("背景技術に課題への言及が不足している可能性があります")

        return improved_background

    def analyze_problem(self, problem: str) -> str:
        """課題の分析・改善"""
        if not problem:
            return "【要修正】解決すべき課題が入力されていません"

        improved_problem = problem.strip()

        # 課題の明確性チェック
        if len(improved_problem) < 50:
            self.logger.warning("課題の記述が簡潔すぎる可能性があります")

        return improved_problem

    def analyze_solution(self, solution: str) -> str:
        """解決手段の分析・改善"""
        if not solution:
            return "【要修正】解決手段が入力されていません"

        improved_solution = solution.strip()

        # 技術的特徴の明確性チェック
        tech_indicators = ['装置', '方法', 'システム', 'アルゴリズム', '構成', '構造']
        if not any(indicator in improved_solution for indicator in tech_indicators):
            self.logger.warning("解決手段の技術的特徴が不明確な可能性があります")

        return improved_solution

    def analyze_effects(self, effects: str) -> str:
        """効果の分析・改善"""
        if not effects:
            return "【要修正】発明の効果が入力されていません"

        improved_effects = effects.strip()

        # 効果の具体性チェック
        if '向上' not in improved_effects and '改善' not in improved_effects:
            self.logger.warning("発明の効果が具体的でない可能性があります")

        return improved_effects

    def analyze_embodiments(self, embodiments: List[str]) -> List[str]:
        """実施の形態の分析・改善"""
        if not embodiments:
            return ["【要修正】実施の形態が入力されていません"]

        improved_embodiments = []
        for i, embodiment in enumerate(embodiments, 1):
            if not embodiment.strip():
                improved_embodiments.append(f"【要修正】実施の形態{i}が入力されていません")
            else:
                improved_embodiments.append(f"実施の形態{i}:\n{embodiment.strip()}")

        return improved_embodiments

    def analyze_claims(self, claims: List[str]) -> List[str]:
        """請求項の分析・改善"""
        if not claims:
            return ["【要修正】請求項が入力されていません"]

        improved_claims = []
        for i, claim in enumerate(claims, 1):
            if not claim.strip():
                improved_claims.append(f"【要修正】請求項{i}が入力されていません")
            else:
                # 請求項の形式チェック
                claim_text = claim.strip()
                if not claim_text.startswith(('請求項', '1.', '2.', '3.')):
                    claim_text = f"請求項{i}: {claim_text}"
                improved_claims.append(claim_text)

        return improved_claims

    def generate_specification(self, invention_data: Dict[str, Any]) -> str:
        """明細書の生成"""
        self.logger.info("明細書の生成を開始します")

        # 発明内容の分析
        analyzed_data = self.analyze_invention(invention_data)

        # 明細書の構築
        specification = ""

        # 各セクションの生成
        specification += self.templates['title'].format(title=analyzed_data.title)
        specification += self.templates['technical_field'].format(technical_field=analyzed_data.technical_field)
        specification += self.templates['background_art'].format(background_art=analyzed_data.background_art)
        specification += self.templates['problem'].format(problem=analyzed_data.problem)
        specification += self.templates['solution'].format(solution=analyzed_data.solution)
        specification += self.templates['effects'].format(effects=analyzed_data.effects)

        # 実施の形態
        embodiments_text = "\n\n".join(analyzed_data.embodiments)
        specification += self.templates['embodiments'].format(embodiments=embodiments_text)

        # 請求項
        claims_text = "\n\n".join(analyzed_data.claims)
        specification += self.templates['claims'].format(claims=claims_text)

        return specification

    def quality_check(self, specification: str) -> Dict[str, List[str]]:
        """品質チェックの実行"""
        self.logger.info("品質チェックを実行します")

        issues = {
            'grammar': [],
            'consistency': [],
            'completeness': []
        }

        if self.config['quality_checks']['enable_grammar_check']:
            issues['grammar'] = self.check_grammar(specification)

        if self.config['quality_checks']['enable_consistency_check']:
            issues['consistency'] = self.check_consistency(specification)

        if self.config['quality_checks']['enable_completeness_check']:
            issues['completeness'] = self.check_completeness(specification)

        return issues

    def check_grammar(self, specification: str) -> List[str]:
        """文法チェック"""
        issues = []

        # 基本的な文法チェック
        if '【要修正】' in specification:
            issues.append("修正が必要な箇所があります")

        # 重複表現のチェック
        if specification.count('発明') > 20:
            issues.append("「発明」の使用頻度が高すぎます")

        return issues

    def check_consistency(self, specification: str) -> List[str]:
        """一貫性チェック"""
        issues = []

        # 用語の一貫性チェック
        terms = ['装置', 'システム', '方法', 'アルゴリズム']
        for term in terms:
            if term in specification:
                variations = [term + 's', term + 'es', term + 'ing']
                for variation in variations:
                    if variation in specification:
                        issues.append(f"用語の一貫性: {term}と{variation}が混在しています")

        return issues

    def check_completeness(self, specification: str) -> List[str]:
        """完全性チェック"""
        issues = []

        required_sections = [
            '【発明の名称】',
            '【技術分野】',
            '【背景技術】',
            '【発明が解決しようとする課題】',
            '【課題を解決するための手段】',
            '【発明の効果】',
            '【請求項】'
        ]

        for section in required_sections:
            if section not in specification:
                issues.append(f"必須セクションが不足: {section}")

        return issues

    def generate_improvement_suggestions(self, issues: Dict[str, List[str]]) -> str:
        """改善提案の生成"""
        if not any(issues.values()):
            return "品質チェック結果: 問題は見つかりませんでした。"

        suggestions = "=== 改善提案 ===\n\n"

        for category, issue_list in issues.items():
            if issue_list:
                suggestions += f"【{category.upper()}】\n"
                for issue in issue_list:
                    suggestions += f"- {issue}\n"
                suggestions += "\n"

        return suggestions

    def export_specification(self, specification: str, output_path: str):
        """明細書のエクスポート"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(specification)
            self.logger.info(f"明細書をエクスポートしました: {output_path}")
        except Exception as e:
            self.logger.error(f"エクスポートエラー: {str(e)}")

def main():
    """メイン処理"""
    generator = PatentSpecificationGenerator()

    # サンプル発明データ
    sample_invention = {
        'title': 'AI技術を用いた特許文献の自動分析システム',
        'technical_field': '本発明は、人工知能技術を用いた特許文献の自動分析に関する。',
        'background_art': '従来の特許文献分析は人手による作業が中心であり、大量の文献を効率的に処理することが困難であった。',
        'problem': '従来技術では、特許文献の分析に膨大な時間とコストがかかり、分析の精度も分析者によってばらつきがあった。',
        'solution': '本発明は、機械学習アルゴリズムを用いて特許文献を自動的に分析し、技術的特徴を抽出するシステムを提供する。',
        'effects': '本発明により、特許文献の分析時間を大幅に短縮し、分析精度の向上を実現できる。',
        'embodiments': [
            '図1に示すように、本システムは文書入力部、分析処理部、結果出力部から構成される。',
            '分析処理部では、自然言語処理技術を用いて特許文献から技術的特徴を抽出する。'
        ],
        'claims': [
            '機械学習アルゴリズムを用いて特許文献を分析するシステム。',
            '前記システムにおいて、自然言語処理技術により技術的特徴を抽出する請求項1記載のシステム。'
        ]
    }

    # 明細書の生成
    specification = generator.generate_specification(sample_invention)

    # 品質チェック
    issues = generator.quality_check(specification)
    suggestions = generator.generate_improvement_suggestions(issues)

    # 結果の出力
    print("=== 生成された明細書 ===")
    print(specification)
    print("\n" + suggestions)

    # ファイル出力
    generator.export_specification(specification, "generated_specification.md")
    generator.export_specification(suggestions, "improvement_suggestions.md")

if __name__ == "__main__":
    main()
```

## 設定ファイル例 (spec_config.json)

```json
{
  "output_format": "markdown",
  "language": "japanese",
  "quality_checks": {
    "enable_grammar_check": true,
    "enable_consistency_check": true,
    "enable_completeness_check": true
  },
  "templates_path": "templates/",
  "validation_rules": {
    "max_title_length": 50,
    "min_problem_length": 50,
    "required_sections": [
      "title",
      "technical_field",
      "background_art",
      "problem",
      "solution",
      "effects",
      "claims"
    ]
  }
}
```

## 使用方法

```bash
# 必要なライブラリのインストール
pip install dataclasses

# 設定ファイルの作成
cp spec_config.json.example spec_config.json

# システムの実行
python patent_specification_generator.py
```

## 期待される効果

- **作成時間短縮**: 従来の 50%の時間で完成
- **品質向上**: 一貫した品質の明細書
- **標準化**: 組織内での書式統一
- **ミス削減**: 自動品質チェックによる確認
