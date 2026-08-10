# Analog Electronics - Written Examination, Paper A

**Time:** 4 hours. **Closed book.** A basic calculator is permitted. **Total: 100 marks.**

This paper exists to let you check your own knowledge. It is not a qualification and it gates
nothing. It has one question per lecture, so **it is meant to be taken once the course is over**,
after L10 and the capstone.

---

## Rubric

**The thermal voltage is 26 mV.** Every intrinsic emitter resistance in this paper follows from
$r_e = V_T/I_C$ and that figure.

**Beta is 50** unless a question says otherwise, and it is a worst case rather than a typical
value.

**The constant-drop model is $V_{BE} = 0.65$ V**, except where a question names the exponential,
and then $V_{BE} = V_T\ln(I_C/I_S)$. Knowing which of the two a calculation needs is examinable.

**Every gain in this paper is a voltage ratio**, so decibels are $20\log_{10}$ throughout.

**Where a question asks for a design, give an E12 value** and state the error it leaves. A design
quoted to four figures has not been designed.

**Where a question asks by how much, give the arithmetic.** An assertion without it scores nothing.

No question asks for C++.

### Device parameters

|                                     | Value        |
| ----------------------------------- | ------------ |
| Thermal voltage $V_T$               | 26 mV        |
| Saturation current $I_S$            | $10^{-14}$ A |
| Forward current gain $\beta$        | 50           |
| Early voltage $V_A$                 | 100 V        |
| Collector-base capacitance $C_{bc}$ | 4 pF         |
| NMOS transconductance at 1 mA       | 4 mS         |
| MOSFET threshold                    | 2 V          |

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

## Question 1 - A divider, its resistance, and the load that takes a third (10 marks)

A 33 kilohm resistor and a 6.8 kilohm resistor form a divider across a 10 V supply, with the output
taken at their junction.

**(a)** Give the open-circuit output voltage, and the divider's Thevenin resistance.

State in one sentence why the Thevenin resistance is neither of the two resistors, and why the
supply does not appear in it. **(3 marks)**

**(b)** A 10 kilohm load is connected to that output.

Give the output voltage now, and the fraction of the unloaded value it retains. State the two
different ways of getting there and show that they agree.

A colleague reports the node as sitting at 1.71 V with the load connected. Say what they have
done. **(3 marks)**

**(c)** The requirement is that the load takes no more than 1 per cent of the output.

Give the smallest load resistance that meets it, and the largest divider Thevenin resistance that
would meet it with the original 10 kilohm load.

Give one way of meeting the requirement without changing either resistor's ratio, and state its
cost. **(2 marks)**

**(d)** This same subtraction appears in six separate places in this course.

Name three of them, with the quantity being divided down in each, and say what the six have in
common. **(2 marks)**

---

## Question 2 - One capacitor, two corners, and the resistance nobody drew (9 marks)

A 159 nF capacitor is connected from the output of the divider in Question 1 to ground, through a
1 kilohm series resistor. The intent is a low-pass filter with a corner at about 1 kHz.

**(a)** Give the capacitor's reactance at 1 kHz, and the corner frequency the 1 kilohm resistor and
the capacitor give on their own. **(2 marks)**

**(b)** Give the corner frequency the circuit actually has, and the ratio between the two.

State what resistance is responsible and why it does not appear anywhere on the schematic.
**(3 marks)**

**(c)** Give the attenuation, in decibels, that this filter applies at the frequency it was
designed to have as its corner. Say what a measurement at that frequency would look like to
somebody who did not know about part (b). **(2 marks)**

**(d)** A series LC circuit uses 10 mH and 1 microfarad with 10 ohm of series resistance.

Give its resonant frequency, the reactance of the inductor at resonance, and its Q. State what the
voltage across the inductor is at resonance, relative to the applied voltage, and why that is not a
violation of anything. **(2 marks)**

---

## Question 3 - Two sections, one buffer, and the factor of 1.72 (11 marks)

**(a)** A single RC low-pass section uses 1 kilohm and 159 nF. Give its corner frequency and its
roll-off in decibels per decade well above it. **(1 mark)**

**(b)** Two such sections are connected directly in series, output of the first to input of the
second.

Give the combined circuit's $-3$ dB frequency, and the ratio between it and the answer to part (a).

Now give the $-3$ dB frequency two such sections would have if a perfect buffer were placed between
them, and the ratio between *that* and part (a). **(4 marks)**

**(c)** State the ratio between your two answers to part (b), and say precisely what the buffer
bought. Say why it did not change the roll-off. **(2 marks)**

**(d)** An ideal operational amplifier is used as a Schmitt trigger, with positive feedback from
the output to the non-inverting input through a 100 kilohm resistor, and a 10 kilohm resistor from
that input to ground. The supplies are $\pm 12$ V.

Give the two thresholds, and the hysteresis between them.

The 10 kilohm resistor is changed to 1 kilohm. Give the new thresholds, and say what has happened
to the circuit's immunity to a noisy input. **(4 marks)**

---

## Question 4 - Loop gain, the error it divides, and a diode that will not converge (10 marks)

**(a)** An amplifier with an open-loop gain of $10^5$ is used with a feedback fraction of 0.1.

Give the ideal closed-loop gain, the loop gain, the actual closed-loop gain, and the error as a
percentage.

Repeat for open-loop gains of $10^3$ and $10^6$, and state the relationship between the loop gain
and the error in one sentence. **(4 marks)**

**(b)** State what feedback does to a stage's input resistance, its output resistance, its
distortion and its bandwidth, giving the factor in each case.

Say which single quantity all four answers are functions of, and why that makes the open-loop gain
on its own an incomplete specification. **(2 marks)**

**(c)** A diode with $I_S = 10^{-14}$ A is connected in series with a 1 kilohm resistor across a
5 V supply.

Give the diode voltage and the current, working to four significant figures. State the equation you
solved and the fact that makes it unsolvable in closed form. **(2 marks)**

**(d)** A Newton-Raphson iteration is started from a diode voltage of zero.

Say what happens on the first step and why. Give the approximate number of iterations the
unlimited iteration takes to settle, and the number it takes with the step limiting this course
specifies.

State what the limiting does, in one sentence, and why it does not change the answer. **(2 marks)**

---

## Question 5 - Sixty millivolts a decade, and a switch that ignores beta (10 marks)

**(a)** Give the base-emitter voltage a transistor with $I_S = 10^{-14}$ A needs for collector
currents of 10 microamps, 1 mA and 10 mA.

State the voltage change per decade of current, and derive it. **(3 marks)**

**(b)** Name the three regions this course uses, in terms of which junction is forward biased.

State which region an amplifier lives in and which two a switch uses, and say what the transistor
is behaving as in each. **(2 marks)**

**(c)** A microcontroller output at 5 V must switch a load drawing 150 mA from a 12 V rail.

Design the base drive using a forced beta of 10. Give the base resistor, the nearest E12 value, the
base current that value delivers, and the forced beta it actually produces.

The transistor's datasheet gives $h_{FE}$ as 100 minimum and 400 typical. State where either
number entered your design, and what that means for building a thousand of them. **(3 marks)**

**(d)** The course's transport model has no branch in it on which region the device is in.

State how saturation arises from it, and say what a model written with three cases instead would
show at the boundaries. **(2 marks)**

---

## Question 6 - A bias point that loads itself, and drift that is a loop gain (9 marks)

A common-emitter stage runs from 10 V. Its base is biased by 33 kilohm and 6.8 kilohm, its emitter
resistor is 1 kilohm and its collector resistor is 4.7 kilohm.

**(a)** Give the collector current the unloaded divider predicts. **(1 mark)**

**(b)** Give the base current at that collector current, the voltage it drops across the divider's
Thevenin resistance, and the collector current that actually results.

Give the error between the two answers as a percentage, and name the lecture whose arithmetic this
is. **(3 marks)**

**(c)** Define the divider's stiffness, compute it for this stage, and state the usual rule of
thumb.

Give the divider current a stiffness of 200 would need, and say why that is usually the point at
which a designer changes the bias arrangement instead. **(2 marks)**

**(d)** A tempting argument for the emitter resistor runs: a one degree rise raises the collector
current 10 per cent to 1.1 mA, so the emitter voltage rises to 1.1 V, so with the base held at
1.65 V the base-emitter voltage falls to 0.55 V, which reduces the current again.

Compute what a base-emitter voltage of 0.55 V would actually do to the collector current, relative
to 0.65 V.

State what is wrong with the argument, give the correct suppression factor for this stage, and name
the quantity that factor is equal to. **(3 marks)**

---

## Question 7 - The emitter factor, and the node it belongs to (11 marks)

A common-emitter stage runs at 1 mA with a 10 kilohm collector resistor and a 234 ohm emitter
resistor.

**(a)** Give $r_e$, the emitter factor, the stage's voltage gain, and the gain the same stage would
have with the emitter resistor bypassed.

Give the resistance looking into the base. **(3 marks)**

**(b)** A tempting rule states that the emitter resistor multiplies the stage's output resistance
by the emitter factor, giving 100 kilohm here.

State why that cannot be true, **without computing anything**.

Then give the resistance looking into the collector, and the stage's actual output resistance.
**(4 marks)**

**(c)** The collector resistor is replaced by a current mirror.

Give the stage's output resistance with and without the emitter resistor, and state what the
emitter factor is now worth.

Say what this establishes about why mirror loads are used. **(2 marks)**

**(d)** The bypassed stage of part (a) is driven from a 1 kilohm source.

Give the capacitance the source sees, and the corner frequency that produces.

State what a cascode does to that number and what it costs. **(2 marks)**

---

## Question 8 - Eight ohms, two Darlingtons, and a bias that is not two drops (10 marks)

**(a)** An emitter follower biased at 120 mA drives an 8 ohm loudspeaker.

Give its voltage gain, and the resistance looking into its base.

Give the same two numbers for a Darlington follower at the same current and load, and state the
relationship between a Darlington's effective emitter resistance and a single transistor's.
**(4 marks)**

**(b)** The stage of Question 7(a), with an output resistance of 9.89 kilohm and a gain of 38.5,
must drive that loudspeaker.

Give the gain it delivers directly into 8 ohms, through the single follower, and through the
Darlington. Express each as a percentage of the unloaded gain. **(3 marks)**

**(c)** A class-AB output stage is to idle at 120 mA.

Give the emitter resistors the 26 millivolt rule specifies, the nearest E12 value, and the emitter
factor that produces.

Give the bias voltage the stage needs between the two bases, computed from the exponential. Then
give the idle current that results if the bias is instead set to two constant drops plus the two
resistor drops, and the ratio between the two currents.

Say in one sentence why the constant-drop model, worth about 1 per cent in Question 5, is worth
that ratio here. **(3 marks)**

---

## Question 9 - The tail, the 520 volts, and the resistor that cancels (11 marks)

A differential pair runs from a 2 mA tail with 10 kilohm collector resistors, and the output is
taken at one collector.

**(a)** Give $r_e$ on each side, and say why it is not $V_T$ divided by the tail current.

Give the differential gain to one collector, and the gain to both. Account for both factors of two.
**(3 marks)**

**(b)** The tail is a 10 kilohm resistor to a negative rail.

Give the common-mode gain and the common-mode rejection ratio, as a ratio and in decibels.

Show that the collector resistor cancels out of the rejection ratio, and state what that means for
a designer who proposes a larger collector resistor to improve it. **(4 marks)**

**(c)** The requirement is 80 dB of rejection at the same tail current.

Give the tail resistance that would need, and the voltage such a resistor would drop.

Give the output resistance a simple current mirror would present at 2 mA and the rejection that
gives, and say what has to be done instead. **(2 marks)**

**(d)** The collector resistors are replaced by a current mirror.

Give the differential gain to the single output, and split the improvement over part (a) into its
two independent causes with a number for each. **(2 marks)**

---

## Question 10 - A gain budget, and the two stages that amplify nothing (9 marks)

An operational amplifier is built from four stages: a mirror-loaded differential pair at a 2 mA
tail, a Darlington emitter follower at 1 mA, a common-emitter stage at 1 mA with a current-source
load, and a class-AB Darlington output idling at 120 mA into 8 ohms. The rails are $\pm 15$ V.

**(a)** Give the unloaded gain of stage 1 and of stage 3.

Give the input resistance of stages 2, 3 and 4. **(3 marks)**

**(b)** Give each stage loaded by the next, and the open-loop gain in decibels.

Give the decibel difference between that and the product of the two unloaded gains, and say which
single stage accounts for most of it. **(3 marks)**

**(c)** Give the open-loop gain the amplifier would have with the Darlington follower removed and
stage 1 driving stage 3 directly.

State what that stage is worth in decibels, and what it costs in signal. **(2 marks)**

**(d)** The amplifier is asked to solve for its DC operating point with the loop open, and the
output is reported at the negative rail.

State whether this is a fault, and justify your answer with one number. **(1 mark)**

---
