#!/bin/bash

# extracted_sections.txtを作成するスクリプト
# pagesディレクトリ内のMarkdownファイルから## \d-パターンにマッチする部分を抽出

# 出力ファイルのパス
OUTPUT_FILE="extracted_sections.txt"

# 出力ファイルをクリア（既存の内容を削除）
> "$OUTPUT_FILE"

echo "Markdownファイルから## \d-パターンのセクションを抽出中..."

# pagesディレクトリ内の各Markdownファイルを処理
for file in pages/*.md; do
    if [ -f "$file" ]; then
        echo "処理中: $file"
        
        # grepで## \d-パターンにマッチする行を抽出し、出力ファイルに追加
        grep -E "^## [0-9]+-" "$file" >> "$OUTPUT_FILE"
    fi
done

echo "抽出完了: $OUTPUT_FILE"
echo "抽出されたセクション数: $(wc -l < "$OUTPUT_FILE")"
