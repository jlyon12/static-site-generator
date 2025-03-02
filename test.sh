#!/usr/bin/env bash

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed or not in PATH." >&2
    exit 1
fi

if [[ ! -d src ]]; then
    echo "Error: src directory does not exist." >&2
    exit 1
fi

# Run the tests
python3 -m unittest discover -s src