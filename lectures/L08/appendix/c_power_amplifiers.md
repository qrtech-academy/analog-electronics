# Appendix C - What a real power amplifier adds

**Reading, not examinable.** There are no exercises on this appendix and nothing in it is in the
test suite. It is here because everything up to this point stops well short of a power amplifier
that could be built, and a reader who went straight from [Appendix B](./b_the_output_stage.md) to
a soldering iron would be surprised. What follows is the shape of what is missing.

Everything in [Appendix B](./b_the_output_stage.md) is still true. This appendix is about what
else has to be present before a class-AB stage survives being connected to a loudspeaker.

---

## C.1 The power arithmetic, done properly

Take 50 W into 8 ohm, and do it carefully, because confusing rms with peak here propagates into
the rail voltage and then into everything else.

$$V_{rms} = \sqrt{P R} = \sqrt{50 \times 8} = 20\ \text{V}, \qquad I_{rms} = 2.5\ \text{A}$$

$$V_{peak} = \sqrt{2}\,V_{rms} = 28.3\ \text{V}, \qquad I_{peak} = 3.54\ \text{A}$$

**Calling 2.5 A the peak current is the easy mistake.** It is the rms current, and the
consequence is not cosmetic: it leads to $\pm 20$ V rails, which deliver at most

$$P = \frac{V_{rail}^2}{2R} = \frac{400}{16} = 25\ \text{W}$$

**half the power the example is about.** A 50 W amplifier into 8 ohm needs at least $\pm 28.3$ V
before any allowance for the output devices' saturation, the emitter resistors, and the supply
sagging under load. In practice $\pm 32$ V or more.

**Then the class comparison, on those rails:**

|          | Idle current          | Idle dissipation |
| -------- | --------------------- | ---------------- |
| Class A  | 3.54 A, the full peak | 226 W            |
| Class AB | 120 mA                | 7.7 W            |

A factor of **29**, for an output stage that measures very nearly as well. That ratio is the whole
argument for class AB, and it is why almost nothing is built in class A.

**Maximum theoretical efficiency**, at full output and with ideal devices: class A **25 per cent**
with a resistive load and 50 with a current-source load; class B **78.5 per cent**, which is
$\pi/4$. Class AB sits just below class B because it also carries the idle current. Real
amplifiers reach the sixties.

---

## C.2 Why one Darlington is not the end of it

[A.5](./a_the_follower.md#a5-the-darlington-and-the-price-of-beta-squared) got the input
resistance to 20 kilohm by using two transistors. A 50 W amplifier needs 3.5 A of output current,
and a power transistor's $h_{FE}$ at 3.5 A is not 50 but more like 20, and falling.

$$I_{base} = \frac{3.54}{20 \times 20} = 8.8\ \text{mA}$$

from a voltage-amplifier stage running at 1 to 10 mA. That is the whole of its current, so the
stage clips before the output does. The answer is a **third** follower, giving $h_{FE}^3$: the
**triple emitter follower**, or 3-EF. Base current falls to 440 microamps and the driver stage is
no longer the limit.

The alternative topology is the **CFP-EF**, a complementary feedback
pair driving an emitter follower. A CFP puts local feedback around two devices so that the output
voltage tracks the input to within one $V_{BE}$ rather than two. Importantly for
[B.4](./b_the_output_stage.md#b4-thermal-runaway-and-a-fix-that-looks-like-nothing), its
thermal behaviour is set by the small driver transistor rather than by the hot power device, so it
needs much less bias tracking. Its weakness is a tendency to oscillate that the plain follower
does not have.

**Both exist for the same reason:** current gain that does not depend on a hot power device's
beta.

---

## C.3 The circuits that are only there to prevent failure

None of these affect the gain. Every one of them is present in every commercial amplifier, and a
schematic without them is a schematic of something that will not survive.

**Base stopper resistors**, 10 to 100 ohm in series with each output base. A power transistor has
enough transit time and enough capacitance to form an oscillator with the inductance of its own
leads, at tens of megahertz, where nobody is looking. The resistor damps it. It costs a few
millivolts of drive.

**The Zobel network**, a resistor and capacitor in series from the output to ground, typically
10 ohm and 100 nF. A loudspeaker is inductive above a few kilohertz, and an inductive load turns
an amplifier's output inductance into a resonance. The Zobel presents a resistive load at high
frequency so the amplifier always sees something it can drive.

**The output inductor**, a few microhenries, usually a coil wound over a resistor. It isolates the
amplifier from a capacitive cable, which would otherwise add phase lag inside the feedback loop.
The parallel resistor stops the inductor itself ringing.

**Snubbers** across the rectifier diodes in the supply, because a diode's reverse recovery is a
step change in current into the transformer's leakage inductance, and that rings at radio
frequency and appears in the output.

**Over-current protection**, usually a transistor across each output device's base-emitter
junction, turned on by the voltage across the emitter resistor. Above a set current it steals the
base drive. The emitter resistors of
[B.3](./b_the_output_stage.md#b3-class-ab-and-the-26-millivolt-rule) are therefore doing three
jobs: thermal stability, current sharing between paralleled devices, and current sensing.

**A DC offset detector** driving a relay in series with the loudspeaker. If an output device
fails short, the loudspeaker sees the full rail through 8 ohm, which is 128 W into a voice coil
rated for a few. The relay disconnects it within a few tens of milliseconds.

---

## C.4 Heat

A class-AB output stage idling at 120 mA on $\pm 32$ V dissipates 7.7 W with no signal, and its
worst case is not full output. Dissipation in each device peaks at about **40 per cent of full
output**, where the current is high and the voltage across the device is still large. For this
amplifier that is around 17 W per device: $V_{CC}^2/\pi^2R_L = 13$ W of class-B dissipation plus
4 W from the idle current.

**Junction-to-ambient thermal resistance** adds in series like electrical resistance: junction to
case, case to heatsink through the insulating washer, heatsink to air. A 1 °C/W heatsink with a
0.5 °C/W washer and a 1 °C/W device gives 2.5 °C/W, so 17 W raises the junction 42 °C above
ambient. At 40 °C ambient inside a case that is an 82 °C junction, which is acceptable for a device
rated to 150.

**The placement rule matters as much as the size.** Every output device and the bias generator
must be on the *same* heatsink, close together, because
[B.4](./b_the_output_stage.md#b4-thermal-runaway-and-a-fix-that-looks-like-nothing) requires them
to be at the same temperature. Two devices on separate heatsinks will not share current, and the
hotter one takes progressively more of it, which is the same runaway one level up.

---

## C.5 Why output stages are usually bipolar

The comparison is worth setting out directly, because it comes to the opposite of the conclusion
[B.6](./b_the_output_stage.md#b6-the-source-follower-and-the-one-thing-that-does-not-carry-across)
reaches for input stages:

|                          | Bipolar                  | MOSFET                                    |
| ------------------------ | ------------------------ | ----------------------------------------- |
| Output resistance        | about ten times lower    | higher, by $r_s/r_e$                      |
| Distortion               | lower                    | higher without correction                 |
| Thermal stability        | needs tracking bias      | inherently stable above a crossover point |
| High-frequency stability | needs stoppers and Zobel | far less prone                            |
| Drive                    | current, so beta matters | voltage, but gate charge matters          |

**So the two devices swap places depending on which end of the amplifier they are at**, and the
reason is the same one: a MOSFET's transconductance is about ten times lower at the same current.
At the input that is irrelevant and the infinite gate resistance is decisive. At the output it is
decisive and the gate resistance is irrelevant.

A MOSFET output stage with an error amplifier correcting its output can reach bipolar distortion
figures. It is more circuitry to reach the same place, and it buys robustness rather than
performance.

---

## C.6 What to take from this appendix

Three things, and none of them is a formula:

1. **A power stage is mostly not the amplifier.** The gain path is a handful of transistors; the
   rest of the schematic is protection, compensation and thermal management.
2. **The failures are thermal and high-frequency**, and neither is visible in the small-signal
   analysis this course teaches. A design that is correct in every equation in L07 and L08 can
   still destroy itself.
3. **The corrections in [C.1](#c1-the-power-arithmetic-done-properly) are the kind that matter.**
   An rms mistaken for a peak is a supply rail specified 40 per cent too low, and no amount of
   care further down recovers it.

---
