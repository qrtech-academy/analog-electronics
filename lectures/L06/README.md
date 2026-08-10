# L06 - Biasing, and what an emitter resistor actually buys

## Agenda
* The quiescent point as three numbers, and the load line that constrains them.
* Voltage-divider bias, and the base current that loads the divider you designed.
* Stiffness: why the divider current must be much larger than the base current, and what happens
  at the usual rule of thumb.
* Thermal drift: the base-emitter voltage falling about 2 mV per degree, and what that does.
* The emitter resistor as local feedback, and the drift divided by the emitter factor.
* An argument that does not survive its own arithmetic, and the correct one.
* The 220 mV rule, and the E12 value it lands on.
* Live-coding `ael::bias`, and adding temperature to the transistor model.

---

## Lecture plan
1. **Holding the device still.** An amplifier is a transistor sitting at an operating point with a
   signal moving it about. Today is the sitting still; L07 is the moving about.
2. **The load line, again.** Same construction as L05's switch, different place on it: an
   amplifier sits in the middle, where there is room to move both ways.
3. **Divider bias, and its first surprise.** The divider that gives 1.71 V unloaded gives 1.60 V
   with a base hanging on it, and the collector current is 12 per cent lower than the design said.
   That is L01's loading, for the fourth time.
4. **The problem worth solving.** At a fixed base voltage, the collector current rises about
   8 per cent per degree. A stage that works at 20 degrees is unusable at 50.
5. **The fix, and a wrong explanation of it.** There is a tempting explanation of the emitter
   resistor's action that does not survive its own numbers. You will do the arithmetic and find
   out where it breaks.
6. **The right explanation.** The emitter resistor is a local feedback loop of gain $R_E/r_e$, and
   it divides the drift by exactly the factor it costs in gain.
7. **Live coding.** `ael::bias`, then temperature in the BJT model, then a temperature sweep.

---

## Before the lecture
* Finish L05. This lecture sweeps a transistor circuit over temperature, which needs L05's device
  in L04's solver.
* Read [Appendix A](./appendix/a_the_quiescent_point.md), which is biasing and the divider.
* Read [Appendix B](./appendix/b_thermal_drift.md) up to
  [B.5](./appendix/b_thermal_drift.md#b5-what-to-build).
* Bring an answer to this: a transistor's base sits at a fixed 1.6 V. The temperature rises ten
  degrees. What has happened to the collector current?

---

## After the lecture
* Write `ael::bias` and add temperature to `ael::device::bjt`, to the specification in
  [B.5](./appendix/b_thermal_drift.md#b5-what-to-build).
* Add a row to the report program for `ael::bias`.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Find the quiescent point of a divider-biased stage, including the base current's effect.
* Say what divider stiffness is, choose it, and say what the usual rule of thumb costs.
* State the thermal drift of a base-emitter voltage, and the collector current drift it implies at
  a fixed base voltage.
* Explain what an emitter resistor does, in terms of feedback rather than in terms of a story
  about voltages moving.
* Compute the drift suppression, and notice it is the same number as the gain reduction.
* Apply the 220 mV rule and say where it comes from.
* Recognise an argument that is self-contradictory, from its own numbers.

---

## Questions to test yourself
* A divider is designed for 1.71 V and measures 1.60 V with the transistor connected. Nothing is
  broken. What is happening, and which L01 result predicts it?
* Divider current ten times base current is the usual rule. What error in the collector current
  does that rule accept?
* At a fixed base voltage the collector current rises 8 per cent per degree. Where does that
  number come from, and which of $V_T$ or $I_S$ contributes most of it?
* An emitter resistor reduces drift and reduces gain. By what factor each, and why is that not a
  coincidence?
* The 220 mV rule puts about a fifth of a volt across the emitter resistor. What would 22 mV give,
  and what would 2.2 V give?
* Somebody argues that when the current rises 10 per cent, the base-emitter voltage falls from
  0.65 V to 0.55 V and pulls it back. Find the contradiction.
* Your stage is biased at 1 mA and drifts 0.2 per cent per degree. What would it drift at 10 mA
  with the same emitter resistor?

---

## Reference
* [Appendix A](./appendix/a_the_quiescent_point.md): the operating point, divider bias, stiffness.
* [Appendix B](./appendix/b_thermal_drift.md): drift, the emitter resistor, and what to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L06 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 2, sections on biasing, for a second
  treatment of the same material.

---

## Next lecture
* L07 is the centre of the course. The small-signal model, the intrinsic emitter resistance the
  whole of Part 2 is written in terms of, and the emitter factor, including the node it actually
  belongs to.

---
