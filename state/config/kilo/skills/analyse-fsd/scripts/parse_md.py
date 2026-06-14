#!/usr/bin/env python3
"""
Parse .md files and extract structured content.

Output: JSON with metadata, sections, tables, code blocks, and full text.
Usage: python parse_md.py <filepath> [--compact]
"""
import sys
import json
import os
import re
from pathlib import Path


def parse_md(filepath: str, compact: bool = False) -> dict:
    """Parse a .md file and return structured content."""
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "format": "markdown"}

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}", "format": "markdown"}

    # Extract YAML frontmatter
    frontmatter = {}
    body = content
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        try:
            import yaml
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except ImportError:
            # Manual simple YAML parsing
            frontmatter = _parse_simple_yaml(fm_match.group(1))
        except Exception:
            frontmatter = {"raw": fm_match.group(1)}
        body = content[fm_match.end():]

    # Parse sections
    sections = []
    current_section = {
        "heading": "Preamble",
        "level": 0,
        "content": [],
        "paragraphs": [],
    }

    # Track code blocks
    code_blocks = []
    in_code_block = False
    code_block_lang = ""
    code_block_lines = []

    # Track lists
    lists = []
    current_list = None

    for line in body.split("\n"):
        # Handle code blocks
        if line.strip().startswith("```"):
            if in_code_block:
                # End code block
                code_blocks.append({
                    "language": code_block_lang,
                    "line_start": code_blocks[-1]["line_start"] + 1 if code_blocks else 1,
                    "content": "\n".join(code_block_lines),
                })
                in_code_block = False
                code_block_lang = ""
                code_block_lines = []
            else:
                # Start code block
                in_code_block = True
                code_block_lang = line.strip()[3:].strip()
                code_block_lines = []
                if current_section["content"]:
                    current_section["paragraphs"].append({
                        "type": "code_block",
                        "language": code_block_lang,
                    })
            continue

        if in_code_block:
            code_block_lines.append(line)
            continue

        # Handle headings
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            # Save previous section
            if current_section["content"] or current_section["paragraphs"]:
                sections.append(current_section)

            level = len(heading_match.group(1))
            current_section = {
                "heading": heading_match.group(2).strip(),
                "level": level,
                "content": [],
                "paragraphs": [],
            }
            continue

        # Handle tables
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # Skip separator rows (---|---|---)
            if all(re.match(r"^[-:]+$", c) for c in cells):
                current_section["paragraphs"].append({"type": "table_separator"})
                continue
            if not current_list or current_list.get("type") != "table":
                current_list = {"type": "table", "rows": []}
                lists.append(current_list)
            current_list["rows"].append(cells)
            current_section["content"].append(line.strip())
            current_section["paragraphs"].append({
                "type": "table_row",
                "cells": cells,
            })
            continue

        # Handle bullet lists
        bullet_match = re.match(r"^(\s*)[-*+]\s+(.*)", line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            text = bullet_match.group(2).strip()
            current_section["content"].append(line.strip())
            current_section["paragraphs"].append({
                "type": "list_item",
                "indent": indent,
                "text": text,
            })
            continue

        # Handle numbered lists
        numbered_match = re.match(r"^(\s*)\d+[.)]\s+(.*)", line)
        if numbered_match:
            indent = len(numbered_match.group(1))
            text = numbered_match.group(2).strip()
            current_section["content"].append(line.strip())
            current_section["paragraphs"].append({
                "type": "numbered_item",
                "indent": indent,
                "text": text,
            })
            continue

        # Regular content
        text = line.strip()
        if text:
            current_section["content"].append(text)
            current_section["paragraphs"].append({
                "type": "text",
                "text": text,
                "is_bold": "**" in text or "__" in text,
                "is_italic": "*" in text or "_" in text,
                "has_links": "[" in text and "](" in text,
                "has_code": "`" in text,
            })

    # Don't forget the last section
    if current_section["content"] or current_section["paragraphs"]:
        sections.append(current_section)

    # Extract links
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body)
    formatted_links = [{"text": t, "url": u} for t, u in links]

    # Calculate statistics
    full_text = content
    word_count = len(full_text.split())
    line_count = len(full_text.split("\n"))
    heading_count = len([s for s in sections if s["heading"] != "Preamble"])

    result = {
        "format": "markdown",
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "frontmatter": frontmatter,
        "statistics": {
            "total_sections": len(sections),
            "total_headings": heading_count,
            "total_code_blocks": len(code_blocks),
            "total_tables": len([l for l in lists if l.get("type") == "table"]),
            "total_links": len(formatted_links),
            "total_lines": line_count,
            "total_words": word_count,
            "total_characters": len(full_text),
        },
        "sections": sections,
        "code_blocks": code_blocks,
        "tables": [l for l in lists if l.get("type") == "table"],
        "links": formatted_links,
        "full_text": full_text,
    }

    if compact:
        for section in result["sections"]:
            section.pop("paragraphs", None)

    return result


def _parse_simple_yaml(text: str) -> dict:
    """Simple YAML parser for frontmatter (no PyYAML dependency)."""
    result = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([^:]+):\s*(.*)", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            # Remove quotes
            if value and value[0] in ['"', "'"] and value[-1] == value[0]:
                value = value[1:-1]
            result[key] = value
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_md.py <filepath> [--compact]")
        print("")
        print("Parses .md files and outputs structured JSON.")
        print("")
        print("Options:")
        print("  --compact    Simplify output (no paragraph details)")
        sys.exit(1)

    filepath = sys.argv[1]
    compact = "--compact" in sys.argv

    result = parse_md(filepath, compact=compact)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
