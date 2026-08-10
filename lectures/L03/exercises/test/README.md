# L03 Test Suite

The tests for `ael::filter`, `ael::opamp::ideal`, and the VCVS that L03 adds to
`ael::net::Netlist`.

---

## Running It

```bash
export AEL_DIR=~/ael
make test LECTURE=L03
```

Nineteen tests against a toolkit, five without one. L01's and L02's suites must still pass.

---

## What Is Covered

| Suite                | Covers                                                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReferenceFilter`    | Complementary outputs summing to unity, the 90 degrees between them, the cascade poles multiplying back to the corner squared, and the buffered answer. Needs no toolkit. |
| `ReferenceResonance` | That Q is a voltage multiplier inside the filter and not only the sharpness of its peak.                                                                                  |
| `Filter`             | Corner, both first-order responses and their phase signs, resonance, Q, the band-pass, and the loaded cascade.                                                            |
| `OpampIdeal`         | The three configuration gains and the Schmitt thresholds.                                                                                                                 |
| `NetlistVcvs`        | The VCVS element count and its four nodes.                                                                                                                                |
| `Cascade`            | The Cross-check through the solver: sections that load each other, a buffer that stops them, and an inverting amplifier against its exact finite-gain result.             |

**`Cascade.ABufferRestoresIndependence` is the one worth reading.** It asserts that inserting a
unity-gain VCVS between the two sections moves the 3 dB point from 0.374 of a section's corner to
0.644, which is what squaring one section's response predicts. A buffer does not improve the
filter; it makes the circuit match the description.

**`Cascade.InvertingAmplifierMatchesTheIdealGain` asserts the finite-gain formula exactly**, rather
than tolerating the shortfall. With an open-loop gain of $10^5$ a nominal gain of ten comes out at
9.9989, and the test requires that number rather than a tolerance wide enough to hide it. The
shortfall is one part in the loop gain, which is L04's first result.

---

## What Is Not Covered

* **Anything real about an op-amp** except its finite gain: no offset, no bias current, no slew
  rate, no bandwidth. L04 adds the bandwidth.
* **Component tolerance.** Every corner here is nominal. A filter from 5 per cent parts has a
  corner good to about 7 per cent, and a high-Q filter is far worse.
* **Stability.** Nothing here would notice a feedback arrangement that oscillates.

---
