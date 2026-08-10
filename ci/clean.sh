#!/usr/bin/env bash
#
# Remove every file the builds in this repository generate.
#
# This script is the authority on what this repository generates: anything named here must also
# be matched by .gitignore, and anything .gitignore hides as a build artifact must be removed
# here. When the two disagree, a generated file eventually gets committed.
#
# It does not touch the committed figures under lectures/*/appendix/images/. Those are outputs of
# `make diagrams`, they are meant to be in the repository, and CI checks them by redrawing and
# diffing rather than by deleting them.
set -euo pipefail
shopt -s nullglob globstar

# Navigate to the root directory.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

removed=0

remove() {
    for path in "$@"; do
        [ -e "$path" ] || continue
        rm -rf "$path"
        echo "  removed $path"
        removed=$((removed + 1))
    done
}

# Each test suite's compiled binary and objects.
for makefile in lectures/L*/exercises/test/Makefile; do
    dir="$(dirname "$makefile")"
    remove "$dir/testsuite"
    remove "$dir"/**/*.o
done

# The QAcademy Test framework's static library, when the submodule is checked out.
if [ -f libs/test/Makefile ]; then
    make -C libs/test clean >/dev/null 2>&1 || true
fi

# Python caches left by the diagram pipeline and the check scripts.
remove **/__pycache__

echo
if [ "$removed" -eq 0 ]; then
    echo "Clean: nothing to remove."
else
    echo "Clean: removed $removed item(s)."
fi
