#!/usr/bin/env python3
"""
Parse .pdf files and extract structured text content.

Output: JSON with metadata, pages, tables, and full text.
Usage: python parse_pdf.py <filepath> [--compact]
"""
import sys
import json
import os


def parse_pdf(filepath: str, compact: bool = False) -> dict:
    """Parse a .pdf file and return structured content."""
    try:
        import pdfplumber
    except ImportError:
        return {
            "error": "pdfplumber not installed. Run: bash scripts/install_deps.sh",
            "format": "pdf",
            "filepath": filepath,
        }

    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "format": "pdf"}

    try:
        pdf = pdfplumber.open(filepath)
    except Exception as e:
        return {"error": f"Failed to parse PDF: {str(e)}", "format": "pdf"}

    pages = []
    full_text = []
    all_tables = []

    try:
        for i, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text() or ""

            # Extract tables
            page_tables = page.extract_tables() or []

            # Process tables into structured format
            processed_tables = []
            for t_idx, table in enumerate(page_tables):
                if not table:
                    continue

                processed_table = {
                    "page": i + 1,
                    "table_index": t_idx,
                    "headers": table[0] if table else [],
                    "rows": table[1:] if len(table) > 1 else [],
                    "row_count": len(table),
                    "col_count": len(table[0]) if table else 0,
                }
                processed_tables.append(processed_table)
                all_tables.append(processed_table)

            # Extract page dimensions
            width = float(page.width) if page.width else 0
            height = float(page.height) if page.height else 0

            page_data = {
                "page_number": i + 1,
                "content": text.strip(),
                "word_count": len(text.split()),
                "char_count": len(text),
                "table_count": len(processed_tables),
                "tables": processed_tables if not compact else len(processed_tables),
                "dimensions": {
                    "width": round(width, 2),
                    "height": round(height, 2),
                },
            }
            pages.append(page_data)
            full_text.append(text)

    finally:
        pdf.close()

    # Extract metadata from PDF info
    metadata = {}
    try:
        pdf = pdfplumber.open(filepath)
        if pdf.metadata:
            metadata = {
                "title": pdf.metadata.get("Title", ""),
                "author": pdf.metadata.get("Author", ""),
                "subject": pdf.metadata.get("Subject", ""),
                "creator": pdf.metadata.get("Creator", ""),
                "producer": pdf.metadata.get("Producer", ""),
                "created": str(pdf.metadata.get("CreationDate", "")),
                "modified": str(pdf.metadata.get("ModDate", "")),
                "keywords": pdf.metadata.get("Keywords", ""),
            }
        pdf.close()
    except Exception:
        pass

    # Calculate statistics
    total_words = sum(p.get("word_count", 0) for p in pages)
    total_chars = sum(p.get("char_count", 0) for p in pages)

    result = {
        "format": "pdf",
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "metadata": metadata,
        "statistics": {
            "total_pages": len(pages),
            "total_words": total_words,
            "total_characters": total_chars,
            "total_tables": len(all_tables),
            "pages_with_tables": len([p for p in pages if (p["table_count"] if isinstance(p["table_count"], int) else 0) > 0]),
            "pages_with_text": len([p for p in pages if p["content"]]),
        },
        "pages": pages,
        "tables": all_tables,
        "full_text": "\n".join(full_text),
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_pdf.py <filepath> [--compact]")
        print("")
        print("Parses .pdf files and outputs structured JSON.")
        print("")
        print("Options:")
        print("  --compact    Simplify table output (show counts only)")
        sys.exit(1)

    filepath = sys.argv[1]
    compact = "--compact" in sys.argv

    result = parse_pdf(filepath, compact=compact)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
