#!/bin/bash

# Check if a keyword was provided
if [ -z "$1" ]; then
    echo "Error: No keyword provided"
    exit 1
fi

KEYWORD="$1"

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Make a request to generate the blog with the provided keyword
curl -X POST -H "Content-Type: application/json" -d "{\"keyword\":\"$KEYWORD\"}" http://localhost:5001/generate

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 