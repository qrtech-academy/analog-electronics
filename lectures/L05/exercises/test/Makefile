# Testsuite target.
TARGET := testsuite

# Root directory of YOUR toolkit. There is no default: this repository ships the specifications
# and the tests, and the implementation is yours. Point this at wherever you keep it:
#
#   make AEL_DIR=~/ael
#
# or export AEL_DIR once and use the repository's own `make test`.
AEL_DIR ?=

# Directory holding the QAcademy Test framework. It is a submodule of this repository, so it is
# already there if you cloned with --recurse-submodules. If you are working somewhere else,
# clone it next to your toolkit and point this at it:
#   git clone https://github.com/qrtech-academy/test-framework.git
QACADEMY_TEST_DIR ?= ../../../../libs/test
QACADEMY_TEST_LIB := $(QACADEMY_TEST_DIR)/libqacademy_test.a

# Any .cpp files your toolkit has. Discovered rather than listed, because how much of your
# toolkit is header-only is your decision and not ours. A toolkit that is entirely headers
# leaves this empty, which is fine.
SOURCE_FILES := $(if $(AEL_DIR),$(shell find $(AEL_DIR)/source -name '*.cpp' 2>/dev/null))

# Test files. Discovered rather than listed, so adding a test file to this directory is enough to
# get it built; see README.md for how a test file for a class you have not written yet stays out
# of the way until you write it.
TEST_FILES := $(shell find . -name '*_test.cpp') testsuite.cpp

# All files.
ALL_FILES := $(SOURCE_FILES) $(TEST_FILES)

# C++ compiler.
CXX_COMPILER := g++

# C++ compiler flags.
CXX_FLAGS := -std=c++17 -Wall -Wextra -Werror \
             $(if $(AEL_DIR),-I$(AEL_DIR)/include) -I$(QACADEMY_TEST_DIR)/include

# Build and run the test suite as default.
default: build run

# Build the QAcademy Test framework.
$(QACADEMY_TEST_LIB):
	@$(MAKE) -C $(QACADEMY_TEST_DIR) lib

# Build the test suite.
build: $(QACADEMY_TEST_LIB)
	@$(CXX_COMPILER) $(ALL_FILES) -o $(TARGET) $(CXX_FLAGS) \
	  -L$(QACADEMY_TEST_DIR) -lqacademy_test

# Run the test suite.
run:
	@./$(TARGET)

# Clean the test suite.
clean:
	@rm -f $(TARGET)

.PHONY: default build run clean
