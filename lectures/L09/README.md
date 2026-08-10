# L09 - The differential amplifier

## Agenda
* The first circuit in the course built to **reject** rather than to amplify.
* The pair, the tail, and the two halves that share it.
* Differential gain: the common-emitter result with a two in it, and where the two comes from.
* Common-mode gain, and the tail acting as a degeneration resistor of twice its value.
* CMRR, and the fact that the collector resistor cancels out of it entirely.
* Why every real pair has a current source in its tail and not a resistor.
* The current-mirror load, and the two independent factors it wins.
* The large-signal transfer: nine millivolts of linearity, and hard limiting beyond.
* Offset, matching, and why almost every modern input stage is MOSFET.
* Live-coding `ael::diffpair`.

---

## Lecture plan
1. **A stage with two inputs and one job.** Amplify the difference, ignore what the two have in
   common. Everything else follows from that sentence.
2. **The tail.** One current, shared. When the inputs move oppositely the tail node does not move
   at all; when they move together it moves with them. That asymmetry *is* the circuit.
3. **Differential gain.** $-R_C/2r_e$ at one collector. The two is because a differential input of
   $v$ is only $v/2$ on each base, and taking one output throws the other half away.
4. **Common-mode gain.** Both halves push on the tail together, so it acts as $2R_{tail}$ of
   degeneration, and L07's emitter factor is back doing the work.
5. **CMRR, and the surprise.** $R_C$ cancels. **No choice of load improves rejection.** The only
   lever is the tail.
6. **And the tail is a supply-voltage question.** 80 dB needs 260 kilohm carrying 2 mA, which is
   **520 V** across it. That is why the tail is a current source.
7. **The mirror load, twice over.** It turns the wasted half back into signal, and it replaces
   10 kilohm with 50. Two mechanisms, and the lecture separates them.
8. **Nine millivolts.** The pair is a tanh, linear over a few millivolts and hard-limiting by
   100. That is an operational amplifier's input stage, and it is where slew rate comes from.
9. **Live coding.** `ael::diffpair`, then the rejection measured through the solver on both tails,
   resistive and current-source.

---

## Before the lecture
* Finish L08. The pair is two common-emitter stages sharing an emitter, and every result comes
  from L07's model unchanged.
* Read [Appendix A](./appendix/a_the_pair.md), the pair and what it does to a difference.
* Read [Appendix B](./appendix/b_rejection_and_the_mirror.md), rejection, the mirror, offset, and
  what to build.
* Come with this in mind: two identical transistors, and the whole circuit's usefulness depends on
  a resistor neither of them is connected to at the top.

---

## After the lecture
* Write `ael::diffpair` to the specification in
  [B.7](./appendix/b_rejection_and_the_mirror.md#b7-what-to-build).
* Add a row to the report program for `ael::diffpair`.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Draw a differential pair and say what its tail current fixes.
* Derive the differential gain and account for both factors of two in it.
* Derive the common-mode gain and say why the tail appears doubled.
* State CMRR, and say which components in the circuit do **not** affect it.
* Choose a tail arrangement from a CMRR requirement, and justify the supply voltage it needs.
* Give the two independent reasons a current-mirror load raises the gain.
* State the pair's linear input range in millivolts, and say what it does outside it.
* Compute an input-referred offset from a stated mismatch, and say which mismatch dominates.

---

## Questions to test yourself
* A pair with a 2 mA tail: what is $r_e$ on each side, and why is it 26 ohm rather than 13?
* The differential gain to one collector is half what it is to both. Where did the other half go,
  and what would recover it?
* Two designers argue about CMRR. One wants a larger collector resistor. Who is right?
* What resistance would the tail need for 80 dB of rejection, and what supply voltage does that
  imply? Now say what is used instead.
* A current-mirror load raises the gain by a factor of ten here. Split that ten into its two
  causes.
* An input signal of 50 mV differential. Is the small-signal gain the right answer? Show why not.
* A 1 per cent mismatch between the two collector resistors: what offset does it produce at the
  input, and how does that compare with 1 mV of $V_{BE}$ mismatch?

---

## Reference
* [Appendix A](./appendix/a_the_pair.md): the pair, the tail, the gain, and the tanh.
* [Appendix B](./appendix/b_rejection_and_the_mirror.md): common-mode, CMRR, the mirror, offset,
  and what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L09 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 2, sections on the differential amplifier,
  for a second treatment of the same material.

---

## Next lecture
* L10 assembles L06 to L09 into one operational amplifier, opens the black box of L03, closes the
  loop with L04's arithmetic, and is the capstone.

---
