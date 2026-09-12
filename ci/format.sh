#!/usr/bin/env bash
#
# Format the C++ with clang-format and the Python with black, or check that they are formatted.
#
# The C++ in this repository is read far more often than it is run: it is the specification of
# what the reader is asked to write, and half of it appears quoted in an appendix. Formatting is
# therefore part of the material, and .clang-format is the same file the other QAcademy courses
# use so that code looks identical across them.
#
# Third-party trees under libs/, the Python virtual environment, and the assembled toolkits
# under build/ are skipped: build/ is a copy of files that were already checked at their source,
# and formatting it would only report the same problem twice.
#
# Usage:
#   format.sh              Format in place.
#   format.sh --check      Report unformatted files and exit non-zero. Changes nothing.
set -euo pipefail
shopt -s nullglob globstar

# Navigate to the root directory.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

check_only=0
if [ "${1:-}" = "--check" ]; then check_only=1; fi

#######################################################################################
# Collect the sources of one kind, skipping the trees that are not ours to format.
# Globals:
#   None
# Arguments:
#   The find(1) -name patterns to match, one per argument.
# Outputs:
#   One path per line, on stdout.
#######################################################################################
sources() {
    local patterns=()
    local first=1
    for pattern in "$@"; do
        if [ "$first" -eq 1 ]; then first=0; else patterns+=(-o); fi
        patterns+=(-name "$pattern")
    done

    find . \
        -name .git   -prune -o \
        -name .venv  -prune -o \
        -path ./libs -prune -o \
        -path ./build -prune -o \
        -type f \( "${patterns[@]}" \) -print | sort
}

mapfile -t cpp_files < <(sources '*.hpp' '*.cpp' '*.h' '*.c')
mapfile -t py_files < <(sources '*.py')

# Prefer the repository's own virtual environment, which is where `make diagrams` already
# needs a Python and where a contributor will have installed black. Falling back to PATH is
# what CI uses, where the dependencies are installed globally into the runner.
BLACK="black"
if [ -x .venv/bin/black ]; then
    BLACK=".venv/bin/black"
fi

status=0

# C++.
if [ "${#cpp_files[@]}" -eq 0 ]; then
    echo "clang-format: no C++ sources yet."
elif ! command -v clang-format >/dev/null 2>&1; then
    echo "error: clang-format not found on PATH. Install it with 'sudo apt install clang-format'." >&2
    exit 1
elif [ "$check_only" -eq 1 ]; then
    if clang-format --dry-run --Werror "${cpp_files[@]}" 2>&1; then
        echo "clang-format: ${#cpp_files[@]} file(s) formatted correctly."
    else
        status=1
    fi
else
    clang-format -i "${cpp_files[@]}"
    echo "clang-format: formatted ${#cpp_files[@]} file(s)."
fi

# Python.
if [ "${#py_files[@]}" -eq 0 ]; then
    echo "black: no Python sources yet."
elif ! command -v "$BLACK" >/dev/null 2>&1; then
    echo "error: black not found on PATH. Install it with 'pip install -r requirements.txt'." >&2
    exit 1
elif [ "$check_only" -eq 1 ]; then
    # black's report of which files it would reformat is the only diagnostic this branch has, so
    # it is captured rather than suppressed and printed when the check fails. --quiet would leave
    # a failure that prints nothing at all; printing it unconditionally would repeat the summary
    # line below in different words. And the success message is gated on black's own result, not
    # on $status, so a clang-format failure earlier cannot make a passing Python check look like
    # it never ran.
    if black_report=$("$BLACK" --check "${py_files[@]}" 2>&1); then
        echo "black: ${#py_files[@]} file(s) formatted correctly."
    else
        echo "$black_report"
        status=1
    fi
else
    "$BLACK" --quiet "${py_files[@]}"
    echo "black: formatted ${#py_files[@]} file(s)."
fi

exit "$status"
