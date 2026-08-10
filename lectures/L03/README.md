# L03 - Passive filters and the operational amplifier

## Agenda
* High-pass and low-pass RC, and the impedances they present on both sides.
* Cascading, and why two sections in a row do not give you the corner you designed.
* LC filters, resonance, and Q as two things at once: a sharpness and an overshoot.
* The band-pass, and the trade its two corners cannot escape.
* The operational amplifier as a black box, with two rules and nothing else.
* Inverting, non-inverting, buffer, summing and difference, all from those two rules.
* The comparator, hysteresis, and the Schmitt trigger, which are not amplifiers at all.
* Live-coding `ael::filter`, the VCVS element, and `ael::opamp`.

---

## Lecture plan
1. **The two first-order sections.** Swap the two components and a low-pass becomes a high-pass.
   Everything else about them is the same, including the corner.
2. **Cascading.** Two identical sections in a row, and the corner that comes out is not the one
   either section has. This is L01's loading and L02's Cross-check for the third time, and it is
   the reason the next part of the lecture exists.
3. **What a buffer is for.** If the loading is the problem, something with a high input impedance
   and a low output impedance between the sections is the answer. That thing is an op-amp.
4. **LC and resonance.** Two reactances that cancel, Q as the ratio of reactance to resistance,
   and the voltage that appears across the parts inside a high-Q filter.
5. **The op-amp, as two rules.** With feedback and enough gain: no current into the inputs, and no
   voltage between them. Every standard configuration is a divider once those two are applied.
6. **Where the rules stop.** A comparator has no feedback, so neither rule applies, and the
   circuit that results behaves in a way the rules would call impossible.
7. **Live coding.** `ael::filter`, then the VCVS stamp, then the configurations.

---

## Before the lecture
* Finish L02. The VCVS added here stamps like the voltage source of L01, and the filter responses
  are checked against the sweep of L02.
* Read [Appendix A](./appendix/a_filters.md), which is the passive filters.
* Read [Appendix B](./appendix/b_the_operational_amplifier.md) up to
  [B.5](./appendix/b_the_operational_amplifier.md#b5-what-to-build).
* Look again at [L02's Cross-check](../L02/appendix/c_exercises.md#c8-cross-check-the-filter-that-is-not-where-you-put-it).
  This lecture's Cross-check is the same phenomenon in a circuit where you cannot see it coming.

---

## After the lecture
* Write `ael::filter`, add the VCVS to `ael::net::Netlist`, and write `ael::opamp`, to the
  specification in [B.5](./appendix/b_the_operational_amplifier.md#b5-what-to-build).
* Add rows to the report program.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Turn a filter requirement into a corner frequency, and say when one pole cannot meet it.
* Compute what a filter's own input and output impedance are, and why both depend on frequency.
* Say what two directly cascaded RC sections actually give, and by how much it differs from the
  answer that assumes they are independent.
* State Q two ways: as the sharpness of a peak, and as the voltage multiplication inside it.
* Apply the two op-amp rules to any of the standard configurations and get the gain in one line.
* Say precisely which assumption each rule is, and name a circuit where each one fails.
* Compute the two thresholds of a Schmitt trigger, and choose them for a given amount of noise.

---

## Questions to test yourself
* A low-pass and a high-pass built from the same R and C have the same corner. What is different
  about them at that corner, other than which side of it they pass?
* You cascade two identical low-pass sections and measure the corner. Is it higher or lower than
  one section's corner, and by roughly what factor?
* Adding a buffer between two filter sections changes the response. Which direction does the
  corner move, and why is that the direction that makes it predictable?
* A band-pass made of one high-pass and one low-pass never quite reaches 0 dB in its passband.
  What decides how close it gets?
* A filter has Q of 10 and you apply 5 V at resonance. What is the largest voltage anywhere in the
  circuit, and where is it?
* The two op-amp rules assume infinite gain. Which of the two survives when the gain is 1000, and
  which one starts to leak?
* A comparator with no hysteresis and a slowly rising noisy input produces a burst of output
  transitions. How much hysteresis stops it, and what does that hysteresis cost you?

---

## Reference
* [Appendix A](./appendix/a_filters.md): passive filters, cascading, resonance and Q.
* [Appendix B](./appendix/b_the_operational_amplifier.md): the two rules, the configurations, and
  what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L03 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapters 1 and 4, for passive filters and for
  the operational amplifier as a black box.

---

## Next lecture
* L04 asks why the two rules work at all. Feedback, the loop gain, what it buys and what it costs,
  and then the diode, which is the first device in the course that a phasor cannot describe.

---
