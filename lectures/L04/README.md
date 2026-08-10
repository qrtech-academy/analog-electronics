# L04 - Feedback, active filters, and the diode

## Agenda
* Loop gain, and the closed-loop gain written so the error term is visible.
* Desensitisation: trading gain you have for accuracy you want.
* What feedback does to input and output impedance, and in which direction.
* Distortion divided by the loop gain, and the nonlinearity that always survives.
* Gain-bandwidth product, and the stability limit that ends the free lunch.
* Active filters, and the loading problem an amplifier solves for them.
* The diode: the exponential, the 0.7 V approximation, and where it stops being one.
* Newton-Raphson, and why plain Newton-Raphson does not work on a diode.
* Live-coding `ael::feedback`, `ael::device::diode` and `ael::nr`.

---

## Lecture plan
1. **Why the two rules worked.** L03 asserted them. This lecture derives them, and the derivation
   produces an error term that says exactly how far from true they are.
2. **One number decides everything.** The loop gain $T$. Gain error is $1/(1+T)$, distortion is
   divided by $1+T$, impedances are multiplied or divided by $1+T$. Learn $T$ and the rest is
   bookkeeping.
3. **What it costs.** The gain you gave up, and the bandwidth you did not get: gain and bandwidth
   trade one for one, so an amplifier is sold by their product.
4. **Where it stops.** Enough phase shift inside the loop turns negative feedback positive, and an
   amplifier becomes an oscillator. Stated, not derived.
5. **Active filters.** L03 needed a buffer between two sections. Sallen-Key does better: it uses
   one amplifier to get a complex pole pair that no passive RC cascade can produce at all.
6. **The diode.** The first device in this course that is not linear, so the first that no phasor
   can describe and no single solve can find.
7. **Live coding.** The diode model, then the Newton-Raphson loop, then the limiting that makes it
   converge.

---

## Before the lecture
* Finish L03. The nonlinear solver here is L01's linear solver called repeatedly, so it needs the
  linear one to work.
* Read [Appendix A](./appendix/a_feedback.md), which is feedback.
* Read [Appendix B](./appendix/b_the_diode_and_newton_raphson.md) up to
  [B.5](./appendix/b_the_diode_and_newton_raphson.md#b5-what-to-build).
* Have the answer to this ready: an amplifier with an open-loop gain of $10^5$ is used at a closed
  loop gain of 10. How accurate is that 10?

---

## After the lecture
* Write `ael::feedback`, `ael::device::diode` and `ael::nr` to the specification in
  [B.5](./appendix/b_the_diode_and_newton_raphson.md#b5-what-to-build).
* Add the diode to `ael::net::Netlist`.
* Add rows to the report program for `ael::feedback`, `ael::device::diode` and `ael::nr`.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Compute the loop gain of any of L03's configurations, and the gain error that follows.
* Say how much open-loop gain a stated accuracy needs, and notice when the answer is unreasonable.
* State what feedback does to input impedance, output impedance and distortion, with the direction
  right in each case.
* Convert between gain-bandwidth product, closed-loop gain and closed-loop bandwidth.
* Say what a Sallen-Key section buys over two cascaded RC sections with a buffer between them.
* Write down the diode equation, and say what a 60 mV change of its voltage does.
* Explain why plain Newton-Raphson fails on a diode from a cold start, and what a simulator does
  about it.

---

## Questions to test yourself
* An amplifier has $10^5$ of open-loop gain. You use it at a closed-loop gain of 1000. What is the
  gain error, and is that amplifier a good choice?
* Feedback divides distortion by $1 + T$. What distortion remains, and why can it not be removed
  by more feedback?
* Two amplifiers have the same gain-bandwidth product. One is used at a gain of 10 and one at 100.
  Which has more loop gain at 10 kHz, and by how much?
* Negative feedback becomes positive when the loop phase reaches 180 degrees. How many first-order
  poles does it take to get there, and what does that say about how many stages a loop can have?
* A diode carries 1 mA at 0.65 V. What voltage does it need for 10 mA? For 1 microamp?
* Why does a nonlinear solver need a convergence criterion at all, when a linear one just solves?
* Your Newton-Raphson loop converges in 6 iterations on one circuit and 400 on another that
  differs only in a resistor value. What is different about the second one?

---

## Reference
* [Appendix A](./appendix/a_feedback.md): loop gain, what it buys, what it costs, active filters.
* [Appendix B](./appendix/b_the_diode_and_newton_raphson.md): the diode and the nonlinear solve.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L04 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 4, for feedback, and chapter 1 for the
  diode.

---

## Next lecture
* L05 begins Part 2. The transistor as a device with an exponential, a current gain and a
  saturation voltage, and with as little semiconductor physics as can be managed.

---
