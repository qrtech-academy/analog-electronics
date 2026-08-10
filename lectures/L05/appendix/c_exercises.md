# Appendix C - Exercises

Eight, ending with the Cross-check. This one is the first in the course where both computational
legs agree with each other and both are wrong about a real device, and saying so is the exercise.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: the device in three facts

1. State the collector current as a function of base-emitter voltage, and name the other component
   in this course that obeys the same equation.
2. What does 60 mV of extra base-emitter voltage do to the collector current?
3. What is the incremental resistance of the base-emitter junction at 1 mA, and what will that
   quantity be called from L07?
4. Give the emitter current in terms of the collector current for $\beta = 50$, and say what
   error is made by treating them as equal.

---

## C.2 Recall: the three regions

1. Name the three regions used, in terms of which junction is forward biased.
2. Which region does an amplifier live in, and which two does a switch use?
3. A MOSFET's *saturation* region and a BJT's *saturation* region are opposite conditions.
   Describe each, and say which BJT region corresponds to a MOSFET's saturation.
4. In the active region a transistor is a current source; in saturation it is a resistor. Which
   fact does a load line rely on, and which does a switch rely on?

---

## C.3 Hand calculation: bias points from voltages

A transistor has $I_S = 10^{-14}$ A, $\beta_F = 50$.

1. What base-emitter voltage gives 1 mA of collector current?
2. What gives 10 mA? What gives 10 microamps?
3. For each of the three, what is the base current, and the emitter current?
4. Sketch the relationship between $V_{BE}$ and $\log I_C$. What is its slope, in volts per decade?

**Check yourself:** `currents`.

---

## C.4 Hand calculation: is it saturated

For each of these, classify the region and justify it in one sentence.

|     | $V_B$ | $V_C$ | $V_E$ |
| --- | ----- | ----- | ----- |
| a   | 0.0 V | 5.0 V | 0.0 V |
| b   | 0.7 V | 3.0 V | 0.0 V |
| c   | 0.8 V | 0.1 V | 0.0 V |
| d   | 2.7 V | 5.0 V | 2.0 V |
| e   | 0.7 V | 0.0 V | 0.0 V |

**Check yourself:** `region`.

---

## C.5 Design: a relay driver

A microcontroller pin at 3.3 V must switch a relay coil drawing 150 mA from a 12 V supply.

1. Choose a forced beta and justify it.
2. Compute the base resistor, and choose an E12 value.
3. State the base current your choice actually delivers, and the resulting forced beta.
4. The transistor's $h_{FE}$ is specified as 100 minimum. Does your design depend on that number?
   Say what would have to be true for it to stop working.
5. The relay coil is inductive. State what that does when the transistor turns off, and what one
   component fixes it. You are not asked to size it.

**Check yourself:** `baseResistor`, `nearest_e12`.

---

## C.6 Code: the two device models

Implement `ael::device::bjt` and `ael::device::mosfet` to the specification in
[Appendix B.4](./b_the_mosfet_and_what_to_build.md#b4-what-to-build).

The BJT model has no branch on region: write the transport expressions and let saturation happen.
If your code tests which region it is in before deciding what to compute, you have written three
models rather than one, and the seams will show as discontinuities in L06.

The MOSFET does need its three cases, because the square law genuinely is piecewise.

---

## C.7 Code: the transistor in the netlist

Add `addBjt` and stamp it in `ael::nr::solve`.

A BJT contributes nine matrix entries: two junction conductances and one controlled source. Take
the derivatives of the two transport expressions with respect to both junction voltages, and stamp
them as a two-port conductance matrix plus two equivalent current sources.

**Apply the step limiting to both junction voltages.** L04's circuit had one junction and would
converge without it in 170 iterations; this one has two, and without limiting it does not converge
at all. That is the failure L04 predicted.

Confirm it converges in under twenty iterations on the switch of [A.4](./a_the_bipolar_transistor.md#a4-designing-a-switch).

---

## C.8 Cross-check: the switch, and the model that agrees with itself

The switch of [A.4](./a_the_bipolar_transistor.md#a4-designing-a-switch): 5 V logic through 470
ohm into the base, 50 ohm from the collector to a 5 V rail, emitter grounded. Find the collector
current.

1. **By hand, with the saturation-voltage model.** Assume the transistor saturates at 0.2 V and
   the collector current is whatever the load resistor allows.
2. **By hand, with the transport model.** Solve the two junction equations for $V_{BE}$ and
   $V_{CE}$.
3. **By your solver.** `ael::nr::solve` on the four-element netlist.

Then answer the question the three numbers raise: **which of them would a bench agree with?**

### What to expect

**Legs 2 and 3 agree to five or six significant figures**, at 98.9 mA and a collector-emitter
voltage of 57 mV. They are the same model solved two ways.

**Leg 1 gives 96.0 mA**, about 3 per cent lower, because it assumed 0.2 V across the transistor
rather than 57 mV.

**And leg 1 is the one closer to a real device.** A small-signal transistor at 100 mA saturates
somewhere near 0.2 V, not near 0.06 V. The transport model has no bulk resistance in it: no
resistance in the collector material, none in the emitter, none in the bond wires. Those are what
produce most of a real saturation voltage at 100 mA, and the model omits all of them.

**This is the first Cross-check where agreement between the legs is not evidence of being right.**
Legs 2 and 3 agree because they are the same physics evaluated twice. What they agree on is
optimistic by a factor of three in the saturation voltage, and a design that budgeted its heat
from 57 mV would run three times hotter than predicted.

**What to do about it.** Nothing, in this course, except know it. The correction is a series
resistance in the model, of a few tenths of an ohm, and it is the first thing a real simulator's
transistor model has that this one does not. What matters is the habit: **two legs agreeing tells
you your arithmetic is right, and says nothing whatever about whether your model contains the
physics that decides the answer.**

**Sensitivity, which is the design's real claim.** Repeat leg 3 with $\beta_F$ set to 300 and then
to 40. The collector current changes by less than a fifth of a per cent, because the design never
used beta. Now set it to 8, below the forced beta of 11, and the transistor leaves saturation: the
current falls to 72 mA and the collector sits at 1.4 V. **That is the boundary the forced-beta
method buys margin against**, and it is three decades away from any real device.

---
