# Analog Electronics - Written Examination, Paper B

**Time:** 4 hours. **Closed book.** A basic calculator is permitted. **Total: 100 marks.**

This paper exists to let you check your own knowledge. It is not a qualification and it gates
nothing. It has one question per lecture, so **it is meant to be taken once the course is over**,
after L10 and the capstone.

Paper B asks for the derivations rather than the numbers. Several parts carry no arithmetic at all,
and they are not worth fewer marks for it.

---

## Rubric

**The thermal voltage is 26 mV.** Every intrinsic emitter resistance in this paper follows from
$r_e = V_T/I_C$ and that figure.

**Beta is 50** unless a question says otherwise.

**The constant-drop model is $V_{BE} = 0.65$ V**, except where a question names the exponential,
and then $V_{BE} = V_T\ln(I_C/I_S)$.

**Every gain in this paper is a voltage ratio**, so decibels are $20\log_{10}$ throughout.

**Where a question says "derive", a stated result scores nothing.** The working is the answer.

**Where a question asks by how much, give the arithmetic.**

No question asks for C++.

### Device parameters

|                                       | Value              |
| ------------------------------------- | ------------------ |
| Thermal voltage $V_T$                 | 26 mV              |
| Saturation current $I_S$              | $10^{-14}$ A       |
| Forward current gain $\beta$          | 50                 |
| Early voltage $V_A$                   | 100 V              |
| Collector-base capacitance $C_{bc}$   | 4 pF               |
| MOSFET threshold                      | 2 V                |
| MOSFET transconductance parameter $k$ | $8\ \text{mA/V}^2$ |

### The E12 series

10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, and every decade of them.

### Marks

| Question | Lecture | Marks   |
| -------- | ------- | ------- |
| 1        | L01     | 10      |
| 2        | L02     | 9       |
| 3        | L03     | 11      |
| 4        | L04     | 10      |
| 5        | L05     | 10      |
| 6        | L06     | 9       |
| 7        | L07     | 11      |
| 8        | L08     | 10      |
| 9        | L09     | 11      |
| 10       | L10     | 9       |
|          |         | **100** |

---

## Question 1 - Where a source resistance comes from (10 marks)

**(a)** Derive the Thevenin equivalent of a two-resistor divider across an ideal supply, giving
both the open-circuit voltage and the source resistance, and stating what you did to the supply and
why that is legitimate. **(3 marks)**

**(b)** A resistor network is driven by two independent sources.

State the superposition principle, the condition a network must satisfy for it to hold, and what
you replace each source with while the other is acting.

Say what happens to the *power* dissipated in a resistor if you try to superpose it, and why.
**(3 marks)**

**(c)** A source with an output resistance $R_s$ drives a load $R_L$.

Derive the value of $R_L$ that extracts the most power from the source, and state the efficiency at
that point.

Then state why almost no circuit in this course is designed that way, and name the two situations
in which it is. **(2 marks)**

**(d)** A colleague argues that a divider's output resistance cannot matter, because "the load is a
million ohms and the divider is only a few kilohms."

State the condition under which they are right, express it as a ratio, and give the error their
argument makes when the ratio is 2. **(2 marks)**

---

## Question 2 - Why a corner is a corner (9 marks)

**(a)** Derive the corner frequency of a series RC low-pass filter from the condition that defines
it, and state that condition in terms of reactance.

Give the phase shift at the corner, and the asymptotic phase shift far above it. **(3 marks)**

**(b)** State why a capacitor's impedance is written as a complex number rather than as a
resistance, and what the imaginary unit is encoding physically.

State the impedance of an inductor and of a capacitor in that notation, and say what the sign
difference means for the current. **(2 marks)**

**(c)** Derive the resonant frequency of a series LC circuit from the condition that the two
reactances cancel.

Then state the Q of a series RLC circuit in terms of its component values, and say what physical
quantity Q is the ratio of. **(2 marks)**

**(d)** An ideal transformer has $N$ times as many turns on its secondary as on its primary.

State what it does to voltage, to current and to impedance, giving the factor in each case, and
show that the third follows from the first two.

Name two things a real transformer does that the ideal model does not. **(2 marks)**

---

## Question 3 - Cascades, virtual shorts, and what an op-amp assumes (11 marks)

**(a)** Two identical RC low-pass sections are connected directly in series.

Explain, without algebra, why the combined circuit's $-3$ dB frequency is **lower** than that of a
buffered pair, and identify the mechanism by name.

Then state the general rule for how the $-3$ dB frequency of $n$ identical buffered sections
relates to the single-section corner, and evaluate it for $n = 2$ and $n = 3$. **(4 marks)**

**(b)** State the two assumptions the ideal operational amplifier model makes, and derive the
virtual short from them.

State precisely which of the two fails first in a real amplifier, and what that failure is called.
**(3 marks)**

**(c)** Derive the closed-loop gain of the inverting configuration from the virtual short, naming
where each assumption is used.

State the inverting amplifier's input resistance and explain why it is not infinite even though the
op-amp's input resistance is. **(2 marks)**

**(d)** A Sallen-Key low-pass filter is built with equal resistors and equal capacitors and a
unity-gain buffer.

State what sets its corner frequency and what sets its Q, and say why those two are separable in
this topology when they are not in a passive cascade. **(2 marks)**

---

## Question 4 - Why everything is a function of the loop gain (10 marks)

**(a)** Derive the closed-loop gain of a negative-feedback amplifier from the summing junction,
stating each step.

Then derive the fractional gain error against the ideal $1/\beta_f$, and show that it depends on
$A$ and $\beta_f$ only through their product. **(4 marks)**

**(b)** State what feedback does to input resistance, output resistance, distortion and bandwidth.

Then explain **why** the same factor appears in all four, in terms of what the loop is doing to a
disturbance introduced inside it. **(2 marks)**

**(c)** An amplifier has a gain-bandwidth product of 1 MHz.

Give its closed-loop bandwidth at closed-loop gains of 10 and of 1000, and its open-loop gain at
1 kHz.

A specification asks for 0.01 per cent gain accuracy at 1 kHz with a closed-loop gain of 10. State
whether this amplifier meets it and justify with a number. **(2 marks)**

**(d)** Explain why Newton-Raphson applied to a diode from a zero starting point fails, in terms of
the shape of the function rather than the arithmetic.

State what step limiting changes and what it deliberately does not, and say why a limiter that
changed the converged answer would be a bug rather than a feature. **(2 marks)**

---

## Question 5 - One equation, three regions (10 marks)

**(a)** Write the transport form of the bipolar transistor's collector and base currents.

Show that with the collector reverse biased it collapses to $I_C = \beta_F I_B$, and show what
happens as the collector-base junction becomes forward biased. **(4 marks)**

**(b)** State why this course prefers a model with no branch in it to one with three cases, giving
two consequences of the branching version. **(2 marks)**

**(c)** Write the MOSFET's square-law drain current in saturation, and derive its transconductance.

Show that $g_m$ goes as the square root of the drain current, and state what that implies about
biasing a MOSFET harder to get more gain. **(2 marks)**

**(d)** At 1 mA, a bipolar transistor's transconductance is about ten times a MOSFET's.

Derive both, state where the factor of ten comes from, and name two design decisions elsewhere in
this course that follow from it. **(2 marks)**

---

## Question 6 - A rule, a load line, and a factor that appears twice (9 marks)

**(a)** Draw or describe the load line of a common-emitter stage with a collector and an emitter
resistor, giving its equation and its two intercepts.

State where on it an amplifier sits and why, and what happens at each end. **(2 marks)**

**(b)** A common rule is to drop about 220 mV across the emitter resistor.

Derive the emitter resistance that gives at an arbitrary collector current, and the emitter factor
it produces.

State why the rule is expressed as a voltage rather than as a resistance, and show that the
resulting emitter factor is independent of the current. **(3 marks)**

**(c)** Show that the factor by which an emitter resistor suppresses thermal drift is the same
factor by which it reduces the stage's gain.

State the consequence in one sentence. **(2 marks)**

**(d)** A designer proposes to fix the thermal problem by choosing a transistor with a lower
temperature coefficient.

State what the coefficient actually is, why it is not a property the designer can choose, and what
the emitter resistor is doing that a better device could not. **(2 marks)**

---

## Question 7 - Three results from one model (11 marks)

**(a)** State the four steps that turn a biased stage into its small-signal schematic, and justify
the first one.

State what the model is blind to, naming three things. **(3 marks)**

**(b)** From the model, derive the common-emitter stage's voltage gain and the resistance looking
into its base.

State which of the two depends on $\beta$ and what that means for specifying it. **(3 marks)**

**(c)** Derive the emitter factor as the ratio of two gains, and then state the two quantities it
is commonly said to decide.

Show which of the two claims is correct as stated, and give the corrected form of the other,
naming the node it belongs to. **(3 marks)**

**(d)** This course introduces $r_s = 1/g_m$ so that every result transfers to a MOSFET by
substitution.

State the two results that transfer and the one that does not, and say why.

Give $r_s$ at 1 mA, the source factor that 220 mV across a source resistor produces, and explain
why it is 2 where the emitter factor is 10. **(2 marks)**

---

## Question 8 - A dead band, a rule, and a thing bolted to a heatsink (10 marks)

**(a)** Derive the emitter follower's voltage gain from the small-signal model, and state the one
quantity its shortfall from unity depends on.

State the follower's input and output resistances, and describe in one sentence what the stage is
for. **(3 marks)**

**(b)** State the three amplifier classes by what conducts when, and give the maximum theoretical
efficiency of two of them.

Explain why crossover distortion is more objectionable than its percentage suggests, in terms of
where in the signal it sits. **(3 marks)**

**(c)** The output-stage rule is to drop one thermal voltage across each emitter resistor.

Show that this makes the emitter factor exactly 2, whatever the idle current.

State the two costs the rule is balancing, and what each would look like if the rule were moved by
a decade in either direction. **(2 marks)**

**(d)** The bias generator of a class-AB stage is two diodes bolted to the output devices'
heatsink.

Explain what they are doing there. State what happens to a stage whose diodes are on the circuit
board instead, and why the two schematics are identical. **(2 marks)**

---

## Question 9 - The tail, the tanh, and the output you choose (11 marks)

**(a)** Explain why a resistance $R_{tail}$ in the tail of a differential pair behaves as
$2R_{tail}$ to one half of the pair.

Then derive the common-mode gain and the common-mode rejection ratio, and show that the collector
resistor cancels. **(4 marks)**

**(b)** State what a current source is, in terms of the two quantities that make it useful in a
tail, and explain why that is the property no resistor can have.

Give the general principle in one sentence, and name two other places in this course where the same
trade appears. **(2 marks)**

**(c)** The pair's difference current is $I_{tail}\tanh(v_d/2V_T)$.

Show that the small-signal transconductance follows from it, and derive the input at which the tanh
falls 1 per cent below its tangent.

Show that this figure does not depend on the tail current, and state what that means for a designer
who wants more linearity. **(3 marks)**

**(d)** A pair's rejection is quoted as 52 dB by one engineer and 98 dB by another, from the same
circuit.

Explain how both can be right, state which measurement each made, and say which quantity limits
each. **(2 marks)**

---

## Question 10 - The gain you cannot buy (9 marks)

**(a)** A common-emitter stage is loaded by a current source rather than a resistor.

Derive its voltage gain, and show that the result does not depend on the collector current.

State what this means for a designer who proposes more supply current to get more gain, and give
the only lever that does work. **(4 marks)**

**(b)** An operational amplifier's two gain stages each give 65.7 dB, and the amplifier delivers
119.9.

Explain where the difference goes and why it cannot be recovered by improving either gain stage.
**(2 marks)**

**(c)** Explain what a Miller compensation capacitor is compensating.

State what it does to the amplifier's open-loop bandwidth, and why deliberately slowing an
amplifier down in one place makes it usable. **(2 marks)**

**(d)** The output stage's input resistance depends on $\beta^2$, which varies by a factor of a
hundred between devices.

Explain in one sentence why the closed-loop gain does not, and name the quantity that makes it so.
**(1 mark)**

---
