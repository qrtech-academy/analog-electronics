#!/usr/bin/env python3
"""Check that a reader following the appendices can actually build the test suites.

    ci/buildable.py            Check every lecture.
    ci/buildable.py --list     Print what each lecture's tests need and where it is named.

A test file for a class the reader has not written yet keeps out of the way by guarding itself:

    #if __has_include("ael/cdac/charge_redistribution.hpp")

That guard is a promise with two ends, and this script checks both, because each end fails
silently in its own way.

**The prose end.** The test end is checked by the compiler; the prose end is not checked by
anything. The appendix specifies an interface and a stub, never mentions the concrete header, and
the reader who follows it exactly ends up with a suite that compiles, passes, and ran none of the
tests that matter. It looks like success. So every path a lecture's tests guard on must be named
by an appendix or by info/, spelled the same way.

A guard on an earlier lecture's header is allowed: L03's suite quantizes a chain L01 specified,
and those tests vanish if L01 has not been done. Naming the header is what stops the vanishing
from being silent, so it is enough for any appendix to name it, not only this lecture's.

**The include end**, in two parts.

First, every "ael/..." a test file includes must be named somewhere, guarded or not. A header the
reader is never told to write is a compile error waiting in a file they cannot fix, and ci/test.sh
reports a failed compile as a whole-lecture SKIP with no diagnostic: one unwritten header hides
every test in the lecture, including the ones the reader has earned. `ael/utils.hpp` and
`ael/factory/interface.hpp` were included by four suites and specified nowhere in the repository
when this check was written, which is the failure it now refuses to let past.

Second, a header is either always optional or never optional. If any suite guards on it, it is a
separate thing the reader writes and might not have yet, so every suite that includes it must
guard on it too. `ael/types.hpp` is guarded nowhere and needs no guard anywhere: a toolkit with a
`quant/uniform.hpp` and no `types.hpp` is not a state a reader can reach, because the one includes
the other. `ael/utils.hpp` is not like that, and was the bug.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = re.compile(r'__has_include\("([^"]+)"\)')
INCLUDE = re.compile(r'^\s*#\s*include\s+"(ael/[^"]+)"', re.MULTILINE)


def lectures() -> list[Path]:
    """Every lecture directory that has both an appendix and a test suite, in order."""
    found = []
    for directory in sorted((ROOT / "lectures").glob("L[0-9][0-9]")):
        if (directory / "appendix").is_dir() and (
            directory / "exercises/test"
        ).is_dir():
            found.append(directory)
    return found


def required(lecture: Path) -> list[str]:
    """The header paths this lecture's tests guard themselves on, deduplicated and sorted."""
    paths: set[str] = set()
    for source in sorted((lecture / "exercises/test").rglob("*.cpp")):
        paths |= set(GUARD.findall(source.read_text()))
    return sorted(paths)


def optional() -> set[str]:
    """Every header any suite in the course guards on, and so treats as one a reader may lack."""
    paths: set[str] = set()
    for source in sorted(ROOT.glob("lectures/L[0-9][0-9]/exercises/test/**/*.cpp")):
        paths |= set(GUARD.findall(source.read_text()))
    return paths


def includes(lecture: Path) -> list[tuple[Path, str, bool]]:
    """Every (file, header, guarded) for the `ael/...` headers this lecture's tests include."""
    found = []
    for source in sorted((lecture / "exercises/test").rglob("*.cpp")):
        text = source.read_text()
        guarded = set(GUARD.findall(text))
        for header in sorted(set(INCLUDE.findall(text))):
            found.append((source, header, header in guarded))
    return found


def naming(lecture: Path, header: str) -> Path | None:
    """Where `header` is specified: this lecture's appendix for preference, then anywhere else."""
    pages = sorted((lecture / "appendix").glob("*.md"))
    pages += sorted(ROOT.glob("lectures/L[0-9][0-9]/appendix/*.md"))
    pages += sorted((ROOT / "info").glob("*.md"))
    for page in pages:
        if header in page.read_text():
            return page
    return None


def main() -> int:
    listing = "--list" in sys.argv[1:]

    problems: list[str] = []
    checked = 0
    directories = lectures()
    treated_as_optional = optional()

    if not directories:
        # Loudly, because an empty sweep and a clean sweep must not print the same thing.
        print(
            "error: no lecture has both an appendix and a test suite.", file=sys.stderr
        )
        return 1

    for lecture in directories:
        headers = required(lecture)
        if listing and not headers:
            print(f"{lecture.name}  (no guarded tests)")
        for header in headers:
            checked += 1
            page = naming(lecture, header)
            if listing:
                where = page.relative_to(ROOT) if page else "NOWHERE"
                print(f"{lecture.name}  {header:44} {where}")
            elif page is None:
                problems.append(
                    f"{lecture.name}: the tests guard on {header}, which no appendix "
                    f"and nothing in info/ names.\n"
                    f"    Until it is named, a reader following the appendix cannot know "
                    f"which file switches those tests on."
                )

        for source, header, guarded in includes(lecture):
            if guarded:
                continue  # Already checked, as a guard, above.
            checked += 1
            page = naming(lecture, header)
            if listing:
                where = page.relative_to(ROOT) if page else "NOWHERE"
                print(f"{lecture.name}  {header:44} {where}  (unguarded)")
            elif page is None:
                problems.append(
                    f"{source.relative_to(ROOT)} includes {header}, which no appendix "
                    f"and nothing in info/ names.\n"
                    f"    A reader is never told to write it, so the suite cannot compile and "
                    f"ci/test.sh reports that as a whole-lecture SKIP with no diagnostic."
                )
            elif header in treated_as_optional:
                by = ", ".join(
                    sorted(
                        s.name
                        for lecture_ in directories
                        for s, h, g in includes(lecture_)
                        if h == header and g
                    )
                )
                problems.append(
                    f"{source.relative_to(ROOT)} includes {header} without guarding on it, "
                    f"but {by} does guard on it.\n"
                    f"    A header is either always optional or never optional. Add it to "
                    f"this file's __has_include, or drop the guard from the other."
                )

    if listing:
        return 0

    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)

    if problems:
        print(
            f"\n{len(problems)} problem(s) out of {checked} header use(s) checked.",
            file=sys.stderr,
        )
        return 1

    print(f"Buildable: {checked} header use(s) are guarded and named.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
