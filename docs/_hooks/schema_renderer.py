import jsonref
import logging
from pathlib import Path
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
import os
import re

log = logging.getLogger('mkdocs')

# Add this at the top level of the file
log.info("Schema renderer hook module loaded")

def _render_property(name: str, prop: dict, required: list = None, level: int = 2, changelog_path: str = None) -> str:
    """Render a single property from the schema into markdown."""
    md = []
    prefix = '#' * level

    # Handle property type
    prop_type = prop.get('type', [])
    if isinstance(prop_type, list):
        type_str = ', '.join(f'`{t}`' for t in prop_type)
    else:
        type_str = f'`{prop_type}`'

    # Build markdown output
    md.append(f"{prefix} <!-- md:setting values.{name} -->")

    md.append("")
    if 'deprecated' in prop and prop['deprecated']:
        md.append("<!-- md:deprecated -->")

    md.append(f"<!-- md:version {prop.get('since', '0.1.0')} -->")
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
                f"{name}.{sub_name}",
                sub_prop,
                prop.get('required', []),
                level=level + 1,
                changelog_path=changelog_path
            ))

    if 'oneOf' in prop:
        md.append("")
        md.append("---")
        md.append(f"???+ abstract \"The `{name}` setting requires **exactly one** of the following configurations:\"")
        md.append("")
        for i, option in enumerate(prop['oneOf'], 1):
            # Determine the option title based on the properties
            option_title = next(iter(option.get('properties', {}).keys()), f'Option {i}')
            md.append(f"    === \"{option_title}\"")
            md.append("")

            # Render the option's properties
            if 'properties' in option:
                for sub_name, sub_prop in option['properties'].items():
                    sub_content = _render_property(
                        f"{name}.{sub_name}",
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
        "",
        f"# {schema.get('title', 'Values Schema')}",
        "",
        schema.get('description', ''),
        ""
    ])

    if 'examples' in schema:
        md.extend(_render_examples(schema['examples']))
        md.append("")

    # Render each top-level property
    for prop_name, prop in schema.get('properties', {}).items():
        try:
            md.append(_render_property(
                prop_name,
            prop,
            schema.get('required', []),
                changelog_path=changelog_path
            ))
            md.append("")
            md.append("---")
        except Exception as e:
            log.error(f"Failed to render property `{prop_name}` {prop}: {e}")
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
    if name is None:
        if isinstance(example, dict):
            return _render_dict_example(example, indent)
        elif isinstance(example, list):
            # Handle array of objects
            yaml_lines = []
            for item in example:
                if isinstance(item, dict):
                    yaml_lines.append(f"{indent}-")  # Start array item
                    # Indent the dictionary content
                    dict_lines = _render_dict_example(item, indent + "  ")
                    yaml_lines.extend(dict_lines)
                else:
                    yaml_lines.append(f"{indent}- {item}")
            return yaml_lines
        else:
            return [f"{indent}{example}"]

    yaml_lines = []

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
            md.append(f"{indent + "    "}```yaml")
            md.extend(_render_example(name, example, indent=indent + "    "))
            md.append(f"{indent + "    "}```")
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
            abs_schema_path = os.path.join(config['docs_dir'], '..', schema_path)
            log.info(f"Loading schema from: {abs_schema_path}")

            with open(abs_schema_path) as f:
                schema = jsonref.load(f)

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
                # Load changelog from project root
                abs_changelog_path = os.path.join(config['docs_dir'], '..', changelog_path)
                if os.path.exists(abs_changelog_path):
                    # Create path for virtual changelog file in same directory as nav_path
                    changelog_nav_path = os.path.join(os.path.dirname(nav_path), 'CHANGELOG.md')

                    # Read changelog content
                    with open(abs_changelog_path, 'r') as f:
                        changelog_content = f.read()

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
                else:
                    log.warning(f"Changelog file not found at {abs_changelog_path}")

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
