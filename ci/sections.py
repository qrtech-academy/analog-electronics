#!/usr/bin/env python3
"""Check that every appendix section this course cites actually exists.

The appendices refer to each other constantly, by section number and in running prose: "A.3
measured the error in the time domain", "that is B.1's second condition", "specified in L07 A.5".
The test suites do it too, 170 times, in the comment above each TEST.

None of that is a link, so ci/links.sh cannot see it. That matters because renumbering a section,
or moving one to another lecture, leaves every bare citation of it pointing at whatever now happens
to occupy that number, which is worse than a dangling link: it reads as correct. The restructure
from six lectures to ten did exactly this, and the citations it invalidated were found by hand.

So this reads the headings, builds the map of what exists, and checks every citation against it:

    A.3         in lectures/L04/...   ->  L04's appendix A, section 3
    L07 A.5     anywhere              ->  L07's appendix A, section 5

A citation inside a link is checked against the lecture the link points at, so
"[B.6](../../L06/appendix/...)" is read as L06's B.6 rather than as the citing file's.

What this cannot catch is a citation that points at a section which exists but is the wrong one.
Only reading it does that.

Usage:
  sections.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

HEADING = re.compile(r"^#{2,3}\s+([ABC])\.(\d+)\b", re.MULTILINE)
# "L07 A.5" or "L07's A.5": an explicit lecture, then a section.
QUALIFIED = re.compile(r"\bL(\d{2})(?:'s)?\s+([ABC])\.(\d+)\b")
# A bare "A.5", not preceded by a lecture tag.
BARE = re.compile(r"(?<![\w./-])([ABC])\.(\d+)\b")

APPENDIX_OF = {"A": "a_", "B": "b_", "C": "c_"}


def lecture_of(path):
    match = re.search(r"lectures/(L\d{2})/", path.as_posix())
    return match.group(1) if match else None


def build_map():
    """lecture -> letter -> set of section numbers that exist."""
    sections = {}
    for path in sorted((ROOT / "lectures").rglob("appendix/*.md")):
        lecture = lecture_of(path)
        name = path.name
        letter = next((k for k, v in APPENDIX_OF.items() if name.startswith(v)), None)
        if lecture is None or letter is None:
            continue
        found = {int(n) for lt, n in HEADING.findall(path.read_text()) if lt == letter}
        sections.setdefault(lecture, {}).setdefault(letter, set()).update(found)
    return sections


LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def strip_uncitable(text):
    """Blank out spans where an "A.3" is not a citation: code and value tags."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text


def split_links(text, home):
    """Return (plain text, [(link text, lecture it points at)]).

    "[B.6](../../L06/appendix/...)" cites L06's B.6, not this file's, so the link text is
    checked against the lecture in the target rather than against the file's own.
    """
    linked = []
    for label, target in LINK.findall(text):
        match = re.search(r"(L\d{2})/", target)
        linked.append((label, match.group(1) if match else home))
    return LINK.sub("", text), linked


def cite(path, sections, lecture, letter, number, failures):
    have = sections.get(lecture, {}).get(letter, set())
    if not have:
        failures.append(
            f"{path}: cites {lecture} {letter}.{number}, "
            f"but {lecture} has no appendix {letter}"
        )
    elif int(number) not in have:
        failures.append(
            f"{path}: cites {lecture} {letter}.{number}, which does not exist "
            f"(that appendix stops at {letter}.{max(have)})"
        )


def check_file(path, sections, failures):
    text = strip_uncitable(path.read_text())
    home = lecture_of(path)
    shown = path.relative_to(ROOT)

    text, linked = split_links(text, home)
    for label, lecture in linked:
        if lecture is None:
            continue
        label = QUALIFIED.sub("", label)
        for letter, number in BARE.findall(label):
            cite(shown, sections, lecture, letter, number, failures)

    for lecture_digits, letter, number in QUALIFIED.findall(text):
        cite(shown, sections, f"L{lecture_digits}", letter, number, failures)

    if home is None:
        return
    # Bare citations mean this file's own lecture. Remove the qualified ones first so their
    # section part is not also read as a bare citation of the wrong lecture.
    bare_text = QUALIFIED.sub("", text)
    for letter, number in BARE.findall(bare_text):
        cite(shown, sections, home, letter, number, failures)


def main():
    sections = build_map()
    if not sections:
        # No appendix has been written yet. That is the state of this repository on the day it is
        # created, and it must not read like a failure: a check that could not run has to say so
        # rather than report red, or the first commit is red for a reason nobody can act on.
        #
        # It says SKIP loudly instead, and starts failing the moment there is an appendix to
        # check, which is the point at which a broken cross-reference becomes possible.
        print("SKIP  no appendix sections yet, so no cross-reference can be checked.")
        return 0

    failures = []
    checked = 0
    paths = (
        sorted((ROOT / "lectures").rglob("*.md"))
        + sorted((ROOT / "lectures").rglob("exercises/**/*.cpp"))
        + sorted((ROOT / "lectures").rglob("exercises/**/*.hpp"))
    )
    for path in paths:
        if "/work/" in path.as_posix():
            continue
        checked += 1
        check_file(path, sections, failures)

    for line in failures:
        print(line, file=sys.stderr)
    total = sum(len(v) for lec in sections.values() for v in lec.values())
    if failures:
        print(
            f"\nerror: {len(failures)} citation(s) point at a section that does not exist.",
            file=sys.stderr,
        )
        return 1
    print(
        f"Sections: every citation in {checked} file(s) resolves against {total} section(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
