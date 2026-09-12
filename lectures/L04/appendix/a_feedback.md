# Appendix A - Feedback, and what one number decides
L03 asserted two rules and used them. This appendix derives them, and the derivation hands back an
error term that says how far from true they are.

---

## A.1 The loop, and the one number
An amplifier of gain $A$, a fraction $\beta$ of its output fed back in opposition:

$$A_{CL} = \frac{A}{1 + A\beta}$$

$A\beta$ is the **loop gain**, written $T$: what a signal is multiplied by on one trip around the
loop, and the only quantity in this appendix that matters. When $T$ is large,

$$A_{CL} \approx \frac{1}{\beta}$$

**which depends on the feedback network alone, and that is the entire reason feedback is used.**
$\beta$ is two resistors; $A$ varies by three between devices and drifts with temperature.

**The two rules of L03 are this restated.** Gain set by $\beta$ alone is rule 2, the virtual short.
Rule 1 is the amplifier's own property, not a feedback result at all.

---

## A.2 The error, which is the useful form
$$A_{CL} = \frac{1}{\beta} \cdot \frac{T}{1 + T} = \frac{1}{\beta}\left(1 - \frac{1}{1+T}\right)$$

**The gain falls short of ideal by one part in $1 + T$,** which turns a judgement into arithmetic.

![Gain error against open-loop gain on logarithmic axes, for closed-loop gains of ten, one hundred and one thousand. Each curve falls as one over the loop gain, and reaching 0.01 per cent error needs an open-loop gain of ten thousand times the closed-loop gain.](./images/gain_error.png)

| Loop gain $T$ | Gain error    |
| ------------- | ------------- |
| 10            | 9 per cent    |
| 100           | 1 per cent    |
| $10^3$        | 0.1 per cent  |
| $10^4$        | 0.01 per cent |

An amplifier with $A = 10^5$ at a closed-loop gain of 10 has $\beta = 0.1$, so $T = 10^4$ and the
error is 0.01 per cent.

<!-- value: 0.01 = gain_error(1e5, 0.1) * 100 -->

At a closed-loop gain of 1000 it has $T = 100$ and 1 per cent error, usually unacceptable.
**High closed-loop gain is expensive,** which the closed form does not show.

---

## A.3 What else $1 + T$ divides
* **Distortion is divided by $1 + T$.** The loop sees the amplifier's own nonlinearity as an error
  to correct: 1 per cent open loop becomes 0.01 per cent closed.
* **Output impedance is divided by $1 + T$** for voltage feedback: 100 ohm open loop with
  $T = 10^4$ presents 10 milliohm.
* **Input impedance is multiplied by $1 + T$** for series feedback, which the non-inverting
  configuration uses. Inverting uses shunt feedback, which divides it: hence its bare $R_{in}$.
* **Gain sensitivity is divided by $1 + T$.** A 50 per cent change in $A$ moves $A_{CL}$ by 50 per
  cent divided by $1 + T$.

**What feedback does not fix.** More feedback cannot drive the remainder to zero, because $T$
itself falls with frequency, and nothing here touches input noise, offset or clipping. **A clipped
amplifier has no loop gain at all, so feedback stops working exactly when it would be most
useful.**

---

## A.4 What it costs: gain-bandwidth
Open-loop gain falls as a single pole from a few hertz upwards, at 20 dB per decade, so the
product of gain and frequency is a constant:

$$\text{GBW} = A_{CL} \times f_{-3\ \text{dB}}$$

A 1 MHz gain-bandwidth product gives 100 kHz at a closed-loop gain of 10, and 10 kHz at 100.

**Gain and bandwidth trade one for one,** which is why a high-gain stage is usually two stages of
moderate gain: two stages of 10 have about six and a half times the bandwidth of one stage of 100,
ten per stage less the 0.644 a cascade of coincident poles costs ([A.6](#a6-active-filters)).

$T$ falls with the open-loop gain, so every benefit in [A.3](#a3-what-else-1--t-divides) evaporates
as frequency rises: 0.01 per cent gain error at DC is 1 per cent at a hundredth of the bandwidth.
**Closed-loop distortion rises with frequency even when the amplifier's own does not.**

---

## A.5 Where feedback stops working
Each pole around the loop contributes up to 90 degrees of lag. **At 180 degrees negative feedback
adds instead of subtracting, and if $T$ is still above one there, the circuit oscillates.**

One pole can never reach 180 degrees, so a single-pole amplifier with resistive feedback is
unconditionally stable; two reach it only asymptotically. **Three reach it with gain to spare,**
which is why a three-stage amplifier needs deliberate compensation: L10's Miller capacitor.

Phase margin, compensation strategy and the Nyquist criterion are a course of their own.

---

## A.6 Active filters
An amplifier can do better than isolate two RC sections: it can put feedback around the passive
network and produce a response no passive RC network can.

A **Sallen-Key** low-pass is two resistors, two capacitors and one amplifier as a follower, with
the first capacitor returned to the output rather than to ground. That capacitor sees the output,
feeds energy back into the network, and **the pole pair becomes complex.**

A passive RC cascade makes only real poles, and real poles give a soft corner: two coincident are
6 dB down. A complex pair can be 3 dB down, or peaked, and far sharper.

| Realisation                           | Poles             | 3 dB point of two sections         |
| ------------------------------------- | ----------------- | ---------------------------------- |
| Two RC sections cascaded directly     | Real, split apart | 0.374 of one section's corner      |
| Two RC sections with a buffer between | Real, coincident  | 0.644                              |
| Sallen-Key, Q = 0.707                 | Complex pair      | 1.0, and a much sharper transition |

<!-- value: 0.374 = cascaded_corner(1e3, 159e-9) / rc_corner(1e3, 159e-9) -->

**One part buys a filter the passive components cannot make at any value.** That is a better
argument for an op-amp than gain is, and the argument L08 makes for an emitter follower.

---

## A.7 What this appendix is blind to
* **Stability, properly.** The condition is stated in [A.5](#a5-where-feedback-stops-working) and
  never developed. A design that needs a phase margin computed needs a different course.
* **Feedback topologies.** There are four, by whether voltage or current is sensed and fed back.
  This appendix assumes voltage sensing and describes two.
* **Noise.** Feedback does not reduce noise generated at the amplifier's input, which in most
  low-noise designs decides everything.

---
