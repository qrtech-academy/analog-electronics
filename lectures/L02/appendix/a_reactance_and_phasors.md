# Appendix A - Reactance, time constants, and phasors

Two new devices, one trick, and the frequency domain falls out of the trick rather than being
imposed on top of it.

---

## A.1 Two devices that remember

A resistor's current depends on the voltage across it now. That is the whole of L01.

A capacitor's current depends on how fast the voltage is changing:

$$I = C \frac{dV}{dt}$$

An inductor's voltage depends on how fast its current is changing:

$$V = L \frac{dI}{dt}$$

Both are devices with memory. A capacitor holding 5 V holds it because of everything that has
happened to it, not because of anything happening now, and that is why a circuit containing one
cannot be solved by the method of L01. There is no single answer; there is a trajectory.

The two are duals of each other, and every result about one has a mirror image about the other.
This course leans on the capacitor, because a capacitor is cheap, accurate and small, and an
inductor is none of those things. Inductors appear in L03's filters and then almost nowhere else.

---

## A.2 The time constant

Charge a capacitor through a resistor from a step of $V_0$ and the voltage approaches it
exponentially:

$$V(t) = V_0 \left( 1 - e^{-t/\tau} \right), \qquad \tau = RC$$

One time constant reaches 63.2 per cent. Five reach 99.33 per cent. That much is usually
remembered. What is usually not:

| Accuracy wanted | Time constants needed |
| --------------- | --------------------- |
| 10 per cent     | 2.3                   |
| 1 per cent      | 4.6                   |
| 0.1 per cent    | 6.9                   |
| 0.01 per cent   | 9.2                   |

The rule is $n = \ln(1/\epsilon)$, so every further decade of accuracy costs 2.3 more time
constants. That is a slow way to buy precision, and it is the reason a settling specification is
usually the thing that decides how fast a circuit can be run.

The important habit is to stop thinking of a time constant as "the time it takes" and start
thinking of it as "the time it takes to get $e$ times closer".

---

## A.3 The trick, and what it depends on

Solving a circuit with capacitors in the time domain means differential equations. The frequency
domain avoids them, and the argument is worth understanding rather than accepting.

**In a linear circuit driven by a sinusoid, every voltage and current in it is a sinusoid at the
same frequency.** Nothing can create a new frequency, because every element's response is
proportional to its excitation. So the only things that can differ between one node and another
are amplitude and phase.

A complex number carries exactly those two things. Write the excitation as $V e^{j\omega t}$, and
every response is $A e^{j(\omega t + \phi)}$ for some $A$ and $\phi$. The common factor
$e^{j\omega t}$ then cancels out of every equation, and what remains is algebra on complex
amplitudes called **phasors**.

The differentiation is what makes it pay. If $v(t) = V e^{j\omega t}$ then

$$\frac{dv}{dt} = j\omega V e^{j\omega t}$$

so **differentiation becomes multiplication by $j\omega$**. The capacitor's differential equation
becomes $I = j\omega C V$, which is Ohm's law with a complex conductance.

**What it depends on.** Linearity, and the steady state. A circuit containing a diode has no
phasor description at all, because a diode creates harmonics that were not in the excitation; that
is why L04 has to solve nonlinear circuits a different way, and why L07
linearises a transistor before daring to use a phasor near one. And a phasor says nothing about
what happens in the first few time constants after switch-on, because it describes the steady
state only.

---

## A.4 Impedance

With that substitution, both new devices have an Ohm's law:

$$Z_C = \frac{1}{j\omega C}, \qquad Z_L = j\omega L$$

The magnitudes are the **reactances**, and they are what a meter would read:

$$|Z_C| = \frac{1}{2\pi f C}, \qquad |Z_L| = 2\pi f L$$

A capacitor's impedance falls with frequency and an inductor's rises, both at six decibels per
octave, and a resistor's does neither.

![Impedance magnitude against frequency for a 1 kilohm resistor, a 1 microfarad capacitor and a 10 millihenry inductor, on logarithmic axes. The resistor is a horizontal line, the capacitor falls and the inductor rises, and the inductor and capacitor cross at 1592 hertz.](./images/reactance.png)

The three crossings in that figure are three different things, and keeping them apart is most of
what L03 is about:

* **R crosses C** at 159 Hz. That is an RC corner, and it depends on the resistor.
* **R crosses L** at 15.9 kHz. That is an RL corner, and it depends on the resistor too.
* **L crosses C** at 1592 Hz. That is a **resonance**, and it is the only one of the three that
  does not depend on any resistor at all.

The $j$ matters as much as the magnitude. A capacitor's current *leads* its voltage by 90 degrees
and an inductor's *lags* by 90 degrees, and it is the sign of that angle, not the size of the
reactance, that decides whether a feedback loop is stable.

---

## A.5 The first-order response

Put a resistor and a capacitor in series and take the output across the capacitor, and the divider
formula of L01 still applies, with impedances instead of resistances:

$$H(j\omega) = \frac{Z_C}{R + Z_C} = \frac{1}{1 + j\omega RC}$$

Define the **corner frequency** as the frequency where the reactance equals the resistance:

$$f_c = \frac{1}{2\pi RC}$$

For 1 kilohm and 159 nanofarads that is 1001 Hz.

<!-- value: 1001 = rc_corner(1e3, 159e-9) -->

![Two panels. On the left, the magnitude of a first-order low-pass against frequency normalised to its corner, flat then falling at twenty decibels per decade, with the exact curve and its two straight-line asymptotes and a marker three decibels down at the corner. On the right, the phase falling from zero to minus ninety degrees, passing minus forty five at the corner.](./images/rc_bode.png)

Everything worth knowing about that response is in four numbers:

| At                        | Magnitude                | Phase        |
| ------------------------- | ------------------------ | ------------ |
| A decade below the corner | 0.04 dB down             | 5.7 degrees  |
| The corner                | 3.01 dB down             | 45 degrees   |
| A decade above            | 20.04 dB down            | 84.3 degrees |
| Far above                 | falling 20 dB per decade | 90 degrees   |

The magnitude is two straight lines and a corner, and drawing it from the corner frequency alone
is a skill worth having.

**The phase is the half that gets skipped.** A decade below the corner the magnitude has lost
0.04 dB, which is nothing, and the phase has already moved 5.7 degrees, which is not. In a
feedback loop the magnitude decides whether the loop has gain left and the phase decides whether
that gain is helping or hurting, and L04 needs both.

---

## A.6 Decibels, briefly

A decibel is a ratio on a logarithmic scale. For a voltage ratio:

$$A_{dB} = 20 \log_{10} \left| \frac{V_{out}}{V_{in}} \right|$$

The factor is 20 rather than 10 because power goes as voltage squared, and the decibel was defined
for power. Everything in this course is a voltage ratio, so it is always 20.

Six values are worth knowing by sight, because they cover most of what a plot ever shows:

| Ratio      | Decibels |
| ---------- | -------- |
| 1          | 0        |
| $\sqrt{2}$ | 3.01     |
| 2          | 6.02     |
| 10         | 20       |
| 100        | 40       |
| 1000       | 60       |

The one that matters most is the second: the corner of a filter is where it is 3 dB down, which is
where the output amplitude is $1/\sqrt{2}$ of the input and the output *power* is half.

---

## A.7 The transformer, briefly

Two coils sharing a magnetic circuit. The voltage ratio is the turns ratio, the current ratio is
its inverse, and an impedance on the secondary appears on the primary multiplied by the turns
ratio squared.

$$\frac{V_2}{V_1} = \frac{N_2}{N_1}, \qquad Z_{reflected} = \left(\frac{N_1}{N_2}\right)^2 Z_2$$

That last one is the only part this course uses, and it uses it once: it is the cleanest example
of impedance transformation, which is what the emitter follower of L08 does by a completely
different mechanism and for the same reason.

**Where the model stops being true**, which is quickly: real transformers have leakage inductance,
winding resistance, a finite magnetising inductance that shorts the primary at low frequency, and
a core that saturates. None of that is in the ratio above, and all of it decides whether a design
works. This course does not pursue it.

---

## A.8 What this appendix is blind to

* **Transients.** Everything here is steady state. What a filter does in the first few time
  constants after a step is a different calculation, and this course never makes it.
* **Real components.** A capacitor has series resistance and series inductance, so its impedance
  stops falling somewhere and starts rising again; a real 1 microfarad part is inductive above a
  few megahertz. An inductor has winding resistance and self-capacitance and does the same in
  reverse.
* **Distributed effects.** At high enough frequency a wire is not a node. That boundary is well
  outside anything in this course, and well inside the working range of a modern transistor.

---
