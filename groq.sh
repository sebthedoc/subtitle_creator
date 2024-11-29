#!/bin/bash

# Check if at least one argument is provided (file path is mandatory)
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 /path/to/files/*.mp4 [optional_sleep_duration_in_seconds]"
    exit 1
fi

# Extract optional sleep duration (default to 0 if not provided)
SLEEP_DURATION=${2:-0}

# Loop over all the files provided as arguments
for file in "$@"; do
    # Skip the sleep duration argument if provided
    if [[ "$file" == "$SLEEP_DURATION" ]]; then
        continue
    fi

    # Run Python script for each file
    python sub_groq.py "$file"

    # Sleep only if sleep duration is a positive number
    if [[ "$SLEEP_DURATION" -gt 0 ]]; then
        sleep "$SLEEP_DURATION"
    fi
done
