# Copyright (c) 2016-2024 Martin Donath <martin.donath@squidfunk.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from __future__ import annotations

import posixpath
import re
import logging
import os
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from re import Match


log = logging.getLogger('mkdocs')

# -----------------------------------------------------------------------------
# Hooks
# -----------------------------------------------------------------------------

# Add at the top with other constants
CONVENTIONS_PATH = "docs/conventions.md"

def on_page_markdown(
    markdown: str, *, page: Page, config: MkDocsConfig, files: Files
):
    # Get conventions path from config or use default
    global CONVENTIONS_PATH
    CONVENTIONS_PATH = config.get('conventions_path', CONVENTIONS_PATH)

    # Replace callback
    def replace(match: Match):
        type, args = match.groups()
        args = args.strip()
        if type == "version":        return _badge_for_version(args, page, files)
        elif type == "flag":         return flag(args, page, files)
        elif type == "option":       return option(args)
        elif type == "setting":      return setting(args)
        elif type == "feature":      return _badge_for_feature(args, page, files)
        elif type == "example":      return _badge_for_example(args, page, files)
        elif type == "type":         return _badge_for_type(args, page, files)
        elif type == "maxLength":    return _badge_for_max_length(args, page, files)
        elif type == "minLength":    return _badge_for_min_length(args, page, files)
        elif type == "pattern":      return _badge_for_pattern(args, page, files)
        elif type == "deprecated":   return _badge_for_deprecated(args, page, files)
        elif type == "enum":         return _badge_for_enum(args, page, files)
        elif type == "default":
            if   args == "none":     return _badge_for_default_none(page, files)
            elif args == "computed": return _badge_for_default_computed(page, files)
            else:                    return _badge_for_default(args, page, files)

        # Otherwise, raise an error
        raise RuntimeError(f"Unknown shortcode: {type}")

    # Find and replace all external asset URLs in current page
    return re.sub(
        r"<!-- md:(\w+)(.*?) -->",
        replace, markdown, flags = re.I | re.M
    )

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

# Create a flag of a specific type
def flag(args: str, page: Page, files: Files):
    type, *_ = args.split(" ", 1)
    if   type == "experimental":  return _badge_for_experimental(page, files)
    elif type == "required":      return _badge_for_required(page, files)
    raise RuntimeError(f"Unknown type: {type}")

# Create a linkable option
def option(type: str):
    _, *_, name = re.split(r"[.:]", type)
    return f"[`{name}`](#+{type}){{ #+{type} }}\n\n"

# Create a linkable setting - @todo append them to the bottom of the page
def setting(type: str):
    _, *_, name = re.split(r"[.*]", type)
    return f"`{name}` {{ #{type} }}\n\n[{type}]: #{type}\n\n"

# -----------------------------------------------------------------------------

# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve_path(path: str, page: Page, files: Files):
    try:
        path, anchor, *_ = f"{path}#".split("#")
        path = _resolve(files.get_file_from_path(path), page)
        return "#".join([path, anchor]) if anchor else path
    except:
        log.error(f"Unknown path: {path}")
        return path
# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve(file: File, page: Page):
    path = posixpath.relpath(file.src_uri, page.file.src_uri)
    return posixpath.sep.join(path.split(posixpath.sep)[1:])

# -----------------------------------------------------------------------------

# Create badge
def _badge(icon: str, text: str = "", type: str = ""):
    classes = f"mdx-badge mdx-badge--{type}" if type else "mdx-badge"
    return "".join([
        f"<span class=\"{classes}\">",
        *([f"<span class=\"mdx-badge__icon\">{icon}</span>"] if icon else []),
        *([f"<span class=\"mdx-badge__text\">{text}</span>"] if text else []),
        f"</span>",
    ])

# Create badge for version
def _badge_for_version(text: str, page: Page, files: Files):
    spec = text
    path = f"{os.path.dirname(page.file.src_uri)}/CHANGELOG.md#{spec}"
    icon = "material-tag-outline"
    href = _resolve_path(f"{CONVENTIONS_PATH}#version", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Minimum version')",
        text = f"[{text}]({_resolve_path(path, page, files)})" if spec else ""
    )

# Create badge for feature
def _badge_for_feature(text: str, page: Page, files: Files):
    icon = "material-toggle-switch"
    href = _resolve_path(f"{CONVENTIONS_PATH}#feature", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Optional feature')",
        text = text
    )

# Create badge for example
def _badge_for_example(text: str, page: Page, files: Files):
    return "\n".join([
        _badge_for_example_download(text, page, files),
        _badge_for_example_view(text, page, files)
    ])

# Create badge for example view
def _badge_for_example_view(text: str, page: Page, files: Files):
    icon = "material-folder-eye"
    href = f"https://github.com/helmless/helmless/tree/main/examples/{text}"
    return _badge(
        icon = f"[:{icon}:]({href} 'View example')",
        type = "right"
    )

# Create badge for example download
def _badge_for_example_download(text: str, page: Page, files: Files):
    icon = "material-folder-download"
    href = f"https://github.com/helmless/helmless/archive/refs/heads/main.zip"
    return _badge(
        icon = f"[:{icon}:]({href} 'Download example')",
        text = f"[`.zip`]({href})",
        type = "right"
    )

# Create badge for default value
def _badge_for_default(text: str, page: Page, files: Files):
    icon = "material-water"
    href = _resolve_path(f"{CONVENTIONS_PATH}#default", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Default value')",
        text = text
    )

# Create badge for empty default value
def _badge_for_default_none(page: Page, files: Files):
    icon = "material-water-outline"
    href = _resolve_path(f"{CONVENTIONS_PATH}#default", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Default value is empty')"
    )

# Create badge for computed default value
def _badge_for_default_computed(page: Page, files: Files):
    icon = "material-water-check"
    href = _resolve_path(f"{CONVENTIONS_PATH}#default", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Default value is computed')"
    )

# Create badge for required value flag
def _badge_for_required(page: Page, files: Files):
    icon = "material-radiobox-marked"
    href = _resolve_path(f"{CONVENTIONS_PATH}#required", page, files)
    return _badge(
        icon = f"[:{icon}:{{.red-icon}}]({href} 'Required value')"
    )

# Create badge for experimental flag
def _badge_for_experimental(page: Page, files: Files):
    icon = "material-flask-outline"
    href = _resolve_path(f"{CONVENTIONS_PATH}#experimental", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Experimental')"
    )

# Create badge for type
def _badge_for_type(text: str, page: Page, files: Files):
    icon = "material-code-brackets"
    href = _resolve_path(f"{CONVENTIONS_PATH}#type", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Schema type')",
        text = text
    )

# Add these new functions at the bottom with other badge functions:

def _badge_for_max_length(text: str, page: Page, files: Files):
    icon = "material-ruler"
    href = _resolve_path(f"{CONVENTIONS_PATH}#max-length", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Maximum length')",
        text = text
    )

def _badge_for_min_length(text: str, page: Page, files: Files):
    icon = "material-ruler"
    href = _resolve_path(f"{CONVENTIONS_PATH}#min-length", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Minimum length')",
        text = text
    )

def _badge_for_pattern(text: str, page: Page, files: Files):
    icon = "material-regex"
    href = _resolve_path(f"{CONVENTIONS_PATH}#pattern", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Pattern')",
        text = text
    )

def _badge_for_deprecated(text: str, page: Page, files: Files):
    icon = "material-alert"
    href = _resolve_path(f"{CONVENTIONS_PATH}#deprecated", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Deprecated')",
        text = text if text else ""
    )

def _badge_for_enum(text: str, page: Page, files: Files):
    icon = "material-format-list-bulleted"
    href = _resolve_path(f"{CONVENTIONS_PATH}#enum", page, files)
    return _badge(
        icon = f"[:{icon}:]({href} 'Enumeration')",
        text = text
    )
