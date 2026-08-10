# Appendix C - Exercises

Eight, ending with the capstone. That one is the whole course in one program: predict every stage,
solve every stage, and reconcile the two, row by row.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: what each stage is for

1. Name the four stages and say what each is responsible for.
2. Two of them have no voltage gain. Which, and what are they for?
3. Which stage decides the amplifier's input offset, and can a later stage improve it?
4. Which node carries the compensation, and why that one?

---

## C.2 Recall: the loop

1. Write the closed-loop gain in terms of the open-loop gain and the feedback fraction.
2. What is the loop gain of this amplifier at a closed-loop gain of 20?
3. Feedback divides the output resistance by one plus the loop gain. Compute it, then say why the
   answer is not a real number.
4. The open-loop gain varies by a factor of 14 across a beta spread. By how much does the
   closed-loop gain vary, and why is that the answer feedback exists to give?

---

## C.3 Hand calculation: the budget

The amplifier of [Appendix A](./a_the_amplifier.md): 2 mA tail, 1 mA buffer, 1 mA voltage stage,
120 mA idle, 8 ohm load, $\beta = 50$.

1. The unloaded gain of stages 1 and 3.
2. The input resistance of stages 2, 3 and 4.
3. Each stage loaded by the next, and the open-loop gain.
4. The difference in decibels between the product of the unloaded gains and your answer to part 3.
   Where is most of it?

**Check yourself:** `budget`, `openLoopGain`.

---

## C.4 Hand calculation: the stages that do nothing

1. What would stage 1's gain be if it drove stage 3 directly? Give the open-loop gain that
   results.
2. What would stage 3's gain be if the output stage were a single follower rather than a
   Darlington? Give the open-loop gain that results.
3. State what each of the two no-gain stages is worth, in decibels.
4. Both stages cost signal. State what each costs, and comment on the exchange rate.

---

## C.5 Design: the input offset that matters

1. What input offset voltage puts the open-loop output at a rail?
2. Two ordinary transistors match their $V_{BE}$ to about 1 mV. How many times larger is that than
   your answer to part 1?
3. State what this means for solving the amplifier open-loop.
4. The closed-loop amplifier has an output offset. Compute it for 1 mV of input offset at a
   closed-loop gain of 20, and say what would reduce it.

---

## C.6 Design: the gain you cannot buy

1. Compute stage 1's gain at a tail current of 0.2 mA, 2 mA and 20 mA, with a mirror load in each
   case. Then do the same for stage 3 at 0.1 mA, 1 mA and 10 mA with a current-source load.
2. Explain the result. Write the gain symbolically and show what cancels.
3. So how *do* you get more gain out of one stage? Compute what your answer gives at 1 mA.
4. The compensation capacitor is 30 pF. Compute the amplifier's slew rate at the 2 mA tail, then
   the tail current that would give 10 V per microsecond, and say what that change costs in gain.

**Check yourself:** `mirrorGain`, `intrinsicEmitterResistance`, `cascodeOutputResistance`.

---

## C.7 Code: PNP support, and the report

Add `Polarity` to `addBjt` and stamp a PNP as an NPN with every voltage and current negated. Then
implement `ael::report` to the specification in
[Appendix B.6](./b_the_budget_and_the_loop.md#b6-what-to-build).

**`budget` must compose the functions from L07 to L09, not restate their formulas.** One shipped
test checks that its stage-1 figure agrees with `ael::diffpair::mirrorGain` to machine precision,
which it can only do by calling it.

---

## C.8 Cross-check: the capstone

**Predict the whole amplifier, solve the whole amplifier, and reconcile the two, row by row.**

1. **Predict.** Run `budget` and record the four stage gains and the open-loop gain.
2. **Solve, stage by stage.** Build each stage as its own netlist, bias it, perturb its input by a
   small voltage, and measure its output. Load each stage with the next stage's input resistance
   as a resistor, so that the solver is measuring the same quantity the closed form predicted.
3. **Reconcile.** Print predicted against measured with the difference in per cent, one row per
   stage.
4. **Then solve the whole amplifier open-loop**, with the four stages connected. Report what
   happens.
5. **Then close the loop** with a feedback divider for a gain of 20, solve again, and report the
   closed-loop gain.

### What to expect

**Every row differs by a few per cent, and every difference has a name.** The closed forms take
$V_T$ as 26 mV where the device computes $kT/q = 25.87$; they take $r_o$ as $V_A/I_C$ where
differentiating the model gives $(V_A + V_{CE})/I_C$; they take $\beta$ as 50 where the transport
model's incremental value differs slightly. **Account for every row.** A reader whose rows agree
to six figures has run the same code twice and learned nothing.

**Part 4 will not converge on a sensible answer, and that is the correct result.** With an
open-loop gain of a million and rails of 15 V, an input offset of **15 microvolts** saturates the
output. Your solver will report the output at a rail, or fail to converge, and both are true
statements about operational amplifiers. Do not tune your solver until it produces a mid-rail
answer; there is not one.

**Part 5 will converge**, and the closed-loop gain should be within a per cent of 20. Notice what
you have just demonstrated: the same circuit is unsolvable open-loop and well-behaved closed-loop,
and nothing about the transistors changed.

**Finally, the exercise that is the course.** Repeat part 5 with $\beta$ at 20 and at 200. The
open-loop gain moves by a factor of 14. Report what the closed-loop gain does, and say in one
sentence what that is worth.

---
