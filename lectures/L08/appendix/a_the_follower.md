# Appendix A - The follower, and the load it exists to survive
A stage with a voltage gain of one, and the arithmetic that makes it the most-used circuit in the
course.

---

## A.1 The same model, at the other terminal
A **follower** is [L07's model](../../L07/appendix/a_the_small_signal_model.md) with the output
taken at the emitter instead of the collector, and no collector resistor.

![An emitter follower: an NPN transistor with its collector tied to the supply rail, its base driven from the input, and an emitter resistor to ground with the output taken at the emitter, annotated at both ends with what the stage does to impedance.](./images/emitter_follower.png)

1. **The output is at the emitter**, not the collector.
2. **There is no collector resistor**, because a follower does not turn current into voltage.
3. In high-voltage work the collector is sometimes grounded rather than tied to the rail, which
   protects the device and changes nothing below.

---

## A.2 Gain, and where the missing part went
The input drives $r_e$ and $R_E$ in series and the output is taken across $R_E$ alone: a divider.

$$G = \frac{R_E}{r_e + R_E}$$

**Always less than one, and the shortfall is $r_e/(r_e + R_E)$.** At 1 mA into 10 kilohm, 0.997.
At 120 mA into an 8 ohm loudspeaker, **0.974**.

<!-- value: 0.974 = follower_gain(0.12, 8.0) -->

The ratio $r_e/R_E$ is the only thing a follower's gain depends on, and there is one lever on it,
$r_e = V_T/I_C$. **The gain is a question about current and nothing else: a follower that is not
good enough is a follower that is not biased hard enough.**

![Follower gain against quiescent current on a logarithmic axis, for an 8 ohm load and a 1 kilohm load, the 8 ohm curve climbing from about 0.03 at 100 microamps through 0.24 at 1 milliamp towards one, with the 120 milliamp design point marked.](./images/follower_into_load.png)

**Read the 8 ohm curve at 1 mA: the gain is 0.24.** Not 0.99, not 0.9, a quarter: $r_e$ is 26 ohm
and the load is 8, so three quarters of the signal drops inside the transistor. That is why
[Appendix B](./b_the_output_stage.md) exists, and why an output stage idles at 120 mA.

---

## A.3 The two resistances, which are the point
**Looking into the base,** the base current is the emitter current divided by $h_{FE}$:

$$Z_{in} = h_{FE}\,(r_e + R_E)$$

**Looking back into the emitter,** the transistor presents $r_e$ and whatever drives the base
appears divided by $h_{FE}$:

$$Z_{out} = r_e + \frac{R_{source}}{h_{FE}}$$

At 1 mA driven from 1 kilohm, $26 + 20 = 46$ ohm.

<!-- value: 46 = follower_output_resistance(1e-3, 1e3) -->

**Together the stage is an impedance transformer:** it shows the driving stage $h_{FE}$ times its
emitter load, and the load $h_{FE}$ times less than its source, at a signal gain of 0.97.

**Both results are proportional to $h_{FE}$,** as
[L05 A.2](../../L05/appendix/a_the_bipolar_transistor.md#a2-beta-and-why-this-course-assumes-50)
and [L07 A.4](../../L07/appendix/a_the_small_signal_model.md#a4-three-results-one-method) warned.
[A.5](#a5-the-darlington-and-the-price-of-beta-squared) is where it starts to hurt.

---

## A.4 The eight ohm problem
Take L07's stage: 1 mA, 10 kilohm collector, 234 ohm emitter, open-circuit gain 38.5, output
resistance 9.89 kilohm. Connect a loudspeaker.

$$G_{loaded} = G \cdot \frac{R_{load}}{R_{out} + R_{load}} = 38.5 \times \frac{8}{9885 + 8}$$

**0.031.** The stage keeps **0.08 per cent** of its gain, and the amplifier does not work at all.

<!-- value: 0.08 = 100 * 8.0 / (ce_output_resistance(10e3, 1e-3, 234.0) + 8.0) -->

![Gain kept against the resistance the driving stage sees, on a logarithmic axis, rising from nearly nothing at 8 ohms through 4 per cent at 411 ohms to 68 per cent at 20 kilohms, with a shaded band showing where the Darlington point moves as h_FE runs from 20 to 200.](./images/impedance_chain.png)

**Now put a follower in between,** biased at 120 mA: $h_{FE}(r_e + R_{load}) = 411$ ohm, so the
driving stage sees 411 instead of 8 and keeps **4 per cent**. **Fifty times better and still
useless. One follower is not enough,** by two orders of magnitude.

---

## A.5 The Darlington, and the price of beta squared
Two transistors, the first driving the base of the second, behave as one device with a current gain
of $h_{FE1} h_{FE2}$ and two base-emitter drops. A.3's multiplication then happens twice:

$$Z_{in} = h_{FE}^2\,(2r_e + R_{load}) = 2500 \times 8.43 = 21.1\ \text{k}\Omega$$

<!-- value: 21.1 = darlington_input_resistance(0.12, 8.0) / 1e3 -->

**The resistance the square multiplies is the pair's own $2r_e$,** not one device's. The input
device runs at the output device's base current, so its $r_e$ is $h_{FE}$ times larger, and is seen
through the output device's gain, contributing $r_e$ again. The two $h_{FE}$s cancel: **a
Darlington's effective emitter resistance is exactly twice a single transistor's.** The driving
stage now sees 21.1 kilohm against its own 9.89 and keeps **68 per cent**, which is why essentially
every discrete output stage is a Darlington.

**Now the bill.** At $h_{FE} = 20$ the input resistance is 3.4 kilohm and the stage keeps 25 per
cent; at 200 it is 337 kilohm and keeps 97. **The same design from the same part number varies by
nearly four in gain across an ordinary production spread.**

<!-- value: 25 = 100 * darlington_input_resistance(0.12, 8.0, 20.0) / (ce_output_resistance(10e3, 1e-3, 234.0) + darlington_input_resistance(0.12, 8.0, 20.0)) -->

That is a design **plus** something that removes the dependence, namely
[L04's feedback](../../L04/README.md): at a loop gain of a few hundred the closed-loop gain stops
caring. L10 builds the loop.

**The Darlington's other costs,** real and not solved by feedback:
* **Two base-emitter drops**, so the swing is 1.3 V short of each rail rather than 0.65.
* **Slow turn-off**, the second base's charge having nowhere to go. A resistor from that base to
  the emitter is the standard fix, present in every practical circuit.
* **Twice the thermal drift** in the bias, which
  [B.4](./b_the_output_stage.md#b4-thermal-runaway-and-a-fix-that-looks-like-nothing) deals with.
* **Twice the intrinsic emitter resistance**, so 0.949 into 8 ohms where one follower gives 0.974.

---

## A.6 The fifth time
The same arithmetic since L01. This lecture is the fifth; [L10](../../L10/README.md) is the last:

| Where                                                                                                | What loaded what                         | Cost                           |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------ |
| [L01 A.6](../../L01/appendix/a_circuits_and_units.md#a6-loading-and-why-it-decides-everything-later) | 10 kilohm on a divider                   | a third of the output          |
| [L02](../../L02/README.md)                                                                           | source resistance on a filter            | the corner moves 6.6 times     |
| [L03](../../L03/README.md)                                                                           | two filter sections on each other        | the corner moves 1.72 times    |
| [L06 A.3](../../L06/appendix/a_the_quiescent_point.md#a3-the-base-current-loads-the-divider)         | base current on a bias divider           | 12 per cent of $I_C$           |
| **L08, here**                                                                                        | **a loudspeaker on a voltage amplifier** | **99.92 per cent of the gain** |
| L10, when it is written                                                                              | each stage on the one before             | 11 dB of open-loop gain        |

**The subtraction is identical every time.** What changes is how much it costs, and here it costs
everything.

---

## A.7 What this appendix is blind to
* **Frequency.** A follower with a capacitive load and an inductive source can oscillate, which is
  what the base resistor in every real output stage is for.
* **Large signals.** 0.974 is a small-signal number at one operating point. A follower driven at
  its rails runs out of current before voltage; [Appendix B](./b_the_output_stage.md) is the fix.
* **The second transistor's operating point** in the Darlington: it runs at the first's base
  current, so its $r_e$ is fifty times larger. In the code, not in the arithmetic above.
* **Power.** 120 mA at 20 V is 2.4 W, a heatsink question rather than a small-signal one.

---
