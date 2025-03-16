#!/bin/bash

cd "$(dirname "$0")" || exit 1

PACKAGE_NAME="otterai"
VENV_DIR="myenv"

python3.8 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate" || {
    echo "Failed to activate virtual environment"
    exit 1
}

pip install -r requirements.txt

echo "Setup complete. Virtual environment '$VENV_DIR' is ready with dependencies installed."

echo "Running tests with coverage..."
pytest --cov="$PACKAGE_NAME" \
    --cov-report=term-missing \
    --cov-report=lcov:lcov.info \
    --cov-report=xml:cov.xml || {
    echo "Tests failed. Exiting..."
    exit 1
}

echo "Coverage reports generated: lcov.info and cov.xml in the root directory."

python3.8 main.py
