#!/bin/bash

# DTLab Build Script (LaTeX Version)
# Usage: ./build.sh [file_or_directory]

TEMPLATE="$(pwd)/template.tex"
AUTHOR="Giuseppe Capasso"
ROOT_DIR=$(pwd)
LATEXMKRC="$ROOT_DIR/.latexmkrc"

# Function to convert MD to TEX and compile to PDF
process_file() {
    local md_file=$1

    # Only process .md files
    [[ "$md_file" != *.md ]] && return
    # Skip README.md
    [[ "$(basename "$md_file")" == "README.md" ]] && return

    local dir=$(dirname "$md_file")
    local filename=$(basename "$md_file" .md)
    local tex_file="$filename.tex"

    echo "--------------------------------------------------"
    echo "Processing: $md_file"

    # Determine course/lab name from directory structure
    local course=""
    if [[ "$md_file" =~ courses/([^/]+) ]]; then
        course="${BASH_REMATCH[1]}"
    elif [[ "$md_file" =~ labs/([^/]+) ]]; then
        course="${BASH_REMATCH[1]}"
    fi

    # Extract title from the first line if it's a header
    local title=$(grep -m 1 "^# " "$md_file" | sed 's/^# //')
    if [ -z "$title" ]; then
        # Fallback to filename if no title found
        title=$(head -n 1 "$md_file" | head -c 100 | sed 's/\\/\\\\/g')
    fi
    [ -z "$title" ] && title="$filename"

    # Convert MD to TEX using Pandoc and our template
    # We run from the file's directory to ensure Pandoc finds relative assets
    (
        cd "$dir" || exit
        pandoc "$(basename "$md_file")" \
            --standalone \
            --template="$TEMPLATE" \
            -V author="$AUTHOR" \
            -V course="$course" \
            -V title="$title" \
            -o "$tex_file"

        echo "  -> Generated $tex_file"

        # Compile TEX to PDF using latexmk
        # -r uses our global .latexmkrc which sets out_dir to 'build'
        latexmk -pdf -interaction=nonstopmode -r "$LATEXMKRC" "$tex_file"

        if [ $? -eq 0 ]; then
            echo "  -> Successfully built PDF in build/ folder"
        else
            echo "  -> Error during LaTeX compilation"
        fi
    )
}

# Main execution
TARGET=${1:-.}

if [ -f "$TARGET" ]; then
    process_file "$TARGET"
elif [ -d "$TARGET" ]; then
    # Find all .md files, excluding common non-content dirs
    find "$TARGET" -name "*.md" -not -path "*/node_modules/*" -not -path "*/.*" | while read -r file; do
        process_file "$file"
    done
else
    echo "Error: $TARGET is not a valid file or directory"
    exit 1
fi

echo "--------------------------------------------------"
echo "Build process finished."
