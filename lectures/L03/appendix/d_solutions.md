# Appendix D - Solutions

In full, including the plausible wrong answers.

---

## D.1 Recall: the two rules

1. **No current into the inputs**, which is a property of the amplifier: its input impedance is
   very large, and nothing about the external circuit changes that. **No voltage between the
   inputs**, which is a property of the feedback: the output moves until the difference is
   negligible, and with no feedback path it does not hold for an instant.
2. **A comparator.** With no feedback, the output is at whichever rail the input difference calls
   for, and the difference is whatever the input happens to be. What replaces rule 2 is nothing;
   the amplifier simply does what its gain says.
3. With $A_{OL} = 10^5$ and 10 V out, the input difference is $10/10^5 = 100$ microvolts.
   **The name is good but not perfect.** It is a short to within a hundred microvolts, which is
   negligible next to a signal of volts and is not negligible next to an offset specification of
   fifty microvolts, which is why offset appears on every datasheet.
4. **Rule 2 fails first**, because $A_{OL}$ falls with frequency. A typical amplifier has $10^5$
   at DC and unity gain at a few megahertz, so at 1 MHz there is almost no loop gain left and the
   virtual short is no longer short at all. That is L04's subject.

---

## D.2 Recall: complementary filters

1. **The low-pass lags 45 degrees; the high-pass leads 45 degrees.** They are 90 degrees apart.
2. **Their sum is the input, exactly, at every frequency.** Adding the two transfer functions:

$$\frac{1}{1 + jf/f_c} + \frac{jf/f_c}{1 + jf/f_c} = \frac{1 + jf/f_c}{1 + jf/f_c} = 1$$

3. **Because they are not in phase.** Two quantities of magnitude 0.707 sum to 1 when they are 90
   degrees apart, by Pythagoras. The contradiction only appears if the phases are ignored, and
   ignoring the phase is exactly the habit [L02](../../L02/README.md) spent a section arguing
   against.

---

## D.3 Hand calculation: what the second section does to the first

1. $f_c = 1/(2\pi \times 1000 \times 159\ \text{nF}) = 1001$ Hz.

<!-- value: 1001 = rc_corner(1e3, 159e-9) -->

2. The poles are at $0.382 f_c = 382$ Hz and $2.618 f_c = 2621$ Hz.
3. **Their geometric mean is $f_c$ exactly**, because $0.382 \times 2.618 = 1$. Loading does not
   move the pair as a whole; it pushes one pole down and the other up by the same factor. That is
   worth remembering as a sanity check: if your two poles do not multiply back to $f_c^2$, the
   arithmetic is wrong.
4. The 3 dB point of the pair is **375 Hz**.

<!-- value: 375 = cascaded_corner(1e3, 159e-9) -->

Assuming the sections independent gives $f_c\sqrt{\sqrt{2}-1} = 644$ Hz, so the real answer is
lower by a factor of **1.72**.

---

## D.4 Hand calculation: what is inside a resonance

1. $f_0 = 1592$ Hz, and each reactance is 100 ohm there.

<!-- value: 1592 = lc_resonance(10e-3, 1e-6) -->

2. $Q = 100/10 = 10$, so the bandwidth is $1592/10 = 159$ Hz.
3. At resonance the LC pair cancels, so the current is $5/10 = 0.5$ A. That gives:

| Component | Voltage                              |
| --------- | ------------------------------------ |
| Resistor  | 5 V, the whole input                 |
| Inductor  | 50 V                                 |
| Capacitor | 50 V, in antiphase with the inductor |

4. **The capacitor needs a rating above 50 V**, so a 63 V part. A reader who looked only at the
   transfer function would have seen a 5 V input and a 5 V output, concluded that nothing in the
   circuit exceeds 5 V, and fitted a 10 V part. It would fail, and it would fail only at
   resonance, which is the one condition the filter was built for.
5. With 0.5 ohm instead of 10:

|                             | Changes?                        |
| --------------------------- | ------------------------------- |
| Resonant frequency, 1592 Hz | No. It depends on L and C only. |
| Reactances, 100 ohm         | No, for the same reason.        |
| Q                           | Yes: 200.                       |
| Bandwidth                   | Yes: 7.96 Hz.                   |
| Voltage across L and C      | Yes: 1000 V.                    |

And the current becomes 10 A, which no 10 millihenry inductor of any reasonable size will carry
without saturating. **A high-Q passive filter is limited by what happens inside it long before it
is limited by its transfer function**, and that is the answer this exercise exists for.

---

## D.5 Design: a Schmitt trigger for a noisy signal

**1. 100 kilohm over 1 kilohm**, giving thresholds of $\pm 0.1188$ V and a gap of 0.238 V.

<!-- value: 0.1188 = schmitt_thresholds(12.0, 100e3, 1e3)[1] -->

**2. Why that gap.** The noise is 100 mV peak-to-peak, so a gap of 238 mV is comfortably more than
twice it: once the output switches, the input has to move 238 mV against the noise to switch back,
and noise alone cannot do that. Making it much larger would be wrong for the reason in part 3: the
gap is a delay and an error, and the whole design is to make it larger than the noise and no
larger. A gap of 2 V means thresholds at plus and minus 1 V, so it would work perfectly and
report the crossing 125 ms late.

**3. The delay.** A 1 Hz triangle of 2 V amplitude swings 4 V in half a period, so its slope
through zero is 8 V per second. Reaching the 0.1188 V threshold takes

$$\frac{0.1188}{8} = 14.9\ \text{ms}$$

so the reported crossing is about 15 milliseconds late, and it is late by different amounts in the
two directions if the signal is not symmetric.

**4. Filter against Schmitt trigger.**

* **In favour of the filter:** it does not shift the threshold, so the crossing is reported at the
  right level rather than at one of two wrong ones.
* **Against it:** it delays the signal, and a low-pass slow enough to remove noise near DC delays
  by far more than 15 ms. It also cannot help at all if the noise is inside the signal band, which
  a Schmitt trigger does not care about.

The real answer in most designs is both: filter what you can, then use hysteresis for what is
left.

---

## D.6 Code: the filter responses

Unpublished; the suite is the answer.

One hint for `cascadedCorner`. Bisect on $\log f$ rather than on $f$. The half-power point is
somewhere between a tenth of the single-section corner and the corner itself, which is a decade,
and twenty bisections on the logarithm locate it to one part in a million. Twenty bisections on
the linear axis over the same range do far worse and it is not obvious why until you try it.

---

## D.7 Code: the VCVS and the configurations

Unpublished, with the one hint that matters: **the VCVS constraint row has a zero right-hand
side.** A voltage source's row says $V_p - V_n = V$; a VCVS's says
$V_{op} - V_{on} - A(V_{ip} - V_{in}) = 0$. If you copy the voltage-source stamp and forget to
zero the right-hand side, every amplifier in your netlist acquires an offset equal to its
nominal value, which looks like a plausible bug in the circuit rather than in the stamp.

The comparison against `invertingGain` should agree to about five decimal places with a gain of
$10^5$. The residual is real: it is $1/(1+T)$, the finite-gain error, and predicting it rather
than observing it is L04's first result.

---

## D.8 Cross-check: the cascade, and the buffer that fixes it

| Leg                                      | 3 dB point |
| ---------------------------------------- | ---------- |
| 1. By hand, sections assumed independent | 644 Hz     |
| 2. By `cascadedCorner`                   | 375 Hz     |
| 3. By the solver, cascaded directly      | 375 Hz     |
| 4. By the solver, with a buffer between  | 644 Hz     |

<!-- value: 375 = cascaded_corner(1e3, 159e-9) -->

**Leg 1 is wrong by 1.72, and it is wrong for an interesting reason.** The mathematics is correct:
if two sections each have response $H$, the pair has $H^2$, and $H^2$ is 3 dB down at 644 Hz.
What is wrong is the premise. The second section's input impedance loads the first, so the first
section's response in the actual circuit is not $H$, and squaring $H$ describes a circuit that was
not built.

**Legs 2 and 3 agree** because they describe the same circuit: two poles at 382 Hz and 2621 Hz,
whose geometric mean is still 1001 Hz.

**Leg 4 returns leg 1's answer, and that is the whole point.** A follower between the sections
makes the premise true. Its input impedance is large enough that the second section no longer
loads the first, so each section really does contribute its own unmodified pole, and $H^2$ becomes
the right description.

**Diagnosing a wrong leg 4:**

* **Still 375 Hz** means the VCVS is not between the sections. The usual cause is its input taken
  from the second section's node rather than the first's, which makes it a follower of the output
  and leaves the loading exactly where it was.
* **Near 1001 Hz** means only one section is in the path: the follower's output has replaced the
  second section rather than driving it.
* **Anything wildly large, or a failure to solve**, usually means the VCVS output is shorted to
  its input, which is what happens if the output node and the sensing node are given the same
  index.

**The lesson.** The buffer does not make the filter better. It makes the circuit match the
description, and a description you can trust is worth more than a better circuit you cannot
predict. That is also the reason the operational amplifier appears in this course before the
transistors that make one: its value here is not gain, it is that it decouples a stage from what
is attached to it, and every remaining lecture is about circuits that cannot do that for
themselves.

---
