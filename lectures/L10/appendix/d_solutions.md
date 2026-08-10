# Appendix D - Solutions

In full. The last one is the capstone, and its answer is a table of discrepancies rather than a
number.

---

## D.1 Recall: what each stage is for

1. **Stage 1**, a mirror-loaded differential pair: gain, and every input specification.
   **Stage 2**, a Darlington follower: nothing, except not loading stage 1. **Stage 3**, a
   common-emitter stage with a current-source load: most of the open-loop gain, and the dominant
   pole. **Stage 4**, a class-AB Darlington output: current, and a low output resistance.
2. **Stages 2 and 4.** They are there to stop one stage loading the next, and between them they
   are worth 62 dB of loop gain, which is more than either gain stage produces.
3. **Stage 1**, and **no**. Feedback divides down what happens after the input, not what happens
   at it. An offset at the input is indistinguishable from signal by construction.
4. **Stage 3's collector**, because it is the highest-impedance node in the amplifier and a pole
   is cheapest where the resistance is largest. It is also where the Miller effect multiplies the
   capacitor by 1923, so 30 pF behaves like 58 nF.

---

## D.2 Recall: the loop

1. $A_{cl} = A/(1 + A\beta_f)$.
2. $A\beta_f = 986000/20 = $ **49,300**.
3. $0.22/(1 + 49300) =$ **4.4 microhm**. It is not a real number because the resistance of the
   wire from the amplifier to the loudspeaker is four orders of magnitude larger, as is the
   resistance of the emitter resistors it is measured through. What the calculation actually says
   is "the amplifier is not the limit", and that is all it says.
4. **Nine parts in a hundred thousand**, from 19.998096 to 19.999862. That insensitivity is what
   feedback exists to give: it converts a forward path that cannot be specified into a closed loop
   that is set by two resistors.

---

## D.3 Hand calculation: the budget

|                          | Value                    |
| ------------------------ | ------------------------ |
| Stage 1 unloaded         | 1923                     |
| Stage 3 unloaded         | 1923                     |
| Stage 2 input resistance | 3.38 megohm              |
| Stage 3 input resistance | 1.30 kilohm              |
| Stage 4 input resistance | 21.1 kilohm              |
| Stage 1 loaded           | 1895                     |
| Stage 2 gain             | 0.962                    |
| Stage 3 loaded           | 570                      |
| Stage 4 gain             | 0.949                    |
| **Open loop**            | **986,000, or 119.9 dB** |

<!-- value: 986000 = round(opamp_open_loop_gain(), -3) -->

**The product of the unloaded gains is 3.70 million, which is 131.4 dB, so loading costs 11.5 dB.**

**And 10.6 of those 11.5 are one row**: stage 3 driving stage 4. Everything else together is under
a decibel. That concentration matters more than the total, because it says where to spend effort:
improving stage 1's loading would recover 0.1 dB.

---

## D.4 Hand calculation: the stages that do nothing

1. **Stage 1 would give 48.7** instead of 1923, because 1.3 kilohm against 50 kilohm keeps
   2.5 per cent. The open-loop gain falls to **26,400, or 88.4 dB**.
2. **Stage 3 would give 15.7** instead of 570, because a single follower presents 411 ohm against
   50 kilohm and keeps 0.8 per cent. The open-loop gain falls to **27,800, or 88.9 dB**.
3. **The buffer is worth 31.5 dB and the output Darlington 31.0 dB.**

<!-- value: 31.5 = opamp_buffer_worth() -->
<!-- value: 31.0 = opamp_output_worth() -->

4. The buffer costs 0.34 dB of signal; the output Darlington costs 0.46 dB against the 0.23 dB a
   single follower would cost, so 0.23 dB.

   **The exchange rate is about a hundred to one in decibels.** A tenth of a decibel of signal
   buys thirty decibels of loop. That is not a close decision, and it is why the answer to almost
   every loading problem in analog design is another follower.

---

## D.5 Design: the input offset that matters

1. $15/986000 =$ **15.2 microvolts**.

   <!-- value: 15.2 = 15.0 / opamp_open_loop_gain() * 1e6 -->

2. **Sixty-six times larger.** Two ordinary transistors match to about 1 mV, and an integrated
   pair to perhaps 0.5 mV; neither is within two orders of magnitude of 15 microvolts.
3. **The amplifier has no open-loop operating point**, so an open-loop DC solve has no sensible
   answer to converge on. A solver that reports the output at a rail is correct. This is a fact
   about amplifiers, not about solvers, and it is why the stage gains must be measured stage by
   stage.
4. **20 mV out**, which is the input offset times the closed-loop gain. It is reduced by reducing
   the *input* offset: matched devices, a trimmed pair, or MOSFET inputs to remove the base
   current contribution of
   [L09 B.6](../../L09/appendix/b_rejection_and_the_mirror.md#b6-offset-matching-and-why-modern-input-stages-are-mosfet).
   **Not by more loop gain.** More loop gain makes the closed-loop gain more accurate and does
   nothing at all to the offset.

---

## D.6 Design: the gain you cannot buy

1.

| Tail or collector current | Load       | Gain |
| ------------------------- | ---------- | ---- |
| 0.2 mA                    | 500 kilohm | 1923 |
| 2 mA                      | 50 kilohm  | 1923 |
| 20 mA                     | 5 kilohm   | 1923 |

   **Identical, over two decades of current**, and the same for stage 3.

2. The load is $r_o \parallel r_o = V_A/2I$ and the transconductance is $I/V_T$, so

   $$A = \frac{V_A}{2I}\cdot\frac{I}{V_T} = \frac{V_A}{2V_T} = \frac{100}{0.052} = 1923$$

   <!-- value: 1923 = intrinsic_gain() -->

   **The current cancels exactly.** The load falls as fast as the transconductance rises.

   **This is the opposite of every other pattern in the course.** In L08 a follower's every
   shortcoming was fixed by more current. Here more current buys nothing, and that is why every
   gain stage in every operational amplifier lands within a few decibels of the same figure: it is
   a property of the *process*, through $V_A$, and not of the design.

3. **Cascode the loads.** That multiplies $r_o$ by $\beta$ and the gain with it:
   **96,900, or 99.7 dB from one stage.**

   <!-- value: 99.7 = decibels(cascoded_intrinsic_gain(1e-3)) -->

   Which is why an integrated operational amplifier is often two cascoded stages rather than four
   plain ones, and it is what
   [L07 B.5](../../L07/appendix/b_the_emitter_factor.md#b5-miller-and-the-cascode) was for.

4. **67 V per microsecond** at 2 mA into 30 pF. **10 V per microsecond needs 0.3 mA**, and by part
   2 that costs **nothing in gain at all**.

   **So slew rate and gain are independent**, which is not obvious and is worth carrying away: the
   tail current is a free parameter for slew rate, bandwidth and noise, and it is not a lever on
   gain.

---

## D.7 Code: PNP support, and the report

Unpublished; the suite is the answer.

The hint worth repeating: **a PNP is your NPN evaluated at $(-v_{BE}, -v_{BC})$ with the currents
negated.** If your PNP stamp is longer than fifteen lines, it is a second device model and it will
disagree with the first one somewhere.

---

## D.8 Cross-check: the capstone

A representative run, at $\beta = 50$:

| Stage           | Predicted   | Measured          | Difference |
| --------------- | ----------- | ----------------- | ---------- |
| 1, input pair   | 1895        | about 1840        | -3 %       |
| 2, buffer       | 0.962       | 0.961             | -0.1 %     |
| 3, voltage gain | 570         | about 550         | -4 %       |
| 4, output       | 0.949       | 0.941             | -0.9 %     |
| **Open loop**   | **986,000** | **about 915,000** | **-7 %**   |

**Every row is a few per cent low, in the same direction, and that is the tell.** Three causes,
all of them already named in this course:

* **The thermal voltage.** The closed forms use 26 mV; the device computes $kT/q = 25.87$ mV at
  300 K. That makes $r_e$ 0.5 per cent smaller than predicted, which raises the gain.
* **The Early effect on the load.** The closed forms take $r_o = V_A/I_C$; differentiating the
  model gives $(V_A + V_{CE})/I_C$, which is larger. That raises the gain too.
* **The loading, at the measured operating point rather than the nominal one.** Each stage's
  actual bias current differs a little from the design value, and $r_e$ and the input resistances
  move with it.

**The first two push the measurement up and the third pushes it down**, and the third wins. A
reader who can attribute each row has understood the ten lectures.

**A reader whose rows agree to six figures has made a mistake**, and it is a specific one: the
"measurement" is calling the same closed form again rather than solving a netlist.

### Part 4: the open-loop solve

**It does not converge on a useful answer, and that is correct.** The output sits at a rail, or
the iteration does not settle. With 986,000 of gain and 15 V of rail, 15 microvolts of input
offset saturates the output, and there is no such thing as a pair matched to 15 microvolts.

**Do not tune the solver until it produces a mid-rail answer.** There is not one to find. This is
the single most useful thing the capstone demonstrates, because it cannot be seen from any
hand analysis: the amplifier that has been designed stage by stage for ten lectures **does not
work as a DC circuit at all** until it is inside a loop.

### Part 5: the closed loop

**Converges immediately, and gives 20.** The same netlist, one divider added, and a circuit with
no operating point acquires one.

### And the last exercise

| $\beta$ | Open loop | Closed loop |
| ------- | --------- | ----------- |
| 20      | 106.4 dB  | 19.998096   |
| 50      | 119.9 dB  | 19.999594   |
| 200     | 129.2 dB  | 19.999862   |

<!-- value: 129.2 = decibels(opamp_budget()["stage1"] * opamp_budget()["buffer"] * abs(loaded_gain(opamp_budget()["stage2_unloaded"], opamp_budget()["stage2_load"], darlington_input_resistance(0.12, 8.0, 200.0))) * opamp_budget()["output"]) -->

**The open-loop gain moves by a factor of 14. The closed-loop gain moves by 0.009 per cent.**

**That is what it is worth**, and it is the sentence the whole course exists to earn. Ten lectures
of models, each of which is approximate, several of which are wrong by tens of per cent, and one
of which was wrong by a factor of sixty until the Cross-check found it. Wrap the result in a loop
with a gain of fifty thousand and the answer is set by two resistors, to five figures.

**Which is not a reason to stop caring about the models.** The loop gain is a product of every
stage gain in this appendix, and if the budget had come out at 88 dB rather than 120 the error
would be 0.06 per cent rather than 0.002, the output resistance would be thirty times higher, and
the distortion thirty times worse. **Feedback divides your errors by the loop gain, and the loop
gain is the thing you spent ten lectures learning to compute.**

---
