#!/bin/bash

# Check if at least one argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 /path/to/files/*.mp4"
    exit 1
fi

# Loop over all the files provided as arguments
for file in "$@"; do
    python sub_groq.py "$file"
    sleep 1800
done
