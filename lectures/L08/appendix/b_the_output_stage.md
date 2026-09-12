# Appendix B - The output stage, and the model that finally breaks
Three classes, one dead band, one sizing rule, and the first place in this course where the
constant-drop model is not merely approximate but wrong by a factor of sixty.

---

## B.1 Class A: the follower you already have
Bias the follower so it conducts for the whole signal. Nothing turns off, so there is no
discontinuity in the transfer curve and the distortion is the exponential's curvature.

**Its vice is arithmetic.** To swing $\pm V$ the device must idle at $V/R_{load}$, the current it
must be able to *stop* delivering at the negative peak, so it burns $V^2/R_{load}$ at idle. Best
case **25 per cent efficiency at full output**, falling to zero as the signal falls: **a 100 W
class-A amplifier draws 400 W playing silence.**

---

## B.2 Class B, and the dead band
Two devices: an NPN follower pushes into the load on positive half-cycles, a PNP pulls on negative
ones, and neither conducts at idle. Idle dissipation goes to zero and efficiency rises to $\pi/4$,
**78.5 per cent**. **And it does not work,** for a reason unrelated to efficiency.

![The transfer curve of a complementary pair, with the unbiased case flat across a dead band 1.3 volts wide centred on zero, and the biased case a straight line through the origin, the dead band shaded.](./images/crossover.png)

Neither conducts until its base-emitter junction is forward biased, so the output stays at zero
across an input band **two diode drops wide**, about 1.3 V: **crossover distortion**.

**Its size is not the problem; its position is.** 1.3 V in a stage swinging 30 V is 4 per cent,
tolerable-sounding, but it sits at the origin and music spends most of its time there. **The
distortion is worst on quiet passages and vanishes at full output,** the opposite of every other
distortion mechanism, and audible far below the level its percentage suggests.

---

## B.3 Class AB, and the 26 millivolt rule
Bias both devices so a small current flows at idle: the dead band closes and idle dissipation is
small rather than zero. Essentially every audio output stage is **class AB**.

![A class-AB output stage: an NPN and a PNP follower with their emitters facing each other through two small resistors to the output node, two series diodes between the bases setting the bias, and an eight ohm load to ground.](./images/class_ab.png)

**How much idle current?** Enough to close the dead band and no more, stated on the resistors:

$$R_E = \frac{V_T}{I_q} = \frac{26\ \text{mV}}{I_q}$$

At the 120 mA a stage of this size idles at, 0.217 ohm, and 0.22 is an E12 value.

<!-- value: 0.22 = nearest_e12(quiescent_emitter_resistor(0.12)) -->

**The rule is $R_E = r_e$ the other way round,** putting $V_T$ across $R_E$, so L07's emitter
factor is exactly 2. That is what it is choosing:

|                                         | Value        |
| --------------------------------------- | ------------ |
| $r_e$ at 120 mA                         | 0.217 ohm    |
| $R_E$, E12                              | 0.22 ohm     |
| Emitter factor                          | 2.0          |
| Drop across $R_E$ at idle               | 26 mV        |
| Cost in the load: 0.22 in series with 8 | 2.7 per cent |

<!-- value: 2.0 = emitter_factor(0.12, quiescent_emitter_resistor(0.12)) -->

**Two per cent of the signal for half the thermal sensitivity.** At 260 mV the emitter factor is 11
and 2.2 ohm in series with 8 has thrown away a fifth of the output power; at 2.6 mV the resistors
do nothing. 26 mV is where those costs cross, the same trade as L06's 220 mV rule.

---

## B.4 Thermal runaway, and a fix that looks like nothing
An output transistor dissipates power, warms, drops its $V_{BE}$ by 2 mV per degree, and draws more
idle current at fixed bias. **That loop can run away, and a runaway output stage destroys itself in
seconds.** Both junctions drift, so a fixed bias is 4 mV per degree too generous, landing across
$2(r_e + R_E)$:

$$\frac{1}{I_q}\frac{dI_q}{dT} = \frac{2\lvert dV_{BE}/dT\rvert}{2(r_e + R_E) I_q}$$

|                      | Per degree   | Over a 30 degree rise |
| -------------------- | ------------ | --------------------- |
| No emitter resistors | 7.7 per cent | a factor of 9         |
| With the 26 mV rule  | 3.8 per cent | a factor of 3         |

<!-- value: 3.8 = 100 * class_ab_drift(0.12, nearest_e12(quiescent_emitter_resistor(0.12))) -->

**A factor of three is still a runaway.** The emitter resistors halve the problem and do not solve
it: the 26 mV rule buys margin, not stability.

**The fix is to make the bias voltage drift too.** Bolt the bias diodes to the output devices'
heatsink and their forward voltages fall 2 mV per degree as well, cancelling to first order.

**So the diodes are not setting a voltage. They are tracking one.** Read them as "about 1.3 volts
of bias" and mount them on the board next to the driver, and the stage is correct at 25 degrees and
destroys itself at 60. **This is the most common way a first output stage fails, and the schematic
does not show it: the two circuits are drawn identically.**

**Real circuits use a $V_{BE}$ multiplier:** one transistor with a divider from collector to base,
giving an adjustable multiple of a base-emitter drop, on the heatsink. Adjustable, because the
tracking is never exact ([B.8](#b8-what-this-appendix-is-blind-to)).

---

## B.5 Where the constant-drop model finally breaks
Since L05, $V_{BE} \approx 0.65$ V has served for bias points at about 1 per cent error. **Here it
fails completely.** What bias voltage does the stage above need to idle at 120 mA?

$$V_{bias} = 2\left(V_{BE}(I_q) + I_q R_E\right)$$

$V_{BE}$ at 120 mA is **0.783 V**, not 0.65: it is $V_T \ln(I_C/I_S)$ and 120 mA is **2.2 decades**
above the 0.72 mA where 0.65 V is right. The resistors add 26 mV each:

$$V_{bias} = 2(0.783 + 0.026) = 1.619\ \text{V}$$

<!-- value: 1.619 = class_ab_bias(0.12, nearest_e12(quiescent_emitter_resistor(0.12))) -->

against **1.353 V** from the constant-drop model: a 16 per cent error in the voltage.

**Run it backwards, which is where the size shows.** Apply 1.353 V and ask what idle current
results. Not 120 mA reduced by a sixth: **1.96 mA**.

<!-- value: 1.96 = class_ab_idle_current(2.0 * (VBE_ON + 0.12 * nearest_e12(quiescent_emitter_resistor(0.12))), nearest_e12(quiescent_emitter_resistor(0.12))) * 1e3 -->

**A factor of 61.** The stage is biased into class B, the dead band is open, and the amplifier
sounds broken.

**Why here and not before.** Every earlier use computed a **current from a voltage across a
resistor**, where 133 mV inside a subtraction yielding 1.06 V is 12 per cent, entering linearly.
Here it computes a **current from a voltage across a junction**, and 133 mV inside an exponential
of scale 26 mV is $e^{5.1}$, a factor of 166. **The emitter resistors turn 166 into 61:** at 120 mA
they carry 26 of the 133 mV, at 2 mA nothing.

**The lesson is not that 0.65 is wrong,** but that a model's error is a property of the calculation
it is used in. **And it explains the circuit:** two signal diodes at a few milliamps give 1.40 V and
an idle current of 4.8 mA, which is why a real stage uses an adjustable multiplier or diodes at the
output current.

---

## B.6 The source follower, and the one thing that does not carry across
[L07 B.6](../../L07/appendix/b_the_emitter_factor.md#b6-the-mosfet-in-one-substitution)'s
substitution of $r_s$ for $r_e$ holds here too:

$$G = \frac{R_S}{r_s + R_S}, \qquad Z_{out} = r_s$$

with the input resistance the bias network, because a gate draws no current. **A strict
improvement:** the $h_{FE}^2$ of
[A.5](./a_the_follower.md#a5-the-darlington-and-the-price-of-beta-squared), factor-of-four spread
and all, becomes a resistor you chose. **The cost is the gain:** at 1 mA $r_s$ is 250 ohm where
$r_e$ is 26, so into 1 kilohm the source follower gives 0.80 against 0.97.

<!-- value: 0.80 = 1e3 / (1e3 + intrinsic_source_resistance(NMOS_GM_AT_1MA)) -->

Ten times the current recovers only three, $g_m$ going as $\sqrt{I_D}$
([L05 B.2](../../L05/appendix/b_the_mosfet_and_what_to_build.md#b2-transconductance-and-the-factor-of-ten)).
**A MOSFET output stage must be biased much harder for the same gain,** which is why output stages
are usually bipolar.

**And here the substitution is not exact.** A MOSFET's threshold rises when its source sits above
its body, as in an integrated CMOS follower it always does. That **body effect** is a source-to-body
transconductance $g_{mb}$, 10 to 30 per cent of the main one, appearing as unasked-for
degeneration:

$$G = \frac{R_S}{r_s(1 + \chi) + R_S}$$

With $\chi = 0.2$, 0.80 becomes **0.77**: why a discrete source follower and a CMOS one do not give
the same answer from the same equation.

---

## B.7 What to build
### `ael/follower/stage.hpp`
| Function                                                     | Returns                                                                                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `gain(collectorCurrent, load)`                               | $R/(r_e + R)$.                                                                                                                 |
| `outputResistance(collectorCurrent, sourceResistance, beta)` | $r_e + R_{src}/h_{FE}$.                                                                                                        |
| `inputResistance(collectorCurrent, load, beta)`              | $h_{FE}(r_e + R)$.                                                                                                             |
| `darlingtonEmitterResistance(outputCurrent)`                 | $2V_T/I$. Twice one device's, and $h_{FE}$ cancels.                                                                            |
| `darlingtonGain(outputCurrent, load)`                        | $R/(2r_e + R)$: a little worse than a single follower.                                                                         |
| `darlingtonInputResistance(outputCurrent, load, beta)`       | $h_{FE}^2(2r_e + R)$.                                                                                                          |
| `loadedGain(unloadedGain, outputResistance, load)`           | The divider of [A.4](./a_the_follower.md#a4-the-eight-ohm-problem).                                                            |
| `intrinsicEmitterResistance(collectorCurrent)`               | $V_T/I_C$. The quantity L07 named, re-exported here so that a follower result can be written without reaching into `ael::ssm`. |

`loadedGain` is three characters of arithmetic and the most-used function in L10, which calls it
eleven times. Write it here rather than inline at each call site.

### `ael/output/classab.hpp`
| Function                                       | Returns                                                                       |
| ---------------------------------------------- | ----------------------------------------------------------------------------- |
| `degenerationResistor(idleCurrent)`            | $V_T/I_q$: the 26 mV rule.                                                    |
| `biasVoltage(idleCurrent, emitterResistor)`    | $2(V_{BE}(I_q) + I_q R_E)$, with $V_{BE}$ from the **exponential**.           |
| `idleCurrent(bias, emitterResistor)`           | The inverse. There is no closed form.                                         |
| `driftPerDegree(idleCurrent, emitterResistor)` | The fraction of [B.4](#b4-thermal-runaway-and-a-fix-that-looks-like-nothing). |
| `transfer(input, bias, vbeOn, load)`           | The dead band of [B.2](#b2-class-b-and-the-dead-band).                        |

**`idleCurrent` must not call a constant-drop approximation.** It inverts an equation with an
exponential and a linear term that do not separate, and the whole of
[B.5](#b5-where-the-constant-drop-model-finally-breaks) is about what happens when you pretend they
do. Bisect in the logarithm, or use Newton with the limiter you wrote in L04.

### What good looks like
About fifty lines. `idleCurrent` is the only one with a loop in it.

---

## B.8 What this appendix is blind to
* **The tracking is never exact.** The generator runs at a few milliamps and the outputs at 120,
  and [L06 B.5](../../L06/appendix/b_thermal_drift.md#b5-what-to-build) established that the
  temperature coefficient depends on current. It also sits on the heatsink rather than the die,
  lagging by seconds. Hence the adjustment.
* **Self-heating,** the loop that makes the drift a runaway.
  [L06 B.6](../../L06/appendix/b_thermal_drift.md#b6-what-this-appendix-is-blind-to) deferred it
  here; still deferred, because a thermal model is a course of its own.
* **Safe operating area.** 5 A with 40 V across it kills a small transistor whatever the average
  power, which is what [Appendix C](./c_power_amplifiers.md)'s protection circuitry is for.
* **A real loudspeaker,** a complex impedance varying by five across the audio band.
* **Distortion, quantitatively.** Crossover distortion is audible; how many parts per million a
  given bias leaves is not said.

---
