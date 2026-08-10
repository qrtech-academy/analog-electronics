# L05 Test Suite

The tests for `ael::device::bjt`, `ael::device::mosfet`, and the BJT as a netlist element.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L05
```

Twenty tests against a toolkit, five without one.

---

## What Is Covered

| Suite             | Covers                                                                                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ReferenceBjt`    | The base-emitter voltage at three currents, sixty millivolts per decade, the 26 ohm at 1 mA, and the emitter exceeding the collector by 2 per cent. Needs no toolkit.    |
| `ReferenceSwitch` | That the forced-beta method never mentions $h_{FE}$.                                                                                                                     |
| `ReferenceMosfet` | The square-root law, and the factor of ten against a BJT at 1 mA.                                                                                                        |
| `Bjt`             | Beta exactly in forward active, the emitter as the sum, a decade per 60 mV, saturation falling out of the same expression, region classification, and the switch design. |
| `Mosfet`          | Cutoff, the square law, the two regions meeting continuously, and the transconductance.                                                                                  |
| `NetlistBjt`      | The element count and its three nodes.                                                                                                                                   |
| `BjtSwitch`       | The Cross-check through the solver: saturation, convergence in single figures, insensitivity to beta from 40 to 300, and collapse below the forced beta.                 |

**`Bjt.SaturationFallsOutOfTheEquation` is the one that matters most.** The transport model handles
all three regions with one expression. A model that branches on region passes the forward-active
tests and fails this one, and the seams would otherwise show up in L06 as small discontinuities
in a bias curve.

**`BjtSwitch.ConvergesQuickly` is the one L04 predicted.** Two junctions rather than one, so the
step limiting has to be applied to both $V_{BE}$ and $V_{BC}$. Limiting only the first leaves the
iteration oscillating rather than merely crawling, and it does not converge at all.

---

## What Is Not Covered

* **Bulk resistance**, and therefore the real saturation voltage. The model gives 57 mV where a
  real device gives 100 to 300 mV. Appendix C.8 is about exactly this, and the suite pins the
  model's number rather than a bench's, deliberately.
* **Speed.** No charge storage, no transit time, no capacitance, so nothing here says how fast a
  transistor switches.
* **Breakdown, second breakdown, safe operating area.** All absent.
* **Channel-length modulation.** A MOSFET's output resistance is infinite in this model. L07
  reintroduces it as $r_o$.

---
