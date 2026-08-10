# Appendix C - Exercises

Eight, ending with the Cross-check. This one has four legs rather than three, because the fourth
is the fix rather than another way of measuring the fault.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: the two rules

1. State the two op-amp rules, and say which one is a property of the amplifier and which is a
   property of the feedback around it.
2. Name a circuit in which the second rule does not hold at all, and say what replaces it.
3. An amplifier has an open-loop gain of $10^5$ and its output sits at 10 V. How much voltage is
   actually between its inputs? Is the virtual short a good name?
4. Which of the two rules is the one that fails first as frequency rises, and why?

---

## C.2 Recall: complementary filters

A low-pass and a high-pass are built from the same resistor and the same capacitor, driven from
the same source.

1. What is the phase of each at the corner?
2. Add the two outputs. What do you get, at the corner and at every other frequency?
3. Each is 3 dB down at the corner, and 3 dB down means 0.707. Two things that are each 0.707 of
   the input sum to the input exactly. Explain, without arithmetic, why that is not a
   contradiction.

---

## C.3 Hand calculation: what the second section does to the first

Two identical RC low-pass sections, each 1 kilohm and 159 nanofarads, connected directly.

1. The corner of one section alone.
2. The two pole frequencies of the pair, from
   [A.3](./a_filters.md#a3-cascading-and-the-corner-you-did-not-design).
3. Their geometric mean. Compare it with part 1 and say what that tells you about what loading
   does.
4. The 3 dB point of the pair, and the factor by which it differs from the answer you would get by
   assuming the two sections are independent.

**Check yourself:** `rcCorner`, `cascadedCorner`.

---

## C.4 Hand calculation: what is inside a resonance

A series RLC: 10 millihenry, 1 microfarad, 10 ohm, driven with 5 V at resonance.

1. The resonant frequency and the reactance of each part at it.
2. The Q, and the bandwidth.
3. The current, and the voltage across each of the three components.
4. You are choosing a capacitor. What voltage rating does it need, and what would a reader who
   looked only at the transfer function have chosen?
5. The 10 ohm resistor is removed and the only resistance left is 0.5 ohm of inductor winding
   resistance. What happens to all five answers above?

**Check yourself:** `lcResonance`, `seriesQ`.

---

## C.5 Design: a Schmitt trigger for a noisy signal

A sensor output crosses zero slowly and carries about 100 mV peak-to-peak of noise. It drives a
comparator on plus and minus 12 V rails, and the comparator's output must make exactly one
transition per crossing.

1. Choose the positive-feedback divider from E12 values. State the two thresholds and the gap.
2. Justify the gap: say why it is larger than the noise and why it is not much larger.
3. The sensor signal is a 1 Hz triangle of 2 V amplitude. By how much does the hysteresis delay
   the reported crossing, in milliseconds?
4. Somebody proposes fixing the noise with a low-pass filter instead. Give one advantage and one
   disadvantage against the Schmitt trigger.

**Check yourself:** `schmittThresholds`, `nearest_e12`.

---

## C.6 Code: the filter responses

Implement `ael::filter` to the specification in
[Appendix B.5](./b_the_operational_amplifier.md#b5-what-to-build).

`cascadedCorner` is the only one that is not a one-liner. Find the two poles, then bisect on a
logarithmic frequency axis for the point where the product of the two first-order magnitudes falls
to $1/\sqrt{2}$. Do not look for a closed form; the exercise is partly to notice that a numerical
answer is fine when the question is "where is this curve equal to that".

---

## C.7 Code: the VCVS and the configurations

Add `addVcvs` to `ael::net::Netlist` and write `ael::opamp::ideal`.

The VCVS stamp is L01's voltage-source stamp with a different constraint row. If your L01 code
wrote that stamp inline rather than as a function, this is the moment it becomes worth extracting.

Then check the two against each other: build an inverting amplifier as a netlist with a VCVS of
gain $10^5$, solve it, and compare with `invertingGain`. They should agree to about five decimal
places, and the discrepancy is the finite gain, which is L04's subject.

---

## C.8 Cross-check: the cascade, and the buffer that fixes it

Two identical RC low-pass sections, 1 kilohm and 159 nanofarads each, connected directly. Find the
frequency at which the pair is 3 dB down.

1. **By hand, assuming the sections are independent.** Square the single-section response and find
   where the result is 3 dB down. Write the number down.
2. **By your closed form.** `cascadedCorner`, which accounts for the loading.
3. **By your solver.** Build the four elements as one netlist and sweep.
4. **Then fix it.** Insert a VCVS of gain 1 between the two sections, as a follower, and sweep
   again.

### What to expect

**Legs 1 and 3 disagree by a factor of 1.72, and leg 1 is wrong.** 644 Hz against 375 Hz. This is
smaller than L02's factor of 6.6 and more insidious, because 644 Hz is a plausible answer arrived
at by a plausible method: multiplying two transfer functions together is exactly what you would do
if nobody had told you the sections interact.

**Legs 2 and 3 should agree to three significant figures**, limited by your sweep density.

**Leg 4 should give 644 Hz**, which is leg 1's answer. That is the point of the fourth leg: leg 1
was not wrong about the mathematics, it was wrong about the circuit, and inserting a buffer makes
the circuit into the one leg 1 was describing.

**If leg 4 still gives 375 Hz**, the VCVS is not isolating the sections. The usual cause is that
its input is taken from the wrong node, so it is measuring the second section rather than the
first.

**If leg 4 gives something near 1001 Hz**, only one section is in the signal path; check that the
follower's output feeds the second section rather than replacing it.

**What to take from it.** A buffer does not improve the filter. It makes the filter behave like the
one you designed, which is a different and more valuable thing. Every op-amp in the rest of this
course is there for that reason rather than for its gain, and in L08 an entire transistor stage
exists for nothing else.

---
