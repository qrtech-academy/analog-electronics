# Analog Electronics - Paper A, Model Answers

Marked out of 100. Marks are shown per part. **Method carries the marks**: a correct rule with an
arithmetic slip is worth more than a correct number with no working, and several questions consume
their own earlier answers, so follow an error through rather than penalising it twice.

---

## Question 1 - A divider, its resistance, and the load that takes a third (10 marks)

### (a) Two numbers, and why one of them is neither resistor (3 marks)

$$V_{out} = 10 \times \frac{6.8}{33 + 6.8} = \mathbf{1.7085\ \text{V}}$$

$$R_{th} = 33\text{k} \parallel 6.8\text{k} = \frac{33 \times 6.8}{39.8}\ \text{k}
= \mathbf{5.638\ \text{k}\Omega}$$

**(1 mark each.)**

**Why it is neither resistor.** Looking back into the output with the supply replaced by its
internal resistance, which for an ideal supply is zero, the two resistors both run from the output
node to ground. They are in parallel. The supply does not appear because setting a voltage source
to zero makes it a short, and a short has no resistance to contribute. **(1 mark. An answer of
6.8 kilohm scores nothing: it is the first named trap.)**

### (b) What a 10 kilohm load does (3 marks)

**Two ways, and they must agree.**

*Reform the divider.* The lower arm becomes $6.8\text{k} \parallel 10\text{k} = 4.048$ kilohm, so

$$V = 10 \times \frac{4.048}{33 + 4.048} = \mathbf{1.0925\ \text{V}}$$

*Or use the Thevenin equivalent.* A source of 1.7085 V behind 5.638 kilohm, loaded by 10 kilohm:

$$V = 1.7085 \times \frac{10}{10 + 5.638} = \mathbf{1.0925\ \text{V}}$$

**(2 marks for both methods and the agreement. 1 mark for either alone.)**

It retains $1.0925/1.7085 = \mathbf{63.9\ \text{per cent}}$, so the load has taken **36 per cent**
of the output. **(1 mark.)**

**What the colleague has done.** Computed the open-circuit voltage and quoted it for a loaded node.
The divider is not a voltage source; it is a source behind 5.638 kilohm, and the moment anything is
connected the answer changes. This is the second named trap.

### (c) Meeting a 1 per cent requirement (2 marks)

For the load to take 1 per cent, $R_{load}/(R_{load} + R_{th}) = 0.99$, so
$R_{load} = 99 R_{th} = \mathbf{558\ \text{k}\Omega}$.

Turning it round, with a 10 kilohm load the divider needs $R_{th} \le 10\text{k}/99 =
\mathbf{101\ \Omega}$. **(1 mark for both.)**

**Without changing the ratio**, scale both resistors down by 5.638k/101 = 56, to about 590 ohm and
120 ohm. **The cost is supply current**: the divider goes from 251 microamps to 14 mA, which is
fifty-six times the power for a node that does exactly what it did before. That trade, accuracy
against current, is why the answer in practice is usually a buffer instead. **(1 mark.)**

### (d) The same subtraction, six times (2 marks)

Any three of:

| Lecture | What loaded what                             | Cost                        |
| ------- | -------------------------------------------- | --------------------------- |
| L01     | 10 kilohm on this divider                    | a third of the output       |
| L02     | the divider's own resistance on an RC filter | the corner moves 6.6 times  |
| L03     | two filter sections on each other            | the corner moves 1.72 times |
| L06     | base current on a bias divider               | 12 per cent of $I_C$        |
| L08     | a loudspeaker on a voltage amplifier         | 99.9 per cent of the gain   |
| L10     | each amplifier stage on the next             | 11.5 dB of open-loop gain   |

**(1 mark for three with their costs.)**

**What they have in common:** in every case a source with a finite output resistance drives a
finite load, and the two form a divider. It is one subtraction. What changes between the six is
only how large the ratio is, and here it costs everything. **(1 mark.)**

---

## Question 2 - One capacitor, two corners, and the resistance nobody drew (9 marks)

### (a) Two easy numbers (2 marks)

$$X_C = \frac{1}{2\pi \times 1000 \times 159\times10^{-9}} = \mathbf{1001\ \Omega}$$

$$f_c = \frac{1}{2\pi \times 1000 \times 159\times10^{-9}} = \mathbf{1001\ \text{Hz}}$$

**(1 mark each. They are the same arithmetic, and noticing that the corner is where the reactance
equals the resistance is worth stating.)**

### (b) The corner the circuit actually has (3 marks)

The capacitor does not see 1 kilohm. It sees the 1 kilohm **in series with the divider's Thevenin
resistance**, because that is what the source looks like:

$$R = 1000 + 5638 = 6638\ \Omega, \qquad
f_c = \frac{1}{2\pi \times 6638 \times 159\times10^{-9}} = \mathbf{151\ \text{Hz}}$$

**(2 marks.)**

The ratio is $1001/151 = \mathbf{6.6}$. **(1 mark.)**

**Why it is not on the schematic.** Nobody drew a 5.638 kilohm resistor; it is what two resistors
that *were* drawn look like from this node. A Thevenin resistance is a property of a network rather
than a component in it, which is exactly why this error is easy to make and hard to see. This is
the third named trap.

### (c) What a measurement would show (2 marks)

At 1001 Hz the filter is far past its real corner. With $f/f_c = 1001/151 = 6.64$:

$$|H| = \frac{1}{\sqrt{1 + 6.64^2}} = 0.1489, \qquad 20\log_{10}(0.1489) = \mathbf{-16.5\ \text{dB}}$$

**(1 mark.)**

**What it would look like.** Not a filter with a slightly wrong corner: a filter that has removed
85 per cent of the signal at the frequency it was supposed to be passing. Somebody who did not know
about part (b) would suspect the capacitor's tolerance, and no capacitor is wrong by a factor of
6.6. **The symptom points at the wrong component**, which is the reason the error is worth a
question of its own. **(1 mark.)**

### (d) A series LC (2 marks)

$$f_0 = \frac{1}{2\pi\sqrt{LC}} = \frac{1}{2\pi\sqrt{10^{-2} \times 10^{-6}}}
= \mathbf{1592\ \text{Hz}}$$

$$X_L = 2\pi f_0 L = \mathbf{100\ \Omega}, \qquad Q = \frac{X_L}{R} = \frac{100}{10} = \mathbf{10}$$

**(1 mark for all three.)**

**The inductor voltage is Q times the applied voltage**, so ten times it. It is not a violation of
anything because the capacitor's voltage is equal and opposite: the two cancel, the circuit
presents 10 ohm, and the energy is being exchanged between L and C rather than supplied. A circuit
that appears to produce more voltage than it is given is a circuit storing energy, and the store is
what Q measures. **(1 mark.)**

---

## Question 3 - Two sections, one buffer, and the factor of 1.72 (11 marks)

### (a) One section (1 mark)

**1001 Hz**, and **20 dB per decade**. **(1 mark for both.)**

### (b) Two sections, loaded and buffered (4 marks)

**Directly in series: 375 Hz.** The second section loads the first, so the two do not behave as two
independent single poles. Solving $|H|^2 = 1/2$ for the loaded cascade gives 0.374 times the
single-section corner. **(2 marks.)**

**With a buffer between them: 644 Hz.** Two independent identical poles give
$|H| = 1/(1 + (f/f_c)^2)$, and setting that to $1/\sqrt2$ gives

$$f_{-3} = f_c\sqrt{\sqrt2 - 1} = 1001 \times 0.6436 = \mathbf{644\ \text{Hz}}$$

**(2 marks.)**

The ratios against one section are **0.374** and **0.644**. **A candidate who gives 1001 Hz for
either has treated the sections as independent and given them the single-section corner**, which
is the fourth named trap.

### (c) What the buffer bought (2 marks)

$$\frac{644}{375} = \mathbf{1.72}$$

**The buffer bought back a factor of 1.72 in corner frequency**, and nothing else. **(1 mark.)**

**It did not change the roll-off**, which is 40 dB per decade either way, because that is set by
the number of poles and there are two of them in both circuits. Loading moves *where* the response
falls, not how fast. **(1 mark.)**

**Note what the buffer is doing**, because it is Question 1 again: the first section has an output
resistance, the second has an input impedance, and the two form a divider. The buffer's only job is
to make that divider's ratio one.

### (d) A Schmitt trigger (4 marks)

The non-inverting input sits at the output divided by the divider:

$$V_{th} = \pm 12 \times \frac{10}{100 + 10} = \mathbf{\pm 1.091\ \text{V}}$$

so the hysteresis is **2.18 V**. **(2 marks.)**

With 1 kilohm instead:

$$V_{th} = \pm 12 \times \frac{1}{100 + 1} = \mathbf{\pm 0.119\ \text{V}}$$

hysteresis **0.238 V**. **(1 mark.)**

**Its noise immunity has fallen by a factor of nine.** The circuit now switches on any disturbance
above 119 mV where it previously needed 1.09 V, so an input with a few hundred millivolts of noise
on it will chatter. The trade is that the thresholds are closer to the real crossing, so the
comparator is more accurate about *when* the input crossed; hysteresis buys immunity and pays in
timing. **(1 mark.)**

---

## Question 4 - Loop gain, the error it divides, and a diode that will not converge (10 marks)

### (a) Three open-loop gains (4 marks)

Ideal closed-loop gain is $1/\beta_f = \mathbf{10}$ in all three cases. **(1 mark.)**

| $A$    | Loop gain $A\beta_f$ | $A_{cl} = A/(1 + A\beta_f)$ | Error         |
| ------ | -------------------- | --------------------------- | ------------- |
| $10^3$ | 100                  | 9.90099                     | **0.990 %**   |
| $10^5$ | 10,000               | 9.99900                     | **0.0100 %**  |
| $10^6$ | 100,000              | 9.99990                     | **0.00100 %** |

**(2 marks for the table.)**

**The error is one part in one plus the loop gain**, so a loop gain of ten thousand gives an error
of one part in ten thousand. Every factor of ten in loop gain is a factor of ten in error. **(1
mark.)**

### (b) What feedback does, and to what (2 marks)

| Quantity          | Factor                                   |
| ----------------- | ---------------------------------------- |
| Gain error        | divided by $1 + A\beta_f$                |
| Distortion        | divided by $1 + A\beta_f$                |
| Output resistance | divided by $1 + A\beta_f$ (series-shunt) |
| Input resistance  | multiplied by $1 + A\beta_f$             |
| Bandwidth         | multiplied by $1 + A\beta_f$             |

**(1 mark.)**

**All five are functions of the loop gain**, not of the open-loop gain. **(1 mark.)** So an
open-loop gain quoted on its own says nothing about any of them: the same amplifier used at a
closed-loop gain of 1 and of 1000 has loop gains differing by a factor of a thousand, and every
result above differs by that factor. **A specification that gives $A$ without saying what $\beta_f$
it will be used at is incomplete**, which is the fifth named trap.

### (c) A diode and a resistor (2 marks)

The equation is Kirchhoff's voltage law with the diode's exponential in it:

$$\frac{5 - V_d}{1000} = I_S\left(e^{V_d/V_T} - 1\right)$$

**(1 mark for stating it.)**

$$V_d = \mathbf{0.6965\ \text{V}}, \qquad I = \frac{5 - 0.6965}{1000} = \mathbf{4.304\ \text{mA}}$$

**(1 mark.)**

**It has no closed form** because $V_d$ appears both linearly and inside an exponential; that is a
transcendental equation and it must be solved numerically. (The Lambert W function expresses it,
which is a name for the answer rather than a way of computing it.)

### (d) Newton from a cold start (2 marks)

**On the first step** the iteration linearises the diode at $V_d = 0$, where its conductance is
$I_S/V_T \approx 4\times10^{-13}$ S. That is essentially an open circuit, so the linear solve puts
almost the whole 5 V across the diode. Evaluating the exponential at 5 V asks for $e^{192}$, which
overflows, and the next Jacobian is meaningless. **(1 mark.)**

**Unlimited: about 170 iterations.** **With the log-domain step limiting: 7.** **(0.5 marks.)**

**The limiting caps how far the junction voltage may move in one step**, replacing a jump into the
exponential with a logarithmic advance. It does not change the answer because it only alters the
*path* to the root, not the equation being solved; the converged point still satisfies the same
Kirchhoff equation to the same tolerance. **(0.5 marks.)**

---

## Question 5 - Sixty millivolts a decade, and a switch that ignores beta (10 marks)

### (a) Three voltages and a slope (3 marks)

$$V_{BE} = V_T\ln\!\left(\frac{I_C}{I_S}\right)$$

| $I_C$        | $V_{BE}$     |
| ------------ | ------------ |
| 10 microamps | **0.5388 V** |
| 1 mA         | **0.6585 V** |
| 10 mA        | **0.7184 V** |

**(2 marks.)**

**59.9 mV per decade**, and the derivation is one line:

$$\Delta V_{BE} = V_T\ln(10) = 0.026 \times 2.3026 = \mathbf{59.9\ \text{mV}}$$

**(1 mark. "About 60 mV" with the $V_T\ln 10$ shown is full marks; 60 mV asserted is not.)**

### (b) Three regions (2 marks)

| Region     | Base-emitter | Base-collector |
| ---------- | ------------ | -------------- |
| Cutoff     | reverse      | reverse        |
| Active     | forward      | reverse        |
| Saturation | forward      | forward        |

**(1 mark.)**

**An amplifier lives in the active region**, where the transistor behaves as a **current source**
controlled by its base-emitter voltage. **A switch uses cutoff and saturation**, where it behaves
as an **open circuit** and as a **resistor** respectively. **(1 mark.)**

### (c) A switch (3 marks)

$$I_B = \frac{I_{load}}{\beta_{forced}} = \frac{150\ \text{mA}}{10} = 15\ \text{mA}, \qquad
R_B = \frac{5 - 0.65}{15\ \text{mA}} = \mathbf{290\ \Omega}$$

**Nearest E12: 270 ohm.** **(1 mark.)**

$$I_B = \frac{5 - 0.65}{270} = \mathbf{16.1\ \text{mA}}, \qquad
\beta_{forced} = \frac{150}{16.1} = \mathbf{9.3}$$

**(1 mark. Note the E12 value moves the drive the safe way, harder into saturation.)**

**Neither datasheet number entered the design.** The forced beta of 10 was chosen; $h_{FE}$ appears
nowhere. **(1 mark.)**

**For a thousand of them, that is the whole point.** A design that used the typical 400 would need
0.375 mA of base drive and would fail on every device near the 100 minimum. A design at a forced
beta of 10 works on any device whose $h_{FE}$ exceeds 10, which is all of them by a factor of ten,
and its saturation voltage does not depend on which device was fitted. **A switch designed from
$h_{FE}$ is the sixth named trap.**

### (d) Saturation without a branch (2 marks)

The transport model carries two exponentials, one for each junction:

$$I_C = I_S\left(e^{V_{BE}/V_T} - e^{V_{BC}/V_T}\right) - \frac{I_S}{\beta_R}\left(e^{V_{BC}/V_T}-1\right)$$

With the collector reverse biased the second exponential is negligible and this collapses to
$I_C = \beta_F I_B$. Drive the base hard enough that the collector falls below it and the second
exponential grows, the collector current stops rising, and the device is saturated. **Saturation is
not a case the model handles; it is what the equation does.** **(1 mark.)**

**A model written with three cases would show discontinuities at the boundaries**, because the
three expressions do not meet with matching values and slopes. Those show up as a solver that will
not converge near the boundary, and as kinks in any curve that crosses it, which is exactly where a
switch operates. **(1 mark.)**

---

## Question 6 - A bias point that loads itself, and drift that is a loop gain (9 marks)

### (a) The naive answer (1 mark)

$$V_B = 1.7085\ \text{V}, \quad V_E = 1.7085 - 0.65 = 1.0585\ \text{V}, \quad
I_C \approx \frac{1.0585}{1000} = \mathbf{1.059\ \text{mA}}$$

**(1 mark.)**

### (b) The answer the circuit gives (3 marks)

The base draws $I_C/\beta$, and that current flows out of the divider through its Thevenin
resistance of 5.638 kilohm. It is self-referential, so it must be solved rather than substituted:
the base voltage depends on the base current, which depends on the collector current, which depends
on the base voltage.

Converged:

$$I_B = \frac{0.934\ \text{mA}}{50} = 18.7\ \mu\text{A}, \qquad
\Delta V_B = 18.7\ \mu\text{A} \times 5.638\ \text{k}\Omega = \mathbf{105\ \text{mV}}$$

$$V_B = 1.7085 - 0.105 = 1.603\ \text{V}, \qquad I_E = \frac{1.603 - 0.65}{1000}
= 0.953\ \text{mA}, \qquad I_C = \frac{\beta}{\beta + 1}I_E = \mathbf{0.934\ \text{mA}}$$

**(2 marks. 1 mark for a single non-iterated pass that lands near 0.93. Taking the emitter
resistor to carry $I_C$ rather than $I_E$ gives 0.951 mA and does not lose a mark, but it is the
$1/\beta$ the rest of the question is about.)**

The error is $(1.059 - 0.934)/1.059 = \mathbf{12\ \text{per cent}}$, and it is **L01's loading
arithmetic**: the divider has a source resistance and the base is a load on it. **(1 mark.
Computing the unloaded answer only is the seventh named trap.)**

### (c) Stiffness (2 marks)

$$\text{stiffness} = \frac{I_{divider}}{I_B} = \frac{10/(33\text{k}+6.8\text{k})}{18.7\ \mu\text{A}}
= \frac{251\ \mu\text{A}}{18.7\ \mu\text{A}} = \mathbf{13.4}$$

**The rule of thumb is ten**, and this stage meets it, which is why the error is 12 per cent rather
than 1: a stiffness of ten *accepts* about a tenth of the droop. **(1 mark.)**

A stiffness of 200 needs a divider current of $200 \times 18.7\ \mu\text{A} =
\mathbf{3.7\ \text{mA}}$, which is four times what the stage amplifies with. **That is the point at
which a designer stops**, because the bias network is now the dominant power consumer, and uses a
Darlington or a MOSFET input instead so that the base current is negligible in the first place.
**(1 mark.)**

### (d) An argument that does not survive its own numbers (3 marks)

$$\frac{I_C(0.55)}{I_C(0.65)} = e^{-0.100/0.026} = \frac{1}{\mathbf{47}}$$

**The collector current would fall by a factor of 47, not by 10 per cent.** **(1 mark.)**

**What is wrong** is not the physics but the size of the step: **the argument applies an open-loop
change to a closed-loop circuit.** The circuit never reaches a base-emitter voltage of 0.55 V,
because long before the emitter voltage has risen 100 mV the current has been pulled back. A story
about voltages moving in sequence has no place to put a loop gain. **(1 mark.)**

**The correct treatment** is a local feedback loop. The disturbance is $V_{BE}$ drifting 2 mV per
degree, the emitter follows, and

$$\Delta I_C = \frac{2\ \text{mV}}{1\ \text{k}\Omega} = 2\ \mu\text{A}
\ \text{on}\ 0.934\ \text{mA} = 0.21\ \text{per cent per degree}$$

against about 8 per cent without the resistor, so the suppression factor is

$$1 + \frac{R_E}{r_e} = 1 + \frac{1000}{27.8} = \mathbf{37}$$

**and that quantity is the emitter factor**, the same number that divides the stage's gain. The
stability costs gain one for one. **(1 mark. The factor of 47 without naming the emitter factor is
2 of the 3.)**

---

## Question 7 - The emitter factor, and the node it belongs to (11 marks)

### (a) Four numbers and a resistance (3 marks)

$$r_e = \frac{26\ \text{mV}}{1\ \text{mA}} = \mathbf{26\ \Omega}, \qquad
EF = \frac{26 + 234}{26} = \mathbf{10}$$

$$A_v = -\frac{R_C}{r_e + R_E} = -\frac{10000}{260} = \mathbf{-38.5}, \qquad
A_{v(bypassed)} = -\frac{10000}{26} = \mathbf{-385}$$

$$Z_{in(base)} = \beta(r_e + R_E) = 50 \times 260 = \mathbf{13\ \text{k}\Omega}$$

**(3 marks, one per pair.)**

### (b) Why the tempting rule cannot be right (4 marks)

**Without computing anything:** a stage's output resistance is the collector resistor **in
parallel** with whatever the transistor presents at that node. A parallel combination is always
smaller than either of its parts. So the answer cannot exceed 10 kilohm, and 100 kilohm does.
**(2 marks. This is the argument, and it is worth two marks precisely because it needs no
arithmetic. A candidate who reaches the right answer only by computing has not made the point.)**

What the emitter factor does multiply is the resistance **looking into the collector**:

$$R_{into\ collector} = r_o\left[1 + g_m(R_E \parallel r_\pi)\right] + (R_E \parallel r_\pi)$$

with $r_o = V_A/I_C = 100$ kilohm and $r_\pi = \beta r_e = 1.3$ kilohm:

$$R_E \parallel r_\pi = 234 \parallel 1300 = 198\ \Omega, \qquad
R_{into\ collector} = 100\text{k}\left[1 + \tfrac{198}{26}\right] + 198 = \mathbf{863\ \text{k}\Omega}$$

$$R_{out} = 10\text{k} \parallel 863\text{k} = \mathbf{9.89\ \text{k}\Omega}$$

**(2 marks.)**

Against **9.09 kilohm** for the same stage with no emitter resistor: **degeneration bought 9 per
cent**, not a factor of ten. **This is the eighth named trap and it is the largest disagreement in
the course.**

### (c) A mirror load (2 marks)

The mirror presents its own $r_o$, 100 kilohm, instead of a 10 kilohm resistor:

$$R_{out} = 100\text{k} \parallel 863\text{k} = \mathbf{89.6\ \text{k}\Omega}, \qquad
\text{without } R_E: 100\text{k} \parallel 100\text{k} = \mathbf{50\ \text{k}\Omega}$$

**The emitter factor is now worth a factor of 1.8** rather than 1.09. **(1 mark.)**

**What this establishes.** With a resistive load the degeneration boost is real and invisible,
because $R_C$ swamps it. A mirror load is how you stop throwing it away. So the correction is not a
demolition of the emitter factor; it supplies the missing reason for mirror loads, which otherwise
appear from nowhere. **(1 mark.)**

### (d) Miller (2 marks)

$$C_{in} = C_{bc}(1 + |A_v|) = 4\ \text{pF} \times 386 = \mathbf{1.54\ \text{nF}}$$

$$f = \frac{1}{2\pi \times 1000 \times 1.54\ \text{nF}} = \mathbf{103\ \text{kHz}}$$

**(1 mark. Quoting 4 pF and 40 MHz is the ninth named trap.)**

**A cascode removes the multiplication entirely**, because the lower transistor's collector no
longer swings, so the input sees 4 pF and the corner moves to about 40 MHz. **The cost** is one
more transistor, one more bias voltage, and about 0.7 V of output swing. **(1 mark.)**

---

## Question 8 - Eight ohms, two Darlingtons, and a bias that is not two drops (10 marks)

### (a) One follower and two (4 marks)

At 120 mA, $r_e = 26\ \text{mV}/120\ \text{mA} = 0.217\ \Omega$.

**Single follower:**

$$A_v = \frac{8}{0.217 + 8} = \mathbf{0.974}, \qquad
Z_{in} = 50 \times 8.217 = \mathbf{411\ \Omega}$$

**Darlington:**

$$A_v = \frac{8}{0.433 + 8} = \mathbf{0.949}, \qquad
Z_{in} = 50^2 \times (0.433 + 8) = \mathbf{21.1\ \text{k}\Omega}$$

**(3 marks.)**

**A Darlington's effective emitter resistance is exactly twice a single transistor's, and $\beta$
does not appear in that statement.** The output device runs at the output current and contributes
$r_e$; the input device runs at the output device's base current, which is $\beta$ times smaller,
so its own $r_e$ is $\beta$ times larger, and it is seen through the output device's current gain,
so it contributes $r_e$ again. The two betas cancel. **(1 mark. Using $\beta^2(r_e + R)$ rather
than $\beta^2(2r_e + R)$ is the tenth named trap and costs this mark only.)**

### (b) What the loudspeaker costs (3 marks)

|                        | What the stage sees | Gain  | Kept       |
| ---------------------- | ------------------- | ----- | ---------- |
| 8 ohm direct           | 8 ohm               | 0.031 | **0.08 %** |
| Through the follower   | 411 ohm             | 1.53  | **4.0 %**  |
| Through the Darlington | 21.1 kilohm         | 26.2  | **68 %**   |

**(3 marks, one per row, each needing the loading divider $R_{load}/(R_{out} + R_{load})$.)**

**One follower is not enough**, and that is not a small shortfall to be tuned away: 4 per cent is
better than 0.08 by a factor of fifty and still useless.

### (c) A class-AB bias (3 marks)

$$R_E = \frac{26\ \text{mV}}{120\ \text{mA}} = 0.217\ \Omega \rightarrow
\mathbf{0.22\ \Omega\ \text{(E12)}}, \qquad EF = \frac{0.217 + 0.22}{0.217} = \mathbf{2.0}$$

**(1 mark.)**

$$V_{bias} = 2\left(V_{BE}(120\ \text{mA}) + I_q R_E\right) = 2(0.783 + 0.026)
= \mathbf{1.619\ \text{V}}$$

The constant-drop version is $2(0.65 + 0.026) = 1.353$ V, and applying that to the real stage gives
an idle current of **1.96 mA**, a ratio of **61**. **(1 mark.)**

**Why the model changes value.** Every earlier use computed a **current from a voltage across a
resistor**: subtract 0.65 from a base voltage and divide by $R_E$. A 133 mV error in a subtraction
that yields a volt is 12 per cent, and it enters linearly. Here the calculation runs the other way:
the bias lands almost entirely across two **junctions**, so inverting it means going backwards
through an exponential of scale 26 mV, and 133 mV is $e^{5.1}$. **A model's accuracy is a property
of the calculation it appears in, not of the model.** **(1 mark. This is the eleventh named trap
and the sentence is the answer.)**

---

## Question 9 - The tail, the 520 volts, and the resistor that cancels (11 marks)

### (a) Half the tail (3 marks)

$$r_e = \frac{V_T}{I_{tail}/2} = \frac{26\ \text{mV}}{1\ \text{mA}} = \mathbf{26\ \Omega}$$

**Each side carries half the tail**, so $r_e$ follows from 1 mA and not from 2. Reading it from the
tail current gives 13 ohm and halves every gain below. **(1 mark. This is the twelfth named trap.)**

$$A_{dm(one\ collector)} = -\frac{R_C}{2r_e} = -\frac{10000}{52} = \mathbf{-192},
\qquad A_{dm(both)} = \mathbf{-385}$$

**(1 mark.)**

**The two factors of two.** The first is the **input split**: a differential input of $v_d$ puts
only $v_d/2$ on each base, and that is what "differential" means. The second is the **output**:
taking one collector discards the other half, which moves oppositely. The first is unavoidable; the
second is a choice, and a current-mirror load recovers it. **(1 mark.)**

### (b) Rejection, and the term that cancels (4 marks)

The tail carries both currents, so one half sees it as $2R_{tail}$ of degeneration:

$$A_{cm} = -\frac{R_C}{2R_{tail} + r_e} = -\frac{10000}{20026} = \mathbf{-0.499}$$

**(1 mark.)**

$$CMRR = \frac{A_{dm}}{A_{cm}} = \frac{R_C/2r_e}{R_C/(2R_{tail} + r_e)}
= \frac{2R_{tail} + r_e}{2r_e} = \frac{20026}{52} = \mathbf{385} = \mathbf{51.7\ \text{dB}}$$

**(2 marks.)**

**$R_C$ cancels**, exactly, because it is in the numerator of both gains. **(1 mark.)**

**So the designer proposing a larger collector resistor is wrong.** It doubles both gains and
rejects exactly as badly as before. Rejection is a property of the tail and the operating current,
and no choice of load affects it. **This is the thirteenth named trap, and the instinct behind it
is close to universal.**

### (c) Eighty decibels (2 marks)

$$CMRR = \frac{2R_{tail} + r_e}{2r_e} = 10^4 \Rightarrow R_{tail} = \mathbf{260\ \text{k}\Omega}$$

$$V = 260\ \text{k}\Omega \times 2\ \text{mA} = \mathbf{520\ \text{V}}$$

**(1 mark.)**

**A simple mirror is not enough either.** Its output resistance is $r_o = V_A/I_{tail} = 50$
kilohm, giving $50000/26 = 1923 = \mathbf{65.7\ \text{dB}}$, which falls 14 dB short. **The answer
is a cascoded mirror**, whose output resistance is $\beta r_o = 2.5$ megohm, giving about 100 dB
for one extra transistor and 0.7 V of headroom. **(1 mark.)**

### (d) A mirror load (2 marks)

$$A_{dm} = -\frac{r_o \parallel r_o}{r_e} = -\frac{50\ \text{k}\Omega}{26} = \mathbf{-1923}$$

**(1 mark.)**

**A factor of ten over part (a), and it is two independent factors:**

* **A factor of two from the mirror as a mirror.** It turns the idle side's current around and adds
  it to the output node, recovering the half a single-ended output discards.
* **A factor of five from the load.** $r_o \parallel r_o$ is 50 kilohm where the resistor was 10.

**(1 mark. Both, with the numbers. Naming only one scores nothing, because the question asks for
the split.)**

---

## Question 10 - A gain budget, and the two stages that amplify nothing (9 marks)

### (a) Six numbers (3 marks)

**Stage 1** is loaded by $r_o \parallel r_o$ at 1 mA per side, which is 50 kilohm, so
$A = 50000/26 = \mathbf{1923}$. **Stage 3** is the same arithmetic at 1 mA: $\mathbf{1923}$.
**(1 mark.)**

| Stage                            | Input resistance                                              |
| -------------------------------- | ------------------------------------------------------------- |
| 3, common-emitter at 1 mA        | $\beta r_e = \mathbf{1.3\ \text{k}\Omega}$                    |
| 2, Darlington follower into that | $\beta^2(2r_e + 1300) = \mathbf{3.4\ \text{M}\Omega}$         |
| 4, Darlington output into 8 ohm  | $\beta^2(2 \times 0.217 + 8) = \mathbf{21.1\ \text{k}\Omega}$ |

**(2 marks.)**

### (b) The budget (3 marks)

| Stage | Loaded gain                                                           |
| ----- | --------------------------------------------------------------------- |
| 1     | $1923 \times 3.4\text{M}/(50\text{k} + 3.4\text{M}) = \mathbf{1895}$  |
| 2     | $1300/(52 + 1300) = \mathbf{0.962}$                                   |
| 3     | $1923 \times 21.1\text{k}/(50\text{k} + 21.1\text{k}) = \mathbf{570}$ |
| 4     | $8/(0.433 + 8) = \mathbf{0.949}$                                      |

$$A_{open} = 1895 \times 0.962 \times 570 \times 0.949 = 986{,}000 = \mathbf{119.9\ \text{dB}}$$

**(2 marks.)**

The two unloaded gains multiply to $1923^2 = 3.70$ million, which is 131.4 dB, so **loading costs
11.5 dB**. **Stage 3 accounts for 10.6 of it**, driving the output stage; everything else together
is under a decibel. **(1 mark. A budget quoted at 131 dB is the fourteenth named trap.)**

### (c) The stage that does nothing (2 marks)

Without the buffer, stage 1 drives 1.3 kilohm from 50 kilohm and keeps 2.5 per cent:

$$1923 \times 0.0253 = 48.7, \qquad
A_{open} = 48.7 \times 570 \times 0.949 = 26{,}400 = \mathbf{88.4\ \text{dB}}$$

**(1 mark.)**

**The buffer is worth $119.9 - 88.4 = 31.5$ dB, and it costs 0.34 dB of signal.** An exchange rate
of about a hundred to one, from a stage with a voltage gain below one, which is why the answer to
almost every loading problem in analog design is another follower. **(1 mark.)**

### (d) A rail is not a fault (1 mark)

**Not a fault.** With an open-loop gain of 986,000 and rails of $\pm 15$ V, an input offset of

$$\frac{15}{986000} = \mathbf{15\ \mu\text{V}}$$

saturates the output, and no pair of transistors matches to 15 microvolts. **The amplifier has no
open-loop operating point**, so there is no mid-rail answer for a solver to find. **(1 mark for the
number and the conclusion. Blaming the solver is the fifteenth named trap.)**

---
