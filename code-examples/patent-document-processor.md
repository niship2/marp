# 特許文献一括処理システム

## 概要

複数の特許文献を一括で処理し、分析結果を自動生成するシステムです。

## 要件

- PDF ファイルの一括読み込み
- テキスト抽出（PyPDF2 使用）
- 技術用語の自動抽出
- 重要度スコアの計算
- CSV 形式での結果出力

## 実装例

```python
import os
import pandas as pd
import PyPDF2
import re
from typing import List, Dict, Any
import logging
from datetime import datetime

class PatentDocumentProcessor:
    def __init__(self, config_file: str = None):
        """特許文献処理システムの初期化"""
        self.setup_logging()
        self.config = self.load_config(config_file)
        self.results = []
        
    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('patent_processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """設定ファイルの読み込み"""
        default_config = {
            'chunk_size': 1000,
            'overlap': 200,
            'keywords': ['発明', '技術', '装置', '方法', 'システム'],
            'output_format': 'csv'
        }
        
        if config_file and os.path.exists(config_file):
            # 設定ファイルの読み込み処理
            pass
            
        return default_config
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """PDFからテキストを抽出"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                    
                return text
        except Exception as e:
            self.logger.error(f"PDF読み込みエラー {pdf_path}: {str(e)}")
            return ""
            
    def extract_technical_terms(self, text: str) -> List[str]:
        """技術用語の抽出"""
        # 基本的な技術用語抽出ロジック
        technical_patterns = [
            r'[A-Z][a-z]+(?:[A-Z][a-z]+)*',  # キャメルケース
            r'[a-zA-Z]+(?:[0-9]+[a-zA-Z]*)*',  # 英数字組み合わせ
            r'[ひらがなカタカナ漢字]+(?:[0-9]+)*'  # 日本語技術用語
        ]
        
        terms = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, text)
            terms.extend(matches)
            
        # 重複除去と頻度計算
        term_freq = {}
        for term in terms:
            if len(term) > 2:  # 短すぎる用語を除外
                term_freq[term] = term_freq.get(term, 0) + 1
                
        # 頻度順でソート
        sorted_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)
        return [term for term, freq in sorted_terms[:50]]  # 上位50個
        
    def calculate_importance_score(self, text: str, terms: List[str]) -> float:
        """重要度スコアの計算"""
        score = 0.0
        
        # キーワードの出現頻度
        for keyword in self.config['keywords']:
            count = text.lower().count(keyword.lower())
            score += count * 0.1
            
        # 技術用語の多様性
        unique_terms = len(set(terms))
        score += unique_terms * 0.05
        
        # 文書の長さ（詳細度の指標）
        score += len(text) * 0.0001
        
        return min(score, 10.0)  # 最大10点
        
    def process_single_document(self, pdf_path: str) -> Dict[str, Any]:
        """単一文書の処理"""
        self.logger.info(f"処理開始: {pdf_path}")
        
        # テキスト抽出
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return None
            
        # 技術用語抽出
        terms = self.extract_technical_terms(text)
        
        # 重要度スコア計算
        importance_score = self.calculate_importance_score(text, terms)
        
        # 結果の整理
        result = {
            'file_name': os.path.basename(pdf_path),
            'file_path': pdf_path,
            'text_length': len(text),
            'technical_terms_count': len(terms),
            'top_terms': terms[:10],  # 上位10個の用語
            'importance_score': importance_score,
            'processed_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"処理完了: {pdf_path} (スコア: {importance_score:.2f})")
        return result
        
    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """ディレクトリ内の全PDFファイルを処理"""
        if not os.path.exists(directory_path):
            self.logger.error(f"ディレクトリが存在しません: {directory_path}")
            return []
            
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        self.logger.info(f"処理対象ファイル数: {len(pdf_files)}")
        
        results = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory_path, pdf_file)
            result = self.process_single_document(pdf_path)
            if result:
                results.append(result)
                
        self.results = results
        return results
        
    def export_results(self, output_path: str = None):
        """結果のエクスポート"""
        if not self.results:
            self.logger.warning("エクスポートする結果がありません")
            return
            
        if not output_path:
            output_path = f"patent_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        # DataFrameに変換
        df = pd.DataFrame(self.results)
        
        # 技術用語を文字列に変換
        df['top_terms'] = df['top_terms'].apply(lambda x: ', '.join(x))
        
        # CSV出力
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        self.logger.info(f"結果をエクスポートしました: {output_path}")
        
    def generate_summary_report(self) -> str:
        """サマリーレポートの生成"""
        if not self.results:
            return "処理結果がありません"
            
        total_files = len(self.results)
        avg_score = sum(r['importance_score'] for r in self.results) / total_files
        total_terms = sum(r['technical_terms_count'] for r in self.results)
        
        report = f"""
=== 特許文献処理サマリーレポート ===
処理日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
処理ファイル数: {total_files}
平均重要度スコア: {avg_score:.2f}
総技術用語数: {total_terms}

=== 重要度スコア上位ファイル ===
"""
        
        # 重要度スコア順でソート
        sorted_results = sorted(self.results, key=lambda x: x['importance_score'], reverse=True)
        
        for i, result in enumerate(sorted_results[:5], 1):
            report += f"{i}. {result['file_name']} (スコア: {result['importance_score']:.2f})\n"
            
        return report

def main():
    """メイン処理"""
    processor = PatentDocumentProcessor()
    
    # 処理対象ディレクトリ
    input_directory = "./patent_documents"
    output_directory = "./analysis_results"
    
    # 出力ディレクトリの作成
    os.makedirs(output_directory, exist_ok=True)
    
    # 文書処理
    results = processor.process_directory(input_directory)
    
    if results:
        # 結果のエクスポート
        output_path = os.path.join(output_directory, "patent_analysis_results.csv")
        processor.export_results(output_path)
        
        # サマリーレポートの生成
        summary = processor.generate_summary_report()
        print(summary)
        
        # サマリーレポートの保存
        summary_path = os.path.join(output_directory, "summary_report.txt")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
    else:
        print("処理対象のファイルが見つかりませんでした")

if __name__ == "__main__":
    main()
```

## 使用方法

```bash
# 必要なライブラリのインストール
pip install PyPDF2 pandas

# スクリプトの実行
python patent_document_processor.py
```

## 設定ファイル例 (config.json)

```json
{
    "chunk_size": 1000,
    "overlap": 200,
    "keywords": ["発明", "技術", "装置", "方法", "システム", "アルゴリズム", "データベース"],
    "output_format": "csv",
    "min_term_length": 3,
    "max_terms": 50
}
```

## 期待される効果

- **処理時間の短縮**: 手動処理の 1/10 の時間
- **精度の向上**: 一貫した分析基準
- **スケーラビリティ**: 大量文書の一括処理
- **追跡可能性**: 詳細なログとレポート