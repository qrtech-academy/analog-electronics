# L07 Test Suite

The tests for `ael::ssm`, for the Early effect L07 adds to `ael::device::bjt`, and for the
Cross-check that measures a stage's output resistance through the solver.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L07
```

Thirty-six tests against a toolkit, eight without one.

---

## What Is Covered

| Suite                    | Covers                                                                                                                                             |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReferenceEmitterFactor` | That the tempting output-resistance rule is refutable from the shape of the expression, the size of the disagreement, and the cascode. No toolkit. |
| `ReferenceMiller`        | The multiplication, the corner it produces, and that gain times bandwidth is fixed without a cascode. No toolkit.                                  |
| `ReferenceSourceFactor`  | Why the same 220 mV gives $SF = 2$ where it gives $EF = 10$. No toolkit.                                                                           |
| `SmallSignal`            | Every function in `ael/ssm/model.hpp`, including the two structural checks below.                                                                  |
| `Early`                  | That `earlyVoltage` is now read, that the factor is exact, and that a large one recovers the L05 device.                                           |
| `OutputResistance`       | The Cross-check: legs 2, 3 and 4 measured through the solver against the closed form and against the tempting rule.                                |

**Three of these check something structural rather than a number.**

`SmallSignal.CascodeIsResistanceIntoCollector` requires the two to agree **to a microhm on five
megohm**, which they can only do if `cascodeOutputResistance` calls `resistanceIntoCollector`. A
separately derived cascode formula agrees to three or four digits and fails here. The lecture
claims a cascode introduces no new machinery; this is the only way the code can demonstrate that
rather than restate it.

`SmallSignal.OutputResistanceNeverExceedsTheLoad` and
`ReferenceEmitterFactor.OutputResistanceCanNeverExceedTheCollectorResistor` assert the bound that
refutes the tempting rule, over a sweep of thirty-six operating points rather than at one. The
conclusion is arithmetic, not physics: a parallel combination is smaller than either part. Both
tests would still hold if every constant in this course changed.

`Early.ALargeEarlyVoltageRecoversThePerfectCurrentSource` is the regression guard for the four
lectures already written against the old device model.

---

## Two Things That Were Nearly Wrong

**Adding the Early effect broke two pinned L05 assertions, and both assertions were at fault.**
`Bjt.ADecadePerSixtyMillivolts` held the base-collector voltage fixed while moving the
base-emitter voltage by 60 mV, which moves the collector-emitter voltage by 60 mV as a side
effect. That was invisible while the collector current did not depend on the collector voltage.
It now does. The decade is a property of the junction, so the test holds $V_{CE}$ fixed and moves
both terminals together. `Bjt.ForwardActiveGivesBeta` had the same fault and one more: beta itself
now rises a few per cent with $V_{CE}$, so what it asserts is that the ratio is the *same* at three
currents three decades apart. L05's suite was corrected rather than L07's tolerances loosened.

**Where the Early factor goes changes the answer by 18 per cent, and only one placement agrees
with the lecture.** Multiplying the whole transport current, so that the base current scales too
and beta stays flat, is the tempting version because it leaves L05 alone. It also makes the base
feed extra current into the emitter as the collector rises, which is degeneration through $R_E$,
and `OutputResistance.TheBoostIsAtTheCollectorNode` then measures a boost of 10.2 against an
emitter factor of 10, which is above it, where the shunting argument says it must land
below.
`Early.BetaRisesWithTheCollectorVoltage` is what rules that version out, and it was found by the
solver disagreeing with the closed form rather than by reading the code.

**Every comparison in `OutputResistance` is made at the same collector current**, found by
bisecting on the base voltage before each measurement. Comparing a degenerated stage against an
undegenerated one at whatever current each happens to sit at compares two different transistors,
because $r_o$ is $V_A/I_C$. The bisection bracket is deliberately narrow, for the reason given in
the source: a generous bracket asks the solver for a base-emitter voltage of over a volt, which is
hundreds of amps, and a solver that fails there fails silently.

---

## What Is Not Covered

* **Frequency, properly.** One capacitance and one pole. A real device has three capacitances and
  a transit time, and the base-emitter capacitance, which is not multiplied but is far larger, is
  what sets the limit above a few megahertz.
* **The body effect**, which costs a MOSFET follower real gain in L08.
* **Distortion.** Everything here is a straight line through an operating point, so the thing
  degeneration is best at is the thing these tests cannot see.
* **Beta against collector voltage.** Deliberately, and the reason is in
  [B.7](../../appendix/b_the_emitter_factor.md#b7-what-to-build).

---
