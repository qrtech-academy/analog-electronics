# Appendix A - Passive filters, cascading, and Q
The first useful circuits in the course, and the third appearance of the one piece of arithmetic
that decides everything.

---

## A.1 Two components, four filters
A resistor and a capacitor in series make a divider whose ratio depends on frequency. Which
component you take the output across decides the kind of filter.

$$H_{LP} = \frac{1}{1 + j f/f_c}, \qquad H_{HP} = \frac{j f/f_c}{1 + j f/f_c}$$

Both have the same corner, $f_c = 1/(2\pi RC)$, and both are 3 dB down there. At that corner the
low-pass lags 45 degrees and the high-pass leads 45, so **their outputs add to give the input back
exactly, at every frequency.** That is the cleanest statement of what complementary means.

![Low-pass, high-pass and band-pass magnitude responses against frequency normalised to a common corner, on logarithmic axes. The low-pass is flat then falls, the high-pass rises then is flat, and the band-pass rises and falls, reaching nearly zero decibels between two corners two decades apart.](./images/filter_family.png)

A **band-pass** is a high-pass and a low-pass in series. It reaches 0 dB in the middle only if
the corners are well apart: a decade apart falls 0.83 dB short, equal corners 6 dB.

---

## A.2 A filter's own impedances
A filter is a two-port and both of its ports have a frequency-dependent impedance. Both matter for
L01's reason: the source upstream and the load downstream form dividers with them.

$$Z_{in} = R + \frac{1}{j\omega C}, \qquad Z_{out} = R \parallel \frac{1}{j\omega C}$$

$Z_{in}$ is capacitor-dominated and large at low frequency, approaching $R$ at high; $Z_{out}$ is
$R$ at low frequency and approaches zero at high. **So a low-pass RC presents its own series
resistance as an output impedance at low frequency, and the next stage sees it.**

---

## A.3 Cascading, and the corner you did not design
Two identical low-pass sections in a row look like they should give the square of one section's
response: 6 dB down at the corner, falling at 40 dB per decade. **That is the answer for two
sections with a buffer between them, and it is wrong for two connected directly.**

![Magnitude against frequency for one RC section, for two sections with a buffer between them, and for two sections cascaded directly. The directly cascaded pair falls away earliest, and a marker shows it is three decibels down at 0.37 of one section's corner.](./images/cascade_loading.png)

The second section loads the first. Its input impedance parallels the first section's capacitor,
so the two poles split apart, their product staying at $f_c^2$:

$$f_{low} = f_c \frac{3 - \sqrt{5}}{2} = 0.382 f_c, \qquad f_{high} = f_c \frac{3 + \sqrt{5}}{2} = 2.618 f_c$$

| Arrangement                     | 3 dB point  |
| ------------------------------- | ----------- |
| One section                     | $1.000 f_c$ |
| Two sections, buffered          | $0.644 f_c$ |
| Two sections, cascaded directly | $0.374 f_c$ |

<!-- value: 0.374 = cascaded_corner(1e3, 159e-9) / rc_corner(1e3, 159e-9) -->

The direct cascade is a factor of **1.72** lower than the buffered pair. **A filter designed by
multiplying two responses together and built by soldering two sections together is not the filter
that was designed.**

**The fix is a buffer:** high input impedance, low output impedance, between the sections so the
second cannot load the first. An op-amp follower is exactly that, which is why this lecture covers
filters and op-amps together.

**This is L01's arithmetic for the third time.** A divider loaded by 10 kilohm loses a third of its
output; here two filter sections move each other's poles. In L10 an op-amp loses 11 dB the same way.

---

## A.4 LC, resonance, and Q
An inductor and a capacitor have reactances of opposite sign, so at one frequency they cancel:

$$f_0 = \frac{1}{2\pi\sqrt{LC}}$$

In series they cancel to zero impedance, in parallel to infinite. **Nothing about that frequency
depends on any resistance,** which is what makes a resonance different in kind from an RC corner.
The resistance decides only the sharpness, for a series RLC taken across the resistor:

$$Q = \frac{1}{R}\sqrt{\frac{L}{C}}, \qquad \text{bandwidth} = \frac{f_0}{Q}$$

![Band-pass magnitude for three values of Q on the same resonance, showing a broad peak at Q of one, a narrower one at Q of 3.3 and a sharp one at Q of 10, all reaching zero decibels at resonance.](./images/resonance_q.png)

**Q is two things at once, and the second is the one that gets people.** It is the sharpness of
the peak, and it is the factor by which the inductor's and the capacitor's own voltages exceed the
input: at resonance the LC is a short, so the current $V/R$ flows through a reactance $Q$ times $R$.

$$V_L = Q \times V_{in}$$

**A Q of 10 with 10 V applied puts 100 V across a capacitor.** That is how a filter correct on
paper destroys a component on a bench, and it is nowhere in the transfer function, which describes
only the output.

---

## A.5 Higher orders, and what this course does not do
Two poles is as far as this course goes, and it gets there by cascading rather than by designing.

Real design starts from a specification, picks the polynomial that meets it with the fewest poles,
and realises it as a circuit: Butterworth for a flat passband, Chebyshev for a steeper transition
at the cost of ripple, Bessel for flat group delay. L04 builds one Sallen-Key, the cheapest complex
pole pair from one amplifier. Left out: pole placement, the approximation problem, tolerance
sensitivity, switched-capacitor realisations.

---

## A.6 What this appendix is blind to
* **Component tolerance.** Every corner here is nominal. A filter of 5 per cent parts has a corner
  good to about 7 per cent, and a high-Q filter is far worse, because Q depends on a ratio of two
  square roots.
* **Real inductors.** The Q values assume the resistance is the one you put there. A real
  inductor's winding resistance is often dominant, and it caps Q where no external resistor can
  lift it.
* **Transients.** A high-Q filter rings, for roughly $Q$ cycles. This course never computes it.

---
