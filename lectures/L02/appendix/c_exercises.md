# Appendix C - Exercises

Eight, ending with the Cross-check. The Cross-check is the first in this course where two of the
three legs are expected to disagree, and by a large amount.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: what a phasor assumes

A phasor replaces a sinusoid with one complex number.

1. State the two properties a circuit must have before that substitution is legitimate.
2. Give a circuit from later in this course that has neither, and say what it does to a sinusoid
   that a phasor cannot describe.
3. A phasor analysis of a filter says the output is 0.707 of the input at the corner. A colleague
   switches the circuit on and measures 0.9 of the input. Neither of you is wrong. What is the
   colleague measuring?

---

## C.2 Recall: reading a response

Without computing anything, sketch the magnitude and phase of a first-order low-pass with a corner
at 1 kHz, from 10 Hz to 100 kHz. Mark on it:

1. The two straight-line asymptotes and where they meet.
2. The magnitude and phase at the corner.
3. The magnitude and phase a decade below the corner.
4. The slope far above the corner, in dB per decade and in dB per octave.

Then say which of those six numbers you had to remember and which follow from the others.

---

## C.3 Hand calculation: time constants

An amplifier's output settles towards its final value with a single dominant time constant, and it
reaches 1 per cent of final in 5 microseconds.

1. What is the time constant?
2. How long does it need to reach 0.01 per cent?
3. The specification is tightened from 8 bits to 14 bits of settling accuracy. By what factor does
   the settling time increase?
4. Somebody proposes doubling the bandwidth to fix it. By what factor does that help, and is it
   the cheaper of the two options?

---

## C.4 Hand calculation: reactance and resonance

A 10 millihenry inductor and a 1 microfarad capacitor.

1. At what frequency do their reactances have the same magnitude?
2. What is that reactance, in ohms?
3. In series, what is the total impedance at that frequency, and why?
4. A 10 ohm resistor is put in series with both. What is the Q, and what voltage appears across
   the inductor alone when 1 V is applied at resonance?
5. Which of the answers above would change if the resistor were removed, and which would not?

**Check yourself:** `lc_resonance`, `inductor_reactance`, `series_rlc_q`.

---

## C.5 Design: an anti-aliasing filter that has to be honest

A sensor drives an RC low-pass. The requirement is at least 20 dB of attenuation at 10 kHz, and no
more than 0.5 dB of loss at 100 Hz.

1. Find the corner frequency that meets both, or show that no single-pole filter can.
2. Choose R and C from E12 values, given that the source driving the filter has an output
   resistance of 200 ohm and the load after it is 100 kilohm.
3. State the actual attenuation at 10 kHz and the actual loss at 100 Hz for your choice.
4. Say what you would do differently if the 20 dB requirement became 40 dB.

**Check yourself:** `rc_corner`, `first_order_response`, `nearest_e12`.

---

## C.6 Code: the complex stamps

Extend `ael::net::Netlist` with capacitors and inductors, and write `ael::ac::solveAt` to the
specification in [Appendix B.4](./b_the_ac_solver.md#b4-what-to-build).

Template your L01 elimination on its scalar type rather than writing a second one. If that turns
out to be difficult, the reason is worth finding: it is almost always `std::fabs` in the pivot
search, which does not accept a complex number, where `std::abs` does and returns the magnitude.

Confirm that the L01 suite still passes. It links the same `Netlist`.

---

## C.7 Code: the sweep

Write `ael::ac::sweep` to the same specification: logarithmic, inclusive at both ends, and
well behaved for one point and for `first == last`.

Then use it. Sweep the RC low-pass from [A.5](./a_reactance_and_phasors.md#a5-the-first-order-response)
from 10 Hz to 100 kHz and print magnitude in dB and phase in degrees. Confirm by eye that the
corner is where you expect and that the phase is negative.

---

## C.8 Cross-check: the filter that is not where you put it

A 33 kilohm over 6.8 kilohm divider on a 10 V supply feeds an RC low-pass: 1 kilohm in series,
then 159 nanofarads to ground. The output is taken across the capacitor.

Find the corner frequency, three ways.

1. **By hand, the obvious way.** The filter is 1 kilohm and 159 nanofarads, so
   $f_c = 1/(2\pi R C)$. Write the number down.
2. **By hand, thinking about it.** What resistance does the capacitor actually see looking back?
   Recompute.
3. **By your solver.** Build all four elements as one netlist, sweep it, and find the frequency at
   which the response is 3 dB below its low-frequency value.

Then reconcile all three, and separately state what the low-frequency output voltage is and why it
is not 10 V.

### What to expect

**Legs 1 and 3 disagree by a factor of 6.6, and leg 1 is the wrong one.** This is the first
Cross-check in the course where the hand calculation is not merely less precise but answering a
different question, and the size of the error is the point: this is not a few per cent.

**Legs 2 and 3 should agree to about three significant figures**, limited only by how finely you
sweep. If you sweep 50 points per decade, expect to locate the corner to better than 1 per cent.

**What leg 1 got wrong.** It used the series resistor and ignored the divider. The capacitor does
not care which resistor is which; it sees everything looking back, which is the 1 kilohm in series
with the divider's Thevenin resistance of 5.64 kilohm. The corner is therefore at 151 Hz, not
1001 Hz, and at 1001 Hz the filter is already 16.5 dB down rather than 3 dB down.

**If leg 3 gives 1001 Hz**, the divider is not in your netlist, or its two resistors are stamped
between the wrong nodes so that they are not in the signal path.

**If leg 3 gives a low-frequency output of 10 V**, the divider is shorted out somewhere. It should
give 1.71 V, which is the unloaded divider from L01, because no direct current flows through the
series resistor once the capacitor has charged.

**The general lesson, which is L01's again.** A filter's corner is set by the total resistance the
capacitor sees, and that includes everything upstream. This is the same arithmetic as
[L01 A.6](../../L01/appendix/a_circuits_and_units.md#a6-loading-and-why-it-decides-everything-later)
in a different costume, and it will appear a third time in L03 when two filter sections are
cascaded, and a fourth in L10 where it costs an amplifier 11 dB.

---
