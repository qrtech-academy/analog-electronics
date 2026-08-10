# L02 - Reactance, phasors, and frequency response

## Agenda
* The capacitor and the inductor as devices that remember, and the time constant that says how
  long for.
* Sinusoidal steady state, and why a complex number can stand in for a sinusoid.
* Impedance: resistance that depends on frequency, and the two stamps that follow from it.
* Magnitude and phase, the decibel, and the Bode plot as two straight lines and a corner.
* The phase, which is the half people skip and the half that decides stability.
* The transformer, briefly, and where its model stops being true.
* Live-coding the complex stamps and `ael::ac`.

---

## Lecture plan
1. **Two devices that remember.** A resistor's current depends on the voltage now. A capacitor's
   depends on how the voltage has been changing. That one difference is the whole lecture.
2. **The time constant.** $\tau = RC$, and the observation that settling to 0.1 per cent takes
   seven time constants rather than the three most people assume.
3. **The trick.** In sinusoidal steady state every voltage and current in a linear circuit is a
   sinusoid at the same frequency, so only amplitude and phase differ. One complex number carries
   both, and differentiation becomes multiplication by $j\omega$.
4. **Impedance and the stamps.** With that substitution a capacitor is a conductance of
   $j\omega C$ and an inductor one of $1/(j\omega L)$. Nothing about the solver changes except the
   scalar type.
5. **Reading a response.** The corner, the two asymptotes, and the 45 degrees of phase that are
   already there when the magnitude has barely moved.
6. **Live coding.** Template the solver on its scalar type, add the two stamps, sweep.

---

## Before the lecture
* Finish L01. This lecture extends `ael::mna` rather than replacing it, and it assumes the L01
  suite is green.
* Read [Appendix A](./appendix/a_reactance_and_phasors.md), which is the physics and the phasor
  argument.
* Read [Appendix B](./appendix/b_the_ac_solver.md) up to
  [B.4](./appendix/b_the_ac_solver.md#b4-what-to-build), which is what gets written live.
* Have a look at your L01 solver and ask what would have to change for it to hold complex numbers.
  The answer is meant to be "the scalar type, and nothing else"; if it is more than that, this
  lecture is a good time to find out why.

---

## After the lecture
* Extend `ael::net::Netlist` with capacitors and inductors, and write `ael::ac` to the
  specification in [B.4](./appendix/b_the_ac_solver.md#b4-what-to-build).
* Add a row to the report program for `ael::ac`.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**. This one
  is the first where two legs are expected to disagree, and by a stated amount.
* Compare against [Appendix D](./appendix/d_solutions.md) afterwards.

---

## What you should be able to do afterwards
* Compute a time constant, and say how many of them a given settling accuracy needs.
* State what a phasor is, and what has to be true of a circuit before one is allowed.
* Write down the impedance of a capacitor and an inductor at any frequency, from memory.
* Sketch a first-order response from its corner frequency alone, magnitude and phase.
* Say what the phase is doing a decade either side of the corner, to within a degree or two.
* Convert between a ratio and decibels without a calculator for the cases that matter.
* Extend a real solver from real to complex arithmetic without duplicating it.

---

## Questions to test yourself
* A capacitor's impedance falls with frequency and an inductor's rises. At what frequency are they
  equal, and what is special about a circuit operating there?
* Why is $j\omega$ a legitimate substitute for $d/dt$, and what property of the circuit does that
  argument depend on?
* A first-order low-pass is 3 dB down at its corner. How far down is it half a decade above?
* At what frequency has a first-order low-pass reached 45 degrees of phase lag, and how much
  magnitude has it lost there?
* A colleague says a filter "does nothing" a decade below its corner. What has it done to the
  phase there, and when would that matter?
* Your AC solver returns the right magnitude and a phase of the wrong sign at every frequency.
  Name the most likely single cause.
* An amplifier settles to within 1 per cent in 5 microseconds. How long does it need for 0.01 per
  cent, assuming one time constant dominates?

---

## Reference
* [Appendix A](./appendix/a_reactance_and_phasors.md): reactance, time constants and phasors.
* [Appendix B](./appendix/b_the_ac_solver.md): the complex stamps and what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L02 test suite](./exercises/test/README.md).
* L01 [Appendix B](../L01/appendix/b_nodal_analysis.md), which is the solver this lecture extends.
* *The Art of Electronics*, Horowitz and Hill, chapter 1, sections on reactance and RC
  circuits, for a second treatment of the same material.

---

## Next lecture
* L03 puts the reactance to work. Passive filters, what cascading two of them actually gives you,
  and then the operational amplifier as a black box with two rules.

---
