# Appendix E - Solutions

In full, including the plausible wrong answers. The Cross-check here retires the constant-drop
model, and the size of the failure is a factor of sixty-one.

---

## E.1 Recall: the stage that does nothing

1. $G = R_E/(r_e + R_E)$; $Z_{in} = h_{FE}(r_e + R_E)$; $Z_{out} = r_e + R_{source}/h_{FE}$.
2. Into $r_e$. The stage is a divider between $r_e$ and the load, and $r_e$ is $V_T/I_C$, so
   **the only lever is the quiescent current.** Not the load, which is given, and not the device.
3. **Both resistances.** The gain does not. That is worth remembering as a pair: the number a
   follower is specified by does not depend on beta, and the two numbers it is *for* both do.
4. **Impedance transformation**, which is showing a driving stage something much larger than the
   real load, and **current gain**, which is the same fact used at the other end, where the point
   is that the output can supply current the driving stage could not.

---

## E.2 Recall: the three classes

1. **Class A** conducts for the whole cycle. **Class B** uses two devices, each conducting for
   half. **Class AB** uses two devices with both conducting near the zero crossing and one taking
   over at larger signals.
2. Class A: **25 per cent** with a resistive load, 50 with a current-source load. Class B:
   **78.5 per cent**, which is $\pi/4$.
3. The flat band in the transfer curve where neither device conducts, **two base-emitter drops
   wide**, about 1.3 V. It is objectionable because it sits **at the origin**, where a music
   signal spends most of its time, so it is worst on quiet passages and vanishes at full output.
   Every other distortion mechanism does the opposite.
4. **Idle dissipation**, and with it a little efficiency. Both devices conduct at idle, so the
   stage burns $V_{supply} \times I_q$ doing nothing. At 120 mA on $\pm 32$ V that is 7.7 W, which
   is a heatsink rather than an objection.

---

## E.3 Hand calculation: a follower at three currents

|        | Gain into 8 ohm | $Z_{out}$ from 1 kilohm | $Z_{in}$ |
| ------ | --------------- | ----------------------- | -------- |
| 1 mA   | 0.235           | 46.0 ohm                | 1700 ohm |
| 10 mA  | 0.755           | 22.6 ohm                | 530 ohm  |
| 120 mA | 0.974           | 20.2 ohm                | 411 ohm  |

<!-- value: 0.974 = follower_gain(0.12, 8.0) -->

**The nearly constant column is $Z_{out}$**, and the reason is that it is
$r_e + R_{source}/h_{FE}$, and at these currents the second term is 20 ohm and dominates. **The
output resistance of a follower driven from a kilohm is a property of the kilohm, not of the
transistor**, once the current is above a few milliamps.

**Which is the more useful statement of what a follower does.** It does not have a low output
resistance; it has *the driving resistance, divided by beta*. Reading the table the other way,
$Z_{in}$ falls by a factor of four across the same range, and that is the number D.4 turns on.

---

## E.4 Hand calculation: what the loudspeaker costs

|              | What the stage sees | Gain  | Kept   |
| ------------ | ------------------- | ----- | ------ |
| 8 ohm direct | 8 ohm               | 0.031 | 0.08 % |
| One follower | 411 ohm             | 1.53  | 4.0 %  |
| A Darlington | 21.1 kilohm         | 26.2  | 68.1 % |

<!-- value: 26.2 = abs(loaded_gain(ce_gain(10e3, 1e-3, 234.0), ce_output_resistance(10e3, 1e-3, 234.0), darlington_input_resistance(0.12, 8.0))) -->

**With the beta spread:**

| $h_{FE}$ | $Z_{in}$    | Gain | Kept |
| -------- | ----------- | ---- | ---- |
| 20       | 3.37 kilohm | 9.79 | 25 % |
| 50       | 21.1 kilohm | 26.2 | 68 % |
| 200      | 337 kilohm  | 37.4 | 97 % |

**What the spread means.** The gain of this amplifier varies by a factor of **3.8** between two
devices of the same part number, and nothing in the design can narrow it, because the quantity is
$h_{FE}^2$ and $h_{FE}$ is what it is.

**So the design is not finished.** It has to be wrapped in a feedback loop whose loop gain is
large enough that a factor of four in the forward path becomes a fraction of a per cent at the
output. That is [L04](../../L04/README.md)'s arithmetic, and it is what L10 builds. **An
output stage is not a circuit that works on its own; it is a circuit that works inside a loop.**

**5. Why the Darlington's emitter resistance is $2r_e$, with no $h_{FE}$ in the answer.**

Call the output device $Q_2$ and the driver $Q_1$, and let the load current be $I$. The two
devices do not run at the same current: $Q_2$ carries $I$, and its base current, which is $Q_1$'s
emitter current, is $I/h_{FE}$. So their intrinsic emitter resistances are

$$r_{e2} = \frac{V_T}{I}, \qquad r_{e1} = \frac{V_T}{I/h_{FE}} = \frac{h_{FE}V_T}{I}$$

and $r_{e1}$ is $h_{FE}$ times the larger of the two. But it is not seen at the output directly:
it sits in $Q_2$'s base, and a resistance in a follower's base appears at its emitter divided by
that follower's current gain, which is the same $h_{FE}$:

$$\frac{r_{e1}}{h_{FE}} = \frac{V_T}{I}$$

**The two $h_{FE}$ cancel.** One multiplied because the driver runs at a smaller current, and one
divided because it is looked at through the output device, and they are the same number. What is
left adds in series with $r_{e2}$:

$$r_{e,\text{Darlington}} = \frac{V_T}{I} + \frac{V_T}{I} = \frac{2V_T}{I} = 2r_e$$

**Which is why the pair costs exactly one extra $r_e$ and not a beta-dependent amount**, and it is
the reason `darlingtonEmitterResistance` takes only a current. Every other Darlington result in
this lecture does depend on beta, most of them on beta squared; this one is the exception, and it
is the exception for a reason worth being able to state.

---

## E.5 Design: a class-AB output stage

|                                 | Value                           |
| ------------------------------- | ------------------------------- |
| Idle current                    | 100 mA                          |
| $r_e$ at idle                   | 0.260 ohm                       |
| $R_E$ by the 26 mV rule         | 0.260 ohm, so **0.27** from E12 |
| Emitter factor                  | 2.04                            |
| $R_E$ as a fraction of the load | 3.4 per cent                    |
| Bias voltage                    | **1.611 V**                     |

<!-- value: 1.611 = class_ab_bias(0.1, nearest_e12(quiescent_emitter_resistor(0.1))) -->

The bias comes from $2(V_{BE}(0.1\ \text{A}) + 0.1 \times 0.27)$, with $V_{BE} = V_T\ln(I_C/I_S)$
giving 0.778 V at 100 mA. **The constant-drop answer is 1.354 V**, and D.8 is about what that
costs.

**Maximum sine power**, ignoring everything: $V_{rail}^2/2R = 625/16 = 39.1$ W.

**What to specify it at: about 33 W.** The difference is real and every part of it is nameable.
Each output device needs a volt or two of collector-emitter voltage to stay out of saturation; the
emitter resistor drops 0.27 V per amp; the supply sags under load because it is a transformer and
a capacitor rather than an ideal source. Two volts lost at each rail turns 39.1 W into 33.1 W, and
a datasheet that claims 39 W is a datasheet quoting an equation rather than a measurement.

---

## E.6 Design: thermal

1. **3.77 per cent per degree.**

   <!-- value: 3.77 = 100 * class_ab_drift(0.1, nearest_e12(quiescent_emitter_resistor(0.1))) -->

2. Compounding over 30 degrees, a factor of **3.0**: the idle current reaches about **300 mA**,
   which triples the idle dissipation, which raises the temperature further. This is a runaway,
   not a drift.
3. Without the emitter resistors, **7.69 per cent per degree**, a factor of **9** over 30 degrees.
   So the resistors bought **a factor of two**, which is the emitter factor of 2 that the 26 mV
   rule chose, and which is exactly the same accounting as L06's.

   **They did not buy stability.** A factor of three is still destruction. The resistors buy time
   and margin; they are not the mechanism that makes the stage safe.

4. **On the same heatsink as the output devices, in good thermal contact.** It is not setting a
   voltage; it is tracking the output devices' $V_{BE}$ so that the bias falls by the same 4 mV
   per degree that the outputs stop needing.

---

## E.7 Code: the follower and the output stage

Unpublished; the suite is the answer.

The two hints worth repeating. **`idleCurrent` has no closed form**, so bisect in the logarithm
and check it against `biasVoltage` by round-tripping, which is one of the shipped tests. And
**`loadedGain` belongs in the library rather than at the call site**, because L10 calls it eleven
times and a gain budget assembled from inline arithmetic is a gain budget nobody can check.

---

## E.8 Cross-check: the bias voltage a class-AB stage actually needs

| Leg                                    | Bias voltage |
| -------------------------------------- | ------------ |
| 1. Constant drop, $2(0.650 + 0.026)$   | 1.353 V      |
| 2. The exponential, $2(0.783 + 0.026)$ | **1.619 V**  |
| 3. The solver, one half by symmetry    | 1.604 V      |

<!-- value: 1.619 = class_ab_bias(0.12, nearest_e12(quiescent_emitter_resistor(0.12))) -->

**Legs 2 and 3 differ by 14 mV, which is 0.9 per cent, and both causes are nameable**: the closed
form takes $V_T$ as 26 mV where the device computes $kT/q = 25.87$ mV at 300 K, and the device has
an Early effect the closed form does not, so it needs slightly less drive with its collector 15 V
up. Both push the same way.

**And that 0.9 per cent in the bias is 31 per cent in the current it produces.** The closed form
says the constant-drop bias leaves 1.96 mA and the solver says 2.56 mA. **This lecture's whole
point, appearing one order of magnitude down and inside the Cross-check itself.** Neither leg is
wrong; they are the same physics with $V_T$ rounded differently, and the rounding is amplified by
the same exponential the exercise is about.

**And backwards: 1.353 V applied to the real stage gives an idle current of 1.96 mA by the closed
form and 2.56 mA by the solver.**

<!-- value: 1.96 = class_ab_idle_current(2.0 * (VBE_ON + 0.12 * nearest_e12(quiescent_emitter_resistor(0.12))), nearest_e12(quiescent_emitter_resistor(0.12))) * 1e3 -->

A factor of **61** or **47** below the 120 mA the stage was designed for, depending on which leg
you ask, and **the disagreement between those two is not the interesting part**. Either way the
dead band is open, the stage is in class B, and the amplifier distorts every quiet passage.

### Why the same model was worth 1 per cent before and a factor of 61 here

**Because of what it is being used to compute, not because of the model.**

Every earlier use in this course computed a **current from a voltage across a resistor**. In
[L06](../../L06/appendix/a_the_quiescent_point.md#a2-divider-bias): take the base voltage, subtract
$V_{BE}$, divide by $R_E$. The subtraction gives about a volt, so a 133 mV error in $V_{BE}$ is a
12 per cent error in the answer, and it enters **linearly**.

Here the calculation runs the other way. The bias voltage lands almost entirely across the two
**junctions**, because the two 0.22 ohm resistors drop 26 mV each and the junctions drop 783.
Inverting that means going backwards through an exponential whose scale is 26 mV, so an error of
133 mV per device is a factor of

$$e^{133/26} = e^{5.1} \approx 166$$

**and the emitter resistors soften it to 61.** They carry 26 of those 133 mV at 120 mA and none at
2 mA, so the junction sees 107 mV rather than 133. That is local feedback acting where it is
needed and nowhere else, and it is the same 26 mV rule doing a third job. **The error enters
exponentially, and it is the same 133 mV that was worth 12 per cent one lecture ago.**

**The general statement**, which is the thing to carry out of this lecture: *a model's accuracy is
a property of the calculation it appears in.* The constant-drop model is fine wherever $V_{BE}$ is
subtracted from something larger and useless wherever $V_{BE}$ is inverted. Both uses look like
"assume 0.65 V" on the page.

### What it explains about the circuit

Two ordinary signal diodes running at a few milliamps produce about 1.40 V, which gives an idle
current of **4.8 mA** rather than 120. So the two-diode bias generator drawn in every textbook
figure, does not work as drawn unless the
diodes carry a current comparable with the output devices'.

**That is why a real class-AB stage uses an adjustable $V_{BE}$ multiplier.** Not for elegance,
and not only for thermal tracking, but because the bias needed is about two and a half diode
drops rather than two, and the exact figure depends on the idle current, the emitter resistors,
the devices and the temperature. It has to be set, not assumed.

---
