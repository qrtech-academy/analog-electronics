#!/usr/bin/env bash
#
# Check the Markdown house rules this course relies on.
#
# One author writing twenty lectures over months drifts, and the drift is invisible until two
# lectures sitting next to each other look like they came from different books. Each rule here
# exists because it is either load-bearing for a reader or impossible to spot by eye:
#
#   1. Alt text. The figures are the material, not decoration; a reader on a slow connection or
#      a screen reader gets nothing from "![](./images/vtc.png)". machine-learning writes empty
#      alt text throughout and digital-design-vhdl writes real alt text by hand. This makes the
#      newer habit a rule.
#   2. Line length. Prose is hard-wrapped at 100 columns so a diff shows which sentence changed
#      rather than which paragraph. Tables, fenced code and unbreakable tokens are exempt.
#   3. Trailing whitespace. Invisible, and two of them are a Markdown line break, so a stray
#      pair silently changes rendering.
#   4. En dashes in headings. GitHub's anchor rules strip them, so "## A.1 - Foo" and
#      "## A.1 – Foo" generate *different* anchors, and ci/links.sh would then reject a link
#      that looks correct. Hyphens everywhere.
#   5. Balanced $$. An odd count means one block was opened and never closed, which renders the
#      rest of the file as mathematics.
#   6. Emoji. The sibling courses have none.
#   7. Dashes used as punctuation. No em dash, no en dash, and neither of the ASCII stand-ins
#      (" -- " and " - ") in running prose. A dash mid-sentence is nearly always a comma, a
#      colon or a full stop that has not been chosen yet, and choosing is the author's job.
#      Hyphens in headings, list markers, table rules and fenced code are untouched: those are
#      syntax rather than punctuation. Inline mathematics and code spans are stripped before the
#      test, because a minus sign in an expression and a hyphen in an identifier are neither of
#      them punctuation either. So are HTML comments, because the "<!-- value: ... -->" tags that
#      ci/numbers.py reads carry arithmetic in them.
#
# Usage:
#   markdown.sh
set -euo pipefail
shopt -s nullglob globstar

# Navigate to the root directory.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

failures=0
checked=0

# Report one violation and count it.
fail() {
    echo "$1" >&2
    failures=$((failures + 1))
}

for file in **/*.md; do
    # Third-party trees are somebody else's house style.
    case "$file" in
        libs/*|.venv/*|build/*) continue ;;
    esac

    checked=$((checked + 1))

    # 1. Every image has non-empty alt text. Matches "![" followed immediately by "]".
    while IFS= read -r line; do
        fail "$file:$line: image has empty alt text"
    done < <(grep -n '!\[\]' "$file" | cut -d: -f1)

    # 2. Lines over 100 columns, outside fenced code and outside tables. A line holding a single
    #    unbreakable token longer than the limit, a URL, a long path, cannot be wrapped and is
    #    exempt; the test is whether any whitespace exists past column 80 that a wrap could have
    #    used.
    #
    #    A line that is nothing but an image is exempt too, and has to be: rule 1 above demands
    #    real alt text, Markdown gives an image no line-continuation syntax, and a sentence of
    #    alt text plus a path is routinely more than 100 characters. Wrapping is there so a diff
    #    shows which sentence changed, and an image line is already one atom.
    #
    #    Display mathematics is exempt for the same reason. A $$...$$ block is one expression,
    #    and breaking it across lines to satisfy a column limit makes the source harder to read
    #    rather than easier, there is no sentence boundary in an equation to break at.
    while IFS= read -r line; do
        fail "$file:$line: line over 100 columns"
    done < <(awk '
        /^[[:space:]]*```/ { fence = !fence; next }
        fence              { next }
        /^[[:space:]]*\|/  { next }                     # table row
        /^!\[.*\]\(.*\)$/  { next }                     # a line that is only an image
        /^<!--.*-->$/      { next }                     # a line that is only an HTML comment
        {
            # Count the $$ delimiters on this line without disturbing it. Two or more means a
            # complete one-line block; exactly one opens or closes a multi-line one.
            copy = $0
            delimiters = gsub(/\$\$/, "&", copy)
        }
        delimiters >= 2 { next }
        delimiters == 1 { math = !math; next }
        math            { next }
        length($0) > 100 {
            tail = substr($0, 81)
            if (tail ~ /[[:space:]]/) print NR
        }' "$file")

    # 3. Trailing whitespace, outside fenced code.
    #
    #    Inside a fence it is content, not formatting. The golden listings quoted from program
    #    output carry whatever column padding printf produced, and rewriting them to satisfy a
    #    whitespace rule would mean the appendix no longer shows what the program prints.
    #    ci/numbers.py reads its values from HTML comments rather than from those listings, so
    #    nothing downstream depends on their whitespace either way.
    while IFS= read -r line; do
        fail "$file:$line: trailing whitespace"
    done < <(awk '
        /^[[:space:]]*```/ { fence = !fence; next }
        !fence && /[[:space:]]$/ { print NR }' "$file")

    # 4. En dash in an ATX heading. Fenced lines are skipped so a comment in a listing does not
    #    read as a heading, the same way ci/links.sh skips them.
    while IFS= read -r line; do
        fail "$file:$line: en dash in heading; use a hyphen (it changes the anchor)"
    done < <(awk '
        /^[[:space:]]*```/ { fence = !fence; next }
        !fence && /^#{1,6} / && /–/ { print NR }' "$file")

    # 5. Balanced $$ display-math delimiters. The "|| true" is load-bearing under pipefail: a
    #    file with no mathematics in it makes grep exit 1, which would otherwise end the run.
    dollars=$({ grep -o '\$\$' "$file" || true; } | wc -l)
    if [ $((dollars % 2)) -ne 0 ]; then
        fail "$file: odd number of \$\$ delimiters ($dollars); a math block is unclosed"
    fi

    # 7. Dashes used as punctuation, in prose only. A leading list marker is stripped before the
    #    test, so "* a - b" is checked but the "* " is not; headings keep their hyphen, which is
    #    the house style for a lecture title; table rows keep theirs, which is the rule; and
    #    fenced code is somebody else's.
    while IFS= read -r line; do
        fail "$file:$line: dash used as punctuation; use a comma, a colon or a full stop"
    done < <(LC_ALL=C.UTF-8 awk '
        /^[[:space:]]*```/ { fence = !fence; next }
        fence              { next }
        /^[[:space:]]*\|/  { next }                     # table row
        /^[[:space:]]*#/   { next }                     # heading
        {
            body = $0
            sub(/^[[:space:]]*([-*+]|[0-9]+\.)[[:space:]]+/, "", body)   # drop a list marker
            gsub(/`[^`]*`/, "", body)                                    # drop code spans
            gsub(/<!--.*-->/, "", body)                                  # drop HTML comments

            # Mathematics is stripped before the test, because a minus sign in an expression is
            # an operator rather than punctuation. Display blocks go first: stripping the inline
            # form first would match the empty string between the two dollars of a "$$" and
            # leave the expression behind, which is how the first version of this rule reported
            # every equation in the course as a dash.
            copy = body
            delimiters = gsub(/\$\$/, "&", copy)
            gsub(/\$\$[^$]*\$\$/, "", body)                              # display math
            gsub(/\$[^$]*\$/, "", body)                                  # inline math
        }
        delimiters == 1 { math = !math; next }
        math            { next }
        body ~ / -- / || body ~ / - / || body ~ /\xe2\x80\x93/ || body ~ /\xe2\x80\x94/ { print NR }
    ' "$file")

    # 6. Emoji. Deliberately narrow: the pictographic planes only, so arrows, checkmarks and the
    #    box-drawing characters the ```text diagrams are made of all stay legal.
    while IFS= read -r line; do
        fail "$file:$line: emoji"
    done < <(grep -nP '[\x{1F000}-\x{1FAFF}\x{FE0F}]' "$file" | cut -d: -f1)
done

if [ "$failures" -gt 0 ]; then
    echo >&2
    echo "error: $failures problem(s) in $checked Markdown file(s)." >&2
    exit 1
fi

echo "Markdown check: $checked file(s) pass."
