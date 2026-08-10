# Appendix D - Solutions

In full, including the plausible wrong answers, of which this lecture has a particularly
tempting one.

---

## D.1 Recall: the operating point

1. The collector current, the collector-emitter voltage and the base-emitter voltage. **It is
   usually two**, because the third is about 0.65 V in every silicon stage and carries no design
   information.
2. $V_{CE} = V_{CC} - I_C(R_C + R_E)$.
3. **Near the middle**, and "the middle" means wherever the headroom above equals the headroom
   below for the signal swing wanted. A stage that never has to swing more than 100 mV can sit
   almost anywhere.
4. **It is nearly saturated.** The negative half of the output would clip almost immediately, and
   the stage's gain would collapse as it entered saturation, so the clipping would be soft and
   asymmetric rather than clean.

---

## D.2 Recall: stiffness

1. Divider current over base current; **ten** is the usual rule.
2. **Roughly ten per cent** in the collector current. The droop is the base current times the
   divider's Thevenin resistance, and at a stiffness of ten that is about a tenth of the base
   voltage's headroom above $V_{BE}$.
3. **Ten times the divider current**, burned continuously, doing nothing but holding a voltage.
4. **A Darlington**, which multiplies the input resistance by a second beta, used in L08; and a
   **MOSFET**, whose gate draws no current at all, used in L09's input stage and in L10's
   inter-stage follower.

---

## D.3 Hand calculation: the quiescent point, twice

1. Ignoring base current: $V_B = 1.709$ V, $V_E = 1.059$ V, $I_C = 1.059$ mA.

<!-- value: 1.709 = divider(10.0, 33e3, 6.8e3) -->

2. $I_B = 1.059/50 = 21.2$ microamps, and the Thevenin resistance is 5.64 kilohm, so the droop is
   about 120 mV.
3. Corrected: $V_B = 1.603$ V, $V_E = 0.953$ V, so $I_E = 0.953$ mA and
   **$I_C = \frac{50}{51}I_E = 0.934$ mA**. The emitter resistor carries the emitter current, and
   at $\beta = 50$ the two per cent between them is worth keeping in a calculation about base
   current.

   **Two iterations are enough** because the correction is a 12 per cent change in a current that
   enters the droop divided by beta; the second pass moves the answer by under two per cent and
   the third by a tenth of one.

<!-- value: 0.934 = 1e3 * loaded_bias_current(10.0, 33e3, 6.8e3, 1e3) -->

4. **The first answer was 13 per cent high.** The stiffness is $251/18.7 = 13.4$.

<!-- value: 13.4 = bias_stiffness(10.0, 33e3, 6.8e3, 1e3) -->

---

## D.4 Hand calculation: breaking the tempting argument

1. $V_{BE} = 0.55$ V is 100 mV below 0.65 V, and 60 mV is a decade, so the current would be
   $e^{-100/26} = 1/47$ of what it was. **It would fall by a factor of 47.**
2. **No.** The argument began by saying the current rose 10 per cent and ends by describing a
   state in which it has fallen to 2 per cent of its original value. Those cannot both describe
   the same circuit.
3. **The wrong step is applying an open-loop change to a closed-loop circuit.** The argument lets
   the current rise the full 10 per cent that it *would* rise with the emitter held fixed, and only
   then asks what the emitter resistor does about it. In the real circuit the emitter resistor is
   acting throughout, so the current never rises 10 per cent and $V_{BE}$ never falls 100 mV. The
   equilibrium is reached at about 2 mV, not 100.
4. **The correct version.** The emitter resistor forms a local feedback loop of gain $R_E/r_e$
   around the transistor. The disturbance, $V_{BE}$ drifting at $-2$ mV per degree, is therefore
   divided by $1 + R_E/r_e$, which here is 37, giving 0.2 per cent per degree instead of 8.

---

## D.5 Design: bias a stage to a specification

|                            | Value                            |
| -------------------------- | -------------------------------- |
| Collector resistor         | 3.3 kilohm                       |
| Emitter resistor           | 390 ohm                          |
| Divider                    | 8.2 kilohm over 1.2 kilohm       |
| Achieved collector current | 2.15 mA, 7 per cent above target |
| Achieved stiffness         | 29.7                             |
| Achieved drift             | 0.24 per cent per degree         |
| Emitter factor             | 31                               |

**1. The collector resistor.** $6\ \text{V}/2\ \text{mA} = 3$ kilohm, so 3.3 kilohm from E12.

**2. The emitter resistor, and the conflict.** The drift requirement is the binding one:

$$\frac{2\ \text{mV}/R_E}{2\ \text{mA}} < 0.003 \implies R_E > 333\ \Omega$$

so 390 ohm. **The 220 mV rule would have given 110 ohm**, three and a half times smaller. The two
requirements disagree, the drift specification wins, and the cost is that the emitter factor is 31
rather than 10, so this stage has given up a factor of three more gain than the rule of thumb
would have.

**That conflict is the exercise.** The 220 mV rule is a default, not a law; it is what to use when
nothing else constrains the choice. A stated drift requirement is something else.

**3 and 4. The divider.** With $V_E = 0.78$ V, the base wants 1.43 V. A stiffness of 20 needs the
divider to carry 800 microamps, so about 15 kilohm in total. Searching E12 pairs for the closest
achievable current at stiffness 20 or better gives **8.2 kilohm over 1.2 kilohm**: 1.53 V
unloaded, drooping to about 1.49 V of base voltage under 42 microamps of base current, and
2.15 mA of collector current.

The current is 7 per cent above target, which is E12 granularity rather than a design error. If
that mattered, the fix is a trimmable emitter resistor, not a stiffer divider.

**5. The emitter factor is 31**, so this stage's gain is thirty-one times lower than the same
stage with no emitter resistor. Stability bought with gain, one for one, exactly as
[B.3](./b_thermal_drift.md#b3-what-actually-happens) said.

---

## D.6 Code: the bias point

Unpublished; the suite is the answer.

The hint: **iterate, and check that it converged.** A first pass with the base current from the
target current, a second with the base current from the first pass's answer, and a third to
confirm nothing moved. If your implementation takes more than about four passes to settle to a
part in a thousand, the iteration is probably being applied to the wrong variable; iterate on the
collector current rather than on the base voltage.

---

## D.7 Code: temperature in the device

Unpublished, with the check that matters repeated: **the coefficient must emerge, not be inserted.**

If `Parameters` contains something like `vbeTempco = -2.0e-3` and the model subtracts it, then the
model contains the answer to the Cross-check and the Cross-check proves nothing. The coefficient
should fall out of $I_S(T)$ and $V_T(T)$, and when it does it comes to $-1.77$ mV per degree at
1 mA rather than exactly $-2$, and it changes with current. Both of those are how you know it is
real.

---

## D.8 Cross-check: the drift, four ways

| Leg                                   | Result                   |
| ------------------------------------- | ------------------------ |
| 1. The tempting argument              | No consistent answer     |
| 2. By hand, linearised, $-2$ mV/K     | 0.21 per cent per degree |
| 3. By the solver, full physics        | 0.17 per cent per degree |
| 4. By the solver, no emitter resistor | 7.1 per cent per degree  |

**Leg 1 cannot be completed**, and that is its result. Followed to the end it predicts a current
that has fallen by a factor of 47 from a premise that it rose by 10 per cent. It is qualitatively
right, it is easy to believe, and it is not close.

**Legs 2 and 3 differ by about 20 per cent**, for two stated reasons, neither of which is an
error, and together they close the gap exactly:

* The $-2$ mV per degree is a round number. The physics gives $-1.77$ mV per degree at 1 mA, which
  alone accounts for about 12 per cent of the gap.
* Leg 2 holds the base voltage fixed. **The solver does not.** As the collector current rises with
  temperature the base current rises with it, and the extra drop across the divider's 5.64 kilohm
  pulls the base down. That is a second feedback loop, acting on top of the emitter resistor's,
  and it is worth a further factor of $1 + R_{th}/(\beta + 1)(R_E + r_e) = 1.11$.

Put the two together: $0.21 \times 0.885 / 1.11 = 0.17$, which is leg 3. Nothing is left over.

**A reader who instead argues that the solver's lower current raises the percentage drift has the
sign backwards.** Leg 2's 0.21 per cent was already computed on 0.93 mA, and if current were the
mechanism it would put leg 3 *above* leg 2 rather than below it.

**Leg 4 is the point of the whole lecture.** Forty times worse, and 7 per cent per degree means a
factor of two every ten degrees. A stage biased at 1 mA on a bench is at 2 mA in a warm enclosure
and at 4 mA in a hot one, and somewhere in there it stops being an amplifier.

**The check worth making is the ratio.** Legs 3 and 4 should differ by about the emitter factor,
which for a 1 kilohm emitter resistor at this current is 37. Forty-two against thirty-seven is
agreement, given that one is a linearised factor and the other is a measured ratio over ten
degrees of a slightly nonlinear relationship.

**If leg 3 agrees with leg 2 exactly**, the temperature coefficient was inserted by hand. A model
that reproduces the hand calculation to the digit is a model that contains the hand calculation,
and it cannot be used to check it. That is the one failure mode this Cross-check is designed to
catch, and it is easy to produce by accident.

---
