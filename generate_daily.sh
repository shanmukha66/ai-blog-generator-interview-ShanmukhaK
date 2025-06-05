#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUTPUT_DIR="${SCRIPT_DIR}/generated_posts"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Generate the post and save it to the output directory
curl "http://localhost:5001/generate?keyword=wireless%20earbuds" > "${OUTPUT_DIR}/$(date +%Y%m%d)_post.json" 