# L10 - Building an operational amplifier, and the capstone

## Agenda
* The black box of L03, opened: eleven transistors, and every one of them already analysed.
* What each stage is responsible for, and why that is the only way to size any of them.
* The gain budget, and the eleven decibels that loading takes.
* The two stages with no voltage gain, which are worth 31 dB each.
* Why the amplifier has no open-loop operating point at all, and what that means for the solver.
* Miller compensation: making one pole dominant on purpose.
* Closing the loop, and L04's arithmetic arriving where it was always going.
* The capstone: one program, every stage predicted and solved, printed side by side.

---

## Lecture plan
1. **Everything in this lecture is already built.** The pair is L09, the mirror is L07, the
   followers are L08, the gain stage is L07 again. L10 adds no new circuit; it adds the
   **accounting**, and the accounting is where the surprises are.
2. **Four stages, and two of them have no gain.** A mirror-loaded pair, a Darlington buffer, a
   common-emitter stage, a class-AB Darlington output.
3. **The budget.** Two stages of 65.7 dB should give 131. The amplifier delivers **120**.
4. **Where the 11 dB went**, and it is not distributed evenly: 10.6 dB of it is stage 3 being
   loaded by the output stage, and that is after the output stage was made a Darlington.
5. **The two stages that have no gain are the most valuable in the amplifier.** Remove the buffer
   and the open loop falls from 120 dB to 88. Remove the output Darlington and it falls to 89.
6. **There is no open-loop operating point.** A gain of a million and a millivolt of offset puts
   the output at a rail. The DC solve only converges with the loop closed, and that is a fact
   about amplifiers rather than about solvers.
7. **Miller compensation.** One capacitor, one dominant pole, and the reason the closed loop is
   stable rather than an oscillator.
8. **Close the loop.** 120 dB open, a gain of 20 closed, and an error of 0.002 per cent. L04
   promised this in the fourth lecture of Part 1.

---

## Before the lecture
* Have L06 through L09 working. This lecture composes them and adds almost nothing.
* Read [Appendix A](./appendix/a_the_amplifier.md), the amplifier stage by stage.
* Read [Appendix B](./appendix/b_the_budget_and_the_loop.md), the budget, the loop, and what to
  build.
* Come with this in mind: two stages with a gain of 1923 each, and an amplifier with an open-loop
  gain of one million rather than 3.7 million. Where does a factor of 3.7 go?

---

## After the lecture
* Add PNP support to your netlist and write `ael::report`, to the specification in
  [B.6](./appendix/b_the_budget_and_the_loop.md#b6-what-to-build).
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**, which is
  the capstone.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Name every stage of a discrete operational amplifier and say what it is responsible for.
* Compute a gain budget with loading, and say why one without loading is not conservative but
  wrong.
* Explain why an amplifier with no voltage gain in half its stages needs those stages.
* Say why an open-loop DC operating point does not exist, and what your solver does about it.
* Explain what a Miller capacitor is compensating and what would happen without it.
* Close the loop and predict the closed-loop gain, the error, and the output resistance.
* Run one program that predicts and solves the whole amplifier and reconciles the two.

---

## Questions to test yourself
* The pair gives 1923 and the common-emitter stage gives 1923. Why is the open-loop gain not
  3.7 million?
* The Darlington buffer has a voltage gain of 0.96. What is it worth, in decibels, and why?
* What is the input resistance of the output stage, and what would it be if it were a single
  follower instead? What does that difference cost?
* You solve the amplifier open-loop and the output sits at the negative rail. Is that a bug?
* What would happen to the closed loop if the Miller capacitor were removed?
* The closed-loop gain is 20 and the open-loop gain is a million. How far is the closed-loop gain
  from exactly 20, and what would make it closer?
* The output stage's input resistance depends on $h_{FE}^2$, which varies by a factor of a
  hundred between devices. Why does the closed-loop gain not?

---

## Reference
* [Appendix A](./appendix/a_the_amplifier.md): the amplifier, stage by stage.
* [Appendix B](./appendix/b_the_budget_and_the_loop.md): the budget, the missing operating point,
  compensation, the loop, and what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the capstone Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L10 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 4x, for a walk through several real
  operational amplifier schematics of the kind this lecture builds.

---

## After the course
* The [exam papers](../../exam/README.md) are four hours each and cover the whole course.
* What this course did not cover, and where to go for it, is in
  [B.8](./appendix/b_the_budget_and_the_loop.md#b8-what-this-course-is-blind-to).

---
