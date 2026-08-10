# The Toolkit

`ael` is the analog analysis library you write across the ten lectures. It is not in this
repository and it never will be. This repository ships the specification of each component, the
interface it must present, and a test suite that judges what you wrote.

---

## Where It Lives

Anywhere you like, as long as you tell the suites:

```bash
export AEL_DIR=~/ael
make test
```

The layout every suite assumes:

```text
$AEL_DIR/
├── include/ael/…      Headers. The suites include these by the paths the appendices specify.
└── source/ael/…       Translation units. Discovered, not listed, so a header-only component is fine.
```

A component specified as `ael/ssm/model.hpp` is included by the tests as exactly that, so the
file must be at `$AEL_DIR/include/ael/ssm/model.hpp`. Nothing else about your tree is inspected.

With `AEL_DIR` unset the suites still build and still run. Every test for a class you write sits
behind an `#if __has_include`, so with no toolkit on the include path those tests compile away and
what remains is each lecture's `reference_test.cpp`, which needs no toolkit at all. That is the
correct state on day one, and it is what CI runs.

---

## What Each Lecture Asks For

The header path is part of the specification, not a suggestion: the test suites include these
exact paths, and a component written somewhere else stays dormant however correct it is.

| Lecture | Header                     | What it does                                                               |
| ------- | -------------------------- | -------------------------------------------------------------------------- |
| L01     | `ael/net/netlist.hpp`      | `Netlist`: nodes, resistors, and independent sources.                      |
| L01     | `ael/mna/solver.hpp`       | `solve`: the DC nodal solve, returning node voltages and source currents.  |
| L02     | `ael/ac/sweep.hpp`         | `solveAt` and `sweep`: the same solve over complex admittances.            |
| L03     | `ael/filter/response.hpp`  | Closed-form filter responses, resonance, Q, and the loaded cascade.        |
| L03     | `ael/opamp/ideal.hpp`      | The standard configuration gains and the Schmitt thresholds.               |
| L04     | `ael/feedback/loop.hpp`    | Loop gain, closed-loop gain, and the error one part in one plus it.        |
| L04     | `ael/device/diode.hpp`     | The diode equation, its conductance, and the Newton step limiter.          |
| L04     | `ael/nr/solve.hpp`         | The nonlinear DC operating point: the linear solve, in a loop.             |
| L05     | `ael/device/bjt.hpp`       | The transport model, the three regions, and the switch design.             |
| L05     | `ael/device/mosfet.hpp`    | The square law, its two regions, and the transconductance.                 |
| L06     | `ael/bias/point.hpp`       | The quiescent point including the droop, stiffness, and the drift results. |
| L07     | `ael/ssm/model.hpp`        | The r_e model: gain, the two resistances, the emitter factor, the cascode. |
| L08     | `ael/follower/stage.hpp`   | Follower gain, both resistances, the Darlington, and the loading divider.  |
| L08     | `ael/output/classab.hpp`   | The 26 mV rule, the bias voltage, the idle current, and the drift.         |
| L09     | `ael/diffpair/pair.hpp`    | The pair: both gains, the rejection ratio, the tanh, and the offset.       |
| L10     | `ael/report/amplifier.hpp` | The capstone: the gain budget, the open loop, and the closed loop.         |

Nothing here is ever renamed: L10's suite links everything L01 asked for, so a path that moved
would break eight lectures at once.

**L10 also adds a `Polarity` argument to `addBjt`.** A PNP is your NPN evaluated at the negated
junction voltages with the resulting currents negated, which is one sign and about six lines.

### The two sign conventions, fixed once

Every component in the course reads these, so they are pinned in L01's test suite rather than left
to prose:

* `addCurrentSource(from, to, current)` drives current through itself from `from` to `to`, so it
  **injects at `to`**. One milliamp into a node with one kilohm to ground gives **+1 V**.
* `Solution::sourceCurrents[k]` is the current leaving voltage source `k`'s **positive terminal
  into the circuit**, in the order the sources were added. A 10 V source driving one kilohm
  reports **+10 mA**. That is the opposite sign to the raw MNA unknown, and negating it is your
  job rather than the caller's.

Get either backwards and L01's suite says so on the first run. Get either backwards and keep it,
and every bias calculation in Part 2 comes out inverted.

---

## What the Toolkit Is For

By L10 the components compose into one program: it reads a description of a discrete operational
amplifier, predicts every quiescent point and every stage gain from the closed forms you wrote,
solves the same circuit numerically with the nodal solver you wrote, and prints both next to each
other with the difference.

Start that program in L01 and add to it every lecture. One row per component, saying whether it is
yours or still a stub:

```text
component            state    notes
ael::net             yours
ael::mna             yours
ael::ac              stub     L02
ael::filter          stub     L03
…
```

The point of the row that says `stub` is that it is honest about what your prediction currently
rests on. The capstone in L10 is this program's output with every row reading `yours`.

---

## The Two Legs

From L07 onwards every stage is computed twice, and the course is built on the two disagreeing.

* **The closed form** is what you can reason with. `ael::ssm` implements the appendices' results
  directly: gain from $-R_C/(r_e + R_E)$, output resistance from the emitter factor, and so on.
  It drops terms on purpose, and the appendix says which.
* **The solver** is what is right. `ael::mna` with `ael::nr` takes the same circuit as a netlist
  and answers without knowing what an amplifier is. It tells you nothing about why.

Neither is the reference. A closed form that disagrees with the solver by 2 % is usually correct
and usefully simpler; one that disagrees by a factor of ten is usually a term attached to the wrong
node. The course contains at least one of each, and distinguishing them is the skill.

---

## What a Component Actually Is

**Free functions and plain structs, in the header the appendix names.** Nothing in this course
needs an abstract interface, a factory, or a class hierarchy, and no shipped test constructs one.
Every "What to build" section is a table of functions and, where a result has several parts, an
aggregate with public data members:

```cpp
namespace ael::bias
{
struct Point
{
    double baseVoltage{0.0};
    double emitterVoltage{0.0};
    double collectorVoltage{0.0};
    double collectorCurrent{0.0};
};

[[nodiscard]] Point quiescentPoint(double supply, double upper, double lower, double emitter,
                                   double collector, double beta = 50.0, double vbe = 0.65);
}
```

That is the whole pattern, repeated sixteen times. **If a test does not compile against what you
wrote, the disagreement is a name or a signature**, and the appendix is authoritative.

**The `stub` row in the report program is bookkeeping, not architecture.** Keep the list of what
you have written in the report program itself; there is nothing to switch over, because the
moment a header exists the suite that guards on it wakes up by itself.

---

## Conventions

* **C++17.** Compiled with `-Wall -Wextra -Werror`.
* **Namespaces** mirror the header *directory*, so everything in `ael/ssm/model.hpp` is in
  `ael::ssm` and everything in `ael/follower/stage.hpp` is in `ael::follower`. **Two directories
  hold more than one component and take the file name as a third level**: `ael/device/bjt.hpp` is
  `ael::device::bjt`, and `ael/opamp/ideal.hpp` is `ael::opamp::ideal`. Those two are the whole
  of the exception, and the suites include the paths and call the namespaces exactly as written
  here.
* **Units are SI and unqualified**: volts, amperes, ohms, farads, henries, hertz, seconds. No
  milliamperes in an interface. Where an appendix quotes 26 mV, the code carries 0.026.
* **Doubles everywhere.** Nothing here is fast enough to care, and single precision costs real
  accuracy in the nodal solve.

---
