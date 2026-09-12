# Appendix C - What a real power amplifier adds
**Reading, not examinable.** No exercises, nothing in the test suite. Everything in
[Appendix B](./b_the_output_stage.md) still holds; this is the shape of what it leaves out.

---

## C.1 The power arithmetic, done properly
50 W into 8 ohm. Confusing rms with peak here propagates into the rail voltage and everything after
it.

$$V_{rms} = \sqrt{P R} = \sqrt{50 \times 8} = 20\ \text{V}, \qquad I_{rms} = 2.5\ \text{A}$$

$$V_{peak} = \sqrt{2}\,V_{rms} = 28.3\ \text{V}, \qquad I_{peak} = 3.54\ \text{A}$$

**Calling 2.5 A the peak current is the easy mistake,** and it leads to $\pm 20$ V rails, which
deliver at most

$$P = \frac{V_{rail}^2}{2R} = \frac{400}{16} = 25\ \text{W}$$

**half the power the example is about.** A 50 W amplifier into 8 ohm needs $\pm 28.3$ V before any
allowance for saturation, the emitter resistors and supply sag: in practice $\pm 32$ V.

|          | Idle current          | Idle dissipation |
| -------- | --------------------- | ---------------- |
| Class A  | 3.54 A, the full peak | 226 W            |
| Class AB | 120 mA                | 7.7 W            |

**A factor of 29,** for a stage that measures very nearly as well. That is the whole argument for
class AB.

**Maximum theoretical efficiency,** ideal devices at full output: class A **25 per cent**
resistively loaded and 50 with a current-source load, class B **78.5 per cent**, which is $\pi/4$.
Class AB sits just below. Real amplifiers reach the sixties.

---

## C.2 Why one Darlington is not the end of it
[A.5](./a_the_follower.md#a5-the-darlington-and-the-price-of-beta-squared) reached 20 kilohm with
two transistors. At the 3.5 A a 50 W amplifier needs, a power transistor's $h_{FE}$ is nearer 20:

$$I_{base} = \frac{3.54}{20 \times 20} = 8.8\ \text{mA}$$

from a voltage-amplifier stage running at 1 to 10 mA. **That is the whole of its current, so the
driver clips before the output does.** A **third** follower gives $h_{FE}^3$: the **triple emitter
follower**, with a base current of 440 microamps.

The alternative is the **CFP-EF**, a complementary feedback pair driving an emitter follower. Local
feedback round two devices makes the output track the input to within one $V_{BE}$ rather than two,
and its thermal behaviour is set by the small driver rather than the hot power device, so it needs
much less bias tracking
([B.4](./b_the_output_stage.md#b4-thermal-runaway-and-a-fix-that-looks-like-nothing)). Its weakness
is a tendency to oscillate. **Both exist for one reason:** current gain that does not depend on a
hot power device's beta.

---

## C.3 The circuits that are only there to prevent failure
None of these affect the gain, and every one is in every commercial amplifier.

* **Base stoppers,** 10 to 100 ohm in series with each output base. A power transistor and its own
  lead inductance oscillate at tens of megahertz, where nobody is looking. The resistor damps it.
* **The Zobel network,** typically 10 ohm and 100 nF from output to ground. A loudspeaker is
  inductive above a few kilohertz; the Zobel keeps something resistive there.
* **The output inductor,** a few microhenries wound over a resistor, isolating a capacitive cable
  whose phase lag would otherwise sit inside the feedback loop.
* **Snubbers** across the rectifier diodes. Reverse recovery steps current into the transformer's
  leakage inductance, which rings at radio frequency and reaches the output.
* **Over-current protection,** a transistor across each output base-emitter junction, turned on by
  the emitter resistor's voltage, stealing base drive above a set current. **So the emitter
  resistors of [B.3](./b_the_output_stage.md#b3-class-ab-and-the-26-millivolt-rule) do three jobs:**
  thermal stability, current sharing between paralleled devices, and current sensing.
* **A DC offset detector** and a relay in series with the loudspeaker. A shorted output device puts
  the full rail across 8 ohm, 128 W into a voice coil rated for a few.

---

## C.4 Heat
**Dissipation per device peaks at about 40 per cent of full output,** not at full output, where the
current is high and the voltage across the device is still large. Here about 17 W:
$V_{CC}^2/\pi^2R_L = 13$ W of class-B dissipation plus 4 W from the idle current.

**Thermal resistances add in series** like electrical ones: junction to case, case to heatsink
through the washer, heatsink to air. 1 plus 0.5 plus 1 is 2.5 °C/W, so 17 W lifts the junction
42 °C: 82 °C at a 40 °C ambient, acceptable for a device rated to 150.

**Placement matters as much as size.** Every output device and the bias generator on the *same*
heatsink, close together, because
[B.4](./b_the_output_stage.md#b4-thermal-runaway-and-a-fix-that-looks-like-nothing) needs them at
the same temperature. **Two devices on separate heatsinks will not share current, and the hotter
one takes progressively more of it:** the same runaway one level up.

---

## C.5 Why output stages are usually bipolar
The opposite conclusion to the one
[B.6](./b_the_output_stage.md#b6-the-source-follower-and-the-one-thing-that-does-not-carry-across)
reaches for input stages:

|                          | Bipolar                  | MOSFET                                    |
| ------------------------ | ------------------------ | ----------------------------------------- |
| Output resistance        | about ten times lower    | higher, by $r_s/r_e$                      |
| Distortion               | lower                    | higher without correction                 |
| Thermal stability        | needs tracking bias      | inherently stable above a crossover point |
| High-frequency stability | needs stoppers and Zobel | far less prone                            |
| Drive                    | current, so beta matters | voltage, but gate charge matters          |

**The two devices swap places depending on which end of the amplifier they are at,** for one
reason: a MOSFET's transconductance is ten times lower at the same current. At the input that is
irrelevant and the infinite gate resistance decisive; at the output, the reverse. A MOSFET stage
with an error amplifier can reach bipolar distortion figures, buying robustness rather than
performance.

---

## C.6 What to take from this appendix
1. **A power stage is mostly not the amplifier.** The gain path is a handful of transistors; the
   rest of the schematic is protection, compensation and thermal management.
2. **The failures are thermal and high-frequency,** neither visible in the small-signal analysis
   this course teaches. A design correct in every equation of L07 and L08 can still destroy itself.
3. **The corrections in [C.1](#c1-the-power-arithmetic-done-properly) are the kind that matter.**
   An rms mistaken for a peak is a rail 40 per cent too low, and nothing further down recovers it.

---
