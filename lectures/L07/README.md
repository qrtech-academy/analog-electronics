# L07 - Small-signal analysis: r_e, the emitter factor, and the cascode

## Agenda
* Small-signal as a straight line through an operating point, and everything that discards.
* Building the small-signal schematic: what to short, what to delete, what to replace.
* The intrinsic emitter resistance, and where the 26 mV comes from.
* Gain, input resistance and output resistance, each from one walk around a loop.
* The emitter factor: one number for what degeneration costs and what it buys.
* Which resistance that factor actually multiplies, which is not the obvious one.
* The Early effect, and the current-mirror load that stops the boost being thrown away.
* The source factor and $r_s$: the same results, transferred to the MOSFET by substitution.
* The Miller effect, and the cascode as the answer to it.
* Live-coding `ael::ssm`, checked against the solver on every stage.

---

## Lecture plan
1. **The centre of the course.** Everything before this was preparation; everything after is this
   applied. If one lecture is worth rereading, it is this one.
2. **Linearising.** A transistor is exponential. Over a small enough excursion an exponential is a
   straight line, and the slope of that line at the operating point is all a signal ever sees.
3. **The one resistance.** That slope has units of conductance; its reciprocal is $r_e$, and it is
   26 ohm at 1 mA. Every result today is written in terms of it.
4. **Three results, one method.** Gain, input resistance, output resistance. Each is one walk
   around one loop, and doing them the same way each time is the point.
5. **The emitter factor.** $EF = (r_e + R_E)/r_e$, one number that answers two questions, and
   the organising idea of this whole treatment.
6. **Where it belongs.** It is tempting to attach EF to the stage's output resistance. It
   belongs to the resistance looking into the collector, and the difference is a factor of ten.
   Getting it right explains why the mirror loads of the next section exist.
7. **The MOSFET, in one substitution.** Name $r_s = 1/g_m$ and every result above transfers
   unchanged. Input resistance is the exception.
8. **Miller, and the cascode.** Four picofarads becomes 1.5 nanofarads, and a stage good to
   hundreds of megahertz rolls off at a hundred kilohertz. The cascode is degeneration again.
9. **Live coding.** `ael::ssm`, then the Early effect in `ael::device::bjt`, then every result
   above checked against the solver on the same netlist.

---

## Before the lecture
* Finish L06. This lecture linearises the operating point L06 found.
* Read [Appendix A](./appendix/a_the_small_signal_model.md), which is the model and the three
  results.
* Read [Appendix B](./appendix/b_the_emitter_factor.md), which is the emitter factor, the
  correction, and what to build.
* Come with this in mind: a stage with a 10 kilohm collector resistor has an output resistance of
  about 10 kilohm. Adding an emitter resistor multiplies something by ten. What?

---

## After the lecture
* Write `ael::ssm` and add the Early effect to `ael::device::bjt`, to the specification in
  [B.7](./appendix/b_the_emitter_factor.md#b7-what-to-build).
* Add a row to the report program for `ael::ssm`.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Draw the small-signal schematic of any stage in this course, and say what each step discarded.
* Write $r_e$ from a collector current without looking it up.
* Derive gain, input resistance and output resistance for a common-emitter stage.
* State the emitter factor, and both of the things it decides.
* Say which node the emitter factor's boost appears at, and why it is invisible at another.
* Explain why a current-mirror load raises the gain by two independent mechanisms.
* Transfer any result to a MOSFET by substituting $r_s$, and name the one result that does not
  transfer.
* Compute a Miller capacitance, and say what a cascode does about it.

---

## Questions to test yourself
* $r_e$ is 26 ohm at 1 mA. Is it a resistor? What happens to it if the stage is switched off?
* A stage has $R_C = 10$ kilohm and $R_E = 234$ ohm. What is its gain, and what would it be with
  the emitter resistor bypassed?
* The emitter factor is ten. Name the two quantities it relates, and say which of them is a
  property of the transistor rather than of the stage.
* Why does adding an emitter resistor barely change the output resistance of a resistively loaded
  stage, when it multiplies the resistance looking into the collector by ten?
* A current mirror as a load raises the gain for two separate reasons. Name both.
* A stage with a gain of 385 and 4 pF of collector-base capacitance is driven from 1 kilohm. Where
  is its input pole?
* A cascode is often described as a new circuit. In what sense is it a stage you have already
  analysed?

---

## Reference
* [Appendix A](./appendix/a_the_small_signal_model.md): the model, and the three results.
* [Appendix B](./appendix/b_the_emitter_factor.md): the emitter factor, the correction, the
  mirror, $r_s$, the cascode, and what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L07 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 2, for the small-signal model, and
  *Microelectronic Circuits*, Sedra and Smith, if you want the hybrid-pi form instead.

---

## Next lecture
* L08 is the stage with no voltage gain at all, and why almost every design contains one.
  Followers, impedance transformation, and the output stage they turn into.

---
