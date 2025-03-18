#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    exit 1
fi

ROOT_DIR="${GITHUB_WORKSPACE:-.}"
CHARTS_DIR="$ROOT_DIR/charts"

# Initialize counters
PROCESSED_COUNT=0
SKIPPED_COUNT=0

echo "Searching for schema files in $CHARTS_DIR..."

# Store the list of files in an array to avoid pipe subshell issues with counters
mapfile -t SCHEMA_FILES < <(find "$CHARTS_DIR" -type f \( -name "values.schema.json" -o -name "values-edit-me.schema.json" \))

# Iterate through the files
for SCHEMA_FILE in "${SCHEMA_FILES[@]}"; do
    echo "Processing schema file: $SCHEMA_FILE"

    # Extract the version from the JSON schema
    VERSION=$(jq -r '.version' "$SCHEMA_FILE")

    if [ -z "$VERSION" ]; then
        echo "  Warning: Could not extract version from schema. Skipping."
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    echo "  Using version: $VERSION"

    # Create a temporary file
    TMP_FILE=$(mktemp)

    # Add $since field to properties and patternProperties that don't have it
    jq --arg version "$VERSION" '
      def process:
        if type == "object" then
          # Handle regular properties
          if .properties then
            .properties |= with_entries(
              if .value | type == "object" and (has("$since") | not) then
                .value += {"$since": $version}
              else
                .
              end
            )
          else
            .
          end |
          # Handle pattern properties
          if .patternProperties then
            .patternProperties |= with_entries(
              if .value | type == "object" and (has("$since") | not) then
                .value += {"$since": $version}
              else
                .
              end
            )
          else
            .
          end |
          # Process nested objects
          with_entries(
            .value |= if type == "object" then process elif type == "array" then map(process) else . end
          )
        elif type == "array" then
          map(process)
        else
          .
        end;
      process
    ' "$SCHEMA_FILE" > "$TMP_FILE"

    # Check if jq command was successful
    if [ $? -eq 0 ]; then
        mv "$TMP_FILE" "$SCHEMA_FILE"
        echo "  Successfully added \$since field to schema properties and patternProperties"
        PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    else
        rm "$TMP_FILE"
        echo "  Error: Failed to process JSON schema"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    fi
done

echo "Schema update completed:"
echo "  Successfully processed: $PROCESSED_COUNT files"
echo "  Skipped or failed: $SKIPPED_COUNT files"
