#!/usr/bin/env bash

SCRIPT_PATH=${1:-src/main.py}
REPO=https://github.com/jlyon12/static-site-generator/

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed or not in PATH." >&2
    exit 1
fi

if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "Error: $SCRIPT_PATH does not exist." >&2
    exit 1
fi

PYTHONPATH=$(pwd) python3 "$SCRIPT_PATH" "$REPO"
