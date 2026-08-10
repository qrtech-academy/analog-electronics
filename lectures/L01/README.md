# L01 - Circuits, units, and the nodal solver

## Agenda
* Charge, current, voltage and power, and the sign convention every later result depends on.
* Series and parallel, and the voltage divider as the one circuit worth memorising.
* Kirchhoff's two laws, which are the only physical content in the whole of circuit theory.
* Thevenin and Norton, and loading as the reason either of them matters.
* Nodal analysis: one unknown per node, one equation per node, and the conductance stamp.
* Why a program that solves circuits is easier to write than the equations are to solve by hand.
* Live-coding `ael::net` and `ael::mna`.

---

## Lecture plan
1. **What the course is, and what it is not.** Ten hours on the transistor amplifier. The first
   four lectures build the circuit theory the last six need, and nothing more than that.
2. **Units, and the sign convention.** Current into a component is positive. Every gain, every
   bias point and every output resistance in Part 2 inherits that choice, so it gets five minutes
   here rather than an argument in L07.
3. **The divider.** Two resistors, one formula, and the observation that it stops being true the
   moment anything uses its output. That observation is the whole of `ael::mna`'s reason to exist.
4. **Thevenin.** Any linear network, seen from two terminals, is a source behind a resistance.
   For a divider that resistance is the two legs in parallel, which is smaller than either.
5. **Kirchhoff, and nodal analysis.** One unknown per node. One current-balance equation per node.
   The conductance stamp is what turns that sentence into a matrix without thinking.
6. **Live coding.** `ael::net::Netlist`, then `ael::mna::solve`, then the divider through both.

---

## Before the lecture
* Read [info/toolkit.md](../../info/toolkit.md), which fixes where your toolkit lives, the two
  sign conventions, and the header paths the test suites include.
* Read [Appendix A](./appendix/a_circuits_and_units.md), which is the circuit theory. If you have
  an electronics background this is a twenty-minute skim; do not skip
  [A.6](./appendix/a_circuits_and_units.md#a6-loading-and-why-it-decides-everything-later).
* Read [Appendix B](./appendix/b_nodal_analysis.md) up to
  [B.5](./appendix/b_nodal_analysis.md#b5-what-to-build), which is what gets written live.
* Check that `make test` runs. With no toolkit it reports four passing tests and that is correct.

---

## After the lecture
* Finish `ael::net` and `ael::mna` to the specification in
  [B.5](./appendix/b_nodal_analysis.md#b5-what-to-build), and get L01's suite to seventeen.
* Start the report program described in
  [info/toolkit.md](../../info/toolkit.md#what-the-toolkit-is-for). One row per component, saying
  whether it is yours or a stub. Every later lecture adds a row, and L10's capstone is its output.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md) once you have your own answers, and not
  before.

---

## What you should be able to do afterwards
* State the sign convention this course uses, and say what breaks if it is inverted.
* Compute a divider's output, its Thevenin resistance, and its output under any load, by hand.
* Say why a 10 kilohm load on a 33k/6.8k divider is not a light load.
* Write the node equation for any node in a resistive network without deriving it from scratch.
* Stamp a resistor, a current source and a voltage source into a matrix.
* Explain why a voltage source needs an extra unknown, and what that unknown is.
* Implement `ael::net` and `ael::mna` against the shipped suite.

---

## Questions to test yourself
* A divider made of 1 megohm and 1 megohm, and one made of 10 ohms and 10 ohms, have the same
  ratio. What is different about them, and which would you put on an oscilloscope probe?
* Why is a divider's Thevenin resistance the same whichever leg you call the upper one?
* Nodal analysis gives one equation per node. A network has five nodes. How many unknowns are
  there, and why is it not five?
* You stamp a resistor between two nodes and get four matrix entries. Two are positive and two are
  negative. Which are which, and what would swapping them mean physically?
* A voltage source between two nodes cannot be written as a conductance. Why not, and what does
  the extra row in the matrix say?
* Your solver returns node voltages that are all zero for a network you know is live. Name two
  causes, and say which one the shipped suite catches.
* Superposition says two sources add. Your solver never mentions superposition. Why does it hold
  anyway, and in which lecture does it stop holding?

---

## Reference
* [Appendix A](./appendix/a_circuits_and_units.md): circuits, units, and loading.
* [Appendix B](./appendix/b_nodal_analysis.md): Kirchhoff, nodal analysis, and what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L01 test suite](./exercises/test/README.md): what it covers and how to run it.
* *The Art of Electronics*, Horowitz and Hill, chapter 1, for a second treatment of the same
  material at roughly the same level.

---

## Next lecture
* L02 makes the solver complex, which is the whole of the frequency domain and costs about thirty
  lines. Reactance, phasors, and the Bode plot as two straight lines and a corner.

---
