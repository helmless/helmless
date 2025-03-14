#!/usr/bin/env python3
"""
Dereferences values-edit-me.schema.json files into values.schema.json for charts.

This script is intended to be used in a pre-commit hook to ensure that all
JSON schema references are resolved before committing changes.

Usage:
    bin/scripts/dereference-schema.py [--chart-dir DIRECTORY]

Options:
    --chart-dir DIRECTORY    Path to the charts directory [default: charts]
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
import jsonref
import json.decoder

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('dereference-schema')

def find_chart_dirs(base_dir):
    """Find all chart directories that have a values-edit-me.schema.json file."""
    chart_dirs = []

    for root, _, files in os.walk(base_dir):
        if 'values-edit-me.schema.json' in files:
            chart_dirs.append(root)

    return chart_dirs

def dereference_schema(input_file, output_file):
    """Dereference all JSON references in the input file and write to output file."""
    logger.info(f"Dereferencing {input_file} -> {output_file}")

    schema = None

    try:
        # First check if input file exists
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return False

        # Load and dereference schema in memory first
        with open(input_file, 'r') as f:
            try:
                base_path = os.path.dirname(os.path.abspath(input_file))
                base_uri = f"file://{base_path}/"
                schema = jsonref.load(f, base_uri=base_uri)
            except json.decoder.JSONDecodeError as e:
                logger.error(f"JSON parsing error in {input_file}: {e}")
                return False
            except Exception as e:
                logger.error(f"Error dereferencing schema in {input_file}: {e}")
                return False

        # Validate schema is not None and is a valid JSON object
        if schema is None:
            logger.error(f"Failed to load schema from {input_file}")
            return False

        # Only write to output file if dereferencing completed successfully
        try:
            with open(output_file, 'w', newline='\n') as f:
                json_str = json.dumps(schema, indent=2)
                # Ensure file ends with a single newline
                if not json_str.endswith('\n'):
                    json_str += '\n'
                f.write(json_str)
            logger.info(f"Successfully dereferenced {input_file}")
            return True
        except PermissionError:
            logger.error(f"Permission denied when writing to {output_file}")
            return False
        except Exception as e:
            logger.error(f"Error writing dereferenced schema to {output_file}: {e}")
            return False

    except Exception as e:
        logger.error(f"Unexpected error processing {input_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Dereference values-edit-me.schema.json files into values.schema.json for charts"
    )
    parser.add_argument(
        "--chart-dir",
        default="charts",
        help="Path to the charts directory [default: charts]"
    )

    args = parser.parse_args()

    # Find all chart directories with a values-edit-me.schema.json file
    logger.info(f"Searching for charts in {args.chart_dir}")
    chart_dirs = find_chart_dirs(args.chart_dir)

    if not chart_dirs:
        logger.info("No values-edit-me.schema.json files found in charts directory")
        return 0

    # Process each chart directory
    success = True
    for chart_dir in chart_dirs:
        input_file = os.path.join(chart_dir, 'values-edit-me.schema.json')
        output_file = os.path.join(chart_dir, 'values.schema.json')

        if not dereference_schema(input_file, output_file):
            success = False

    if not success:
        logger.error("Failed to dereference all schemas")
        return 1

    logger.info("Successfully dereferenced all schemas")
    return 0

if __name__ == "__main__":
    sys.exit(main())
