# L09 Test Suite

The tests for `ael::diffpair`, and for the Cross-check that measures common-mode rejection through
the solver and finds the closed form running out.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L09
```

Twenty-eight tests against a toolkit, nine without one.

---

## What Is Covered

| Suite             | Covers                                                                                                            |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| `ReferencePair`   | Half the tail per side, both factors of two, the cancellation of $R_C$, the 520 V tail, and the tanh. No toolkit. |
| `ReferenceOffset` | That the source imbalance dominates every other offset by two orders of magnitude. No toolkit.                    |
| `DiffPair`        | Every function in `ael/diffpair/pair.hpp`, including the two structural checks below.                             |
| `Rejection`       | The Cross-check: the solver against the closed form, the ideal tail's finite answer, and the lever that reverses. |

**Two of these check something structural rather than a number.**

`DiffPair.RejectionIsTheRatioOfTheTwoGains` asks for the rejection at loads four decades apart and
requires the answers to agree to machine precision. It catches any separately derived formula that
still contains the load. **It does not catch a separate formula that happens to have already
cancelled the load**. `DiffPair.RejectionOfTheWorkedPair` and three others catch that one on the
value instead, and the mutation run confirmed it.

`DiffPair.LinearRangeTakesNoTailCurrent` is enforced by the signature: `linearRange` takes only a
tolerance. The physical claim it protects is that biasing the pair harder does not improve its
linearity, which is the opposite of the pattern L08 established and is the kind of thing a reader
will assume rather than check.

---

## The Cross-check Is the Interesting Part

Four tests in `Rejection` exist because of one result: **the closed form is qualitatively wrong
about a design lever, in a regime a designer can reach.**

`AnIdealTailGivesAFiniteAndMisleadingNumber` requires the common-mode gain of an
ideal-current-source-tailed pair to be **positive and non-zero**, giving about 101 dB, where the
expected answer is zero and infinity. The resistor-tailed pair's common-mode gain is negative, and
the test asserts both signs, because the sign is what says the two are different mechanisms.

`TheIdealTailsResidueIsTheEarlyEffect` and `TheIdealTailsResidueScalesWithBeta` identify the
mechanism rather than just recording it. The Early factor is on the collector current and not the
base current, so $h_{FE}$ rises with $V_{CE}$; an ideal source fixes the **emitter** current, and a
common-mode input moves $V_{CE}$ and so moves the split. Setting $V_A$ to $10^9$ collapses the
effect to the solver's arithmetic floor; setting $\beta$ to 5000 divides it by a hundred.

`MoreTailResistanceIsNotAlwaysBetter` is the conclusion. The two mechanisms have opposite signs, so
they cancel near 3 megohm, and above that the rejection **falls**. The same test asserts that
`commonModeRejection` does the opposite over the same range, so the disagreement is recorded rather
than smoothed over.

**None of this is a defect in either.** The closed form describes one mechanism exactly and is
silent about the other. Two hundred kilohms of tail is well inside where it is right, which is why
it is the formula to design with.

---

## What Is Not Covered

* **Mismatch, in the solver.** Both halves are identical in every netlist here. The
  differential-output rejection of
  [B.5](../../appendix/b_rejection_and_the_mirror.md#b5-the-other-output-and-why-the-answer-changes-completely)
  is checked against the closed form only.
* **The mirror load as a circuit.** `mirrorGain` is tested; the PNP mirror is not built in a
  netlist, because the solver of this course has no PNP.
* **Common-mode input range**, and what happens when the tail source runs out of headroom.
* **Frequency and noise**, as everywhere in this course.

---
