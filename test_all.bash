#!/bin/bash

# Directory path
directory="../test_programs"

# Iterate through files in the directory
for file in "$directory"/*; do
    # Check if the item is a file
    if [[ -f "$file" ]]; then
        # Echo out the file name
        echo "Running $file"
        python3 myrpal.py "$file"
        echo " "
    fi
done