# Appendix C - Exercises

Eight, ending with the Cross-check. That one settles which resistance the emitter factor
multiplies, and the answer differs from the obvious one by a factor of ten.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: what linearising discards

1. State $r_e$, and say whether it is a resistor.
2. How large may a base signal be before the straight-line model is misleading? Give a number and
   the reason for it.
3. Name three things a small-signal model cannot describe.
4. A stage is switched off. What happens to $r_e$?

---

## C.2 Recall: the four rules

1. List the four steps that turn a stage into its small-signal schematic.
2. Why does a supply rail become a ground?
3. A bias divider of 33 kilohm over 6.8 kilohm sits on the base of a stage whose base looks like
   13 kilohm. Which dominates the input resistance, and by how much?
4. Bypassing the emitter resistor recovers the gain. What else does it recover, and what does it
   throw away?

---

## C.3 Hand calculation: the three results

A stage at 1 mA with $R_C = 10$ kilohm, $R_E = 234$ ohm, $\beta = 50$.

1. $r_e$, and the emitter factor.
2. The gain, and what it would be with the emitter resistor bypassed.
3. The input resistance looking into the base.
4. The same three at 10 mA with the same resistors. Which of them changed, and which did not?

**Check yourself:** `intrinsicEmitterResistance`, `emitterFactor`, `gain`, `inputResistance`.

---

## C.4 Hand calculation: two nodes, two answers

For the same stage:

1. The resistance looking into the collector, with $R_C$ removed.
2. The stage's output resistance, with $R_C$ in place.
3. The same two with the emitter resistor removed.
4. State, in one sentence each, what degeneration did to each of the two quantities.

**Check yourself:** `resistanceIntoCollector`, `outputResistance`.

---

## C.5 Design: a stage with a stated gain and bandwidth

Design a common-emitter stage: 12 V supply, gain of 40 with the emitter resistor unbypassed, and
an input corner above 3 MHz when driven from 600 ohm. Take $C_{bc} = 4$ pF.

1. Choose a collector current and a collector resistor.
2. Choose the emitter resistor for the gain.
3. Compute the Miller capacitance and the input corner. Does it meet the requirement?
4. If it does not, say what you would change, and give the two options with their costs.

**Check yourself:** `gain`, `millerCapacitance`, `intrinsicEmitterResistance`.

---

## C.6 Code: the small-signal model

Implement `ael::ssm` to the specification in
[Appendix B.7](./b_the_emitter_factor.md#b7-what-to-build).

**`cascodeOutputResistance` must call `resistanceIntoCollector`** with $R_E = r_o$, rather than
implementing a separate formula. The lecture claims a cascode is degeneration by $r_o$; writing it
that way makes the code demonstrate the claim instead of restating it.

---

## C.7 Code: the Early effect

Multiply the forward transport current by $(1 + V_{CE}/V_A)$ in `ael::device::bjt`.

Then check it: solve a stage at two collector voltages a volt apart and confirm the collector
current changes by about one part in a hundred, which is $1/V_A$ per volt. If the current does not
move at all, $r_o$ is infinite and the Cross-check below cannot work.

---

## C.8 Cross-check: what the emitter factor multiplies

A stage at 1 mA with $R_C = 10$ kilohm and $R_E = 234$ ohm, so $EF = 10$. Find its **output
resistance**, four ways.

1. **By the tempting rule.** $R_{out} = R_C \cdot EF$.
2. **By the corrected closed form.** $R_C$ in parallel with the resistance looking into the
   collector.
3. **By your solver.** Perturb the collector node by a small voltage with the input held, and
   divide the voltage change by the current change.
4. **Then replace the collector resistor with a current mirror** and repeat legs 2 and 3.

### What to expect

**Leg 1 gives 100 kilohm. Legs 2 and 3 give about 9.9 kilohm.** A factor of ten, and it is the
largest disagreement in this course.

**Leg 1 cannot be right, and you can see it without computing anything.** The output resistance is
$R_C$ in parallel with something. A parallel combination is smaller than either part. So the
answer cannot exceed 10 kilohm, and 100 kilohm does.

**Compare against the same stage with no emitter resistor: 9.09 kilohm.** So all that degeneration
bought, at the cost of a factor of ten in gain, was **9 per cent** of output resistance. The boost
is real, it is a factor of ten, and it is happening at a node where $R_C$ hides it.

**Leg 4 is where it stops being hidden.** With a current mirror the load is $r_o$, 100 kilohm
rather than 10, and the numbers become 50 kilohm without degeneration and **89.6 kilohm** with it.
The emitter factor is finally visible, because there is no longer a resistor swamping it.

**And that is the point of the correction.** It is not only that leg 1's number is wrong; it is
that getting the node right explains why mirror loads exist at all. Without it, a mirror load is a
technique that appears from nowhere. With it, it is the only way to collect something you have
already paid for.

**If leg 3 gives exactly 10 kilohm**, the Early effect is missing from your device model, so $r_o$
is infinite and the transistor is a perfect current source. Check [C.7](#c7-code-the-early-effect).

**If leg 3 gives 100 kilohm**, the collector resistor is not in the netlist.

**If legs 2 and 3 differ by a few per cent**, that is expected: leg 2's closed form uses
$R_E \parallel r_\pi$ where the solver uses the full nonlinear device, and the two agree to about
the accuracy of $\beta$.

---
