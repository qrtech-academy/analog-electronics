# L01 Test Suite

The tests for `ael::net` and `ael::mna`, the netlist and the DC nodal solver L01 asks you to
write. This directory ships the tests and nothing else: the implementation is yours and lives
outside this repository.

---

## Running It

```bash
export AEL_DIR=~/ael          # wherever you keep your toolkit
make test LECTURE=L01         # from the repository root
```

or from here:

```bash
make AEL_DIR=~/ael
```

With `AEL_DIR` unset the suite still builds and still runs, and reports four passing tests instead
of seventeen. That is the correct state on day one and it is not a failure. It is also what CI
runs, because there is no implementation in this repository for CI to test against.

---

## Why a Test for a Class You Have Not Written Still Compiles

Every test file for a class you write is wrapped in a guard:

```cpp
#if __has_include("ael/net/netlist.hpp")
```

With no toolkit on the include path the header is not found, the file compiles to nothing, and the
tests inside it are never registered. Write the header and they switch themselves on. There is no
list to edit and nothing to enable.

One file is deliberately not guarded. `reference_test.cpp` needs no toolkit at all and pins the
arithmetic the appendix quotes. It is there because `qacademy::test::runAllTests()` returns false
when no tests are registered, and prints nothing while doing it; a suite in which every test was
dormant would report red, silently, before you had written a line.

---

## What Is Covered

| Suite              | Covers                                                                                                                                                   |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReferenceDivider` | The closed forms L01 quotes: the divider, its Thevenin resistance, and what a load does to both. Needs no toolkit.                                       |
| `Netlist`          | Node numbering, ground as node zero, and the element counts.                                                                                             |
| `Mna`              | Ohm's law, both source conventions, the divider loaded and unloaded, series and parallel, superposition, a Thevenin measurement, and a singular network. |

The two sign conventions are pinned here rather than left to the appendix, because every component
in the rest of the course reads them:

* `addCurrentSource(from, to, current)` drives current through itself from `from` to `to`, so it
  **injects** at `to`. One milliamp into a node with one kilohm to ground gives **+1 V**.
* `sourceCurrents[k]` is the current leaving voltage source `k`'s **positive terminal into the
  circuit**, in the order the sources were added. A 10 V source driving one kilohm reports
  **+10 mA**, which is the opposite sign to the raw MNA unknown.

Get either backwards and the suite says so immediately. Get either backwards and *ship it*, and
every bias calculation in Part 2 comes out inverted.

---

## What Is Not Covered

* **Numerical conditioning.** The networks here are small and well behaved. A solver that works on
  them can still fall over on a circuit spanning twelve orders of magnitude in conductance, which
  is what happens the moment L04 adds a diode.
* **Performance.** Nothing here is large enough to care, and nothing later in the course is either.
* **The interface beyond what the solver needs.** How you expose a netlist's contents to the solver
  is yours to decide; the tests only require that `solve` can be handed a `const Netlist&`.

---

## Adding Your Own Tests

Any `*_test.cpp` under this directory is discovered and built; the Makefile finds them rather than
listing them. Put a test for `ael::foo::Bar` in `ael/foo/bar_test.cpp`, guard it on the header it
needs, and it joins the suite.

---
