# L02 Test Suite

The tests for `ael::ac` and for the two reactive elements L02 adds to `ael::net::Netlist`.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L02
```

Sixteen tests against a toolkit, five without one. **L01's suite must still pass**: this lecture
extends the same `Netlist` rather than replacing it, and `make test` with no `LECTURE` runs both.

---

## What Is Covered

| Suite               | Covers                                                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReferenceResponse` | The corner as an identity, 3 dB and 45 degrees, a decade either side, and the odd symmetry of the phase. Needs no toolkit.                  |
| `ReferenceSettling` | That settling accuracy is bought logarithmically, so fourteen bits costs 1.75 times what eight does rather than 64 times.                   |
| `NetlistReactive`   | Capacitor and inductor counts, and that a reactive element extends the node count like any other.                                           |
| `Ac`                | The low-pass against its closed form at four frequencies, the high-pass, a series resonance, and the Cross-check circuit from Appendix C.8. |
| `Sweep`             | Logarithmic spacing, inclusive endpoints, the single-point case, and refusal of a non-positive frequency.                                   |

**The phase sign is what most of the `Ac` suite is really testing.** A capacitor stamped as an
impedance where its admittance belongs gives the right magnitude everywhere and the wrong sign
everywhere, which no magnitude plot will ever reveal. `Ac.CornerMagnitudeAndPhase` and
`Ac.HighPassLeads` cannot both pass with an inverted convention, which is why both are here.

---

## What Is Not Covered

* **DC.** The stamps break at zero frequency by construction, and `Sweep.RefusesNonPositiveFrequencies`
  pins that as deliberate rather than accidental. L01's real solver is still the one that answers
  a DC question.
* **Transients.** Everything here is steady state. Nothing in this suite would notice a solver
  that got the settling behaviour wrong, because no part of this course computes it.
* **Conditioning.** These networks span four orders of magnitude in admittance. From L04 a diode
  makes that twelve, and the pivoting stops being a formality.

---

## Adding Your Own Tests

Any `*_test.cpp` under this directory is discovered and built. Guard it on the headers it needs,
and it joins the suite.

---
