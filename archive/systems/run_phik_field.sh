#!/bin/bash
# Wrapper script to run phik_field_python.py with .venv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Use venv Python if available
if [ -f "$PROJECT_ROOT/.venv/bin/python3" ]; then
    exec "$PROJECT_ROOT/.venv/bin/python3" "$SCRIPT_DIR/phik_field_python.py" "$@"
else
    exec python3 "$SCRIPT_DIR/phik_field_python.py" "$@"
fi

