#!/bin/bash

# Run Ruff to check for linting errors
echo "Running Ruff linter..."
ruff .

# Run Black to format the code
echo "Running Black formatter..."
black .

echo "Code quality checks complete."