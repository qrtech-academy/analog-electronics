# Appendix C - Exercises

Eight, ending with the Cross-check.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: what the loop gain decides

1. Write the closed-loop gain in the form that makes the error visible, and identify the loop gain
   in it.
2. List four quantities that $1 + T$ divides or multiplies, and give the direction of each.
3. Name two things feedback does not improve, and say why not.
4. An amplifier is driven into clipping. What happens to its loop gain, and what does that say
   about the distortion at that moment?

---

## C.2 Recall: the diode

1. How much voltage does a decade of current cost, and where does that number come from?
2. A diode carries 1 mA at 0.65 V. What is its incremental resistance, and what else in this
   course is the same quantity?
3. State the constant-drop model, and say at how many currents it is exact.
4. Between 0.5 microamps and 4 mA a real diode's drop moves by about 240 mV. Give one design in
   which that matters and one in which it does not.

---

## C.3 Hand calculation: how much gain do you need

An amplifier is to have a closed-loop gain of 100, accurate to 0.1 per cent.

1. What loop gain does that need?
2. What open-loop gain?
3. The amplifier available has $A = 10^5$ and a gain-bandwidth product of 1 MHz. Does it meet the
   accuracy at DC? At 1 kHz?
4. At what frequency does the gain error reach 1 per cent?

**Check yourself:** `loopGain`, `gainError`.

---

## C.4 Hand calculation: the diode at two currents

A 5 V supply drives a diode through a series resistor. $I_S = 10^{-14}$ A.

1. For a 1 kilohm resistor, find the diode voltage and current, by hand. Two iterations of guess
   and correct is enough; start from 0.65 V.
2. Repeat for 100 kilohm.
3. Compare both with the constant-drop model's answer, and give the percentage error in the
   current for each.
4. The error in the current is small in both cases and the error in the diode voltage is not.
   Explain why, and say which of the two a bias network in L06 will care about.

**Check yourself:** `current`, `conductance`.

---

## C.5 Design: a half-wave rectifier with a stated ripple

A 12 V peak, 50 Hz sinusoid feeds a half-wave rectifier into a smoothing capacitor and a 1 kilohm
load. The output ripple must not exceed 0.5 V peak-to-peak.

1. Choose the capacitor. State the assumption you are making about the discharge, and say whether
   it makes your answer optimistic or pessimistic.
2. State the DC output voltage, remembering the diode.
3. What peak current does the diode carry, roughly, and why is it so much larger than the load
   current?
4. Doubling the capacitor halves the ripple. What does it do to the peak diode current, and what
   does that suggest about how far this approach scales?

---

## C.6 Code: feedback and the diode model

Implement `ael::feedback` and `ael::device::diode` to the specification in
[Appendix B.5](./b_the_diode_and_newton_raphson.md#b5-what-to-build).

`limit` is four lines and is the only one that is not obvious. Damp only steps that are increasing
and larger than two thermal voltages; leave everything else alone. Damping a decreasing step makes
convergence worse, not better.

---

## C.7 Code: the nonlinear solve

Add `addDiode` to the netlist and write `ael::nr::solve`.

Do this by calling your existing linear solve inside a loop, not by writing a second solver. Each
iteration recomputes the diode stamps from the present guess and re-solves.

Check three things before you believe it:

1. A netlist with no diodes gives the same answer as `ael::mna::solve`, in one iteration.
2. The 5 V through 1 kilohm circuit converges in fewer than ten iterations.
3. Turning the limiting off makes it take about 170. If it does not, the limiting was not doing
   anything.

---

## C.8 Cross-check: the diode, and the model that is nearly right

A 5 V supply, a series resistor, and a diode with $I_S = 10^{-14}$ A. Find the current, three
ways, at two very different operating points.

**Point one: a 1 kilohm resistor.**

1. **By hand, with the constant-drop model.** $(5 - 0.65)/1000$.
2. **By hand, with the exponential.** Iterate from 0.65 V until it stops moving.
3. **By your solver.** `ael::nr::solve`.

**Point two: repeat all three with a 10 megohm resistor.**

Then state, for each point, the percentage disagreement between legs 1 and 3, and separately the
difference in the diode voltage.

### What to expect

**At 1 kilohm, leg 1 is 1.1 per cent high.** At 10 megohm it is **4.2 per cent low**. The sign
reverses, and that is the interesting part: the constant-drop model is exact at exactly one
current, the one where the diode really does sit at 0.65 V, and it errs in opposite directions
either side.

**Legs 2 and 3 should agree to about six significant figures.** Both are solving the same
transcendental equation, one by hand iteration and one by Newton-Raphson.

**The diode voltage disagrees far more than the current does.** 0.697 V against 0.65 V at one
point, 0.458 V against 0.65 V at the other. The model calls a quantity constant that moves by
240 mV across the range.

**Why the current error stays small anyway.** The diode voltage is subtracted from 5 V, so a
240 mV error in it is a 5 per cent error in what remains. The current error is bounded by that
subtraction, and it would not be if the supply were 1 V instead of 5.

**Try that.** Repeat point one with a 1 V supply and a 100 ohm resistor. The constant-drop model
now errs by a much larger fraction, because the diode drop is most of the supply. That is the
condition under which the model should not be used, and it is exactly the condition inside a
transistor's base-emitter loop, which is why L06 computes the drift from the
exponential rather than from a constant.

**If your solver reports 170 iterations**, the limiting is not working. If it reports `converged`
false at 100, the limiting is inverted and it is damping the wrong steps.

---
