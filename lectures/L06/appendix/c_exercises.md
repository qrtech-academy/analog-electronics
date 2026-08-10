# Appendix C - Exercises

Eight, ending with the Cross-check. That one has four legs, and one of them is a tempting
argument you are asked to break.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: the operating point

1. Name the three numbers that describe a quiescent point, and say why it is usually two.
2. Write the load line of a stage with both a collector and an emitter resistor.
3. Where on it does an amplifier sit, and what decides "where"?
4. A stage is biased so that the collector sits at 0.5 V above the emitter. What is wrong with it,
   and what would the output look like?

---

## C.2 Recall: stiffness

1. Define divider stiffness, and give the usual rule of thumb.
2. What error in the collector current does that rule of thumb accept?
3. What does buying a factor of ten more stiffness cost?
4. Name two ways of making the base current negligible instead, and say which lectures use them.

---

## C.3 Hand calculation: the quiescent point, twice

For the stage in [A.2](./a_the_quiescent_point.md#a2-divider-bias): 10 V, 33 kilohm over
6.8 kilohm, 1 kilohm emitter, 4.7 kilohm collector, $\beta = 50$.

1. The base voltage, emitter voltage and collector current, ignoring base current.
2. The base current that implies, and the droop it causes across the divider's Thevenin
   resistance.
3. The corrected base voltage and collector current. One iteration is enough; say why.
4. The percentage error the first answer made, and the stiffness of this divider.

**Check yourself:** `quiescentPoint`, `stiffness`.

---

## C.4 Hand calculation: breaking the tempting argument

The argument in [B.2](./b_thermal_drift.md#b2-an-argument-that-does-not-survive-its-own-numbers)
claims a 10 per cent current rise drops $V_{BE}$ from 0.65 V to 0.55 V, which then restores the
current.

1. What collector current does $V_{BE} = 0.55$ V actually give, relative to 0.65 V?
2. Is that consistent with "the current rose 10 per cent"?
3. Identify the step in the argument that is wrong. It is not the 10 per cent.
4. Write the correct version in two sentences, using the word "loop".

**Check yourself:** `currents`.

---

## C.5 Design: bias a stage to a specification

Design a common-emitter stage: 12 V supply, 2 mA quiescent collector current, the collector
sitting at half the supply, and drift below 0.3 per cent per degree.

1. Choose the collector resistor from the quiescent voltage requirement.
2. Choose the emitter resistor from the drift requirement, then check it against the 220 mV rule.
3. Choose the divider for a stiffness of at least 20, in E12 values.
4. State the quiescent point your design actually achieves, including the base-current droop.
5. State the emitter factor, and therefore what this design has given up in gain.

**Check yourself:** `quiescentPoint`, `stiffness`, `degenerationResistor`, `emitter_factor`.

---

## C.6 Code: the bias point

Implement `ael::bias` to the specification in [B.5](./b_thermal_drift.md#b5-what-to-build).

`quiescentPoint` is the only one that needs thought, because it is self-referential: the base
current depends on the collector current which depends on the base voltage which depends on the
base current. Iterate it. Two or three passes converge to well under a per cent.

---

## C.7 Code: temperature in the device

Add `temperature` to `ael::device::bjt::Parameters` and make both the thermal voltage and the
saturation current depend on it.

Then check the model against the number everyone quotes: at 1 mA and fixed collector current, the
base-emitter voltage should fall by about 1.8 mV per degree. **If yours gives exactly 2.0, you
have put the coefficient in by hand rather than letting it emerge**, and the Cross-check below
will not work.

---

## C.8 Cross-check: the drift, four ways

The stage of [A.2](./a_the_quiescent_point.md#a2-divider-bias). How much does its collector
current change per degree?

1. **By the tempting argument.** Follow [B.2](./b_thermal_drift.md#b2-an-argument-that-does-not-survive-its-own-numbers)
   to its conclusion and state what it predicts. You will not be able to.
2. **By hand, linearised.** The base-emitter voltage drifts $-2$ mV per degree at a held base, so
   the emitter voltage rises 2 mV and the current rises by 2 mV over the emitter resistor.
3. **By your solver.** Sweep the temperature from 27 to 37 degrees and measure.
4. **With the emitter resistor removed**, by the solver, for comparison.

### What to expect

**Leg 1 does not produce a number.** Followed honestly it says the current falls by a factor of
47, which contradicts the 10 per cent rise it started from. That is the exercise: an argument can
be qualitatively right, easy to believe, and still not close.

**Leg 2 gives about 0.21 per cent per degree.**

**Leg 3 gives about 0.17 per cent per degree**, roughly 20 to 30 per cent below leg 2.

**That gap is real and has two named causes**, and neither is an error:

* The $-2$ mV per degree is a round figure. The physics gives $-1.77$ mV per degree at 1 mA, and
  the coefficient itself depends on the operating current.
* Leg 2 holds the base voltage fixed. The solver lets it droop further as the current rises,
  because [A.3](./a_the_quiescent_point.md#a3-the-base-current-loads-the-divider)'s base current
  rises with it. That is a second loop the hand calculation does not contain.

**Leg 4 gives about 7 per cent per degree**, forty times worse, and that is the number the whole
lecture exists to prevent.

**The ratio between legs 3 and 4 should be about the emitter factor**, and checking that is the
real content of the Cross-check. If it is not, the suppression is coming from somewhere other than
where the theory says.

**If leg 3 gives exactly leg 2's answer**, the temperature coefficient was put into the model by
hand instead of emerging from $I_S(T)$ and $V_T(T)$. That is worth catching: a model that agrees
with the hand calculation exactly is a model that contains the hand calculation.

---
