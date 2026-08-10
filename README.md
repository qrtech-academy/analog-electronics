# Analog Electronics

Repository for the course **Analog Electronics**.

Ten lectures, in two parts, for embedded engineers who read a schematic every week and have never
been shown how one is arrived at. It takes you from Ohm's law to a discrete operational amplifier
you have designed, sized, predicted and solved, transistor by transistor.

**The subject is the transistor amplifier.** Circuit theory, passives and op-amps are built in the
first four lectures because the last six need them, not for their own sake. See
[Prerequisites](./info/README.md#prerequisites) for what that assumes.

---

## About the Course

| Lecture | Part        | Topic                                                           |
| ------- | ----------- | --------------------------------------------------------------- |
| L01     | Foundations | Circuits, units, and the nodal solver                           |
| L02     | Foundations | Reactance, phasors, and frequency response                      |
| L03     | Foundations | Passive filters and the operational amplifier                   |
| L04     | Foundations | Feedback, active filters, and the diode                         |
| L05     | Transistors | The transistor as a device and as a switch                      |
| L06     | Transistors | Biasing, and what an emitter resistor actually buys             |
| L07     | Transistors | Small-signal analysis: r_e, the emitter factor, and the cascode |
| L08     | Transistors | Followers, and the output stage they turn into                  |
| L09     | Transistors | The differential amplifier                                      |
| L10     | Transistors | Building an operational amplifier, and the capstone             |

Each lecture is one hour, of which roughly a third is live coding. Topics include:
* Circuit analysis as something a program does: nodal analysis, conductance stamps, and why a
  solver is easier to write than a set of simultaneous equations is to solve by hand.
* Reactance and the frequency domain, arrived at by making the solver complex rather than by
  deriving the Laplace transform.
* Passive and active filters, their corner frequencies and impedances, loaded and unloaded.
* The operational amplifier as a black box, then as a feedback system, then as a circuit made of
  transistors you have designed yourself.
* Negative feedback: loop gain, desensitisation, what it does to input and output impedance, what
  it does to distortion, and what it costs in bandwidth.
* The bipolar transistor without the semiconductor physics: h_FE, saturation, the exponential, and
  the intrinsic emitter resistance r_e.
* Biasing, thermal stability, and the emitter factor: a single number that says what a degeneration
  resistor costs in gain and buys in stability.
* Gain, input resistance and output resistance for every stage, derived the same way each time.
* The current mirror as a load, the Miller effect, and the cascode.
* The differential pair, common-mode rejection, and the matching that decides it.

Every result is a formula you can write down and a function you can run. The course refuses to
quote a number it has not given you the means to compute.

---

## There Is No Instrument Here, and That Is the Design

A course like this one usually comes with a breadboard, a bench supply, an oscilloscope and
LTspice. This one does not. There is nothing to install but a C++ compiler, `make` and `git`.

What replaces it is that **you write the instrument**. Across the ten lectures you build `ael`, an
analog analysis library in C++: a netlist, a nodal solver, complex stamps for reactance, a
Newton-Raphson loop, device models for the diode, the BJT and the MOSFET, and on top of them the
closed-form results for every amplifier stage in the course. By L10 they compose into one program
that takes a discrete operational amplifier, predicts every node in it, and then solves it.

**None of that code is in this repository.** Every component is specified in prose, with its
interface declaration, in the appendix of the lecture that asks for it, and every one ships with a
test suite that judges what you wrote. Most of it is written live, in the lecture; the rest is what
you finish afterwards. See [info/toolkit.md](./info/toolkit.md) for the shape it takes and where to
keep it.

That trade cuts both ways:
* **What you lose.** No breadboard, no oscilloscope, no real device spread, no parasitics, no
  thermal behaviour you can feel with a fingertip, and no experience driving an instrument. Where a
  number here differs from what a real measurement would give, the appendix says so and says by how
  much.
* **What you gain.** Every step is a function you wrote and can read. "The simulator says the gain
  is -84" stops being an oracle. You know which term that came from, what it assumed, and what
  would have to change to move it.

Verification works in three layers, and none of them is a bench:
* **The Cross-check.** Every lecture ends with one exercise where you compute a number by hand,
  then run your own closed-form code on it, then solve the same circuit numerically with your own
  nodal solver. Three legs, and they are not equally authoritative: the hand calculation drops
  terms on purpose, the closed form drops fewer, and the solver drops none but tells you nothing
  about why. When two of them disagree by 8 %, finding out which one is wrong, or that neither is,
  is the exercise, and each one ends by saying how large a discrepancy to expect.
* **The shipped test suites.** Every component you implement comes with a unit-test suite written
  against the [QAcademy Test](https://github.com/qrtech-academy/test-framework) framework. They
  tell you *whether* you are right without telling you *why*, which is the middle ground self-study
  otherwise lacks.
* **The two models against each other.** From L07 on, every stage is computed twice: once from the
  closed form, once by the solver from the same netlist. The closed form is the one you can reason
  with and the solver is the one that is right. Where they part company, the appendix names the
  term responsible.

---

## Structure

```text
Makefile     Entry point for the checks below; run `make help` for the target list.
ci/          Check scripts: test suites, Markdown rules, quoted numbers, formatting.
info/        Prerequisites, the course plan, per-lecture topics, and the toolkit spec.
lectures/    Per lecture: README, appendix/, exercises/.
diagrams/    Python sources for the generated figures, and the models they are computed from.
exam/        Two four-hour papers and their worked solutions. Optional, marked by nobody here,
             and only for checking your own knowledge once the course is over.
libs/test/   The QAcademy Test framework, as a submodule.
```

---

## Building

Clone the repo and initialize the test framework submodule:

```bash
git clone <url>
git submodule update --init --recursive
```

```bash
make help                 # List every target.
make test                 # Build and run each lecture's test suite against your toolkit.
make numbers              # Check the numbers the appendices quote against diagrams/models.py.
make buildable            # Check each appendix names the headers its own tests guard on.
make lint                 # Links, appendix sections, Markdown rules, quoted numbers, the
                          # capstone schematic, header names, and formatting.
make clean                # Remove every generated file.
```

`make test` needs to know where your toolkit is:

```bash
export AEL_DIR=~/ael
make test
```

With `AEL_DIR` unset it still runs, and reports that only each lecture's reference tests were
active. That is the correct state on day one.

A C++17 compiler, `make` and `git` need to be installed and on PATH. On WSL/Ubuntu:

```bash
sudo apt -y update
sudo apt -y install git make g++
g++ --version             # 9 or newer; CI builds with the g++ on ubuntu-24.04.
```

Anything not yet implemented is **skipped, loudly**, rather than failing: a test for a class you
have not written is dormant behind an `#if __has_include`. That is what makes `make test`
meaningful on day one and on the last day.

---

## Code Formatting

`make format` formats the C++ with `clang-format` and the Python with `black`:

```bash
make format               # Format all files.
make format-check         # Check formatting without modifying files.
```

`clang-format` is installed via `apt`:

```bash
sudo apt -y update
sudo apt -y install clang-format
```

`black` is installed via `requirements.txt`:

```bash
pip install -r requirements.txt
```

---
