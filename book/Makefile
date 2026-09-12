# Build the book: LuaLaTeX until the contents and the cross-references stop moving.
#
#   make                   build analog-electronics.pdf, dated today
#   make VERSION=v1.2.3    the same, with the release's version on the title page
#   make clean             remove everything the build writes
#
# Every figure is included straight from the lecture tree, so `make diagrams` at the repository
# root redraws the book's figures along with the lectures' own.

ROOT    := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
BOOK    := $(ROOT)/book
BUILD   := $(BOOK)/build
VERSION ?=
LATEX   := lualatex -interaction=nonstopmode -halt-on-error -file-line-error \
           -output-directory=$(BUILD)
# The book, with its version defined before anything is read; -jobname keeps the output book.pdf.
BOOKTEX := $(LATEX) -jobname=book '\def\bookversion{$(VERSION)}\input{book.tex}'

SOURCES := book.tex aelbook.sty aelbook.lua \
           $(wildcard front/*.tex chapters/*/*.tex back/*.tex back/*/*.tex)
FIGURES := $(wildcard $(ROOT)/lectures/*/appendix/images/*.png)

.PHONY: all clean FORCE

all: analog-electronics.pdf

# The version the last build was made for. The file is rewritten only when VERSION changes, so a
# new version, or none after one, rebuilds the title page and nothing else does.
$(BUILD)/version: FORCE
	@mkdir -p $(BUILD)
	@echo '$(VERSION)' | cmp -s - $@ || echo '$(VERSION)' > $@

analog-electronics.pdf: $(SOURCES) $(FIGURES) $(BUILD)/version
	@mkdir -p $(BUILD)
	cd $(BOOK) && $(BOOKTEX) >/dev/null || (tail -40 $(BUILD)/book.log; exit 1)
	@# Again until the contents and the cross-references stop moving. Two passes settle a small
	@# change and three a new chapter; four has never been needed.
	@for pass in 2 3 4; do \
	    cd $(BOOK) && $(BOOKTEX) >/dev/null || (tail -40 $(BUILD)/book.log; exit 1); \
	    grep -q "Rerun to get cross-references right" $(BUILD)/book.log || break; \
	done
	@grep -E "^(Overfull|Underfull)|Warning" $(BUILD)/book.log | sort | uniq -c | sort -rn | head -20 || true
	@! grep -q "There were undefined references" $(BUILD)/book.log || \
	    (echo "error: undefined references; see $(BUILD)/book.log"; exit 1)
	cp $(BUILD)/book.pdf $@

clean:
	rm -rf $(BUILD) analog-electronics.pdf
