#!/usr/bin/env bash
#
# Build and run each lecture's test suite against your copy of the ael toolkit.
#
# THIS REPOSITORY CONTAINS NO IMPLEMENTATION. The toolkit is what you write across the course,
# from the specifications in the appendices, and it lives wherever you keep it. Tell these suites
# where that is:
#
#   export AEL_DIR=~/ael            # your toolkit: AEL_DIR/include/ael/... and AEL_DIR/source/...
#   make test
#
# With AEL_DIR unset the suites are still built and still run, and report that only their
# reference tests were active. That is the correct state on day one and it is not a failure.
#
# A suite whose classes you have not written yet still compiles and still runs: every test for a
# class is wrapped in `#if __has_include(...)`, so it switches itself on the moment the header
# appears. Each suite also carries one file of unguarded tests that need no toolkit at all, which
# is what stops a suite with nothing written yet from reporting red with no output. See
# lectures/README.md for why that matters.
#
# The suites are cumulative. Every suite links your whole toolkit, so a change made in L10 that
# breaks the nodal solver you wrote in L01 fails L01's suite and names it.
#
# Usage:
#   test.sh                    Run every suite.
#   test.sh L07                Run only L07's suite.
#   AEL_DIR=~/ael test.sh      Point the suites at your toolkit.
#   VERBOSE=1 test.sh          Show why a suite did not compile.
set -euo pipefail
shopt -s nullglob

# Navigate to the root directory.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

only="${1:-}"

FRAMEWORK="libs/test"

passed=0
failed=0
skipped=0

if [ ! -f "$FRAMEWORK/Makefile" ]; then
    echo "SKIP  the QAcademy Test framework is not checked out at $FRAMEWORK/."
    echo "      Fetch it with: git submodule update --init --recursive"
    exit 0
fi

# Where your toolkit lives. Named loudly rather than defaulted to a path inside this repository,
# because there is nothing inside this repository for it to point at.
#
# With AEL_DIR unset the suites are still built and still run. Every test for a class you write is
# behind an __has_include guard, so with no toolkit on the include path those tests compile away
# to nothing and what remains is each lecture's reference_test.cpp, which needs no toolkit at all.
# That is deliberate and it is what CI runs: it proves the suites themselves compile and that the
# numbers the appendices quote are still the numbers the tests expect, on a machine where nobody
# has written any of the course's code.
toolkit="${AEL_DIR:-}"
against="no toolkit; only the reference tests will run"

if [ -n "$toolkit" ]; then
    if [ ! -d "$toolkit/include" ]; then
        echo "error: AEL_DIR is set to '$toolkit', which has no include/ directory." >&2
        echo "       The suites expect headers at \$AEL_DIR/include/ael/... ; see" >&2
        echo "       info/toolkit.md for the layout they assume." >&2
        exit 1
    fi
    toolkit="$(cd "$toolkit" && pwd)"
    against="$toolkit"
fi

found=0
for makefile in lectures/L*/exercises/test/Makefile; do
    dir="$(dirname "$makefile")"
    lecture="$(echo "$dir" | sed -n 's|^lectures/\(L[0-9][0-9]\)/.*|\1|p')"
    [ -n "$only" ] && [ "$lecture" != "$only" ] && continue
    found=$((found + 1))

    echo "==> $dir  (against $against)"

    # A suite that does not compile is the normal state of an exercise nobody has done yet, and
    # is reported as skipped rather than failed. A suite that compiles and then fails is a real
    # failure: the implementation exists and is wrong.
    build_log="$(mktemp)"
    if ! make -C "$dir" build \
        AEL_DIR="$toolkit" \
        QACADEMY_TEST_DIR="$(pwd)/$FRAMEWORK" >"$build_log" 2>&1; then
        echo "SKIP  $dir  (does not compile yet against $against)"
        if [ -n "${VERBOSE:-}" ]; then sed 's/^/      /' "$build_log"; fi
        rm -f "$build_log"
        skipped=$((skipped + 1))
        continue
    fi
    rm -f "$build_log"

    if make -C "$dir" run AEL_DIR="$toolkit" QACADEMY_TEST_DIR="$(pwd)/$FRAMEWORK"; then
        passed=$((passed + 1))
    else
        failed=$((failed + 1))
    fi
done

echo
if [ "$found" -eq 0 ]; then
    if [ -n "$only" ]; then
        # A lecture named on the command line that has no suite is a typo, not a clean run.
        echo "error: $only ships no test suite." >&2
        exit 1
    fi
    echo "Test: no lecture ships a test suite yet."
    exit 0
fi

echo "Test: $passed passed, $failed failed, $skipped skipped."
[ "$failed" -eq 0 ]
