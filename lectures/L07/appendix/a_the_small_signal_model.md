# Appendix A - The small-signal model, and the three results
The centre of the course. One resistance, one construction, three results, and the same method
every time.

---

## A.1 A straight line through a curve
An amplifier does not use the whole exponential. It sits at an operating point, found in
[L06](../../L06/README.md), and the signal moves it a little way either side. **Over a small enough
excursion, any smooth curve is a straight line,** and that slope is the whole small-signal model.

$$g_m = \left.\frac{dI_C}{dV_{BE}}\right|_{Q} = \frac{I_C}{V_T}$$

**How small is small enough.** The exponential's scale is $V_T$, 26 mV, so a few millivolts is
linear to a fraction of a per cent and 26 mV is not linear at all. **A stage handling 10 mV of base
signal is already distorting noticeably,** and that is the mechanism L04's feedback divided down.

**What linearising discards:** clipping, distortion, the fact that the device turns off, and any
signal large enough to move the operating point.

---

## A.2 The one resistance
$$r_e = \frac{V_T}{I_C} = \frac{26\ \text{mV}}{I_C}$$

At 1 mA it is 26 ohm.

<!-- value: 26 = intrinsic_emitter_resistance(1e-3) -->

**It is not a resistor.** It is the slope of the device's own exponential at the operating point,
depending on nothing but current and temperature. It cannot be bought or specified, and if the
stage is switched off it does not become large: it ceases to exist with the operating point.

This course uses it in preference to $g_m$ throughout, a resistance in series with the emitter
being easier to reason about than a transconductance. The translation is $g_m = 1/r_e$.

---

## A.3 Building the small-signal schematic
Four rules, applied in order:
1. **Every DC source becomes a short to ground.** A rail that does not move carries no signal.
2. **Every coupling and bypass capacitor becomes a short.** That is what they were chosen for.
3. **The bias network disappears** wherever it is now in parallel with something much smaller.
4. **The transistor becomes $r_e$ from base to emitter, and a current source from collector to
   emitter** carrying the current that $r_e$ passes.

![The small-signal schematic of a common-emitter stage: the input drives r_e in series with the emitter resistor to ground, and on the output side the supply rail is drawn as a ground with the collector resistor descending to the output node, where a current source draws the collector current to ground.](./images/re_model.png)

The result has no transistor in it: one resistance, one current source, the external resistors.
**The one equation** links its halves, that the current the input drives through $r_e$ and $R_E$
*is* the current the collector source delivers. Everything else is bookkeeping.

---

## A.4 Three results, one method
**Gain.** The input drives $v_{in}/(r_e + R_E)$ through the emitter branch; that current comes out
of the collector and through $R_C$, giving $-i R_C$ at the output.

$$A_v = -\frac{R_C}{r_e + R_E}$$

The minus sign is real: more base voltage means more collector current means a lower collector
voltage. For 10 kilohm and 1 mA with no emitter resistor that is $-385$; with 234 ohm, $-38.5$.

<!-- value: 385 = abs(ce_gain(10e3, 1e-3)) -->

**Input resistance.** The base draws the emitter current divided by $\beta$, at the voltage across
the emitter branch:

$$Z_{in(base)} = \beta\,(r_e + R_E)$$

At 1 mA with 234 ohm and $\beta = 50$, 13 kilohm. **This is the one result in Part 2 that depends
on beta,** as [L05 A.2](../../L05/appendix/a_the_bipolar_transistor.md#a2-beta-and-why-this-course-assumes-50)
warned, so an input resistance is always a range. The stage's actual input resistance is that in
parallel with the bias divider, usually the smaller of the two.

**Output resistance** is the subject of [Appendix B](./b_the_emitter_factor.md), because it is the
one result here that the obvious answer gets wrong.

---

## A.5 What the emitter resistor does to the gain
Dividing the two gain expressions:

$$\frac{A_v(\text{no } R_E)}{A_v(\text{with } R_E)} = \frac{r_e + R_E}{r_e}$$

That ratio is the **emitter factor**, and the gain falls by exactly it.

![Gain and the emitter factor plotted against the emitter resistor on logarithmic axes, the gain falling as the factor rises and the two crossing, with the 234 ohm design point marked where the gain of 385 has become 38.5.](./images/gain_against_ef.png)

**An emitter resistor costs gain one for one.** What it buys was L06's subject, thermal stability,
and what else it buys is [Appendix B](./b_the_emitter_factor.md)'s.

**Bypassing it** with a capacitor recovers the gain at signal frequencies while keeping the DC
stability, which is why almost every discrete common-emitter stage has one. **It also throws away
the distortion reduction,** because that was feedback and the capacitor removed it at exactly the
signal frequencies.

---

## A.6 What this appendix is blind to
* **Everything nonlinear.** Distortion, clipping and slew rate are outside a model built by
  assuming a straight line.
* **Capacitance.** Nothing here has a frequency in it. The Miller effect of
  [B.5](./b_the_emitter_factor.md#b5-miller-and-the-cascode) is where that starts.
* **The Early effect**, so far. $r_o$ arrives in [B.2](./b_the_emitter_factor.md#b2-the-early-effect-and-r_o)
  and changes the output resistance results and nothing else.
* **Noise.** The model says what a stage does to a signal, not what signal the stage adds itself.

---
