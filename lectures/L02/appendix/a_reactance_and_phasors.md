# Appendix A - Reactance, time constants, and phasors
Two new devices and one trick; the frequency domain falls out of the trick rather than being
imposed on top of it.

---

## A.1 Two devices that remember
A resistor's current depends on the voltage across it now. That is the whole of L01. A capacitor
and an inductor depend on a rate of change instead:

$$I = C \frac{dV}{dt}, \qquad V = L \frac{dI}{dt}$$

**Both have memory,** so a circuit containing one has no single answer, only a trajectory, and the
method of L01 cannot solve it. The two are duals. This course leans on the capacitor, which is
cheap, accurate and small; inductors appear in L03's filters and then almost nowhere.

---

## A.2 The time constant
$$V(t) = V_0 \left( 1 - e^{-t/\tau} \right), \qquad \tau = RC$$

One time constant reaches 63.2 per cent, five reach 99.33 per cent. What is usually forgotten:

| Accuracy wanted | Time constants needed |
| --------------- | --------------------- |
| 10 per cent     | 2.3                   |
| 1 per cent      | 4.6                   |
| 0.1 per cent    | 6.9                   |
| 0.01 per cent   | 9.2                   |

$n = \ln(1/\epsilon)$, so each further decade of accuracy costs 2.3 more time constants. **A time
constant is not the time it takes, but the time it takes to get $e$ times closer.**

---

## A.3 The trick, and what it depends on
**In a linear circuit driven by a sinusoid, every voltage and current in it is a sinusoid at the
same frequency.** Nothing can create a new one, so only amplitude and phase differ from node to
node, and a complex number carries exactly those two. Write the excitation as $V e^{j\omega t}$,
the common factor cancels from every equation, and what remains is algebra on **phasors**.

$$\frac{dv}{dt} = j\omega V e^{j\omega t}$$

**Differentiation becomes multiplication by $j\omega$,** so $I = C\,dV/dt$ becomes
$I = j\omega C V$: Ohm's law with a complex conductance.

**It depends on linearity and on the steady state.** A diode has no phasor description at all,
because it creates harmonics that were not in the excitation. That is why L04 solves nonlinear
circuits a different way, and why L07 linearises a transistor before putting a phasor near one.

---

## A.4 Impedance
$$Z_C = \frac{1}{j\omega C}, \qquad Z_L = j\omega L$$

The magnitudes are the **reactances**, and they are what a meter would read:

$$|Z_C| = \frac{1}{2\pi f C}, \qquad |Z_L| = 2\pi f L$$

![Impedance magnitude against frequency for a 1 kilohm resistor, a 1 microfarad capacitor and a 10 millihenry inductor, on logarithmic axes. The resistor is a horizontal line, the capacitor falls and the inductor rises, and the inductor and capacitor cross at 1592 hertz.](./images/reactance.png)

A capacitor's impedance falls with frequency and an inductor's rises, both at six decibels per
octave. The three crossings are three different things, and keeping them apart is most of L03:
* **R crosses C** at 159 Hz: an RC corner, set by the resistor.
* **R crosses L** at 15.9 kHz: an RL corner, set by the resistor too.
* **L crosses C** at 1592 Hz: a **resonance**, set by no resistor at all.

**The $j$ matters as much as the magnitude.** A capacitor's current leads its voltage by 90
degrees and an inductor's lags; that sign decides whether a feedback loop is stable.

---

## A.5 The first-order response
The L01 divider formula still applies, with impedances instead of resistances:

$$H(j\omega) = \frac{Z_C}{R + Z_C} = \frac{1}{1 + j\omega RC}$$

The **corner frequency** is where the reactance equals the resistance:

$$f_c = \frac{1}{2\pi RC}$$

For 1 kilohm and 159 nanofarads that is 1001 Hz.

<!-- value: 1001 = rc_corner(1e3, 159e-9) -->

![Two panels. On the left, the magnitude of a first-order low-pass against frequency normalised to its corner, flat then falling at twenty decibels per decade, with the exact curve and its two straight-line asymptotes and a marker three decibels down at the corner. On the right, the phase falling from zero to minus ninety degrees, passing minus forty five at the corner.](./images/rc_bode.png)

| At                        | Magnitude                | Phase        |
| ------------------------- | ------------------------ | ------------ |
| A decade below the corner | 0.04 dB down             | 5.7 degrees  |
| The corner                | 3.01 dB down             | 45 degrees   |
| A decade above            | 20.04 dB down            | 84.3 degrees |
| Far above                 | falling 20 dB per decade | 90 degrees   |

The magnitude is two straight lines and a corner, and drawing it from $f_c$ alone is a skill.

**The phase is the half that gets skipped.** A decade below the corner the magnitude has lost
0.04 dB, which is nothing, and the phase has moved 5.7 degrees, which is not. The magnitude says
whether a loop has gain left; the phase says whether that gain helps or hurts. L04 needs both.

---

## A.6 Decibels, briefly
$$A_{dB} = 20 \log_{10} \left| \frac{V_{out}}{V_{in}} \right|$$

The factor is 20 rather than 10 because the decibel was defined for power and power goes as
voltage squared. Every ratio in this course is a voltage ratio, so it is always 20.

| Ratio      | Decibels |
| ---------- | -------- |
| 1          | 0        |
| $\sqrt{2}$ | 3.01     |
| 2          | 6.02     |
| 10         | 20       |
| 100        | 40       |
| 1000       | 60       |

**The second row is the one that matters:** a filter's corner is where it is 3 dB down, which is
$1/\sqrt{2}$ in amplitude and half in power.

---

## A.7 The transformer, briefly
Two coils sharing a magnetic circuit. The voltage ratio is the turns ratio, the current ratio its
inverse, and an impedance on the secondary is reflected to the primary by the ratio squared.

$$\frac{V_2}{V_1} = \frac{N_2}{N_1}, \qquad Z_{reflected} = \left(\frac{N_1}{N_2}\right)^2 Z_2$$

The course uses the second form once, as the cleanest example of impedance transformation, which
is what L08's emitter follower does by a completely different mechanism for the same reason.

**The model stops being true quickly:** real transformers have leakage inductance, winding
resistance, a finite magnetising inductance that shorts the primary at low frequency, and a core
that saturates. All of that decides whether a design works, and none of it is in the ratio above.

---

## A.8 What this appendix is blind to
* **Transients.** Everything here is steady state. What a filter does in the first few time
  constants after a step is a calculation this course never makes.
* **Real components.** A capacitor has series resistance and inductance, so its impedance stops
  falling and starts rising: a real 1 microfarad part is inductive above a few megahertz.
* **Distributed effects.** At high enough frequency a wire is not a node. That boundary is outside
  this course and inside the working range of a modern transistor.

---
