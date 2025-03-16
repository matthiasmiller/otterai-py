#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PACKAGE_NAME="otterai"
VENV_DIR="myenv"

cd "$(dirname "$0")" || exit 1

echo "Setting up virtual environment..."
python3.8 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate" || {
    echo "Failed to activate virtual environment"
    exit 1
}
pip install -r requirements.txt
echo "Virtual environment '$VENV_DIR' is ready with dependencies installed."

echo "Running tests with coverage..."
pytest --cov="$PACKAGE_NAME" \
    --cov-report=term-missing \
    --cov-report=lcov:lcov.info \
    --cov-report=xml:cov.xml || {
    echo "Tests failed. Exiting..."
    exit 1
}
echo "Coverage reports generated: lcov.info and cov.xml in the root directory."

echo "Starting the application..."
python3.8 main.py
