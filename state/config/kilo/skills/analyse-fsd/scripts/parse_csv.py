#!/usr/bin/env python3
"""
Parse .csv files with automatic encoding and delimiter detection.

Output: JSON with metadata, columns, data, and statistics.
Usage: python parse_csv.py <filepath> [--compact] [--max-rows N] [--encoding ENC]
"""
import sys
import json
import os
import csv
from pathlib import Path


def detect_encoding(filepath: str) -> str:
    """Detect file encoding using chardet."""
    try:
        import chardet
        with open(filepath, "rb") as f:
            raw = f.read(min(os.path.getsize(filepath), 1024 * 1024))  # Read max 1MB
        result = chardet.detect(raw)
        encoding = result.get("encoding", "utf-8")
        confidence = result.get("confidence", 0)
        return encoding if confidence > 0.5 else "utf-8"
    except ImportError:
        # Fallback: try common encodings
        for enc in ["utf-8", "latin-1", "cp1252", "iso-8859-1"]:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    f.read(1024)
                return enc
            except (UnicodeDecodeError, UnicodeError):
                continue
        return "utf-8"


def detect_delimiter(filepath: str, encoding: str) -> str:
    """Detect CSV delimiter."""
    try:
        with open(filepath, "r", encoding=encoding) as f:
            sample = f.read(8192)  # Read 8KB sample

        # Use csv.Sniffer
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except Exception:
        # Fallback: try each delimiter
        for delim in [",", ";", "\t", "|"]:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    reader = csv.reader(f, delimiter=delim)
                    row = next(reader, None)
                    if row and len(row) > 1:
                        return delim
            except Exception:
                continue
        return ","


def parse_csv(filepath: str, compact: bool = False, max_rows: int = None,
              encoding: str = None) -> dict:
    """Parse a .csv file and return structured content."""
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "format": "csv"}

    # Auto-detect encoding if not specified
    if encoding is None:
        encoding = detect_encoding(filepath)

    # Auto-detect delimiter
    delimiter = detect_delimiter(filepath, encoding)

    try:
        with open(filepath, "r", encoding=encoding, errors="replace") as f:
            reader = csv.DictReader(f, delimiter=delimiter)

            if reader.fieldnames is None:
                return {"error": "Empty CSV file", "format": "csv"}

            columns = list(reader.fieldnames)
            rows = []
            row_count = 0
            null_counts = {col: 0 for col in columns}

            for row in reader:
                row_count += 1
                if max_rows and row_count > max_rows:
                    break

                # Count nulls
                for col in columns:
                    if not row.get(col, "").strip():
                        null_counts[col] += 1

                rows.append(row)

    except UnicodeDecodeError as e:
        return {
            "error": f"Encoding error: {str(e)}. Try specifying --encoding.",
            "format": "csv",
            "detected_encoding": encoding,
        }
    except Exception as e:
        return {"error": f"Failed to parse CSV: {str(e)}", "format": "csv"}

    # Get total row count (without reading all data)
    total_rows = row_count
    if max_rows and row_count >= max_rows:
        try:
            with open(filepath, "r", encoding=encoding, errors="replace") as f:
                total_rows = sum(1 for _ in f) - 1  # Subtract header
        except Exception:
            pass

    # Detect column types
    column_types = {}
    if rows:
        for col in columns:
            values = [row.get(col, "") for row in rows[:100]]  # Sample first 100
            column_types[col] = _detect_column_type(values)

    # Calculate statistics
    stats = {}
    if not compact:
        for col in columns:
            non_empty = [row.get(col, "") for row in rows if row.get(col, "").strip()]
            stats[col] = {
                "non_empty_count": len(non_empty),
                "unique_count": len(set(non_empty)),
                "null_count": null_counts[col],
                "type": column_types.get(col, "string"),
            }

    # File metadata
    file_stat = os.stat(filepath)

    result = {
        "format": "csv",
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "metadata": {
            "file_size_bytes": file_stat.st_size,
            "file_size_human": _format_size(file_stat.st_size),
            "encoding": encoding,
            "delimiter": delimiter,
            "delimiter_name": _delimiter_name(delimiter),
            "columns": columns,
        },
        "statistics": {
            "total_rows": total_rows,
            "total_columns": len(columns),
            "rows_returned": len(rows),
            "truncated": total_rows > len(rows),
            "null_summary": null_counts,
        },
        "column_types": column_types,
        "data": rows,
    }

    if not compact:
        result["column_statistics"] = stats

    return result


def _detect_column_type(values: list) -> str:
    """Detect the type of a column from sample values."""
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return "empty"

    # Check for numbers
    int_count = 0
    float_count = 0
    for v in non_empty:
        try:
            int(v)
            int_count += 1
        except ValueError:
            try:
                float(v)
                float_count += 1
            except ValueError:
                pass

    if int_count == len(non_empty):
        return "integer"
    if (int_count + float_count) == len(non_empty):
        return "number"

    # Check for dates (common formats)
    date_patterns = 0
    for v in non_empty[:20]:  # Sample
        if any(c in v for c in ["/", "-", "."]) and len(v) >= 6:
            date_patterns += 1
    if date_patterns > len(non_empty) * 0.7:
        return "date-like"

    return "string"


def _delimiter_name(delim: str) -> str:
    """Get human-readable delimiter name."""
    names = {
        ",": "comma",
        ";": "semicolon",
        "\t": "tab",
        "|": "pipe",
    }
    return names.get(delim, f"unknown ({repr(delim)})")


def _format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_csv.py <filepath> [--compact] [--max-rows N] [--encoding ENC]")
        print("")
        print("Parses .csv files and outputs structured JSON.")
        print("")
        print("Options:")
        print("  --compact        Simplify output (no statistics)")
        print("  --max-rows N     Limit rows returned (default: all)")
        print("  --encoding ENC   Force encoding (default: auto-detect)")
        sys.exit(1)

    filepath = sys.argv[1]
    compact = "--compact" in sys.argv
    max_rows = None
    encoding = None

    if "--max-rows" in sys.argv:
        idx = sys.argv.index("--max-rows")
        if idx + 1 < len(sys.argv):
            try:
                max_rows = int(sys.argv[idx + 1])
            except ValueError:
                print("Error: --max-rows requires a number")
                sys.exit(1)

    if "--encoding" in sys.argv:
        idx = sys.argv.index("--encoding")
        if idx + 1 < len(sys.argv):
            encoding = sys.argv[idx + 1]

    result = parse_csv(filepath, compact=compact, max_rows=max_rows, encoding=encoding)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
