# Appendix D - Solutions

In full, including the plausible wrong answers.

---

## D.1 Recall: what the loop gain decides

1. $A_{CL} = \frac{1}{\beta}\left(1 - \frac{1}{1+T}\right)$ with $T = A\beta$. The gain falls
   short of the ideal $1/\beta$ by one part in $1 + T$.
2. Four of them:

| Quantity         | Effect of $1 + T$               |
| ---------------- | ------------------------------- |
| Gain error       | Divided                         |
| Distortion       | Divided                         |
| Output impedance | Divided, for voltage sensing    |
| Input impedance  | Multiplied, for series feedback |

3. **Noise generated at the input**, because it arrives at the same place as the signal and is
   amplified identically; the loop cannot tell them apart. **Offset**, for the same reason. Also
   **output swing**: no amount of feedback gets more volts out of an amplifier than its rails
   allow.
4. **The loop gain collapses to zero**, because a clipped amplifier's incremental gain is zero and
   $T = A\beta$. So the distortion at that moment is the amplifier's raw open-loop distortion,
   undivided. **Feedback stops working exactly when it would be most useful**, which is why a
   clipping amplifier sounds far worse than its distortion specification suggests.

---

## D.2 Recall: the diode

1. **60 mV**, from $V_T \ln 10 = 0.026 \times 2.303 = 59.9$ mV.
2. $r = V_T/I = 26$ ohm. **It is the same quantity as $r_e$**, the intrinsic emitter resistance
   that the whole of Part 2 is built on, and it is the same for the same reason: a base-emitter
   junction is a diode.
3. The drop is a constant 0.65 V once conducting and the device is open otherwise. **It is exact
   at exactly one current:** the one at which the real diode happens to sit at 0.65 V, which for
   $I_S = 10^{-14}$ A is about 0.72 mA.
4. **It does not matter** in a bias network where the drop is subtracted from a supply of several
   volts, because a 240 mV error in a 10 V subtraction is a few per cent. **It matters completely**
   wherever the drop appears inside an exponential, which is L06's thermal drift: at 60 mV to the
   decade, 240 mV is four decades of current.

---

## D.3 Hand calculation: how much gain do you need

1. 0.1 per cent error needs $1/(1+T) = 10^{-3}$, so $T = 999$, call it **1000**.
2. $A = T/\beta = T \times A_{CL} = 1000 \times 100 = 10^5$.
3. **At DC, just barely.** $A = 10^5$ gives exactly $T = 1000$ and 0.1 per cent, with no margin
   for the open-loop gain being lower than typical, which it usually is.

   **At 1 kHz, no.** With a 1 MHz gain-bandwidth product the open-loop gain at 1 kHz is only
   $10^6/10^3 = 1000$, so $T = 10$ and the error is 9 per cent.
4. 1 per cent error needs $T = 99$, so $A = 9900$, which the amplifier reaches at
   $10^6/9900 = 101$ Hz.

**The lesson, and the plausible wrong answer.** It is tempting to check the accuracy at DC, find
it acceptable, and stop. The bandwidth over which it is acceptable is about 100 Hz, on an
amplifier whose datasheet says 1 MHz. **Closed-loop accuracy has a bandwidth of its own, and it is
much narrower than the closed-loop bandwidth.**

---

## D.4 Hand calculation: the diode at two currents

**1. One kilohm.** Start at 0.65 V: the current would be $(5-0.65)/1000 = 4.35$ mA, and the diode
needs $V_T \ln(I/I_S) = 0.026 \ln(4.35\times10^{-3}/10^{-14}) = 0.697$ V for that. Repeat with
0.697 V: current $(5-0.697)/1000 = 4.303$ mA, needing 0.6965 V. Converged.

$$V_D = 0.697\ \text{V}, \qquad I = 4.30\ \text{mA}$$

**2. One hundred kilohm.** The same two steps give

$$V_D = 0.578\ \text{V}, \qquad I = 44.2\ \mu\text{A}$$

**3. Against the constant-drop model.**

| Resistor   | Real            | Model          | Error         |
| ---------- | --------------- | -------------- | ------------- |
| 1 kilohm   | 4.303 mA        | 4.35 mA        | +1.1 per cent |
| 100 kilohm | 44.22 microamps | 43.5 microamps | -1.6 per cent |

**The sign reverses**, because 0.65 V is below the real drop at the higher current and above it at
the lower one.

**4. Why the current error stays small.** The diode voltage is subtracted from 5 V. An error of
50 mV in a subtraction that leaves 4.3 V is about 1 per cent, and it cannot be more than the ratio
of the voltage error to the supply. The diode voltage error is not bounded that way: it is
whatever the exponential says, and across this range it is 119 mV. Widen the range to the
Cross-check's 10 megohm and it becomes 240.

**Which one L06 cares about.** The current, at first: a bias network sets a collector current and
gets it right to a few per cent with a constant drop. But L06's real subject is what happens when
temperature moves that drop by 2 mV per degree, and 2 mV inside an exponential is 8 per cent of
current per degree. **The constant-drop model can find the operating point and can say nothing
whatever about its stability.**

---

## D.5 Design: a half-wave rectifier with a stated ripple

**1. The capacitor: 470 microfarads.**

The output is about 11.3 V into 1 kilohm, so 11.3 mA. Between peaks the capacitor supplies all of
it, for one full period of 20 ms, because half-wave rectification recharges once per cycle:

$$C = \frac{I \Delta t}{\Delta V} = \frac{11.3\ \text{mA} \times 20\ \text{ms}}{0.5\ \text{V}} = 452\ \mu\text{F}$$

so 470 microfarads, which gives 0.48 V of ripple.

**The assumption is that the load current is constant during the discharge**, which it is not: as
the output falls the current falls with it. That makes the answer **pessimistic**, so the real
ripple is slightly less than calculated, and erring that way is the right direction.

**2. The DC output is about 11.3 V**, not 12: one diode drop below the peak, and the drop is
nearer 0.7 V than 0.65 at 11 mA.

**3. The peak diode current is about 0.5 amps**, which is **44 times the load current**.

The reason is that the capacitor is recharged in a short burst near the peak of each cycle. The
conduction angle is roughly $\sqrt{2\Delta V/V_{pk}} = 0.28$ radians, which at 50 Hz is 0.9 ms out
of 20. All 226 microcoulombs the load will take over the whole cycle has to be delivered in that
0.9 ms, and a triangular pulse of that charge and duration peaks at half an amp.

**4. Doubling the capacitor halves the ripple and raises the peak current** by about $\sqrt{2}$,
because the conduction angle narrows as the square root of the ripple while the charge stays the
same.

**So the approach does not scale.** Every factor of two of ripple reduction costs 40 per cent more
peak current, in the diode, in the transformer winding and in the capacitor's own ripple-current
rating. Beyond a point the answer is a regulator rather than a bigger capacitor, and that is why
every real supply has one.

---

## D.6 Code: feedback and the diode model

Unpublished; the suite is the answer.

The hint that matters is in `limit`. **Damp only steps that are increasing and larger than two
thermal voltages.** A decreasing step is heading away from the exponential's steep region and
damping it slows convergence for no benefit. Damping every step makes the solver look like it
works, take twice as many iterations as it should, and the reason will not be obvious.

---

## D.7 Code: the nonlinear solve

Unpublished. The three checks in the exercise are the ones worth insisting on, and the third is
the one people skip: **turn the limiting off and confirm it takes about 170 iterations.** If it
does not, the limiting was never doing anything, and the solver will fail on the first transistor
circuit in L06 rather than here where it is easy to diagnose.

One structural hint: recompute the diode stamps each iteration and re-solve, rather than building
a fresh matrix from nothing. The linear part of the matrix does not change between iterations, and
noticing that is what stops the loop being slow.

---

## D.8 Cross-check: the diode, and the model that is nearly right

| Point          | Leg 1, constant drop | Leg 2, by hand  | Leg 3, solver   | Leg 1 error   |
| -------------- | -------------------- | --------------- | --------------- | ------------- |
| 5 V, 1 kilohm  | 4.350 mA             | 4.303 mA        | 4.303 mA        | +1.1 per cent |
| 5 V, 10 megohm | 0.435 microamps      | 0.454 microamps | 0.454 microamps | -4.2 per cent |

**Legs 2 and 3 agree to six significant figures.** They solve the same transcendental equation.

**Leg 1's error reverses sign**, and that is the result to keep. The constant-drop model is exact
at one current and wrong either side, so its error is not a bias that can be corrected for; it is
a function of where you are operating.

**The diode voltage disagrees far more than the current does.** 0.697 V and 0.458 V against a
model that says 0.65 V both times. That is a 240 mV spread in a quantity the model calls constant,
and it is invisible in the current because the current is set by a subtraction from 5 V.

**The 1 V experiment.** With a 1 V supply and 100 ohm, the constant-drop model gives 3.50 mA and
the real answer is 3.12 mA, an error of **12.2 per cent**.

Nothing about the diode changed. What changed is that the drop is now most of the supply, so the
subtraction no longer buries the error. **The constant-drop model is accurate when the diode drop
is small compared with what it is subtracted from, and not otherwise**, and that is a much more
useful statement of its validity than "it is accurate to about a per cent".

It also says exactly why Part 2 cannot use it for everything. Inside a transistor's base-emitter
loop the drop *is* the whole story: there is nothing else in that loop to subtract it from. L06
computes bias currents with the constant drop and computes drift from the exponential, and now the
reason is arithmetic rather than assertion.

**Diagnosing the solver:**

* **170 iterations** means the limiting is not being applied.
* **`converged` false after 100** usually means the limiting is inverted and is damping decreasing
  steps, so the iterate oscillates instead of settling.
* **A NaN** means the exponential overflowed, which happens if a proposed voltage of several volts
  is evaluated before being limited rather than after.

---
