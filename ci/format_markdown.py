#!/usr/bin/env python3
"""Align the columns of every Markdown table in the repository.

    ci/format_markdown.py            Rewrite the tables in place.
    ci/format_markdown.py --check    Fail if any table is unaligned. Changes nothing.

A Markdown table renders identically whether or not its pipes line up, so this is entirely about
the source. These files are read as often in an editor as in a browser: an author checking a
number, a reader following a link into the repository, a reviewer reading a diff. A table whose
columns line up can be read in the source; one whose columns do not has to be rendered first.

The alignment is by display width rather than by character count, because a cell holding
mathematics or a code span is still ASCII but a cell holding a box-drawing character is not.
Combining marks and zero-width characters count as nothing, wide East Asian characters count as
two, everything else counts as one.

Escaped pipes inside a cell (`\\|`) are not column separators and are not split on. An unescaped
pipe inside a code span still is, which is a real limitation of Markdown itself rather than of
this script: write it as `\\|`.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

SKIP_PARTS = {".git", ".venv", "libs", "build", "__pycache__", "temp"}

# A delimiter row: pipes, hyphens, and optional colons for alignment. This is what tells a table
# apart from two consecutive lines that happen to contain pipes.
DELIMITER = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")


def width(text: str) -> int:
    """The display width of a string, in terminal columns."""
    total = 0
    for character in text:
        if unicodedata.combining(character):
            continue
        total += 2 if unicodedata.east_asian_width(character) in ("W", "F") else 1
    return total


def split_row(line: str) -> list[str]:
    """Split one table row into its cells, honouring escaped pipes."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]

    cells = []
    current = ""
    escaped = False
    for character in body:
        if escaped:
            current += character
            escaped = False
        elif character == "\\":
            current += character
            escaped = True
        elif character == "|":
            cells.append(current.strip())
            current = ""
        else:
            current += character
    cells.append(current.strip())
    return cells


def alignment_of(cell: str) -> str:
    """Read a delimiter cell's colons: "left", "right", "center" or "default"."""
    body = cell.strip()
    left = body.startswith(":")
    right = body.endswith(":")
    if left and right:
        return "center"
    if right:
        return "right"
    if left:
        return "left"
    return "default"


def pad(text: str, target: int, align: str) -> str:
    """Pad a cell to `target` display columns."""
    slack = max(0, target - width(text))
    if align == "right":
        return " " * slack + text
    if align == "center":
        left = slack // 2
        return " " * left + text + " " * (slack - left)
    return text + " " * slack


def format_table(rows: list[list[str]], aligns: list[str]) -> list[str]:
    """Render a parsed table back out with every column padded to its widest cell."""
    columns = max(len(row) for row in rows)
    aligns = (aligns + ["default"] * columns)[:columns]

    # A short row is padded with empty cells rather than rejected: a table whose last row is
    # missing a trailing cell is legal Markdown and reformatting it should not lose data.
    rows = [row + [""] * (columns - len(row)) for row in rows]

    # The delimiter row is excluded from the measurement. Its cells are runs of hyphens whose
    # length is whatever the author happened to type, and counting them would let "|------|" pin
    # a column two characters wider than its widest real cell, forever.
    content = [row for number, row in enumerate(rows) if number != 1]

    widths = []
    for index in range(columns):
        # Three is the narrowest a delimiter cell can be and still carry both colons.
        widths.append(max(3, max(width(row[index]) for row in content)))

    out = []
    for number, row in enumerate(rows):
        if number == 1:
            cells = []
            for index in range(columns):
                align = aligns[index]
                size = widths[index]
                if align == "center":
                    cells.append(":" + "-" * (size - 2) + ":")
                elif align == "right":
                    cells.append("-" * (size - 1) + ":")
                elif align == "left":
                    cells.append(":" + "-" * (size - 1))
                else:
                    cells.append("-" * size)
            out.append("| " + " | ".join(cells) + " |")
        else:
            # The last column is padded like every other one, so the closing rule lines up down
            # the whole table. That is the entire point of doing this: a table you can read in
            # the source without rendering it first.
            cells = [
                pad(row[index], widths[index], aligns[index])
                for index in range(columns)
            ]
            out.append("| " + " | ".join(cells) + " |")

    return out


def format_text(text: str) -> str:
    """Align every table in one Markdown document."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    index = 0
    fence = False

    while index < len(lines):
        line = lines[index]

        if line.lstrip().startswith("```"):
            fence = not fence
            out.append(line)
            index += 1
            continue

        is_table = (
            not fence
            and "|" in line
            and index + 1 < len(lines)
            and DELIMITER.match(lines[index + 1])
            and "|" in lines[index + 1]
        )
        if not is_table:
            out.append(line)
            index += 1
            continue

        # Collect the header, the delimiter, and every body row that follows.
        block = [lines[index], lines[index + 1]]
        cursor = index + 2
        while cursor < len(lines) and "|" in lines[cursor] and lines[cursor].strip():
            block.append(lines[cursor])
            cursor += 1

        rows = [split_row(row) for row in block]
        aligns = [alignment_of(cell) for cell in rows[1]]
        for formatted in format_table(rows, aligns):
            out.append(formatted + "\n")

        index = cursor

    return "".join(out)


def main() -> int:
    """Format, or check, every Markdown file under the repository root."""
    check = "--check" in sys.argv[1:]
    unknown = [arg for arg in sys.argv[1:] if arg != "--check"]
    if unknown:
        print(f"usage: {sys.argv[0]} [--check]", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parent.parent
    changed = []
    total = 0

    for path in sorted(root.rglob("*.md")):
        if SKIP_PARTS & set(path.relative_to(root).parts):
            continue
        total += 1
        original = path.read_text(encoding="utf-8")
        formatted = format_text(original)
        if formatted == original:
            continue
        changed.append(path.relative_to(root))
        if not check:
            path.write_text(formatted, encoding="utf-8")

    if check:
        if changed:
            for path in changed:
                print(f"{path}: table columns are not aligned", file=sys.stderr)
            print(
                f"\nerror: {len(changed)} file(s) with unaligned tables; "
                "run ci/format_markdown.py.",
                file=sys.stderr,
            )
            return 1
        print(f"Markdown tables: {total} file(s) aligned correctly.")
        return 0

    for path in changed:
        print(f"aligned {path}")
    print(f"Markdown tables: {len(changed)} of {total} file(s) rewritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
