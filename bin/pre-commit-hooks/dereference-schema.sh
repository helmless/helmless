#!/bin/bash
# Pre-commit hook to dereference JSON schema files
#
# Finds all values-edit-me.schema.json files and converts them to values.schema.json
# by resolving all JSON references.

set -e

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel)"

# Check if Python and jsonref are available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed."
    exit 1
fi

# Check if jsonref is installed
if ! python3 -c "import jsonref" &> /dev/null; then
    echo "Error: jsonref Python package is required but not installed."
    echo "Install with: pip install jsonref"
    exit 1
fi

# Run the dereference script
echo "Dereferencing schema files..."
if ! python3 "${REPO_ROOT}/bin/scripts/dereference-schema.py"; then
    echo "Error: Schema dereferencing failed. Check the logs above for details."
    exit 1
fi

# Check if any schemas were changed
if git diff --name-only | grep -q "values.schema.json"; then
    echo "Schema files were dereferenced. Adding changes to commit."

    # Calculate checksum of modified files before adding
    for file in $(git diff --name-only | grep "values.schema.json"); do
        echo "Processing updated schema file: $file"

        # Add the file to git
        git add "$file"
    done
else
    echo "No schema changes detected."
fi

exit 0
