# Appendix A - The pair, the tail, and the two factors of two
The first stage in this course whose purpose is to ignore something.

---

## A.1 Two halves and one current
![A differential pair: two matched NPN transistors with their emitters joined to a tail current source, collector resistors to the positive rail, both bases driven, and the output taken at one collector.](./images/differential_pair.png)

Two matched transistors with their emitters tied together and a **tail** current source below. The
tail fixes the total, $I_{C1} + I_{C2} = I_{tail}$; the inputs decide only how it is **divided**.
Both properties of the circuit follow from that:
* **A differential input redistributes the current** between the halves. The tail node barely
  moves, because the sum is unchanged.
* **A common-mode input moves both halves together,** which the tail cannot supply, so the tail
  node has to move instead.

**Each side runs at half the tail current.** For a 2 mA tail, 1 mA per side:

$$r_e = \frac{V_T}{I_{tail}/2} = 26\ \Omega$$

<!-- value: 26 = diffpair_re(2e-3) -->

**26 ohm, not 13.** Reading $r_e$ from the tail current rather than the side current is the
commonest slip in this lecture, and it is a factor of two on top of the two below.

---

## A.2 Differential gain, and both factors of two
Apply $+v_d/2$ to one base and $-v_d/2$ to the other. The tail node does not move, so each half is
a common-emitter stage with its emitter at signal ground: **exactly L07's circuit**, no new
derivation.

$$A_1 = -\frac{R_C}{r_e} \cdot \frac{v_d/2}{v_d} = -\frac{R_C}{2 r_e}$$

For 10 kilohm and a 2 mA tail, $-192$.

<!-- value: 192 = abs(diffpair_differential_gain(10e3, 2e-3)) -->

* **The first two is the input split.** A differential input of $v_d$ puts only $v_d/2$ on each
  base. Unavoidable: it is what differential means.
* **The second two is the output.** Take the difference between the two collectors and the gain is
  $-R_C/r_e = -385$, the collectors moving oppositely. Take **one** collector and the other half
  is thrown away.

<!-- value: 385 = 2 * abs(diffpair_differential_gain(10e3, 2e-3)) -->

**The second two is recoverable and the first is not.** Recovering it is what the current mirror of
[B.4](./b_rejection_and_the_mirror.md#b4-the-mirror-load-and-its-two-mechanisms) does, and one of
the two reasons that mirror exists. This course takes the **single-ended** output throughout,
because that is what feeds the next stage in an operational amplifier.

---

## A.3 Input and output resistance
**Looking into either base,** L07's result with the same factor of two:

$$Z_{in(diff)} = 2 h_{FE} r_e$$

2.6 kilohm at a 2 mA tail with $\beta = 50$: the two bases in series as far as a differential
source is concerned. Low, and the reason
[B.6](./b_rejection_and_the_mirror.md#b6-offset-matching-and-why-modern-input-stages-are-mosfet)
prefers MOSFETs here.

**Looking into a collector,** L07's `resistanceIntoCollector` with the tail as the degeneration
resistor. With a current-source tail that is enormous, so the output resistance is $R_C$, or the
mirror's $r_o$ when there is a mirror.

**And the base current is not zero,** which matters more here than anywhere else. Each base draws
$I_{tail}/2\beta$, 20 microamps at a 2 mA tail. Those currents flow through whatever drives the
inputs, and **if the two source resistances differ, the difference becomes an input voltage the
amplifier cannot distinguish from signal.**

---

## A.4 What the small-signal model cannot see
Two exponentials dividing one current is a hyperbolic tangent:

$$I_{C1} - I_{C2} = I_{tail}\tanh\!\left(\frac{v_d}{2 V_T}\right)$$

![The difference between the two collector currents against differential input, an S-shaped curve saturating at plus and minus the tail current, with the small-signal tangent drawn through the origin and the region where the two agree to one per cent shaded.](./images/diffpair_transfer.png)

**The pair is linear over nine millivolts.** Beyond $\pm 9.1$ mV the tanh has fallen 1 per cent
below its tangent, and that is the pair's honest input range.

<!-- value: 9.1 = diffpair_linear_range(0.01) * 1e3 -->

**And that figure does not depend on the tail current at all.** The tail scales the whole curve and
cancels out of the ratio. **Biasing the pair harder buys gain and no linearity whatever,** which is
not what anyone expects and is worth checking in the code.

**The pair hard-limits.** At $\pm 100$ mV, 96 per cent of the tail has moved to one side and the
other is off. Past that the output stops responding: a ceiling, not soft compression.

**That ceiling is where slew rate comes from.** The pair drives a compensation capacitor, and once
fully switched the largest current it can deliver is $I_{tail}$, so the output ramps at
$I_{tail}/C$ and no feedback loop can make it faster. Slew rate is not a small-signal parameter,
and this is why.

---

## A.5 What this appendix is blind to
* **Mismatch.** Everything here assumes the two halves are identical. They are not, and
  [B.6](./b_rejection_and_the_mirror.md#b6-offset-matching-and-why-modern-input-stages-are-mosfet)
  is about what that costs.
* **The tail's own behaviour.** Ideal here; the whole of
  [Appendix B](./b_rejection_and_the_mirror.md) is about it not being.
* **Frequency.** The pair has any stage's Miller problem, mitigated by each half seeing only half
  the signal. Not treated.
* **Noise**, where a differential input stage earns much of its reputation, and which this course
  does not cover anywhere.

---
