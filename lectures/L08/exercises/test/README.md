# L08 Test Suite

The tests for `ael::follower` and `ael::output`, and for the Cross-check that measures a class-AB
stage's bias through the solver.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L08
```

Thirty-one tests against a toolkit, ten without one.

---

## What Is Covered

| Suite               | Covers                                                                                                               |
| ------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `ReferenceFollower` | The gain being a question about current, the 8 ohm problem and both fixes, and the beta-squared spread. No toolkit.  |
| `ReferenceOutput`   | The 26 mV rule as a scale-free identity, the dead band, the efficiencies, and the constant-drop failure. No toolkit. |
| `Follower`          | Every function in `ael/follower/stage.hpp`, including the two structural checks below.                               |
| `ClassAb`           | Every function in `ael/output/classab.hpp`. `RoundTripsThroughTheBias` is the load-bearing one.                      |
| `IdleCurrent`       | The Cross-check: the bias measured through the solver against both closed forms, and the decade rule.                |

**Four of these check something structural rather than a number.**

`ClassAb.RoundTripsThroughTheBias` requires `idleCurrent` to be a real inverse of `biasVoltage`
across **five decades** of current, to a part in a million. The equation has an exponential term
and a linear term that do not separate, so the only way to satisfy it is to solve rather than to
rearrange. The five decades matter: at 2 mA the emitter resistors drop half a millivolt and an
implementation that ignores them passes everything else in the file. At 1 A they drop 220 mV.

`ClassAb.BiasIsNotTheConstantDropAnswer` requires `biasVoltage` to differ from
$2(0.65 + I_q R_E)$ by more than 200 mV. Without it, a constant-drop implementation would make the
Cross-check compare a model with itself and report perfect agreement.

`ClassAb.TheBiasRisesByADecadeRule` pins the slope at $2 V_T \ln 10$ per decade rather than any
absolute value, so it holds whatever the saturation current is and fails if the factor of two for
the two junctions in series is missing.

`Follower.DarlingtonIsAFollowerDrivingAFollower` asserts the identity rather than the number, and
`Follower.LoadedGainNeverExceedsTheUnloadedGain` asserts the same bound over a sweep that L07's
output-resistance test does: a divider's output is smaller than its input, whatever is on either
side of it.

---

## Two Things Worth Knowing About the Cross-check

**Only one half of the stage is simulated, and that is exact rather than a shortcut.** At idle the
two halves are symmetric, no current flows in the load, and the output node sits at zero. One NPN
with its base held at half the bias and its emitter resistor returned to ground is therefore a
complete model of the idle condition. It also means the suite needs no PNP in the netlist, which
would otherwise have extended L05's device contract for one test.

**Legs 2 and 3 disagree by 0.9 per cent in the bias and 31 per cent in the current, and that is
the lecture happening twice.** The closed form takes $V_T$ as 26 mV where the device computes
$kT/q = 25.87$ mV, and the device has an Early effect the closed form does not. Both push the same
way, giving 14 mV. Fourteen millivolts inside an exponential of scale 26 is a third. The tests are
written to assert the **bias** tightly and the **current** loosely, because that is which of the
two quantities is well conditioned.

---

## What Is Not Covered

* **Anything with a frequency in it.** A follower into a capacitive load can oscillate, which is
  what the base stopper resistors of [Appendix C](../../appendix/c_power_amplifiers.md) are for,
  and nothing here would see it.
* **Self-heating**, so the drift tests measure a drift and not the runaway it becomes.
* **Distortion.** The transfer-curve test checks that the dead band closes, not what is left of
  the curvature once it has.
* **The PNP half**, by the symmetry argument above. A stage with mismatched halves has a quiescent
  output offset, and this suite would not notice.

---
