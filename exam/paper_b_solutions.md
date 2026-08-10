# Analog Electronics - Paper B, Model Answers

Marked out of 100. Marks are shown per part. **Where a question says "derive", the working carries
the marks and a stated result scores nothing.** Several parts carry no arithmetic at all; they are
not worth fewer marks for it, and a paper marked only on the numbers would pass a candidate who has
understood none of the course.

---

## Question 1 - Where a source resistance comes from (10 marks)

### (a) The Thevenin equivalent, derived (3 marks)

**Open-circuit voltage.** With nothing connected, the same current flows through both resistors, so

$$V_{oc} = V_{supply}\frac{R_2}{R_1 + R_2}$$

**(1 mark.)**

**Source resistance.** Look back into the output terminal with every independent source set to
zero. An ideal voltage source set to zero is a short circuit, because a source that holds zero
volts whatever current flows through it *is* a short. With the supply shorted, $R_1$ runs from the
output node to ground and so does $R_2$:

$$R_{th} = R_1 \parallel R_2 = \frac{R_1 R_2}{R_1 + R_2}$$

**(2 marks: 1 for the answer, 1 for justifying the shorting rather than asserting it.)**

**Why that is legitimate.** The source resistance is defined as $\partial V/\partial I$ at the
terminal, and a fixed source contributes nothing to a *derivative*. Setting it to zero is not an
approximation; it is what differentiating means for a linear network.

### (b) Superposition (3 marks)

**The principle.** In a linear network the response to several independent sources acting together
is the sum of the responses to each acting alone. **(1 mark.)**

**The condition is linearity**: every element's response must be proportional to its excitation.
Resistors, capacitors and inductors qualify; a diode, a transistor's exponential and anything with
a product of two signals in it do not. **(1 mark.)**

**While one source acts, replace the others by their internal resistances:** voltage sources by
short circuits, current sources by open circuits.

**Power does not superpose.** Power in a resistor is $V^2/R$, and

$$(V_1 + V_2)^2 = V_1^2 + V_2^2 + 2V_1V_2$$

The cross term is not zero, so the total power is not the sum of the individual powers. **Power is
a quadratic function of the response, and superposition applies only to linear ones.** **(1 mark.
This is the whole answer and it fits in one equation.)**

### (c) Maximum power transfer (2 marks)

$$P = I^2 R_L = \left(\frac{V}{R_s + R_L}\right)^2 R_L$$

Differentiating with respect to $R_L$ and setting the result to zero:

$$\frac{dP}{dR_L} = V^2\frac{(R_s + R_L)^2 - 2R_L(R_s + R_L)}{(R_s + R_L)^4} = 0
\Rightarrow R_s + R_L = 2R_L \Rightarrow \boxed{R_L = R_s}$$

At that point the two resistances drop equal voltages, so **the efficiency is 50 per cent**: as
much power is burnt in the source as delivered to the load. **(1 mark.)**

**Almost nothing in this course is designed that way**, because a circuit that throws away half its
power to maximise the absolute quantity delivered is optimising the wrong thing. Voltage
amplification wants $R_L \gg R_s$, which delivers less power and more signal.

**The two situations where matching is right** are **radio-frequency work**, where an unmatched
line reflects and the reflection is the problem rather than the loss, and **anything where the
source's power is fixed and small**, such as an antenna or a transducer, where there is no more to
be had and efficiency is meaningless. **(1 mark.)**

### (d) When the colleague is right (2 marks)

They are right when $R_L \gg R_{th}$, and the useful form is the ratio:

$$\text{fraction retained} = \frac{R_L}{R_L + R_{th}} = \frac{1}{1 + R_{th}/R_L}$$

so the error is about $R_{th}/R_L$ for small ratios. A megohm on a few kilohm is a ratio of about
500, so the error is 0.2 per cent and they are right. **(1 mark.)**

**At a ratio of 2**, the node retains $2/3$ and the error is **33 per cent**. **(1 mark.)**

**The argument is not wrong; it is unquantified.** The same sentence is correct at a ratio of 500
and catastrophic at 2, and it contains nothing that distinguishes them. That is why this course
computes the ratio every time rather than judging it.

---

## Question 2 - Why a corner is a corner (9 marks)

### (a) The corner, derived (3 marks)

$$H(j\omega) = \frac{1/j\omega C}{R + 1/j\omega C} = \frac{1}{1 + j\omega RC}$$

$$|H| = \frac{1}{\sqrt{1 + (\omega RC)^2}} = \frac{1}{\sqrt2}
\Rightarrow \omega RC = 1 \Rightarrow \boxed{f_c = \frac{1}{2\pi RC}}$$

**(2 marks.)**

**The condition is that the capacitor's reactance equals the resistance.** $X_C = 1/\omega C$, and
setting $X_C = R$ gives the same $\omega = 1/RC$. That is what a corner *is*: the frequency at
which the two impedances in the divider are equal, so the output is the input divided by $\sqrt2$
and shifted by 45 degrees. **(1 mark.)**

**Phase:** $\arg H = -\arctan(\omega RC)$, which is $\mathbf{-45}$ degrees at the corner and tends
to $\mathbf{-90}$ degrees far above it.

### (b) Why complex (2 marks)

**Because a capacitor's current and voltage are not proportional; they are related by a
derivative.** For a sinusoid, differentiating multiplies by $\omega$ and advances the phase by 90
degrees, and $j$ is exactly "multiply by one, rotate by 90 degrees". So the imaginary unit encodes
**the quarter-cycle phase relationship**, and writing the impedance as a complex number lets a
differential equation be solved with the algebra of a resistor divider. **(1 mark.)**

$$Z_L = j\omega L, \qquad Z_C = \frac{1}{j\omega C} = -\frac{j}{\omega C}$$

**The signs are opposite**, so in an inductor the current **lags** the voltage and in a capacitor
it **leads**. That opposition is why they can cancel, which is resonance. **(1 mark.)**

### (c) Resonance and Q (2 marks)

$$X_L = X_C \Rightarrow \omega L = \frac{1}{\omega C} \Rightarrow \omega^2 = \frac{1}{LC}
\Rightarrow \boxed{f_0 = \frac{1}{2\pi\sqrt{LC}}}$$

**(1 mark.)**

$$Q = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}}$$

**Q is the ratio of energy stored to energy dissipated per radian of oscillation.** Equivalently it
is the ratio of the resonant frequency to the $-3$ dB bandwidth, and it is why the voltage across
either reactance at resonance is Q times the applied voltage: that voltage is the store, not a
gain. **(1 mark.)**

### (d) The transformer (2 marks)

|                               | Factor         |
| ----------------------------- | -------------- |
| Voltage                       | $\times N$     |
| Current                       | $\times 1/N$   |
| Impedance seen at the primary | $\times 1/N^2$ |

**The third follows from the first two.** An impedance $Z$ on the secondary carries $V_s/Z$. The
primary supplies $N$ times that current at $1/N$ times that voltage, so

$$Z_{primary} = \frac{V_p}{I_p} = \frac{V_s/N}{N I_s} = \frac{1}{N^2}\cdot\frac{V_s}{I_s}
= \frac{Z}{N^2}$$

**(1 mark for the table, 1 for the derivation.)**

**Two things a real transformer does:** any two of leakage inductance (flux that does not couple),
winding resistance, core loss, magnetising current (a finite primary inductance, so it will not
pass DC and rolls off at low frequency), and saturation.

---

## Question 3 - Cascades, virtual shorts, and what an op-amp assumes (11 marks)

### (a) Why the loaded cascade is worse (4 marks)

**Without algebra:** the second section is a load on the first. At any frequency where the second
section's input impedance is comparable with the first section's output impedance, the two form a
divider, and the first section delivers less than it would into an open circuit. That loss grows
with frequency, because the second section's shunt capacitor's reactance falls. So the combined
response is lower everywhere above DC, and the frequency at which it reaches $-3$ dB comes sooner.
**The mechanism is loading**, and it is the same one as Question 1. **(2 marks.)**

**For $n$ identical buffered sections:**

$$|H| = \left(\frac{1}{\sqrt{1 + (f/f_c)^2}}\right)^{n} = \frac{1}{\sqrt2}
\Rightarrow f_{-3} = f_c\sqrt{2^{1/n} - 1}$$

**(1 mark.)**

| $n$ | Factor | With $f_c = 1001$ Hz |
| --- | ------ | -------------------- |
| 2   | 0.644  | 644 Hz               |
| 3   | 0.510  | 510 Hz               |

**(1 mark.)**

**Note that even buffered, cascading lowers the corner.** Two sections at 1001 Hz do not give a
corner at 1001 Hz with a steeper slope; they give 644 Hz. Loading then takes it further, to 375 Hz.
Both effects are real and they are different effects.

### (b) The two assumptions (3 marks)

1. **The open-loop gain is infinite.**
2. **The input current is zero**, so the input resistance is infinite.

**(1 mark.)**

**The virtual short, derived.** The output is $A(V_+ - V_-)$. For the output to be finite with $A$
infinite, $V_+ - V_-$ must be zero, so $V_+ = V_-$. The inputs are at the same voltage without
being connected, which is why it is a virtual short and not a short: no current flows between them.
**(1 mark. An answer that asserts $V_+ = V_-$ without the limiting argument gets nothing: the point
is that it is a *consequence* of the gain, and it fails exactly when the gain does.)**

**The gain assumption fails first**, and its failure has a name in this course: the **gain error**,
one part in one plus the loop gain. It fails at every frequency (the gain rolls off), at every
signal level (finite output swing) and at every closed-loop gain (the loop gain falls as the
closed-loop gain rises). The input-current assumption fails much more gently, as an input bias
current of tens of nanoamps. **(1 mark.)**

### (c) The inverting configuration (2 marks)

With $V_+$ grounded, the virtual short puts $V_-$ at ground too. No current enters the input, so
all the current through $R_{in}$ continues through $R_f$:

$$\frac{V_{in} - 0}{R_{in}} = \frac{0 - V_{out}}{R_f}
\Rightarrow \boxed{A = -\frac{R_f}{R_{in}}}$$

**The virtual short set $V_- = 0$** and **the zero input current** let the two currents be equated.
**(1 mark.)**

**The input resistance is $R_{in}$**, not infinity, because the source does not drive the op-amp's
input; it drives the left end of $R_{in}$, whose right end is held at ground by the loop. The
op-amp's own input resistance is behind that node and the source never sees it. **(1 mark.)**

### (d) Sallen-Key (2 marks)

**The corner is set by the RC product**, $f_c = 1/2\pi RC$ for the equal-component case. **The Q is
set by the amplifier's gain**, which for the unity-gain equal-component form is fixed at 0.5, and
which is adjusted in practice either by making the gain greater than one or by making the two
resistors or two capacitors unequal. **(1 mark.)**

**They are separable because the amplifier supplies energy.** In a passive cascade every section
loads every other, and both the corner and the damping are consequences of the same component
values; there is nothing left to adjust independently. A Sallen-Key stage feeds part of the output
back through a capacitor, and how much it feeds back is a free parameter that moves the poles'
angle without moving their radius. **Q is a property of positive feedback here, and passive
networks have none available.** **(1 mark.)**

---

## Question 4 - Why everything is a function of the loop gain (10 marks)

### (a) The closed loop, derived (4 marks)

The amplifier sees the input minus the fed-back fraction of the output:

$$V_{out} = A\left(V_{in} - \beta_f V_{out}\right)$$

$$V_{out}(1 + A\beta_f) = A V_{in} \Rightarrow \boxed{A_{cl} = \frac{A}{1 + A\beta_f}}$$

**(2 marks.)**

**The error against the ideal.** As $A \to \infty$, $A_{cl} \to 1/\beta_f$. So

$$\frac{1/\beta_f - A_{cl}}{1/\beta_f} = 1 - \frac{A\beta_f}{1 + A\beta_f}
= \boxed{\frac{1}{1 + A\beta_f}}$$

**(2 marks.)**

**$A$ and $\beta_f$ enter only as their product**, which is the loop gain. Neither appears alone
anywhere in the result. That is the whole content of the derivation and it is why the loop gain is
the quantity worth naming.

### (b) Why one factor for four results (2 marks)

| Quantity          | Factor                  |
| ----------------- | ----------------------- |
| Gain error        | $\div (1 + A\beta_f)$   |
| Distortion        | $\div (1 + A\beta_f)$   |
| Output resistance | $\div (1 + A\beta_f)$   |
| Input resistance  | $\times (1 + A\beta_f)$ |
| Bandwidth         | $\times (1 + A\beta_f)$ |

**(1 mark.)**

**Why the same factor.** Every one of them is a **disturbance introduced inside the loop**: a
distortion product generated by the amplifier, a voltage drop caused by load current, a gain that
is not what it should be. The loop measures the output, compares it with what the input asked for,
and drives the difference back in with a gain of $A\beta_f$. Any disturbance originating inside
therefore appears at the output divided by one plus that. **It is one mechanism seen four times,
and the four are not independent properties that happen to share a formula.** **(1 mark.)**

### (c) Gain-bandwidth (2 marks)

| Closed-loop gain | Bandwidth   |
| ---------------- | ----------- |
| 10               | **100 kHz** |
| 1000             | **1 kHz**   |

Open-loop gain at 1 kHz: $10^6/10^3 = \mathbf{1000}$. **(1 mark.)**

**It does not meet the specification.** At 1 kHz with a closed-loop gain of 10, the loop gain is
$1000 \times 0.1 = 100$, so the error is $1/101 = \mathbf{0.99\ \text{per cent}}$ against a
requirement of 0.01. It is short by a factor of a hundred, and it is short at 1 kHz on an amplifier
whose datasheet says 1 MHz. **Closed-loop accuracy has a bandwidth of its own and it is far below
the closed-loop bandwidth.** **(1 mark.)**

### (d) Newton on an exponential (2 marks)

**The shape is the problem.** Newton replaces the function with its tangent and jumps to where the
tangent crosses zero. At $V_d = 0$ the diode's slope is $I_S/V_T$, about $4\times10^{-13}$ siemens,
so the tangent is almost horizontal and crosses zero a very long way away. The method is built on
the function being locally straight, and an exponential is locally straight only over a few
$V_T$. **(1 mark.)**

**Step limiting caps how far a junction voltage may move in one iteration**, replacing a jump into
the exponential with a logarithmic advance. **It changes the path and not the equation.** The
converged point is where the residual is zero, and the residual is computed from the same
Kirchhoff equation either way.

**A limiter that changed the answer would be a bug**, because it would mean the solver was
reporting the solution to a problem nobody posed. The whole contract of a nonlinear solver is that
the answer depends on the circuit and the tolerance, never on how it got there. **(1 mark.)**

---

## Question 5 - One equation, three regions (10 marks)

### (a) The transport form (4 marks)

$$I_C = I_S\left(e^{V_{BE}/V_T} - e^{V_{BC}/V_T}\right)
- \frac{I_S}{\beta_R}\left(e^{V_{BC}/V_T}-1\right)$$

$$I_B = \frac{I_S}{\beta_F}\left(e^{V_{BE}/V_T}-1\right)
+ \frac{I_S}{\beta_R}\left(e^{V_{BC}/V_T}-1\right)$$

**(2 marks.)**

**Collector reverse biased.** $V_{BC}$ is negative and large, so $e^{V_{BC}/V_T} \to 0$:

$$I_C \to I_S e^{V_{BE}/V_T}, \qquad I_B \to \frac{I_S}{\beta_F}e^{V_{BE}/V_T}
\Rightarrow \frac{I_C}{I_B} = \beta_F$$

**(1 mark.)**

**Collector junction forward biased.** $e^{V_{BC}/V_T}$ grows. In $I_C$ it appears with a **minus**
sign, so the collector current stops rising and then falls; in $I_B$ it appears with a **plus**
sign, so the base current rises. The ratio $I_C/I_B$ collapses. **That is saturation, and it is
what the equation does rather than a case it handles.** **(1 mark.)**

### (b) Why no branch (2 marks)

Two consequences of the three-case version, either of which is worth the marks:

* **Discontinuities at the boundaries.** Three separately written expressions do not meet with
  matching values and slopes, so a curve that crosses a boundary has a kink in it, and a solver
  whose Jacobian jumps there may not converge. A switch operates exactly at that boundary.
* **The model stops being one model.** Three cases have three sets of parameters that can drift
  apart, and a correction applied to one is not applied to the others. The transport form has one
  saturation current and two betas, and every region is the same expression.

**(2 marks, 1 each.)**

### (c) The square law (2 marks)

$$I_D = \frac{k}{2}(V_{GS} - V_{th})^2$$

$$g_m = \frac{dI_D}{dV_{GS}} = k(V_{GS} - V_{th})$$

and substituting $V_{GS} - V_{th} = \sqrt{2I_D/k}$:

$$\boxed{g_m = \sqrt{2 k I_D}}$$

**(1 mark.)**

**So $g_m$ goes as $\sqrt{I_D}$.** Biasing a MOSFET four times harder doubles its transconductance,
where a bipolar transistor's would quadruple. Current is therefore an expensive way to buy gain
from a MOSFET, and the cheaper lever is width. **(1 mark.)**

### (d) The factor of ten (2 marks)

$$g_{m(BJT)} = \frac{I_C}{V_T} = \frac{1\ \text{mA}}{26\ \text{mV}} = \mathbf{38.5\ \text{mS}}$$

$$g_{m(MOS)} = \sqrt{2 \times 8\ \text{mA/V}^2 \times 1\ \text{mA}} = \mathbf{4.0\ \text{mS}}$$

Ratio **9.6**. **(1 mark.)**

**Where it comes from:** the bipolar transistor's current is *exponential* in its control voltage
and the MOSFET's is *quadratic*. A derivative of an exponential is the exponential itself divided
by 26 mV; a derivative of a square is linear. The scale $V_T$ is small and fixed by physics,
whereas the MOSFET's overdrive is hundreds of millivolts and chosen by the designer.

**Two decisions that follow** (any two): the 220 mV degeneration rule gives an emitter factor of 10
and a source factor of 2, because $r_s$ is ten times $r_e$; a source follower's gain is 0.80 into
1 kilohm where an emitter follower gives 0.97; MOSFETs go at the input of a differential pair,
where infinite input resistance matters and gain does not, and bipolars go at the output, where the
reverse is true. **(1 mark.)**

---

## Question 6 - A rule, a load line, and a factor that appears twice (9 marks)

### (a) The load line (2 marks)

$$V_{CE} = V_{CC} - I_C(R_C + R_E)$$

A straight line with intercepts at $V_{CE} = V_{CC}$ when $I_C = 0$, and at
$I_C = V_{CC}/(R_C + R_E)$ when $V_{CE} = 0$. **(1 mark.)**

**An amplifier sits near the middle**, because it must be able to move both ways and "the middle"
means whichever point leaves equal headroom above and below the wanted swing. **Near the supply
end the positive half clips; near saturation the negative half clips**, and both waste the stage.
**(1 mark.)**

### (b) The 220 millivolt rule (3 marks)

$$R_E = \frac{220\ \text{mV}}{I_C}$$

**(1 mark.)**

$$EF = \frac{r_e + R_E}{r_e} = \frac{V_T/I_C + 0.220/I_C}{V_T/I_C}
= 1 + \frac{0.220}{0.026} = \mathbf{9.46}$$

**The current cancels**, so the emitter factor is 9.46 at any collector current whatever. **(1
mark.)**

**Why a voltage rather than a resistance.** Because that is what makes it current-free. A rule
stating a resistance would give a different emitter factor at every bias current and would have to
be restated for each; a rule stating a *drop* fixes the ratio $R_E/r_e$ directly, since $r_e$ is
itself a voltage over the current. **(1 mark. A candidate who notes that 220 mV also lands the
answer on the E12 grid across the useful decade earns credit but not the mark; the cancellation is
the point.)**

### (c) One factor, two jobs (2 marks)

**Gain.** With and without the emitter resistor,

$$\frac{A_v(\text{no } R_E)}{A_v(\text{with } R_E)} = \frac{R_C/r_e}{R_C/(r_e + R_E)}
= \frac{r_e + R_E}{r_e}$$

**Drift.** The disturbance is $V_{BE}$ falling with temperature, which is equivalent to the base
rising. With the base held, the emitter follows, so $\Delta I_C = \Delta V/R_E$ instead of
$\Delta I_C = \Delta V/r_e$, and the ratio is

$$\frac{r_e + R_E}{r_e}$$

**the same expression.** **(1 mark for both derivations.)**

**The consequence:** the emitter resistor divides the drift by exactly the factor by which it
divides the gain. **The stability is not free and it is not cheap; it costs gain one for one.**
**(1 mark.)**

### (d) A better transistor will not help (2 marks)

**The coefficient is about $-2$ mV per degree in $V_{BE}$ at a fixed collector current**, and it
comes from the saturation current's temperature dependence, which is set by the bandgap. **It is
not a parameter a designer chooses**: every silicon bipolar transistor has very nearly the same
figure, because they are all made of silicon. **(1 mark.)**

**What the emitter resistor does that no device could.** It is not reducing the drift; it is
**feeding the drift back**. The resistor converts a change in collector current into a change in
emitter voltage that opposes it, which is a local feedback loop with a loop gain of $R_E/r_e$. A
better device would still drift; a loop divides whatever drift there is by its own loop gain, and
that is a property of the circuit rather than of the transistor. **(1 mark.)**

---

## Question 7 - Three results from one model (11 marks)

### (a) Four steps (3 marks)

1. **Every DC source becomes a short to ground.**
2. **Every coupling and bypass capacitor becomes a short.**
3. **The bias network disappears** wherever it is now in parallel with something much smaller.
4. **The transistor becomes $r_e$ from base to emitter and a current source from collector to
   emitter**, carrying the current $r_e$ passes.

**(2 marks.)**

**Justifying the first.** A small-signal model describes *changes*. A rail that holds a constant
voltage has no change on it, and a node with no change on it is indistinguishable from ground as
far as signals are concerned. It is not an approximation about the supply being stiff; it is what
"small-signal" means. **(1 mark.)**

**Blind to** (any three): everything nonlinear, so clipping, distortion and slew rate; the fact
that the device turns off; capacitance and therefore every frequency; the Early effect, until it is
added; noise.

### (b) Two results (3 marks)

**Gain.** The input drives a current $v_{in}/(r_e + R_E)$ through the emitter branch. That same
current comes out of the collector and flows through $R_C$:

$$A_v = -\frac{R_C}{r_e + R_E}$$

**(1 mark.)**

**Input resistance.** The current drawn at the base is the emitter current divided by $\beta$, and
the voltage is that current times the emitter branch:

$$Z_{in(base)} = \beta(r_e + R_E)$$

**(1 mark.)**

**The input resistance depends on $\beta$ and the gain does not.** So the gain can be specified;
the input resistance can only be bounded. A datasheet quoting $\beta$ as 100 minimum and 400
typical is quoting an input resistance with a factor of four in it, which is why every stage in
this course that needs a defined input resistance gets it from a bias network or a MOSFET rather
than from a base. **(1 mark.)**

### (c) The emitter factor, and the node (3 marks)

Dividing the two gain expressions:

$$\frac{A_v(\text{no } R_E)}{A_v(\text{with } R_E)} = \frac{r_e + R_E}{r_e} \equiv EF$$

**(1 mark.)**

**It is often said to decide two things:** the factor by which the stage's gain **decreases**,
and the factor by which the stage's **output resistance increases**.

**The gain claim is correct as stated**, and the derivation above is its proof. **(1 mark.)**

**The output-resistance claim is not.** A stage's output resistance is $R_C$ **in parallel** with
whatever the transistor presents, and a parallel combination is smaller than either part, so no
amount of degeneration can push it above $R_C$. The corrected statement is that the emitter factor
multiplies the **resistance looking into the collector**:

$$R_{into\ collector} = r_o\left[1 + g_m(R_E \parallel r_\pi)\right] + (R_E \parallel r_\pi)
\approx r_o \cdot EF$$

**and the stage's output resistance is that in parallel with $R_C$.** **(1 mark.)**

### (d) The substitution (2 marks)

**Transfers:** the **gain**, $A_v = -R_D/(r_s + R_S)$, and the **source factor**,
$SF = (r_s + R_S)/r_s$. Output resistance transfers too.

**Does not transfer: the input resistance.** A gate draws no current, so there is no
$\beta(r_e + R_E)$ term to carry across; a common-source stage's input resistance is its bias
network and nothing else. **(1 mark.)**

$$r_s = \frac{1}{g_m} = \frac{1}{4\ \text{mS}} = \mathbf{250\ \Omega}, \qquad
SF = 1 + \frac{220}{250} = \mathbf{1.88}$$

**Why 2 where the emitter factor is 10.** The same 220 mV is divided by a different intrinsic
resistance. $r_e$ is 26 ohm and $r_s$ is 250, a factor of 9.6, because a MOSFET's transconductance
is about ten times lower at the same current. **The correspondence between the two factors follows
from that one ratio.** **(1 mark.)**

---

## Question 8 - A dead band, a rule, and a thing bolted to a heatsink (10 marks)

### (a) The follower (3 marks)

The input drives $r_e$ and $R_E$ in series; the output is taken across $R_E$ alone, which is a
divider:

$$A_v = \frac{R_E}{r_e + R_E}$$

**(1 mark.)**

**The shortfall from unity is $r_e/(r_e + R_E)$, and $r_e = V_T/I_C$, so the only quantity it
depends on is the current.** Not the device, not the load, which is given. A follower that is not
good enough is a follower that is not biased hard enough. **(1 mark.)**

$$Z_{in} = \beta(r_e + R_E), \qquad Z_{out} = r_e + \frac{R_{source}}{\beta}$$

**What the stage is for:** it is an **impedance transformer**. It shows the driving stage $\beta$
times what is on its emitter, and shows the load the driving resistance divided by $\beta$, while
passing the signal at a gain of about one. **(1 mark.)**

### (b) Three classes (3 marks)

| Class | What conducts                                | Max efficiency           |
| ----- | -------------------------------------------- | ------------------------ |
| A     | one device, the whole cycle                  | 25 % (resistive load)    |
| B     | two devices, half each                       | 78.5 %, which is $\pi/4$ |
| AB    | two devices, both near zero, one taking over | just below B             |

**(2 marks: 1 for the definitions, 1 for two efficiencies.)**

**Why crossover distortion is worse than its size.** The dead band is about 1.3 V wide, which in a
stage swinging 30 V is 4 per cent and sounds tolerable. But it sits **at the origin**, and a music
signal spends most of its time near the origin. So the distortion is **worst on quiet passages and
vanishes at full output**, which is the opposite of every other distortion mechanism in an
amplifier and is why it is audible far below the level its percentage suggests. **(1 mark. "It is
nonlinear" scores nothing; the position is the answer.)**

### (c) The 26 millivolt rule (2 marks)

$$R_E = \frac{V_T}{I_q} \Rightarrow
EF = \frac{r_e + R_E}{r_e} = \frac{V_T/I_q + V_T/I_q}{V_T/I_q} = \mathbf{2}$$

**exactly, and at any idle current**, because the rule sets $R_E$ equal to $r_e$ by construction.
**(1 mark.)**

**The two costs being balanced** are **thermal sensitivity**, which the resistors halve, and
**output power**, which they take because they sit in series with the load.

At **260 mV** the emitter factor is 11 and the stage is very stable, and 2.2 ohm in series with an
8 ohm loudspeaker has thrown away a fifth of the output power. At **2.6 mV** the resistors are
0.022 ohm, they cost nothing, and they have stopped suppressing anything. **The 26 mV point is
where the two costs cross.** **(1 mark.)**

### (d) Two diodes on a heatsink (2 marks)

**They are not setting a voltage. They are tracking one.** The output transistors' $V_{BE}$ falls
2 mV per degree as they warm, so at a fixed bias the idle current rises, which raises the
dissipation, which raises the temperature: a runaway. Diodes at the same temperature drop 2 mV per
degree less as well, so the bias falls by exactly as much as the outputs stop needing, and the
drift cancels to first order. **(1 mark.)**

**A stage with the diodes on the circuit board is correct at 25 degrees and destroys itself at 60.**
The emitter resistors halve the drift and do not stop it: 3.8 per cent per degree compounds to a
factor of three over thirty degrees.

**And the two schematics are identical**, because thermal contact is not a circuit property.
Nothing about the netlist distinguishes a working amplifier from one that fails in ten minutes,
which is why this is the most common way a first output stage is destroyed. **(1 mark.)**

---

## Question 9 - The tail, the tanh, and the output you choose (11 marks)

### (a) The tail, doubled (4 marks)

**Why $2R_{tail}$.** For a common-mode input both halves change their current by the same amount
$i$. The tail carries the **sum**, so it carries $2i$, and the voltage it develops is $2iR_{tail}$.
One half sees a voltage of $2iR_{tail}$ in response to its own current $i$, which is a resistance
of $2R_{tail}$ in its own emitter. **(1 mark.)**

It is then L07's degenerated stage, unchanged:

$$A_{cm} = -\frac{R_C}{2R_{tail} + r_e}$$

**(1 mark.)**

$$CMRR = \frac{A_{dm}}{A_{cm}}
= \frac{R_C/2r_e}{R_C/(2R_{tail} + r_e)} = \frac{2R_{tail} + r_e}{2r_e}
\approx \frac{R_{tail}}{r_e}$$

**(1 mark.)**

**$R_C$ cancels exactly**, because it is in the numerator of both gains. **Rejection is a property
of the tail and the operating current, and no choice of load affects it.** **(1 mark.)**

### (b) What a current source is (2 marks)

**A current source is a device with a large incremental resistance and a small voltage across it.**
Those are the two quantities, and they are independent: $r_o = V_A/I_C$ has nothing to do with the
voltage the device is sitting at.

**No resistor can have both**, because a resistor's incremental resistance *is* its resistance, so
a large one carrying the tail current necessarily drops a large voltage. 260 kilohm at 2 mA is
520 V. **(1 mark.)**

**The general principle:** wherever a circuit needs a large resistance without a large voltage
across it, the answer is a current source. **(1 mark for the principle plus two of:** the mirror
load of L07, which needs $r_o$ rather than a large $R_C$ that would take all the headroom; the
mirror load of L09's pair; the current-source load of L10's gain stage; the emitter sink under
L10's buffer.**)**

### (c) The tanh (3 marks)

**The small-signal transconductance** is the slope at the origin. Since $\tanh x \to x$ for small
$x$:

$$\frac{d}{dv_d}\left[I_{tail}\tanh\frac{v_d}{2V_T}\right]_{v_d=0}
= \frac{I_{tail}}{2V_T} = \frac{I_{tail}/2}{V_T} = \frac{1}{r_e}$$

**which is $1/r_e$ and not $1/2r_e$**: the two in the *gain to one collector* comes from taking one
collector, and the difference current has no two in it. **(1 mark.)**

**The 1 per cent point.** Solve $\tanh(x)/x = 0.99$ with $x = v_d/2V_T$, which gives $x = 0.1743$
and

$$v_d = 2 \times 26\ \text{mV} \times 0.1743 = \mathbf{9.06\ \text{mV}}$$

**(1 mark.)**

**The tail current does not appear.** It multiplies both the tanh and its tangent, so it cancels
out of the ratio. **Biasing the pair harder buys transconductance and buys no linearity at all**,
which is the opposite of the pattern followers establish. The only lever on linearity is
degeneration, which trades gain for range one for one. **(1 mark.)**

### (d) Fifty-two decibels and ninety-eight (2 marks)

**Both are right, and they measured different outputs.**

**52 dB is the single-ended figure**, taken at one collector. A common-mode input genuinely moves
that collector, by $R_C/2R_{tail}$, and **the tail alone decides how much**. Matching does not
enter at first order.

**98 dB is the differential figure**, taken between the two collectors. The common-mode motion is
identical on both, so it subtracts out exactly when the halves match, and what survives is the
**load mismatch** acting on it: $CMRR = 2R_{tail}/\delta r_e$, which for 1 per cent resistors is
98 dB. **(1 mark for the distinction, 1 for naming the limit in each.)**

**So "the CMRR of a differential pair" is not a statement about a circuit** unless it says which
output is taken. The two differ by 46 dB at ordinary component tolerances, from the same
transistors.

---

## Question 10 - The gain you cannot buy (9 marks)

### (a) The gain that does not depend on current (4 marks)

The load is the current source's own output resistance in parallel with the transistor's:

$$R_{load} = r_o \parallel r_o = \frac{V_A}{2I_C}$$

and the transconductance is $g_m = I_C/V_T$, so

$$|A_v| = g_m R_{load} = \frac{I_C}{V_T}\cdot\frac{V_A}{2I_C}
= \boxed{\frac{V_A}{2V_T}} = \frac{100}{0.052} = \mathbf{1923} = \mathbf{65.7\ \text{dB}}$$

**(3 marks: 2 for the derivation, 1 for showing the cancellation explicitly.)**

**The collector current cancels exactly.** The load falls as $1/I$ and the transconductance rises
as $I$.

**So the designer proposing more supply current gets nothing.** Gain here is a property of the
process, through $V_A$, and not of the design, which is why every gain stage in every operational
amplifier lands within a few decibels of the same figure.

**The only lever that works is a cascode**, which multiplies $r_o$ by $\beta$ and the gain with it:
$\beta V_A/2V_T = \mathbf{96{,}000}$, or **99.7 dB from one stage**. **(1 mark.)**

### (b) Where 11.5 dB goes (2 marks)

**Into loading.** Each stage's output resistance and the next stage's input resistance form a
divider, and the product of the *unloaded* gains counts none of it. The largest single term is the
gain stage driving the output stage: 50 kilohm of output resistance into 21 kilohm of input
resistance keeps 30 per cent, which is 10.6 dB. **(1 mark.)**

**It cannot be recovered by improving either gain stage**, because the loss is not in either of
them. Doubling a gain stage's own gain doubles what arrives at the divider and the divider still
takes 70 per cent of it. **The fix is at the interface, not at the stages**, and it is another
follower: the output stage is already a Darlington, and a third follower is what a real power
amplifier uses. **(1 mark.)**

### (c) Compensation (2 marks)

**It is compensating the amplifier's own poles.** Four stages give at least four poles, each
contributing up to 90 degrees of phase lag, and a loop with 180 degrees of lag and a loop gain
above one oscillates. **(1 mark.)**

**The capacitor makes one pole dominant**, deliberately, at a few tens of hertz, so the open-loop
gain is already falling at 20 dB per decade long before any other pole contributes phase. By the
time the others matter the loop gain is below one, and a loop with a gain below one cannot
oscillate.

**Slowing it down is what makes it usable** because stability is about the *order* in which the
gain and the phase arrive, not about speed. An amplifier fast enough to have all four poles inside
its loop bandwidth is an oscillator; one slowed at a single point is an amplifier. **(1 mark. It is
worth noting that this is the Miller effect of L07, which ruined a stage's bandwidth there, used on
purpose here.)**

### (d) Why the closed loop does not care (1 mark)

**Because the closed-loop gain is set by the feedback network, and the forward path only has to be
large.** With a loop gain of 49,000 the error is one part in 49,000, and a factor of fourteen
change in the open-loop gain moves that error from 0.0007 per cent to 0.0095 per cent: both are
nothing. **The quantity that makes it so is the loop gain.** **(1 mark.)**

---
