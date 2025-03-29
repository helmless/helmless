import jsonref
import logging
from pathlib import Path
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
import os
import re
import requests

log = logging.getLogger('mkdocs')

# Add this at the top level of the file
log.info("Schema renderer hook module loaded")

def _render_property(name: str, prop: dict, required: list = None, level: int = 1, changelog_path: str = None) -> str:
    """Render a single property from the schema into markdown."""
    md = []
    prefix = '#' * level

    if prop.get('$hidden', False):
        return ""

    # Handle allOf by merging properties
    if 'allOf' in prop:
        # Create a copy of the original property without allOf
        merged_prop = {k: v for k, v in prop.items() if k != 'allOf'}

        # Initialize properties dict if it doesn't exist
        if 'properties' not in merged_prop:
            merged_prop['properties'] = {}

        # First merge all referenced properties from allOf
        for ref_prop in prop['allOf']:
            if '$ref' in ref_prop:
                # Skip rendering the allOf reference directly
                continue
            if 'properties' in ref_prop:
                # Add allOf properties first
                merged_prop['properties'] = {
                    **ref_prop['properties'],
                    **(merged_prop['properties'] or {})
                }
            # Merge other fields if needed
            for key, value in ref_prop.items():
                if key != 'properties' and key not in merged_prop:
                    merged_prop[key] = value

        # Use the merged properties for rendering
        prop = merged_prop

    # Handle property type
    prop_type = prop.get('type', [])
    if isinstance(prop_type, list):
        type_str = ', '.join(f'`{t}`' for t in prop_type)
    else:
        type_str = f'`{prop_type}`'

    if level > 1:
        # Build markdown output
        md.append(f"{prefix} <!-- md:setting values.{name} -->")

        md.append("")
        if 'deprecated' in prop and prop['deprecated']:
            md.append("<!-- md:deprecated -->")

        md.append(f"<!-- md:version {prop.get('$since', 'next')} -->")
        md.append(f"<!-- md:type {type_str} -->")
        if 'enum' in prop:
            enum_values = ' · '.join(f'`{v}`' for v in prop['enum'])
            md.append(f"<!-- md:enum {enum_values} -->")

        if 'maxLength' in prop:
            md.append(f"<!-- md:maxLength {prop['maxLength']} -->")
        if 'minLength' in prop:
            md.append(f"<!-- md:minLength {prop['minLength']} -->")
        if 'pattern' in prop:
            md.append(f"<!-- md:pattern `{prop['pattern']}` -->")

        default = prop.get('default', None)
        if default is not None:
            md.append(f"<!-- md:default `{default}` -->")
        else:
            md.append("<!-- md:default none -->")


        if name.split('.')[-1] in (required or []):
            md.append("<!-- md:flag required -->")

    # Add description
    if 'description' in prop:
        md.append("")
        md.append(prop['description'])

    if 'examples' in prop:
        md.extend(_render_examples(prop['examples'], name))

    # Render sub-properties if this is an object type
    if 'properties' in prop:
        md.append("")
        md.append("---")
        for sub_name, sub_prop in prop['properties'].items():
            md.append("")
            md.append(_render_property(
                f"{name}.{sub_name}" if level > 1 else sub_name,
                sub_prop,
                prop.get('required', []),
                level=level + 1,
                changelog_path=changelog_path
            ))

    # Render pattern properties if present
    if 'patternProperties' in prop:
        md.append("")
        md.append("---")
        for pattern, pattern_prop in prop['patternProperties'].items():
            # Use $id if present, otherwise use the pattern
            pattern_name = pattern_prop.get('$id', pattern)
            pattern_prop["pattern"] = pattern
            md.append("")
            md.append(_render_property(
                f"{name}.{pattern_name}" if level > 1 else pattern_name,
                pattern_prop,
                pattern_prop.get('required', []),
                level=level + 1,
                changelog_path=changelog_path
            ))

    if 'oneOf' in prop:
        # Only proceed if any of the oneOf options have properties
        if any('properties' in option for option in prop['oneOf']):
            md.append("")
            md.append("---")
            md.append(f"???+ abstract \"The `{name}` setting requires **exactly one** of the following configurations:\"")
            md.append("")
            for i, option in enumerate(prop['oneOf'], 1):
                if 'properties' in option:
                    # Determine the option title based on the properties
                    option_title = next(iter(option.get('properties', {}).keys()), f'Option {i}')
                    md.append(f"    === \"{option_title}\"")
                    md.append("")

                    # Render the option's properties
                    for sub_name, sub_prop in option['properties'].items():
                        sub_content = _render_property(
                            f"{name}.{sub_name}" if level > 1 else sub_name,
                            sub_prop,
                            option.get('required', []),
                            level=level + 1,
                            changelog_path=changelog_path
                        )
                        # Indent each line of the sub-content with 4 spaces
                        indented_content = '\n'.join(f"        {line}" for line in sub_content.split('\n'))
                        md.append(indented_content)
                    md.append("")

    return f"\n".join(md)

def _render_schema(schema: dict, changelog_path: str = None) -> str:
    """Render a complete schema into markdown."""
    md = []

    # Add frontmatter and header
    md.extend([
        "---",
        f"title: {schema.get('title', 'Values Schema')}",
        f"description: {schema.get('description', '')}",
        "---",
        f"# {schema.get('title', 'Values Schema')}",
    ])

    try:
        md.append(_render_property(
            "root",
            schema,
            schema.get('required', []),
            changelog_path=changelog_path
        ))
        md.append("")
        md.append("---")
    except Exception as e:
        log.error(f"Failed to render schema: {e}")
        log.exception("Full traceback:")

    return '\n'.join(md)

def _render_dict_example(data: dict, indent: str, prefix: str = "") -> list[str]:
    """Helper function to render dictionary examples with proper YAML formatting."""
    yaml_lines = []

    # Handle $value special case
    if "$value" in data:
        return [f"{indent}{prefix} {data['$value']}"]

    # Add prefix if provided (for nested objects)
    if prefix:
        yaml_lines.append(f"{indent}{prefix} ")
        indent = indent + "  "

    # Format as YAML with proper indentation
    for k, v in data.items():
        if k.startswith('$'):
            continue
        if isinstance(v, dict) or isinstance(v, list):
            yaml_lines.extend(_render_example(k, v, indent=indent))
        else:
            # Convert Python bool to YAML bool
            if isinstance(v, bool):
                v = str(v).lower()
            yaml_lines.append(f"{indent}{k}: {v}")

    return yaml_lines

def _render_example(name: str, example: any, indent: str = "") -> list[str]:
    """Render a single example as YAML with proper indentation."""
    yaml_lines = []

    if name == 'root':
        yaml_lines.extend(_render_dict_example(example, indent))
        return yaml_lines

    # Handle dotted names by creating nested structure
    if '.' in name:
        parts = name.split('.')
        for part in parts[:-1]:
            yaml_lines.append(f"{indent}{part}:")
            indent = indent + "  "
        name = parts[-1]

    # Now handle the actual value with the final name part
    if isinstance(example, dict):
        yaml_lines.extend(_render_dict_example(example, indent, f"{name}:"))
    elif isinstance(example, list):
        yaml_lines.append(f"{indent}{name}:")
        for item in example:
            if isinstance(item, dict):
                yaml_lines.append(f"{indent}  -")  # Start array item
                # Indent the dictionary content
                dict_lines = _render_dict_example(item, indent + "    ")
                yaml_lines.extend(dict_lines)
            else:
                yaml_lines.append(f"{indent}  - {item}")
    else:
        # Convert Python bool to YAML bool
        if isinstance(example, bool):
            example = str(example).lower()
        yaml_lines.append(f"{indent}{name}: {example}")

    return yaml_lines

def _render_examples(examples: list, name: str = None, indent: str = "") -> list[str]:
    """Render a list of examples as YAML with proper formatting.

    Args:
        examples: List of example values
        name: The property name (optional)
        indent: Additional indentation prefix for nested examples

    Returns:
        List of strings containing the formatted examples
    """
    md = []
    md.append("")
    if len(examples) == 1:
        example = examples[0]
        md.append(f"{indent}```yaml")
        md.extend(_render_example(name, example, indent=indent))
        md.append(f"{indent}```")
    elif len(examples) > 1:
        for example in examples:
            if isinstance(example, dict) and '$title' in example:
                title = example.pop('$title')
                md.append(f"{indent}=== \"{title}\"")
            else:
                md.append(f"{indent}=== \"Example {examples.index(example) + 1}\"")
            md.append(f"{indent}    ```yaml")
            md.extend(_render_example(name, example, indent=indent + "    "))
            md.append(f"{indent}    ```")
    return md

def on_files(files: Files, config, **kwargs) -> Files:
    """
    Hook to process schema files based on the schema_renderer configuration.
    """
    log.info("Starting schema file processing")

    # Get schema_renderer configuration
    renderer_config = config.get('schema_renderer', {})
    schemas = renderer_config.get('schemas', [])
    write_output = renderer_config.get('write_output', False)

    if not schemas:
        log.info("No schemas configured, skipping")
        return files

    for schema_config in schemas:
        try:
            # Get schema configuration
            schema_path = schema_config['schema_path']
            nav_path = schema_config['nav_path']
            changelog_path = schema_config.get('changelog_path')

            log.info(f"Processing schema: {schema_path} -> {nav_path}")

            # Load and parse the schema
            if schema_path.startswith('http://') or schema_path.startswith('https://'):
                log.info(f"Loading schema from URL: {schema_path}")
                response = requests.get(schema_path)
                response.raise_for_status()
                base_uri = '/'.join(schema_path.split('/')[:-1])
                schema = jsonref.loads(response.text, base_uri=base_uri)
            else:
                abs_schema_path = os.path.join(config['docs_dir'], '..', schema_path)
                log.info(f"Loading schema from: {abs_schema_path}")
                with open(abs_schema_path) as f:
                    schema = jsonref.load(f, base_uri=f"file://{os.path.dirname(abs_schema_path)}")

            # Convert schema to markdown
            markdown_output = _render_schema(schema, changelog_path=changelog_path)

            # Create a virtual file for the markdown output
            virtual_file = File(
                path=nav_path,
                src_dir=config['docs_dir'],
                dest_dir=config['site_dir'],
                use_directory_urls=config.get('use_directory_urls', True)
            )
            virtual_file.content_string = markdown_output
            virtual_file.generated_by = 'schema_renderer'

            # Add the virtual file to the files collection
            files.append(virtual_file)

            # Handle changelog if provided
            if changelog_path:
                # Determine if changelog is a URL or a local path
                if changelog_path.startswith('http://') or changelog_path.startswith('https://'):
                    log.info(f"Loading changelog from URL: {changelog_path}")
                    try:
                        response = requests.get(changelog_path)
                        response.raise_for_status()
                        changelog_content = response.text
                    except requests.RequestException as e:
                        log.warning(f"Failed to load changelog from URL {changelog_path}: {e}")
                        changelog_content = None
                else:
                    # Load changelog from project root
                    abs_changelog_path = os.path.join(config['docs_dir'], '..', changelog_path)
                    if os.path.exists(abs_changelog_path):
                        log.info(f"Loading changelog from: {abs_changelog_path}")
                        with open(abs_changelog_path, 'r') as f:
                            changelog_content = f.read()
                    else:
                        log.warning(f"Changelog file not found at {abs_changelog_path}")
                        changelog_content = None

                if changelog_content:
                    # Create path for virtual changelog file in same directory as nav_path
                    changelog_nav_path = os.path.join(os.path.dirname(nav_path), 'CHANGELOG.md')

                    # Add IDs to version headers
                    changelog_content = re.sub(
                        r'^## (?:\[)?(\d+\.\d+\.\d+)(?:\])?(.*?)$',
                        r'## \1\2 { id="\1" }',
                        changelog_content,
                        flags=re.MULTILINE
                    )

                    # Create virtual file for changelog
                    changelog_file = File(
                        path=changelog_nav_path,
                        src_dir=config['docs_dir'],
                        dest_dir=config['site_dir'],
                        use_directory_urls=config.get('use_directory_urls', True)
                    )
                    changelog_file.content_string = changelog_content
                    changelog_file.generated_by = 'schema_renderer'

                    # Add changelog virtual file to files collection
                    files.append(changelog_file)
                    log.info(f"Added changelog virtual file at {changelog_nav_path}")

            # Optionally write the markdown output to disk
            if write_output:
                output_path = os.path.join(config['docs_dir'], 'rendered_schemas', nav_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                log.info(f"Writing generated markdown to: {output_path}")
                with open(output_path, 'w') as f:
                    f.write(markdown_output)

            log.info(f"Successfully rendered schema {schema_path} to {nav_path}")

        except Exception as e:
            log.error(f"Failed to process schema {schema_path}: {e}")
            log.exception("Full traceback:")

    return files
