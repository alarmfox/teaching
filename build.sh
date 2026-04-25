#!/bin/bash

# DTLab Build Script
# Usage: ./build.sh <directory> [banner_path_or_text]

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <directory> [banner_path_or_text]"
    exit 1
fi

SOURCE_DIR=$1
BANNER=$2
OUTPUT_DIR="$SOURCE_DIR/build"

mkdir -p "$OUTPUT_DIR"

echo "Building materials for: $SOURCE_DIR"

for md in "$SOURCE_DIR"/*.md; do
    [ -e "$md" ] || continue
    [ "$(basename "$md")" == "README.md" ] && continue
    
    filename=$(basename "$md" .md)
    echo "  -> Processing $filename..."
    
    # Check if banner exists and is an image/pdf
    if [[ -f "$BANNER" ]]; then
        # If it's a file, we use it as a header or include it
        # For simplicity in PDF conversion, we add it to the top of the MD
        # We create a temporary MD file with the image/banner prepended
        TEMP_MD=$(mktemp)
        echo "![$BANNER]($BANNER)" > "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        cat "$md" >> "$TEMP_MD"
        pandoc "$TEMP_MD" -o "$OUTPUT_DIR/$filename.pdf"
        rm "$TEMP_MD"
    else
        # Fallback to simple text banner
        pandoc "$md" -V title="${BANNER:-DTLab Material}" -o "$OUTPUT_DIR/$filename.pdf"
    fi
done

echo "Build complete. Artifacts are in $OUTPUT_DIR"
