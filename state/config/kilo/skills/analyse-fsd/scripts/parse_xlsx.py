#!/usr/bin/env python3
"""
Parse .xlsx files and extract structured content.

Output: JSON with metadata, sheets, data, and statistics.
Usage: python parse_xlsx.py <filepath> [--compact] [--max-rows N]
"""
import sys
import json
import os
from pathlib import Path


def parse_xlsx(filepath: str, compact: bool = False, max_rows: int = None) -> dict:
    """Parse an .xlsx file and return structured content."""
    try:
        import pandas as pd
    except ImportError:
        return {
            "error": "pandas + openpyxl not installed. Run: bash scripts/install_deps.sh",
            "format": "xlsx",
            "filepath": filepath,
        }

    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "format": "xlsx"}

    try:
        xls = pd.ExcelFile(filepath, engine="openpyxl")
    except Exception as e:
        return {"error": f"Failed to parse XLSX: {str(e)}", "format": "xlsx"}

    sheets = {}
    total_rows = 0
    total_cells = 0

    for sheet_name in xls.sheet_names:
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name, engine="openpyxl")

            row_count = len(df)
            col_count = len(df.columns)
            total_rows += row_count
            total_cells += row_count * col_count

            # Get column types
            column_types = {}
            for col in df.columns:
                dtype = str(df[col].dtype)
                column_types[str(col)] = dtype

            # Get basic statistics for numeric columns
            stats = {}
            if not compact:
                for col in df.columns:
                    if df[col].dtype in ["int64", "float64"]:
                        stats[str(col)] = {
                            "mean": round(float(df[col].mean()), 2) if not df[col].isna().all() else None,
                            "min": round(float(df[col].min()), 2) if not df[col].isna().all() else None,
                            "max": round(float(df[col].max()), 2) if not df[col].isna().all() else None,
                            "null_count": int(df[col].isna().sum()),
                        }

            # Handle max_rows limit
            data_rows = df.fillna("").to_dict(orient="records")
            truncated = False
            if max_rows and len(data_rows) > max_rows:
                data_rows = data_rows[:max_rows]
                truncated = True

            sheet_data = {
                "columns": [str(col) for col in df.columns],
                "column_types": column_types,
                "row_count": row_count,
                "col_count": col_count,
                "data": data_rows,
                "null_counts": {str(col): int(df[col].isna().sum()) for col in df.columns},
                "has_empty_rows": int(df.isna().all(axis=1).sum()),
            }

            if not compact:
                sheet_data["statistics"] = stats
            if truncated:
                sheet_data["truncated"] = True
                sheet_data["total_rows"] = row_count

            sheets[sheet_name] = sheet_data

        except Exception as e:
            sheets[sheet_name] = {
                "error": f"Failed to parse sheet '{sheet_name}': {str(e)}",
                "columns": [],
                "row_count": 0,
                "data": [],
            }

    # File metadata
    file_stat = os.stat(filepath)

    result = {
        "format": "xlsx",
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "metadata": {
            "file_size_bytes": file_stat.st_size,
            "file_size_human": _format_size(file_stat.st_size),
            "sheet_names": xls.sheet_names,
        },
        "statistics": {
            "total_sheets": len(sheets),
            "total_rows": total_rows,
            "total_cells": total_cells,
            "sheet_summary": {
                name: {
                    "rows": s.get("row_count", 0),
                    "cols": s.get("col_count", 0),
                    "has_data": s.get("row_count", 0) > 0,
                }
                for name, s in sheets.items()
            },
        },
        "sheets": sheets,
    }

    return result


def _format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_xlsx.py <filepath> [--compact] [--max-rows N]")
        print("")
        print("Parses .xlsx files and outputs structured JSON.")
        print("")
        print("Options:")
        print("  --compact        Simplify output (no statistics)")
        print("  --max-rows N     Limit rows per sheet (default: all)")
        sys.exit(1)

    filepath = sys.argv[1]
    compact = "--compact" in sys.argv
    max_rows = None

    if "--max-rows" in sys.argv:
        idx = sys.argv.index("--max-rows")
        if idx + 1 < len(sys.argv):
            try:
                max_rows = int(sys.argv[idx + 1])
            except ValueError:
                print("Error: --max-rows requires a number")
                sys.exit(1)

    result = parse_xlsx(filepath, compact=compact, max_rows=max_rows)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
