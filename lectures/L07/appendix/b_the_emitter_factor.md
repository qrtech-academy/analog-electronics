# Appendix B - The emitter factor, and where it belongs
The organising idea of this treatment, the node it belongs to, and the three circuits that follow
from getting that right.

---

## B.1 The emitter factor
$$EF = \frac{r_e + R_E}{r_e}$$

The factor by which a degeneration resistor raises the *total* emitter resistance, answering two
questions at once: by what factor does the **gain fall**, and the **resistance it presents rise**?

**The gain half is exactly right** ([A.5](./a_the_small_signal_model.md#a5-what-the-emitter-resistor-does-to-the-gain)).
**The second half is the one to be careful about:** the obvious reading, that the *stage's output
resistance* rises by $EF$, is wrong for an arithmetic reason
([B.3](#b3-where-the-emitter-factor-actually-belongs)). L06's 220 mV rule gives $EF \approx 10$.

---

## B.2 The Early effect and r_o
Extending the collector-base depletion region shortens the base, raising the collector current
slightly with collector voltage. One parameter, the Early voltage:

$$r_o = \frac{V_A}{I_C}$$

With $V_A = 100$ V and 1 mA that is 100 kilohm.

<!-- value: 100 = early_resistance(1e-3) / 1e3 -->

Ignorable until now, at under a per cent of a resistively loaded stage's gain. From here it is the
subject of the next three sections.

---

## B.3 Where the emitter factor actually belongs
The tempting way to write the stage's output resistance is

$$R_{out} \approx R_C \cdot EF$$

**That cannot be right, and the reason is arithmetic.** The output resistance is $R_C$ in parallel
with what the transistor presents there, and a parallel combination is smaller than either part.
**No degeneration can raise a stage's output resistance above $R_C$,** yet $R_C \cdot EF$ is ten
times it.

What degeneration does raise is the resistance **looking into the collector**, with $R_C$ removed:

$$R_{into\ collector} = r_o\left[1 + g_m (R_E \parallel r_\pi)\right] + (R_E \parallel r_\pi)$$

very nearly $r_o \cdot EF$: at 1 mA with 234 ohm, 863 kilohm against 1000. So

$$R_{out} = R_C \parallel R_{into\ collector} = 10\ \text{k} \parallel 863\ \text{k} = 9.89\ \text{k}\Omega$$

<!-- value: 9.89 = ce_output_resistance(10e3, 1e-3, 234.0) / 1e3 -->

against **9.09 kilohm** for the same stage with no emitter resistor.

![Four curves against the emitter resistor on logarithmic axes: the resistance looking into the collector rising steeply, the stage with a current-mirror load rising to a plateau, the stage with a ten kilohm resistive load lying flat, and the tempting R_C times EF rising far above all of them.](./images/ef_attribution.png)

**With a resistive load, degeneration buys 9 per cent of output resistance, not a factor of ten.**
The boost is real and it is invisible, because $R_C$ swamps it.

---

## B.4 Which is exactly why a current-mirror load exists
If $R_C$ throws the boost away, stop using $R_C$. A **current mirror** load presents its own $r_o$,
100 kilohm rather than 10.

![A common-emitter stage with a PNP current mirror as its load: a diode-connected reference transistor setting the current, its base tied to the output transistor whose collector feeds the amplifier's collector, with the reference resistor in the left leg.](./images/current_mirror.png)

| Load               | Output resistance, no $R_E$ | With $R_E$ for $EF = 10$ |
| ------------------ | --------------------------- | ------------------------ |
| 10 kilohm resistor | 9.09 kilohm                 | 9.89 kilohm              |
| Current mirror     | 50 kilohm                   | 89.6 kilohm              |

<!-- value: 89.6 = ce_output_resistance(early_resistance(1e-3), 1e-3, 234.0) / 1e3 -->

The degeneration now nearly doubles the output resistance, and so the gain. **A mirror load raises
gain for two independent reasons,** easy to run together:
* **Its own $r_o$ is large,** loading the output node with 100 kilohm instead of 10. Nothing to do
  with degeneration.
* **It stops the degeneration boost being swamped.** This is the emitter factor finally paying.

The resistively loaded gain of 385 becomes 1923, five times more, from the first mechanism alone.

<!-- value: 1923 = abs(ce_gain_exact(early_resistance(1e-3), 1e-3)) -->

---

## B.5 Miller and the cascode
The collector-base capacitance bridges input to output, and the output moves the other way by the
gain, so the input sees

$$C_{in} = C_{bc}(1 + |A_v|)$$

Four picofarads across a stage with a gain of 385 is **1.5 nanofarads** at the input.

<!-- value: 1.5 = miller_capacitance(ce_gain(10e3, 1e-3)) * 1e9 -->

![Input corner frequency against stage gain on logarithmic axes, falling as the gain rises, against a horizontal line showing where the corner would be if the capacitance were not multiplied.](./images/miller_bandwidth.png)

Driven from 1 kilohm, a corner at **103 kHz** on a device good to hundreds of megahertz. **The
Miller effect, not the transistor, limits an ordinary common-emitter stage.**

![A cascode: a common-emitter transistor whose collector feeds the emitter of a second transistor held at a fixed base voltage, with the load resistor on the upper collector and the output taken there.](./images/cascode.png)

**The cascode is the answer, and a stage you have already analysed.** A second transistor above
the first, base held fixed, keeps the lower collector at a constant voltage: **no swing there means
no Miller multiplication.**

$$R_{out(cascode)} = r_o\left[1 + g_m(r_o \parallel r_\pi)\right] + \dots \approx \beta r_o = 5\ \text{M}\Omega$$

<!-- value: 5.04 = cascode_output_resistance(1e-3) / 1e6 -->

**That is [B.3](#b3-where-the-emitter-factor-actually-belongs)'s expression with $R_E = r_o$:** a
cascode is a degenerated stage whose degeneration resistor is another transistor's $r_o$. The
emitter factor that would apply is 3847, but the boost caps at $\beta$ because $r_\pi$ shunts the
degeneration, reaching 5.04 megohm against a $\beta r_o$ ceiling of 5.00. **No new machinery.**

---

## B.6 The MOSFET, in one substitution
No textbook gives the MOSFET a quantity behaving as $r_e$ does, so this course names one:

$$r_s = \frac{1}{g_m}$$

![Two identical stages side by side, a common-emitter BJT and a common-source MOSFET, with the same supply, load and degeneration resistors, labelled r_e and r_s respectively, and a note that one substitution carries every result across except input resistance.](./images/re_to_rs.png)

Every result here transfers by writing $r_s$ for $r_e$; the 220 mV rule is unchanged:

$$A_v = -\frac{R_D}{r_s + R_S}, \qquad SF = \frac{r_s + R_S}{r_s}$$

**The one exception is input resistance.** A gate draws no current, so there is no
$\beta(r_e + R_E)$ term: a common-source stage's input resistance is its bias network. That is why
L09's input stage and L10's inter-stage buffer are both MOSFETs.

**Why $SF \approx 2$ where $EF \approx 10$,** both from 220 mV: $r_s$ at 1 mA is 250 ohm where $r_e$
is 26, transconductance being ten times lower
([L05 B.2](../../L05/appendix/b_the_mosfet_and_what_to_build.md#b2-transconductance-and-the-factor-of-ten)).

---

## B.7 What to build
### The Early effect in `ael/device/bjt.hpp`
Multiply the forward transport current by $(1 + V_{CE}/V_A)$. That is what makes $r_o$ finite and
[B.3](#b3-where-the-emitter-factor-actually-belongs) measurable.

**Multiply the collector current only. The base current does not get the factor,** so $h_{FE}$ comes
out as $\beta_F(1 + V_{CE}/V_A)$ and rises with collector voltage, as a datasheet's curve does.

**That placement is not a detail.** Putting the factor on the whole transport current, so both
currents scale and beta stays flat, is tempting: it leaves L05's contract untouched. It also makes
the base inject extra current into the emitter as the collector rises, which is degeneration
through $R_E$, so the resistance into the collector comes out **18 per cent high** and *above* the
emitter factor instead of below it. Your own solver would then contradict
[B.3](#b3-where-the-emitter-factor-actually-belongs). One test catches that version.

**One number the lecture does not quote.** Differentiating gives $r_o = (V_A + V_{CE})/I_C$: 105
kilohm at a collector 5 V up, not 100. Every closed form here uses the round figure, and that 5 per
cent is one of the things the Cross-check's legs disagree about.

### `ael/ssm/model.hpp`
| Function                                    | Returns                                                                 |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| `intrinsicEmitterResistance(ic)`            | $V_T/I_C$.                                                              |
| `intrinsicSourceResistance(gm)`             | $1/g_m$.                                                                |
| `emitterFactor(ic, re)`                     | $(r_e + R_E)/r_e$.                                                      |
| `sourceFactor(gm, rs)`                      | The same, for a MOSFET.                                                 |
| `gain(rc, ic, re)`                          | $-R_C/(r_e + R_E)$.                                                     |
| `inputResistance(ic, re, beta)`             | $\beta(r_e + R_E)$.                                                     |
| `resistanceIntoCollector(ic, re, beta, va)` | The expression of [B.3](#b3-where-the-emitter-factor-actually-belongs). |
| `outputResistance(rc, ic, re, beta, va)`    | That, in parallel with the load.                                        |
| `cascodeOutputResistance(ic, beta, va)`     | `resistanceIntoCollector` with $R_E = r_o$.                             |
| `millerCapacitance(gain, cbc)`              | $C(1 + \lvert A \rvert)$.                                               |

**`cascodeOutputResistance` must be implemented by calling `resistanceIntoCollector`,** not by a
separate formula. Separate, and the claim that a cascode is degeneration by $r_o$ is an assertion
rather than something the code demonstrates.

### What good looks like
About seventy lines, of which none is longer than three.

---

## B.8 What this appendix is blind to
* **The body effect**, which raises a MOSFET follower's threshold and costs real gain in L08.
* **Base resistance.** Ohmic resistance in the base adds to $r_e$ at high current and limits noise.
* **The second Miller capacitance.** The base-emitter capacitance is not multiplied but is far
  larger, and at high frequency it, not $C_{bc}$, sets the limit.
* **High frequency, properly.** One capacitance and one pole is a caricature of a device with three
  capacitances and a transit time.

---
