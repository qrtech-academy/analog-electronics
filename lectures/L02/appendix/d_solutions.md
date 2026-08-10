# Appendix D - Solutions

In full, including the plausible wrong answers.

---

## D.1 Recall: what a phasor assumes

1. **Linearity and steady state.** Linearity so that no new frequency can appear, which is what
   lets one complex number stand for the whole response; steady state so that the transient from
   switch-on has died away, because a phasor describes a sinusoid that has been going on forever.
2. **A diode has neither**, and from L05 a transistor is worse. Driven with a sinusoid a diode
   produces harmonics at every integer multiple of the input frequency, and a phasor has no way to
   express a frequency that was not in the excitation. That is why
   L04 solves nonlinear circuits by linearising repeatedly rather than by
   transforming.
3. **The colleague is measuring the transient.** Switched on at a zero crossing, the output of an
   RC low-pass takes several time constants to settle into its steady-state amplitude, and during
   that time it can be anywhere between the input amplitude and the final one. Both answers are
   right about different things, and the phasor is right about the one that lasts.

---

## D.2 Recall: reading a response

The six numbers:

|                | Magnitude                            | Phase              |
| -------------- | ------------------------------------ | ------------------ |
| A decade below | 0.04 dB down                         | 5.7 degrees of lag |
| At the corner  | 3.01 dB down                         | 45 degrees         |
| A decade above | 20.04 dB down                        | 84.3 degrees       |
| Far above      | 20 dB per decade, or 6 dB per octave | 90 degrees         |

The asymptotes are a horizontal line at 0 dB and a line falling at 20 dB per decade, and they meet
at the corner. That is why it is called the corner.

**Only two of the six need remembering: 3 dB and 45 degrees at the corner.** Everything else
follows. The 20 dB per decade is the definition of a single pole. The 0.04 dB a decade below is
$1/\sqrt{1.01}$, which is obviously almost one. The 84.3 degrees is 90 minus the 5.7, by the
symmetry of $\arctan$ about the corner.

That symmetry is worth noticing on its own: the phase curve is odd about the corner on a
logarithmic frequency axis, so whatever it has done a decade below, it has 90 degrees minus that
much left to do a decade above.

---

## D.3 Hand calculation: time constants

1. Reaching 1 per cent means $e^{-t/\tau} = 0.01$, so $t = \tau \ln 100 = 4.605\tau$. With
   $t = 5\ \mu\text{s}$, $\tau = 1.086\ \mu\text{s}$.
2. 0.01 per cent needs $\ln(10^4) = 9.21$ time constants, so **10.0 microseconds**. Exactly double,
   because $\ln(10^4)$ is twice $\ln(10^2)$; every extra factor of 100 in accuracy costs the same
   4.6 time constants.
3. $n$ bits of settling means an error below $2^{-n}$, needing $n \ln 2$ time constants. Going
   from 8 bits to 14 is a factor of **14/8 = 1.75**, and it does not depend on the time constant
   at all.
4. Doubling the bandwidth halves the time constant, so it is a factor of **2**, which more than
   covers the 1.75 the extra bits cost. Whether it is cheaper depends on what sets the bandwidth,
   and usually it is not free: a faster amplifier costs more current, and in L08 that trade is the
   whole design.

**The plausible wrong answer to part 3** is to reason that 14 bits is $2^6$ times more accurate
than 8 bits, so the time must go up by 64. It goes up by 1.75, because the settling is exponential
and accuracy is bought logarithmically. Getting that intuition the wrong way round is what makes
people over-design settling by an order of magnitude.

---

## D.4 Hand calculation: reactance and resonance

1. Equal reactances at $f = 1/(2\pi\sqrt{LC}) = 1592$ Hz.

<!-- value: 1592 = lc_resonance(10e-3, 1e-6) -->

2. The reactance there is $2\pi f L = 100$ ohm.

<!-- value: 100 = inductor_reactance(lc_resonance(10e-3, 1e-6), 10e-3) -->

3. **In series the total impedance is zero.** The reactances are equal in magnitude and opposite in
   sign, $+100j$ and $-100j$, so they cancel exactly. A series LC at resonance is a short circuit,
   and that is the entire reason resonance is interesting.
4. $Q = \sqrt{L/C}/R = 100/10 = 10$. With 1 V applied and the LC pair a short, all 1 V appears
   across the resistor and the current is 100 mA. That current through the inductor's 100 ohm of
   reactance puts **10 V across the inductor**, and $-10$ V across the capacitor.

<!-- value: 10 = series_rlc_q(10.0, 10e-3, 1e-6) -->

5. **The resonant frequency and the reactance at it would not change**; they depend on L and C
   only. **The Q and the voltage across the inductor would**, and both would go to infinity as the
   resistance went to zero. In practice the winding resistance of the inductor sets a ceiling, and
   the ceiling is usually a Q of a few hundred.

That fourth answer is the one to keep. **A Q of ten means ten times the input voltage appears
inside the circuit**, on components rated for the input. This is how a filter that works perfectly
on paper destroys a capacitor on a bench.

---

## D.5 Design: an anti-aliasing filter that has to be honest

**1. The window.** For 20 dB at 10 kHz, $|H| = 0.1$ needs $f_c \le 1005$ Hz. For 0.5 dB at 100 Hz,
$|H| \ge 0.9441$ needs $f_c \ge 286$ Hz. Both are satisfiable together, so a single pole is enough,
and the window is 286 Hz to 1005 Hz.

**2. The choice: R = 2.7 kilohm, C = 100 nF**, aiming near the middle of the window.

The source and the load both have to be in the arithmetic, and this is the part the exercise is
for:

* The 200 ohm source resistance is **in series** with R, so the capacitor sees 2.9 kilohm looking
  back, not 2.7.
* The 100 kilohm load is **in parallel** with the capacitor, so it forms a divider with the series
  resistance at every frequency including DC.

The corner is therefore set by $(2900 \parallel 100000) = 2818$ ohm, giving 565 Hz, comfortably
inside the window.

**3. What it actually achieves.**

|           | Value                                                             |
| --------- | ----------------------------------------------------------------- |
| DC gain   | 0.9718, which is 0.248 dB of loss before the filter does anything |
| At 100 Hz | 0.382 dB down, inside the 0.5 dB budget                           |
| At 10 kHz | 25.2 dB down, comfortably past the 20 dB requirement              |

Note that the load alone eats half the 0.5 dB budget at DC. A design that computed the corner and
declared victory would have missed it.

**4. If the requirement became 40 dB at 10 kHz**, a single pole needs $f_c \le 100$ Hz, and 100 Hz
is below the 286 Hz that the passband requirement demands. **No single-pole filter can do it.** The
answer is a second pole, and the honest way to get one is L03's: two sections with something
between them, because two sections cascaded directly do not give what they look like they give.

---

## D.6 Code: the complex stamps

No implementation is published; the suite is the answer.

The one hint worth giving: if templating the L01 elimination was hard, the cause is nearly always
the pivot search. `std::fabs` takes a `double`. `std::abs` is overloaded for `std::complex` and
returns the magnitude, which is exactly the right thing to pivot on. Change that one call and the
rest usually compiles unchanged.

---

## D.7 Code: the sweep

Also unpublished, with two hints:

* **Logarithmic spacing** is `first * std::pow(last / first, i / (points - 1.0))`, and the
  `points - 1.0` is what makes the last point land exactly on `last` rather than short of it.
* **Guard `points == 1`** before that expression divides by zero. Returning a single point at
  `first` is the sensible answer and the one the suite expects.

---

## D.8 Cross-check: the filter that is not where you put it

| Leg                           | Corner frequency |
| ----------------------------- | ---------------- |
| 1. By hand, the obvious way   | 1001 Hz          |
| 2. By hand, thinking about it | 151 Hz           |
| 3. By the solver              | 151 Hz           |

<!-- value: 1001 = rc_corner(1e3, 159e-9) -->
<!-- value: 151 = rc_corner(divider_output_resistance(33e3, 6.8e3) + 1e3, 159e-9) -->

**Leg 1 is wrong by a factor of 6.6, and it is wrong in the direction that matters.** It says the
filter passes everything up to a kilohertz. The filter is in fact 16.5 dB down at a kilohertz.

<!-- value: 16.5 = -decibels(abs(first_order_response(rc_corner(1e3, 159e-9), rc_corner(divider_output_resistance(33e3, 6.8e3) + 1e3, 159e-9)))) -->

**Why.** The capacitor does not know which resistor was drawn as "the filter". It sees the total
resistance looking back into the network, which is the 1 kilohm in series with the divider's
Thevenin resistance:

$$R_{seen} = 1000 + (33000 \parallel 6800) = 1000 + 5638 = 6638\ \Omega$$

$$f_c = \frac{1}{2\pi \times 6638 \times 159\ \text{nF}} = 151\ \text{Hz}$$

**Legs 2 and 3 agree** because they are the same circuit. The residual difference is how finely
you swept; at 50 points per decade the corner is located to better than 1 per cent.

**The low-frequency output is 1.71 V, not 10 V.** At low frequency the capacitor is an open
circuit, so no current flows through the 1 kilohm series resistor, so it drops nothing, and the
output is simply the unloaded divider from L01. The series resistor is invisible at DC and
dominant at high frequency, which is a compact statement of what a filter is.

<!-- value: 1.71 = divider(10.0, 33e3, 6.8e3) -->

**Diagnosing a wrong leg 3:**

* **1001 Hz** means the divider is missing from the netlist, or its resistors are stamped between
  nodes that are not in the signal path. Check `resistorCount()` and the node numbers.
* **10 V at low frequency** means the divider is shorted: most likely the supply is stamped
  directly onto the output node.
* **A corner near 159 Hz rather than 151** is not an error. That is what you get if you take the
  Thevenin resistance as 5.6 kilohm rather than 5638 ohm, and it is a 5 per cent difference from
  rounding a resistance to two significant figures.

**The lesson, for the third time in two lectures.** What a stage does depends on what is attached
to it on both sides. L01 met it as a divider losing a third of its output;
L03 meets it again as two filter sections that do not give the corner they
were designed for; L10 meets it as an amplifier losing 11 dB of open-loop gain. It is the same
arithmetic every time, and it is the single most common reason a circuit that was right on paper
is wrong on the bench.

---
