#!/usr/bin/env bash

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed or not in PATH." >&2
    exit 1
fi

if [[ ! -d src ]]; then
    echo "Error: src directory does not exist." >&2
    exit 1
fi

if command -v pytest &>/dev/null; then
    echo "Running tests with pytest..."
    pytest tests
else
    echo "pytest not found, falling back to unittest..."
    python3 -m unittest discover -s tests
fi