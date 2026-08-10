# L08 - Followers, and the output stage they turn into

## Agenda
* The stage with no voltage gain, and why nearly every amplifier contains several.
* Gain just under one, and the shortfall as a design quantity rather than a rounding error.
* Impedance transformation: $h_{FE}$ going in, $r_e$ coming out.
* The 8 ohm problem, and the arithmetic that says one follower is not enough.
* The Darlington, $h_{FE}^2$, and the price of leaning on beta.
* Class A, class B, and the dead band between them.
* Class AB, and the 26 millivolt rule that sizes the emitter resistors.
* Why the bias diodes must be bolted to the same heatsink as the output devices.
* The source follower, the body effect, and the one place $r_s$ does not carry across cleanly.
* Live-coding `ael::follower` and `ael::output`.

---

## Lecture plan
1. **A stage that does nothing, usefully.** Its gain is 0.97. Everything it is for is in the two
   resistances rather than the one gain.
2. **The three results, again.** Same method as L07, different node. Gain $R_E/(r_e + R_E)$, input
   resistance $h_{FE}(r_e + R_E)$, output resistance $r_e$ plus the source divided by $h_{FE}$.
3. **The 8 ohm problem.** A common-emitter stage with a gain of 38 delivers **0.08 per cent** of it
   into a loudspeaker. One follower recovers 4 per cent. A Darlington recovers 68.
4. **Which is the whole reason output stages exist**, and it is L01's loading arithmetic for the
   fifth time in this course.
5. **The bill for the Darlington.** It is $h_{FE}^2$, so the answer spans 25 to 97 per cent across
   an ordinary beta spread. A number that depends on beta squared is not a number.
6. **Class A, B and AB.** A follower biased to carry the whole signal is class A and wastes most of
   its supply. Two followers sharing the work is class B and has a dead band 1.3 V wide.
7. **The 26 millivolt rule.** Bias each output device so its emitter resistor drops one thermal
   voltage. Then $R_E = r_e$, the emitter factor is 2, and the stage is stable without giving away
   the load.
8. **Thermal runaway, and the fix that looks like nothing.** The bias diodes go on the heatsink.
   They are not setting a voltage; they are tracking one.
9. **Live coding.** `ael::follower`, then `ael::output`, then the idle current solved numerically
   and compared with what the constant-drop model predicted.

---

## Before the lecture
* Finish L07. This lecture is L07's model applied at the emitter instead of the collector, and
  nothing new is derived.
* Read [Appendix A](./appendix/a_the_follower.md), the follower and what it transforms.
* Read [Appendix B](./appendix/b_the_output_stage.md), the output stage and what to build.
* [Appendix C](./appendix/c_power_amplifiers.md) is reading, not examinable, and there are no
  exercises on it.
* Come with this in mind: a stage with a voltage gain of one is worth building. Why?

---

## After the lecture
* Write `ael::follower` and `ael::output` to the specification in
  [B.7](./appendix/b_the_output_stage.md#b7-what-to-build).
* Add rows to the report program for `ael::follower` and `ael::output`.
* Work through [Appendix D](./appendix/d_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix E](./appendix/e_solutions.md).

---

## What you should be able to do afterwards
* Derive a follower's gain, input resistance and output resistance from the same model as L07.
* Say what a follower costs and what it buys, in ohms rather than in adjectives.
* Compute what a given load does to a given stage, and choose between a follower, a Darlington and
  a redesign.
* State the three amplifier classes by what conducts when, and give the efficiency of each.
* Explain crossover distortion, and why it is worse than its size suggests.
* Size the emitter resistors of a class-AB stage from the idle current.
* Say why the bias generator must be thermally coupled to the output devices, and what happens if
  it is not.
* Carry every follower result to a MOSFET, and name the one thing that stops it being exact.

---

## Questions to test yourself
* A follower's gain is 0.974. Where did the other 2.6 per cent go, and what would you change to
  get it back?
* Looking into a follower's base with 8 ohms on its emitter, what do you see? Now say it again
  with the beta spread included.
* Why does a stage with 10 kilohms of output resistance lose 99.9 per cent of its gain into a
  loudspeaker, when the same load costs a follower only 3 per cent?
* Class B is 78 per cent efficient and class A is 25. Why is class A used at all?
* A class-AB stage idles at 120 mA. What emitter resistors does the 26 mV rule give, and what is
  the emitter factor it produces?
* The bias generator is two silicon diodes. Name the failure that follows from mounting them on
  the circuit board instead of the heatsink.
* A source follower's gain is lower than an emitter follower's at the same current. Give the
  number and the reason.

---

## Reference
* [Appendix A](./appendix/a_the_follower.md): the follower, the three results, and the 8 ohm
  problem.
* [Appendix B](./appendix/b_the_output_stage.md): classes, crossover, the 26 mV rule, thermal
  coupling, the source follower, and what to build.
* [Appendix C](./appendix/c_power_amplifiers.md): what a real power amplifier adds. Reading only.
* [Appendix D](./appendix/d_exercises.md): the exercises, ending with the Cross-check.
* [Appendix E](./appendix/e_solutions.md): worked solutions, in full.
* [The L08 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 2, for followers, and chapter 2x for
  output stages at more length than this course has room for.

---

## Next lecture
* L09 is the stage that subtracts: the differential pair, what its tail decides, and why the
  current mirror of L07 turns up again as its load.

---
