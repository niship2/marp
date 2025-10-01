#!/bin/bash

# extracted_sections.txtを作成するスクリプト
# pagesディレクトリ内のMarkdownファイルから## \d-\d+パターンにマッチする目次を抽出

# 出力ファイルのパス
OUTPUT_FILE="extracted_sections.txt"
TEMP_FILE="temp_sections.txt"

# 出力ファイルをクリア（既存の内容を削除）
> "$OUTPUT_FILE"
> "$TEMP_FILE"

echo "Markdownファイルから## \d-\d+パターンの目次を抽出中..."

# pagesディレクトリ内の各Markdownファイルを処理
for file in pages/*.md; do
    if [ -f "$file" ]; then
        echo "処理中: $file"
        
        # grepで## \d-\d+パターンにマッチする行を抽出し、一時ファイルに追加
        grep -E "^## [0-9]+-[0-9]+" "$file" >> "$TEMP_FILE"
    fi
done

echo "重複目次の処理中..."

# 重複する目次を処理
# ##n-nn の番号が同じものを重複として削除（最初のもののみ残す）
awk '
{
    # 目次番号を抽出（## 数字-数字 の部分）
    if (match($0, /^## ([0-9]+-[0-9]+)/)) {
        toc_number = substr($0, RSTART+3, RLENGTH-3)
    } else {
        next
    }
    
    # この目次番号が初めて出現する場合のみ出力
    if (!seen[toc_number]) {
        print $0
        seen[toc_number] = 1
    }
}' "$TEMP_FILE" > "$OUTPUT_FILE"

# 一時ファイルを削除
rm "$TEMP_FILE"

echo "抽出完了: $OUTPUT_FILE"
echo "抽出された目次数: $(wc -l < "$OUTPUT_FILE")"
