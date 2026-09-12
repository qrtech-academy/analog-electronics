# Appendix A - Circuits, units, and loading
The circuit theory the rest of the course needs. With a background in electronics, read
[A.1](#a1-the-sign-convention-and-why-it-is-worth-five-minutes) for the conventions this course
fixes, then skip to [A.6](#a6-loading-and-why-it-decides-everything-later).

---

## A.1 The sign convention, and why it is worth five minutes
Neither current direction nor voltage polarity is discoverable from a schematic. Fixed once:
* **Current into a terminal is positive.**
* **A voltage is a difference.** $V_{AB}$ is the potential at A minus that at B; a single
  subscript such as $V_C$ is measured against ground.
* **Ground is node zero,** by definition rather than by measurement.

**A bias voltage that comes out negative, or an inverting stage whose gain comes out positive, is
a convention error before it is a physics error.**

---

## A.2 The three quantities, and the one that is usually the answer
| Quantity   | Symbol | Unit   | What it is                                         |
| ---------- | ------ | ------ | -------------------------------------------------- |
| Current    | $I$    | ampere | Charge per second past a point.                    |
| Voltage    | $V$    | volt   | Energy per unit charge between two points.         |
| Resistance | $R$    | ohm    | The ratio of the two, when that ratio is constant. |
| Power      | $P$    | watt   | $VI$, and therefore $I^2R$ or $V^2/R$.             |

Ohm's law, $V = IR$, defines a resistor rather than stating a law of nature. Every device in
Part 2 has a curve instead, and the work is choosing where on it to sit.

**Power decides whether a design survives a bench.** 10 V across 1 kilohm is 100 mW, which a
common surface-mount part will not tolerate, and nothing in the schematic says so.

---

## A.3 Series, parallel, and the divider
Series adds resistance; parallel adds conductance.

$$R_{series} = R_1 + R_2$$

$$\frac{1}{R_{parallel}} = \frac{1}{R_1} + \frac{1}{R_2}, \qquad R_{parallel} = \frac{R_1 R_2}{R_1 + R_2}$$

**The parallel combination is always smaller than either part,** which catches most slips.

The **voltage divider** is the one circuit worth memorising: it is inside the bias network of L06,
the feedback network of L04, and the attenuator in front of every oscilloscope.

$$V_{out} = V_{in} \frac{R_{lower}}{R_{upper} + R_{lower}}$$

![A voltage divider from a 10 V supply, 33 kilohm over 6.8 kilohm, with the output node marked at 1.71 V and two annotations giving the Thevenin resistance of 5.6 kilohm and the loaded output of 1.09 V.](./images/divider.png)

33 kilohm over 6.8 kilohm on a 10 V supply:

$$V_{out} = 10 \times \frac{6800}{33000 + 6800} = 1.71\ \text{V}$$

<!-- value: 1.71 = divider(10.0, 33e3, 6.8e3) -->

**1.71 V, not the 1.65 V it looks like it ought to be.** No E12 pair gives 1.65 V from 10 V here,
and L06 designs a transistor stage around the difference.

---

## A.4 Kirchhoff's two laws
The only physical content in circuit theory. **Current law:** currents into a node sum to zero,
because charge does not accumulate at a junction.

$$\sum_k I_k = 0$$

**Voltage law:** voltages around a closed loop sum to zero, because potential belongs to a point.

$$\sum_k V_k = 0$$

**The current law is the one a program wants:** one equation per node, and a netlist has nodes.

---

## A.5 Thevenin and Norton
Any network of linear elements, seen from two terminals, behaves exactly like a voltage source in
series with a resistance.

* $V_{th}$ is the open-circuit voltage: what appears with nothing attached.
* $R_{th}$ is the resistance looking back in with every independent source killed. A voltage
  source becomes a short, a current source an open circuit.

Killing the divider's supply grounds the top of the upper leg, so the legs are in parallel:

$$R_{th} = R_{upper} \parallel R_{lower} = 5.64\ \text{k}\Omega$$

<!-- value: 5.64 = divider_output_resistance(33e3, 6.8e3) / 1e3 -->

**$R_{th}$ does not depend on which leg is the upper one, and is smaller than either.** Two
megohms give one megohm; two ten-ohm resistors give five ohms.

**Norton** is the same source drawn as a current source in parallel with the same resistance,
$I_{no} = V_{th}/R_{th}$, and is the form [Appendix B](./b_nodal_analysis.md) wants.

---

## A.6 Loading, and why it decides everything later
The divider formula assumes nothing is attached. Attach something, and the lower leg becomes the
lower leg in parallel with it. A 10 kilohm load on the 33k/6.8k divider:

$$V_{out} = 10 \times \frac{6800 \parallel 10000}{33000 + (6800 \parallel 10000)} = 1.09\ \text{V}$$

<!-- value: 1.09 = divider(10.0, 33e3, 6.8e3, 10e3) -->

**A third of the output gone, to a load most people would call light.** $R_{th}$ predicts it:
10 kilohm is not large compared with 5.6 kilohm.

![Divider output against load resistance, falling from 1.71 V unloaded to below 0.2 V at a 100 ohm load, with a marker showing that a load equal to the 5.6 kilohm Thevenin resistance halves the output.](./images/divider_loading.png)

$$V_{delivered} = V_{th} \frac{R_{load}}{R_{th} + R_{load}}$$

A load equal to $R_{th}$ halves the output; ten times larger costs about 9 per cent; ten times
smaller leaves about 9 per cent.

**This is the idea the course is built on.** L03: cascaded filter sections miss the corner you
designed, because the second loads the first. L08: an emitter follower exists only to break a
loading chain. L10: an op-amp loses 11 dB of open-loop gain to it, more than any other term.

---

## A.7 What this appendix is blind to
* **Everything is linear.** From L04 the solver needs Newton-Raphson.
* **Everything is at DC.** No capacitor, no inductor, no frequency. L02 adds them by making this
  same solver complex, not by starting again.
* **Nothing has a tolerance.** Two 5 per cent resistors give a ratio good to about 10 per cent.
  Ignored until L09, where the matching of two transistors decides a stage's whole performance.

---
