# L10 Test Suite

The tests for `ael::report`, for the PNP the netlist gains here, and for the two conclusions the
course has been building towards.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L10
```

Eighteen tests against a toolkit, seven without one.

---

## What Is Covered

| Suite             | Covers                                                                                                          |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| `ReferenceGain`   | That a current-source-loaded stage's gain does not depend on its current, and that a cascode is the only lever. |
| `ReferenceBudget` | The 11.5 dB of loading, the 31 dB each no-gain stage is worth, and the 15 microvolts that saturate the output.  |
| `ReferenceLoop`   | The closed loop's insensitivity to beta, and the 0.002 per cent error. No toolkit needed for any of these.      |
| `Report`          | Every function in `ael/report/amplifier.hpp`, including the composition check below.                            |
| `Pnp`             | That a PNP is an NPN with every voltage and every current negated, asserted as an exact mirror.                 |

---

## The Two Structural Checks

`Pnp.IsAnNpnWithEverythingNegated` builds the same stage twice, once each way up, and requires
every node voltage to be the **exact negative** of its counterpart, to a nanovolt. That is the
entire specification of a PNP and it is four lines. A separately written PNP model agrees to a few
digits and fails. `Pnp.TheSourceCurrentsMirror` catches the version that negates the voltages and
forgets the currents, which passes the first test on a symmetric circuit.

`Report.BudgetComposesTheEarlierComponents` requires the budget to agree with
`ael::diffpair::mirrorGain` and `ael::follower::darlingtonGain` across a sweep of twenty-seven
designs, varying tail current, Early voltage and beta.

**And it has a limit worth stating.** A restatement that is *algebraically identical* to the
component it replaces cannot be detected by any test, and the first version of this file tried:
the mutation run showed a hand-written `pairLoad / (V_T/(I/2))` passing all eighteen tests, because
it is the same expression. What the sweep does catch is a restatement that is nearly right, which
is the realistic failure. Two were checked and both are caught: $r_e$ read from the tail current
rather than from one side, and a Darlington's emitter resistance not doubled.

---

## What Is Not Covered

* **The amplifier as one netlist.** The suite measures stages, not the whole circuit, for the
  reason in [B.3](../../appendix/b_the_budget_and_the_loop.md#b3-the-operating-point-that-does-not-exist):
  open-loop it has no operating point, and closed-loop what you measure is 20.
* **Compensation.** No test computes a pole, because nothing in this course models a device
  capacitance.
* **The mirrors as circuits.** The three current sources are ideal in every netlist here.
* **The report's formatting**, beyond checking that every stage name appears in it.

---
