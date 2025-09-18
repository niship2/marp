# 特許文献の一括処理
gemini process patents/*.pdf --output analysis/ --format json

# 定期レポートの自動生成
gemini generate-report --template weekly --data patents.json --output reports/

# 技術動向の監視
gemini monitor-trends --keywords "AI,patent" --interval daily --output trends/

# 文書の自動翻訳
gemini translate --input japanese_patents/ --output english_patents/ --source ja --target en

# 複数の特許文献を一括で分析
gemini analyze-patents \
  --input-dir ./patent_documents/ \
  --output-dir ./analysis_results/ \
  --analysis-type "technical_trends,competitor_analysis,classification" \
  --format "json,csv,pdf"

# 特定技術分野の動向を自動監視
gemini setup-monitoring \
  --technology "artificial intelligence" \
  --keywords "machine learning,deep learning,neural networks" \
  --frequency "daily" \
  --notification "email,slack" \
  --output "./monitoring_results/"
