# Appendix D - Solutions

In full, including the plausible wrong answers. The Cross-check here overturns the obvious
answer, and the correction is a factor of ten.

---

## D.1 Recall: what linearising discards

1. $r_e = V_T/I_C$, 26 ohm at 1 mA. **It is not a resistor.** It is the slope of the device's
   exponential at the operating point, and it exists only because the operating point does.
2. **A few millivolts.** The exponential's scale is $V_T$, 26 mV, so an excursion of 2.6 mV is
   linear to about 5 per cent and an excursion of 26 mV is not linear at all.
3. Clipping, distortion, and any signal large enough to move the operating point. Also slew rate,
   turn-off, and everything about large-signal behaviour.
4. **It ceases to exist.** With no collector current there is no operating point and no slope. It
   does not become large; the model simply stops applying.

---

## D.2 Recall: the four rules

1. DC sources become grounds; coupling and bypass capacitors become shorts; the bias network
   disappears where it is swamped; the transistor becomes $r_e$ plus a current source.
2. **Because it does not move.** A small-signal model describes changes, and a rail that holds a
   constant voltage has no change on it, which is the same thing as ground as far as signals are
   concerned.
3. The divider's parallel combination is 5.64 kilohm against the base's 13 kilohm, so
   **the divider dominates**, and the stage's input resistance is about 3.9 kilohm. The
   transistor is the larger of the two and therefore the less important, which surprises people.
4. It recovers the gain and **the bandwidth**, and it throws away **the distortion reduction and
   the signal-frequency stability**, because both of those were feedback and the capacitor removes
   the feedback at exactly the frequencies the signal occupies. The DC stability survives, which
   is the whole reason the arrangement is used.

---

## D.3 Hand calculation: the three results

|                  | 1 mA        | 10 mA       |
| ---------------- | ----------- | ----------- |
| $r_e$            | 26.0 ohm    | 2.6 ohm     |
| Emitter factor   | 10.0        | 91.0        |
| Gain, unbypassed | 38.5        | 42.3        |
| Gain, bypassed   | 385         | 3846        |
| $Z_{in(base)}$   | 13.0 kilohm | 11.8 kilohm |

<!-- value: 38.5 = abs(ce_gain(10e3, 1e-3, 234.0)) -->

**What changed and what did not.** $r_e$ fell by ten, and the emitter factor rose by nine. The
**bypassed** gain rose by ten, because it is $R_C/r_e$. The **unbypassed** gain barely moved, from
38.5 to 42.3, because it is $R_C/(r_e + R_E)$ and $R_E$ dominates that sum at both currents.

**That insensitivity is the reason degeneration is used at all**, and it is worth noticing here
rather than being told: a stage whose gain is set by two resistors does not care what current it
is running at, and therefore does not care about temperature, beta, or the device.

---

## D.4 Hand calculation: two nodes, two answers

|                            | With $R_E = 234$ | With no $R_E$ |
| -------------------------- | ---------------- | ------------- |
| Looking into the collector | 863 kilohm       | 100 kilohm    |
| Stage output resistance    | 9.89 kilohm      | 9.09 kilohm   |

<!-- value: 9.89 = ce_output_resistance(10e3, 1e-3, 234.0) / 1e3 -->

**What degeneration did to each, in one sentence apiece.**

To the resistance looking into the collector: **multiplied it by 8.6**, which is the emitter
factor of 10 reduced slightly because $r_\pi$ shunts part of the degeneration.

To the stage's output resistance: **raised it by 9 per cent**, because the 10 kilohm collector
resistor was already far smaller than either 100 kilohm or 863, and a parallel combination is
dominated by its smaller part.

---

## D.5 Design: a stage with a stated gain and bandwidth

**The design, and it does not meet the requirement.**

|                           | Value                                                |
| ------------------------- | ---------------------------------------------------- |
| Collector current         | 1 mA                                                 |
| Collector resistor        | 5.6 kilohm, putting the collector at half the supply |
| Emitter resistor          | 114 ohm exactly, 120 from E12                        |
| Gain                      | 40 exactly, 38.4 as built                            |
| Miller capacitance        | 157 pF                                               |
| Input corner from 600 ohm | 1.68 MHz                                             |

The gain requirement fixes $R_C/(r_e + R_E) = 40$; with 5.6 kilohm and $r_e$ of 26 ohm that needs
$R_E = 114$ ohm, and the nearest E12 value is 120, which lands the gain at 38.4 rather than 40.
**Say which of the two numbers you are quoting.** A design whose gain is stated as 40 and built
from E12 parts has a gain of 38.4, and the 4 per cent is not an error, it is the resistor series.

**The corner comes to 1.68 MHz against a requirement of 3.** The Miller capacitance is
$4\ \text{pF} \times 39.4 = 157$ pF, and 600 ohm into 157 pF is 1.68 MHz.

**The two options, with their costs.**

* **Reduce the gain.** The Miller capacitance is very nearly proportional to the gain, so halving
  it to 19 moves the corner to 3.3 MHz, which just clears. The cost is half the gain, and if the
  gain was a requirement this option does not exist.
* **Use a cascode.** The lower transistor's collector no longer swings, so there is no
  multiplication at all and the input sees 4 pF, giving a corner of **66 MHz**, twenty times more
  than required. The cost is one more transistor, one more bias voltage, and about 0.7 V of
  output swing lost to the extra device.

**The cascode is the right answer**, and the size of the win is why: it does not scrape past the
requirement, it removes the constraint. That is the usual experience with a cascode and the reason
it appears in almost every wideband stage.

---

## D.6 Code: the small-signal model

Unpublished; the suite is the answer.

The hint worth repeating: **`cascodeOutputResistance` calls `resistanceIntoCollector`.** If you
write it as a separate formula, the two will agree numerically and the code will have stopped
demonstrating the lecture's claim. One of the shipped tests checks that the two agree to machine
precision, which they can only do if one calls the other.

---

## D.7 Code: the Early effect

Unpublished. The check: solve a stage at two collector voltages a volt apart and confirm the
collector current moves by about 1 per cent, which is $1/V_A$ per volt with $V_A = 100$.

**If it does not move at all**, the Early term is missing, $r_o$ is infinite, and the Cross-check
will return exactly $R_C$ and prove nothing.

---

## D.8 Cross-check: what the emitter factor multiplies

| Leg                                 | Output resistance |
| ----------------------------------- | ----------------- |
| 1. The tempting $R_C \cdot EF$      | 100 kilohm        |
| 2. Corrected closed form            | 9.89 kilohm       |
| 3. The solver                       | about 9.9 kilohm  |
| 4. Same, with a current-mirror load | 89.6 kilohm       |

<!-- value: 89.6 = ce_output_resistance(early_resistance(1e-3), 1e-3, 234.0) / 1e3 -->

**Leg 1 is wrong by a factor of ten, and it can be refuted without arithmetic.** The output
resistance is $R_C$ in parallel with whatever the transistor presents. A parallel combination is
smaller than either part. So the answer cannot exceed 10 kilohm, and 100 kilohm does. Any result
of that form is wrong before the numbers are checked.

**What leg 1 got right.** The factor of ten is real and the emitter factor is the right number
for it. It belongs to the resistance **looking into the collector**, which goes from 100 kilohm to
863. A correct factor, attached to the wrong node.

**What that costs, and what it explains.** With a 10 kilohm collector resistor, degeneration takes
the stage's output resistance from 9.09 kilohm to 9.89, which is 9 per cent, in exchange for a
factor of ten in gain. On leg 1's account that trade looks excellent; on the corrected account
it looks absurd, and it is absurd, **with a resistive load**.

With a current mirror the same degeneration takes 50 kilohm to 89.6, and now it is worth having.

**So the correction does not throw the emitter factor away; it is the missing argument for
[B.4](./b_the_emitter_factor.md#b4-which-is-exactly-why-a-current-mirror-load-exists) and for the
whole of [L09](../../L09/README.md).** Mirror loads and cascodes otherwise arrive without a stated
reason. The reason is this: with a resistive load you are paying for a boost you cannot collect,
and a mirror is how you collect it.

**Diagnosing leg 3:**

* **Exactly 10 kilohm** means the Early effect is missing and the transistor is a perfect current
  source. Nothing else can produce exactly $R_C$.
* **100 kilohm** means the collector resistor is not in the netlist, so you have measured leg 3 of
  the mirror-loaded case by accident.
* **A few per cent away from leg 2** is expected and not a fault. Leg 2's closed form uses
  $R_E \parallel r_\pi$ with $\beta = 50$; the solver uses the full device, whose incremental beta
  at the operating point is not exactly 50.

---
