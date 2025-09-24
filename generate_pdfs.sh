#!/bin/bash

# PDF生成スクリプト
# pagesフォルダ内のMarkdownファイルをPDFに変換し、output_pdfフォルダに出力

set -e  # エラーが発生したらスクリプトを停止

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 出力ディレクトリの作成
OUTPUT_DIR="output_pdf"
log_info "出力ディレクトリを作成: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Marp CLIの確認
if ! command -v marp &> /dev/null; then
    log_error "Marp CLIがインストールされていません"
    log_info "以下のコマンドでインストールしてください:"
    log_info "npm install -g @marp-team/marp-cli"
    exit 1
fi

log_info "Marp CLIが見つかりました"

# pagesディレクトリの確認
if [ ! -d "pages" ]; then
    log_error "pagesディレクトリが見つかりません"
    exit 1
fi

# Markdownファイルの検索と変換
log_info "Markdownファイルを検索中..."
MD_FILES=$(find pages -name "*.md" -type f | sort)

if [ -z "$MD_FILES" ]; then
    log_warning "Markdownファイルが見つかりません"
    exit 0
fi

# 変換処理
CONVERTED_COUNT=0
FAILED_COUNT=0

for md_file in $MD_FILES; do
    # ファイル名から拡張子を除いてベース名を取得
    base_name=$(basename "$md_file" .md)
    output_file="$OUTPUT_DIR/${base_name}.pdf"
    
    log_info "変換中: $md_file -> $output_file"
    
    # MarpでPDF変換（ローカルファイルアクセスを許可）
    if marp --pdf --allow-local-files --output "$output_file" "$md_file"; then
        log_success "変換完了: $output_file"
        ((CONVERTED_COUNT++))
    else
        log_error "変換失敗: $md_file"
        ((FAILED_COUNT++))
    fi
done

# 結果サマリー
echo ""
log_info "=== 変換結果サマリー ==="
log_success "成功: $CONVERTED_COUNT ファイル"
if [ $FAILED_COUNT -gt 0 ]; then
    log_error "失敗: $FAILED_COUNT ファイル"
fi

# 生成されたPDFファイルの一覧表示
echo ""
log_info "生成されたPDFファイル:"
if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A $OUTPUT_DIR)" ]; then
    ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null | while read -r line; do
        echo "  $line"
    done
else
    log_warning "PDFファイルが生成されませんでした"
fi

# ファイルサイズの合計
if [ $CONVERTED_COUNT -gt 0 ]; then
    total_size=$(du -sh "$OUTPUT_DIR" 2>/dev/null | cut -f1)
    log_info "出力ディレクトリの総サイズ: $total_size"
fi

log_success "PDF生成処理が完了しました"
