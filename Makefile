SHELL := /bin/bash

# Absolute path to this Makefile's directory, so the targets work from anywhere.
ROOT := $(abspath $(dir $(firstword $(MAKEFILE_LIST))))/

PYTHON := $(ROOT).venv/bin/python

.DEFAULT_GOAL := help
.PHONY: help test numbers lint links schematic buildable sections markdown tables tables-check \
        format format-check diagrams clean

help: ## Show this help.
	@echo "Targets:"
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) \
	  | sed -e 's/:.*## / /' -e 's/^/  /' \
	  | awk '{ printf "  %-18s %s\n", $$1, substr($$0, index($$0, $$2)) }'
	@echo
	@echo "This repository ships specifications and tests, not implementations."
	@echo "Point the suites at the toolkit you are building:"
	@echo "  export AEL_DIR=~/ael && make test"
	@echo
	@echo "Run one lecture's suite instead of all of them:"
	@echo "  make test LECTURE=L07"

test: ## Build and run each lecture's test suite against $AEL_DIR.
	$(ROOT)ci/test.sh $(LECTURE)

# Uses the drawing environment's interpreter when there is one, because models.py imports numpy.
# Falling back to the system python3 is not a mistake: ci/numbers.py skips loudly when it cannot
# import models.py, which is the right answer for a reader who has not created the venv.
numbers: ## Check the numbers quoted in the appendices against diagrams/models.py.
	@if [ -x $(PYTHON) ]; then $(PYTHON) $(ROOT)ci/numbers.py; else $(ROOT)ci/numbers.py; fi

# Mirrors the CI lint job exactly, so a green "make lint" locally means a green lint in CI.
lint: links sections markdown tables-check numbers schematic buildable format-check ## Run every check that needs no compiler.

links: ## Check that every relative Markdown link resolves.
	$(ROOT)ci/links.sh

schematic: ## Check that the capstone schematic is wired the way L10 says it is.
	@if [ -x $(PYTHON) ]; then $(PYTHON) $(ROOT)ci/schematic.py; else $(ROOT)ci/schematic.py; fi

buildable: ## Check that every appendix names the headers its own tests guard on.
	$(ROOT)ci/buildable.py

sections: ## Check that every appendix section cited by prose or a test actually exists.
	$(ROOT)ci/sections.py

markdown: ## Check the Markdown house rules: alt text, wrapping, headings, math fences.
	$(ROOT)ci/markdown.sh

tables: ## Align the columns of every Markdown table, in place.
	$(ROOT)ci/format_markdown.py

tables-check: ## Fail if any Markdown table's columns are not aligned.
	$(ROOT)ci/format_markdown.py --check

format: ## Format the C++ with clang-format and the Python with black, in place.
	$(ROOT)ci/format.sh

format-check: ## Fail if any C++ or Python source is unformatted.
	$(ROOT)ci/format.sh --check

# Deliberately not part of test or lint: the generated PNGs are committed, and redrawing them
# needs a Python environment this repo does not otherwise require. CI has its own job for it,
# which redraws every figure and diffs it. See diagrams/README.md for the one-time venv setup.
diagrams: ## Redraw the generated lecture figures. Optional: FIGURE=<name>
	@test -x $(PYTHON) || { \
	  echo "No Python environment at $(PYTHON). Create it once with:"; \
	  echo "  python3 -m venv .venv"; \
	  echo "  .venv/bin/pip install -r diagrams/requirements.txt"; \
	  exit 1; }
	$(PYTHON) $(ROOT)diagrams/build.py $(FIGURE)

clean: ## Remove every generated file.
	$(ROOT)ci/clean.sh
