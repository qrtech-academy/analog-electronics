# L06 Test Suite

The tests for `ael::bias`, and for the temperature dependence L06 adds to `ael::device::bjt`.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L06
```

Eighteen tests against a toolkit, five without one.

---

## What Is Covered

| Suite            | Covers                                                                                                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReferenceDrift` | That the tempting argument contradicts itself by a factor of 47, the 8 per cent per degree at a held base, and that the suppression equals the emitter factor. Needs no toolkit. |
| `ReferenceBias`  | The base current drooping the divider, and the 220 mV rule.                                                                                                                      |
| `Bias`           | The quiescent point including the droop, the three voltages being consistent, stiffness, drift suppression, and the degeneration resistor.                                       |
| `BjtTemperature` | That the temperature coefficient emerges from the model rather than being inserted.                                                                                              |
| `Drift`          | The Cross-check through the solver: the quiescent point, the degenerated drift, the fixed-base drift, and the ratio between them.                                                |

**`BjtTemperature.CoefficientEmergesRatherThanBeingInserted` is the load-bearing one.** It requires
the drift to be near 1.8 mV per degree **and not exactly 2.0**, because a model that returns the
textbook figure to the digit has had the coefficient put in by hand, and then the Cross-check is
checking the model against itself. A companion test requires the coefficient to *change with
current*, which a fixed constant cannot do.

**`Drift.UndegeneratedStageIsNot` compares against a fixed base voltage, not a tiny emitter
resistor.** Shrinking the emitter resistor does not remove the degeneration: the divider's own
Thevenin resistance still carries the base current, so the base still falls as the current rises,
and that is a feedback path of its own. It also saturates the transistor, where drift is
meaningless. This was a real defect in the first version of this suite.

---

## What Is Not Covered

* **Self-heating.** The transistor's own dissipation is not fed back into its temperature. At
  these currents it is negligible; in L08's output stage it is the dominant effect.
* **Beta's temperature coefficient**, and the resistors'. Both are second-order on top of a
  first-order effect.
* **Signal behaviour.** Everything here is the operating point. What the stage does to a signal is
  L07.

---
