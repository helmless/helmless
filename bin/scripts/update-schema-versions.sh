#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    exit 1
fi

SCHEMA_FILE="${GITHUB_WORKSPACE:-.}/charts/cloudrun/service/values.schema.json"

# Extract the version from the JSON schema
VERSION=$(jq -r '.version' "$SCHEMA_FILE")

if [ -z "$VERSION" ]; then
    echo "Error: Could not extract version from schema"
    exit 1
fi

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
    echo "Successfully added \$since field to schema properties and patternProperties"
else
    rm "$TMP_FILE"
    echo "Error: Failed to process JSON schema"
    exit 1
fi
