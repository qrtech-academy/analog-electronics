# L04 Test Suite

The tests for `ael::feedback`, `ael::device::diode`, `ael::nr`, and the diode element.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L04
```

Twenty tests against a toolkit, six without one.

---

## What Is Covered

| Suite               | Covers                                                                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ReferenceFeedback` | The error as one part in one plus the loop gain, accuracy costing loop gain decade for decade, and gain-bandwidth as a product. Needs no toolkit.                                                |
| `ReferenceDiode`    | Sixty millivolts per decade, the incremental resistance, and the constant-drop model erring both ways around one current.                                                                        |
| `Feedback`          | Loop gain, closed-loop gain approaching the ideal from below, the error, and that accuracy has a far narrower bandwidth than the amplifier does.                                                 |
| `Diode`             | The equation, the conductance, and that the limiter damps only large increasing steps.                                                                                                           |
| `NetlistDiode`      | The element count.                                                                                                                                                                               |
| `Nr`                | Linear circuits unchanged, two operating points against hand iteration, convergence in single figures, non-convergence reported, and the supply at which the constant-drop model fails outright. |

`Nr` checks the solver against a **fixed-point iteration of the transcendental equation**, not
against a stored answer. The two methods are different, so agreement is evidence.

---

## A Trap in the Test Framework Itself

`EXPECT_NEAR` is implemented as `if (difference > tolerance) throw`. When the difference is NaN
that comparison is **false**, so **a NaN silently passes**. Verified against the framework as
shipped.

That matters here because a limiter that damps decreasing steps takes the logarithm of a negative
number and returns NaN, which `EXPECT_NEAR` alone would report as a pass.

**Wherever a defect could plausibly produce NaN, assert finiteness first:**

```cpp
const double result{ael::device::diode::limit(0.100, 5.000)};
EXPECT_TRUE(std::isfinite(result));
EXPECT_NEAR(result, 0.100, 1.0e-12);
```

`Diode.LimitDampsOnlyLargeIncreasingSteps` does exactly that, and without the finiteness line the
mutation goes undetected.

---

## What Is Not Covered

* **Stability.** Nothing here would notice a feedback arrangement that oscillates.
* **Reverse breakdown, junction capacitance, temperature.** The diode model is the ideal equation
  and nothing else.
* **Convergence in general.** One exponential device converges with the limiting above. A circuit
  with several interacting nonlinearities can still fail, and real simulators carry more
  strategies than this one.

---
