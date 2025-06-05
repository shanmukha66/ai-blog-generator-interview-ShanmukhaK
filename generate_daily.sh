#!/bin/bash

# Create output directory if it doesn't exist
OUTPUT_DIR="generated_content"
mkdir -p "$OUTPUT_DIR"

# Generate timestamp for unique filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$OUTPUT_DIR/blog_${TIMESTAMP}.json"

# Make the API call and save the response
curl "http://localhost:5001/generate?keyword=wireless+earbuds" > "$OUTPUT_FILE"

# Check if the curl command was successful
if [ $? -eq 0 ]; then
    echo "Content generated successfully and saved to $OUTPUT_FILE"
else
    echo "Error: Failed to generate content" >&2
fi 