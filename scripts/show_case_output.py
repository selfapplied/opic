#!/usr/bin/env python3
"""
Pretty-print OPIC case study outputs.

Many of the `.out` artifacts are generated as single lines with double-space
separators.  This helper restores human-friendly newlines (falling back to the
original text when true line breaks are already present) and optionally wraps
the content for terminals.
"""

from __future__ import annotations

import argparse
import sys
import re
from pathlib import Path
from textwrap import fill


def restore_newlines(text: str) -> str:
    """If the file is a single unbroken line, treat double spaces as newlines."""
    stripped = text.strip("\n")
    if "\n" in stripped:
        return stripped

    # Replace consecutive double-spaces with newlines while preserving spacing
    # inside numbers like "1 000" by only collapsing sequences of two or more.
    restored = []
    buffer = []
    i = 0
    length = len(stripped)
    while i < length:
        if stripped[i] == " " and i + 1 < length and stripped[i + 1] == " ":
            if buffer:
                restored.append("".join(buffer).rstrip())
                buffer = []
            restored.append("\n")
            while i < length and stripped[i] == " ":
                i += 1
            continue
        buffer.append(stripped[i])
        i += 1
    if buffer:
        restored.append("".join(buffer))
    joined = "".join(restored).strip("\n")

    # Inject newlines before bullets and after colons that precede lists.
    joined = joined.replace(":\n- ", ":\n- ")
    joined = joined.replace(":- ", ":\n- ")
    joined = joined.replace(": - ", ":\n- ")
    joined = re.sub(r' - (?=[A-Za-z`])', '\n- ', joined)
    joined = re.sub(r'(?<!\n)(={6,})', r'\n\1', joined)
    joined = re.sub(r'\n+', '\n', joined)
    return joined.strip("\n")


def format_text(text: str, width: int | None) -> str:
    if width is None:
        return text
    return "\n".join(
        fill(line, width=width, replace_whitespace=False)
        if line.strip() and not line.startswith(" ")
        else line
        for line in text.splitlines()
    )


def show_file(path: Path, width: int | None) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    restored = restore_newlines(text)
    formatted = format_text(restored, width)
    print(f"===== {path} =====")
    print(formatted)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pretty-print OPIC case study output files."
    )
    parser.add_argument("files", nargs="+", type=Path, help="Path(s) to .out files")
    parser.add_argument(
        "--wrap",
        type=int,
        default=None,
        metavar="WIDTH",
        help="Wrap paragraphs to WIDTH columns (default: no reflow)",
    )
    args = parser.parse_args()

    for file_path in args.files:
        if not file_path.exists():
            print(f"[warn] {file_path} does not exist", file=sys.stderr)
            continue
        show_file(file_path, args.wrap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

