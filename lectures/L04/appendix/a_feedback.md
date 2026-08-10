# Appendix A - Feedback, and what one number decides

L03 asserted two rules and used them. This appendix derives them, and the derivation hands back an
error term that says how far from true they are.

---

## A.1 The loop, and the one number

Take an amplifier of gain $A$, feed a fraction $\beta$ of its output back to its input in
opposition, and the closed-loop gain is

$$A_{CL} = \frac{A}{1 + A\beta}$$

The product $A\beta$ is the **loop gain**, written $T$. It is what a signal is multiplied by on a
complete trip around the loop, and it is the only quantity in this appendix that matters.

When $T$ is large the expression collapses to

$$A_{CL} \approx \frac{1}{\beta}$$

which depends on the feedback network alone. That is the entire reason feedback is used: $\beta$
is two resistors, and two resistors are stable, cheap and accurate, where $A$ is a transistor
parameter that varies by a factor of three between devices and drifts with temperature.

**The two rules of L03 are this result restated.** The gain being set by $\beta$ alone is rule 2,
the virtual short. Rule 1, no input current, is the amplifier's own property and is not a feedback
result at all.

---

## A.2 The error, which is the useful form

Writing the result as its ideal value times a correction is more useful than the closed form:

$$A_{CL} = \frac{1}{\beta} \cdot \frac{T}{1 + T} = \frac{1}{\beta}\left(1 - \frac{1}{1+T}\right)$$

**The gain falls short of ideal by one part in $1 + T$.** That is the single most useful result in
the whole of feedback, because it turns a judgement into arithmetic.

![Gain error against open-loop gain on logarithmic axes, for closed-loop gains of ten, one hundred and one thousand. Each curve falls as one over the loop gain, and reaching 0.01 per cent error needs an open-loop gain of ten thousand times the closed-loop gain.](./images/gain_error.png)

Some values worth having:

| Loop gain $T$ | Gain error    |
| ------------- | ------------- |
| 10            | 9 per cent    |
| 100           | 1 per cent    |
| $10^3$        | 0.1 per cent  |
| $10^4$        | 0.01 per cent |

An amplifier with $A = 10^5$ used at a closed-loop gain of 10 has $\beta = 0.1$, so $T = 10^4$ and
the error is 0.01 per cent.

<!-- value: 0.01 = gain_error(1e5, 0.1) * 100 -->

Used at a closed-loop gain of 1000, the same amplifier has $T = 100$ and the error is 1 per cent,
which is usually unacceptable. **High closed-loop gain is expensive**, and that is not obvious
until the error is written this way.

---

## A.3 What else $1 + T$ divides

The same factor appears everywhere, and this is why learning $T$ is worth more than learning the
individual results.

* **Distortion is divided by $1 + T$.** The amplifier's nonlinearity produces an error at its
  output; the loop feeds that error back, sees it as something to correct, and reduces it by the
  loop gain. This is the reason an audio amplifier with 1 per cent of open-loop distortion can
  deliver 0.01 per cent closed loop.
* **Output impedance is divided by $1 + T$** for voltage feedback. An amplifier with 100 ohm of
  open-loop output impedance and $T = 10^4$ presents 10 milliohm.
* **Input impedance is multiplied by $1 + T$** for series feedback, which is what the
  non-inverting configuration uses. The inverting configuration uses shunt feedback, which divides
  it instead, and that is why the inverting configuration's input impedance is just $R_{in}$.
* **Gain sensitivity is divided by $1 + T$.** A 50 per cent change in $A$ moves $A_{CL}$ by 50
  per cent divided by $1+T$.

**What feedback does not fix.** The distortion that remains after division by $1 + T$ is still
there, and it cannot be driven to zero by more feedback because $T$ itself falls with frequency.
Nor does feedback do anything about noise generated at the input, offset, or an amplifier that has
run out of output swing. A clipped amplifier has no loop gain at all, because its incremental gain
is zero, so feedback stops working exactly when it would be most useful.

---

## A.4 What it costs: gain-bandwidth

An amplifier's open-loop gain falls with frequency, typically as a single pole from a few hertz
upwards. Above that pole the gain falls at 20 dB per decade, so the product of gain and frequency
is a constant:

$$\text{GBW} = A_{CL} \times f_{-3\ \text{dB}}$$

An amplifier with a 1 MHz gain-bandwidth product used at a closed-loop gain of 10 has a bandwidth
of 100 kHz. Used at a gain of 100 it has 10 kHz.

**Gain and bandwidth trade one for one**, and the trade is the reason the product is what appears
on a datasheet. It also explains why a high-gain stage is usually built as two stages of moderate
gain: two stages of 10 each have about six and a half times the bandwidth of one stage of 100.
Ten times per stage, less the 0.644 that a cascade of two coincident poles costs
([A.6](#a6-active-filters)).

The same fact says what the loop gain is doing with frequency. $T$ falls as the open-loop gain
falls, so every benefit in [A.3](#a3-what-else-1--t-divides) evaporates as frequency rises. An
amplifier with 0.01 per cent gain error at DC has 1 per cent at a hundredth of its bandwidth, and
distortion behaves the same way. **Closed-loop distortion rises with frequency even when the
amplifier's own distortion does not.**

---

## A.5 Where feedback stops working

Around the loop, each pole contributes up to 90 degrees of phase lag. Negative feedback subtracts;
180 degrees of additional lag makes it add instead, and if the loop gain is still above one at
that frequency the circuit oscillates.

One pole can never reach 180 degrees, so a single-pole amplifier with resistive feedback is
unconditionally stable. Two poles reach 180 degrees only asymptotically. Three poles reach it with
gain to spare, and that is why a three-stage amplifier needs deliberate compensation, which is
what L10's Miller capacitor is for.

This course states the condition and does not develop it. Phase margin, gain margin, compensation
strategy and the Nyquist criterion are a course of their own.

---

## A.6 Active filters

L03 needed a buffer between two RC sections so they would stop loading each other. An amplifier
can do better than isolate: it can put feedback around the passive network and produce a response
no passive RC network can.

A **Sallen-Key** low-pass is two resistors, two capacitors and one amplifier configured as a
follower, with the first capacitor returned to the output rather than to ground. Because that
capacitor sees the output rather than ground, it feeds energy back into the network, and the pole
pair becomes complex.

That matters because a passive RC cascade can only ever produce real poles, and real poles give a
soft corner. Two real poles at the same frequency are 6 dB down at that frequency; a complex pair
can be 3 dB down, or peaked, and its transition is far sharper.

| Realisation                           | Poles             | 3 dB point of two sections         |
| ------------------------------------- | ----------------- | ---------------------------------- |
| Two RC sections cascaded directly     | Real, split apart | 0.374 of one section's corner      |
| Two RC sections with a buffer between | Real, coincident  | 0.644                              |
| Sallen-Key, Q = 0.707                 | Complex pair      | 1.0, and a much sharper transition |

<!-- value: 0.374 = cascaded_corner(1e3, 159e-9) / rc_corner(1e3, 159e-9) -->

The amplifier costs one part and buys a filter that the passive components cannot make between
them at any value. That is a better argument for an op-amp than gain is, and it is the same
argument L08 makes for an emitter follower.

---

## A.7 What this appendix is blind to

* **Stability, properly.** The condition is stated in [A.5](#a5-where-feedback-stops-working) and
  never developed. A design that needs a phase margin computed needs a different course.
* **Feedback topologies.** There are four, by whether voltage or current is sensed and fed back.
  This appendix quietly assumes voltage sensing and describes only two of them.
* **Noise.** Feedback does not reduce the noise generated at the input of the amplifier, and in
  most low-noise designs that is the term that decides everything.

---
