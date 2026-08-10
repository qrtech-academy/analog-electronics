# Course Information
## Instructor
Erik Pihl ([erik.axel.pihl@gmail.com](mailto:erik.axel.pihl@gmail.com))

---

## Who This Is For
Embedded and software engineers who read schematics, place parts, and have at some point been
handed an amplifier stage and had no way to tell whether it was right. You can write C++, you are
comfortable rearranging an expression, and you have never been shown where a bias resistor value
comes from. This course is ten hours on where.

It is deliberately narrow. Ten hours is not long enough for everything an analog textbook
carries, so this edition keeps what decides a design and says plainly what it dropped. See
[What This Edition Leaves Out](#what-this-edition-leaves-out).

---

## Prerequisites
Participants are expected to arrive already comfortable with:
* Ohm's law and what a resistor, a capacitor and a voltage source are. Nothing beyond that is
  assumed about circuits; L01 and L02 build the rest.
* Engineering calculations: rearranging an expression, working in decibels, taking a logarithm,
  and being willing to carry an approximation and say how wrong it is.
* Complex numbers far enough to accept that $j$ rotates by ninety degrees. L02 uses that and
  builds the frequency domain out of it.

**No semiconductor physics is taught, and none is needed.** The transistor is introduced as a
device with an exponential, a current gain, and a saturation voltage. Depletion regions, carrier
transport and the Ebers-Moll derivation are named once and not used.

**C++ is used, and this is not a C++ course.** You write a small analysis library across the ten
lectures. The C++ involved is free functions, plain structs, `std::vector` and `std::complex`.
There is no class hierarchy anywhere in it. If you have written embedded C++, you have written
harder code than any of it.

**No LTspice, no breadboard, no instrument.** A C++17 compiler, `make` and `git`. See
[There Is No Instrument Here](../README.md#there-is-no-instrument-here-and-that-is-the-design)
for why, and what replaces it.

---

# Course Plan - Analog Electronics

| Lecture | Part        | Topic                                                           |
| ------- | ----------- | --------------------------------------------------------------- |
| L01     | Foundations | Circuits, units, and the nodal solver                           |
| L02     | Foundations | Reactance, phasors, and frequency response                      |
| L03     | Foundations | Passive filters and the operational amplifier                   |
| L04     | Foundations | Feedback, active filters, and the diode                         |
| L05     | Transistors | The transistor as a device and as a switch                      |
| L06     | Transistors | Biasing, and what an emitter resistor actually buys             |
| L07     | Transistors | Small-signal analysis: r_e, the emitter factor, and the cascode |
| L08     | Transistors | Followers, and the output stage they turn into                  |
| L09     | Transistors | The differential amplifier                                      |
| L10     | Transistors | Building an operational amplifier, and the capstone             |

Each lecture is one hour, of which roughly a third is live coding. Three things about the ordering
are deliberate, and all three differ from how the subject is usually taught.

**The solver comes first.** L01 has you write nodal analysis before you have met a single active
device. It costs an hour and it pays for the rest of the course: from then on every claim the
material makes about a circuit can be checked against a program you wrote, and no result has to be
taken on authority.

**The operational amplifier comes before the transistor.** You use one as a black box in L03 and
L04, and only in L10 do you build one. That inversion is the whole arc of the course: the thing you
were told to trust in the fourth lecture is the thing you design in the last one.

**The imperfections come before the topologies.** Biasing, thermal drift and the emitter factor are
met in L06, before any of the clever stages. Meeting them early means that in L07 the question "why
would anyone use a current mirror as a load" has an answer you can compute rather than remember.

---

## Lecture Content
Two parts. **Foundations** (L01-L04) is circuit theory, passives, filters and the op-amp as a black
box; **Transistors** (L05-L10) is the subject of the course.

---

### Part 1 - Foundations
#### L01 - Circuits, Units, and the Nodal Solver
Circuit analysis as something a program does, built before there is anything interesting to analyse.
* Charge, current, voltage and power, and the sign convention that decides every later result.
* Series and parallel, the voltage divider, and why the divider is the only circuit worth
  memorising.
* Kirchhoff's two laws as the only physical content in the whole of circuit theory.
* Thevenin and Norton, and loading as the reason they matter.
* Nodal analysis: one unknown per node, one equation per node, and the conductance stamp.
* Why a solver is easier to write than the equations are to solve by hand.
* Live-coding `ael::net` and `ael::mna`.

#### L02 - Reactance, Phasors, and Frequency Response
The frequency domain, arrived at by making the solver complex rather than by deriving a transform.
* The capacitor and the inductor as devices that remember, and the RC time constant.
* Sinusoidal steady state, the phasor, and why $j\omega$ replaces $d/dt$.
* Impedance as resistance that depends on frequency, and the stamps that follow.
* Magnitude and phase, the decibel, and the Bode plot as two straight lines and a corner.
* Reading a first-order response: what the corner is, and what it is not.
* The transformer, briefly, and where its model stops being true.
* Live-coding the complex stamps and `ael::ac`.

#### L03 - Passive Filters and the Operational Amplifier
The first useful circuits, and the first active device.
* High-pass and low-pass RC: the transfer function, the corner frequency, and the impedances.
* Loaded against unloaded, and why cascading two filters does not give you the two corners.
* LC filters, resonance, and Q as the number that says how much the corner overshoots.
* The band-pass, its bandwidth, and the trade its two corners cannot escape.
* The operational amplifier as a black box: the ideal rules, and the virtual short.
* Inverting, non-inverting, buffer, summing and difference, all from the same two rules.
* The comparator, hysteresis, and the Schmitt trigger, which are not amplifiers at all.
* Live-coding `ael::filter`, the VCVS element in `ael::net`, and `ael::opamp`.

#### L04 - Feedback, Active Filters, and the Diode
Why the ideal rules work, what they cost, and the first nonlinear device.
* Loop gain, and the closed-loop gain written so that the error term is visible.
* Desensitisation: feedback trading gain you have for accuracy you want.
* What feedback does to input and output impedance, and in which direction.
* Distortion reduced by the loop gain, and the nonlinearity that always survives.
* Gain-bandwidth product, and the stability limit that ends the free lunch.
* Active filters, and the loading problem they solve.
* The diode: the exponential, the 0.7 V approximation, and when it is a lie.
* Newton-Raphson, and why a nonlinear solver is a linear solver in a loop.
* Live-coding `ael::feedback`, `ael::device::diode` and `ael::nr`.

---

### Part 2 - Transistors
#### L05 - The Transistor as a Device and as a Switch
The device, with as little semiconductor physics as can be managed, which is almost none.
* The BJT as an exponential with a current gain, and $h_{FE}$ as the number you must not trust.
* Why the course assumes $h_{FE} = 50$ everywhere, and what that assumption is worth.
* Active, saturation and cutoff, and the one of the three a switch lives in.
* Designing a switch: base resistor, forced beta, and the saturation voltage you pay.
* The MOSFET: threshold, triode and saturation, and the square law.
* BJT against MOSFET, honestly: transconductance, input current, turn-on voltage, and matching.
* Live-coding `ael::device::bjt` and `ael::device::mosfet`.

#### L06 - Biasing, and What an Emitter Resistor Actually Buys
The quiescent point, and the first place the obvious argument needs correcting.
* The quiescent point as three numbers, and the load line that constrains them.
* Voltage-divider bias, and the stiffness the divider needs.
* Thermal drift: $V_{BE}$ falling 2 mV per degree, and what that does to the collector current.
* The emitter resistor as local feedback, and the drift divided by $1 + R_E/r_e$.
* The plausible wrong answer: why the collector current does not simply "increase 10 % and come
  back", and what $V_{BE}$ actually moves by.
* The 220 mV rule, and the E12 value it lands on.
* Live-coding `ael::bias`.

#### L07 - Small-Signal Analysis: r_e, the Emitter Factor, and the Cascode
The centre of the course, and the model the whole of Part 2 is built on.
* Small-signal as a straight line through an operating point, and everything that discards.
* Building the small-signal schematic: what to short, what to delete, what to replace.
* The intrinsic emitter resistance $r_e = 26\ \text{mV}/I_C$, and where the 26 mV comes from.
* Gain, input resistance and output resistance, each from one walk around a loop.
* **The emitter factor** $EF = (r_e + R_E)/r_e$: one number for what degeneration costs and buys.
* Which resistance EF actually multiplies, and why a resistive load throws the boost away.
* The Early effect, r_o, and the current mirror as the load that keeps what EF earned.
* **The source factor** and $r_s = 1/g_m$: every result above, transferred to the MOSFET by
  substitution.
* The Miller effect, and the cascode as the answer to it.
* Live-coding `ael::ssm`, checked against the solver on every stage.

#### L08 - Followers, and the Output Stage They Turn Into
The stage with no voltage gain, and why almost every design has one.
* The emitter follower: gain just under one, high input resistance, low output resistance.
* Output resistance $\approx r_e$, and the impedance transformation that is the point.
* The Darlington, and the two things it costs.
* The source follower, and where it beats the emitter follower.
* Class A, B and AB, and the crossover distortion that decides between them.
* Quiescent biasing by the 26 mV rule, and thermal runaway if you get it wrong.
* Live-coding `ael::follower` and `ael::output`.

#### L09 - The Differential Amplifier
The input stage of every operational amplifier, and the first circuit that rejects rather than
amplifies.
* The pair, the tail current, and the split that makes it differential.
* Differential gain, and why it is the common-emitter result with a factor of two in it.
* Common-mode gain, the tail resistance that sets it, and the current source that kills it.
* CMRR: what it measures, what it hides, and what a datasheet means by it.
* Input and output resistance in both modes, which are four different answers.
* The current mirror as an active load, and the single-ended output it makes possible.
* Offset and matching, and why almost every modern input stage is MOSFET.
* Live-coding `ael::diffpair`.

#### L10 - Building an Operational Amplifier, and the Capstone
The black box from L03, opened and rebuilt from the six lectures since.
* The four stages, and which parameter each one is responsible for.
* Sizing the reference currents, and the mirrors that distribute them.
* Miller compensation, and the pole it moves on purpose.
* Predicting the open-loop gain term by term, then closing the loop and predicting the error.
* Where the prediction and the solver disagree, and which one to believe.
* The capstone: a requirement in words, turned into a design you can defend.
* Live-coding `ael::report`, then the whole toolkit on the capstone.

---

## What This Edition Leaves Out
About 1000 pages became ten lectures. What went, in full, and where to find it:

| Cut                                                                            | Kept here as                               |
| ------------------------------------------------------------------------------ | ------------------------------------------ |
| Basic electronics as eight chapters: transformer design, rectifier sizing, rms | L01 and L02, at the level later work needs |
| Passive filters as six chapters, each with its own full impedance treatment    | L03, one treatment covering all of them    |
| Telescopic cascodes and CMOS amplifier topologies                              | Not covered; the cascode itself is L07 B.5 |
| Output stages up to 1 kW: triple class-AB, CFP-EF, Zobel networks, protection  | A reference appendix in L08, as reading    |
| Sixteen appendices of full derivations                                         | The results, with the derivations cited    |
| Noise analysis, Miller's theorem as a chapter, and CMOS frequency response     | The Miller effect in L07; noise not at all |
| Oscillators, voltage regulators, and a CMOS comparator                         | Not covered                                |

The last two rows are material a full treatment would carry and this edition does not. Noise in
particular is a real omission: it decides the input stage of any amplifier that matters, and it is
the first thing to add if this course is ever extended. It is covered from the system side in a
sibling course on mixed-signal design, which assumes exactly what this course teaches and is the
natural thing to read next.

PCB layout, datasheet reading and phase margin as a design procedure are in neither.

**Where the obvious answer is wrong**, the correction is taught rather than applied quietly. The
two largest are L06's thermal argument and L07's output resistance, and both are worked
demolitions: the tempting claim, the arithmetic that breaks it, and the version that survives.

---

## Course Material
### Literature
* Consists of the README and appendix documents in this repository. There is no set textbook:
  every derivation, figure and number here is written for this course.
* *The Art of Electronics* (Horowitz and Hill, 3rd edition) is the natural companion. It uses the
  same intrinsic-emitter-resistance approach this course is built on.
* *Microelectronic Circuits* (Sedra and Smith) if you want the hybrid-pi treatment instead, and the
  device physics this course skips.

### Software
* A C++17 compiler (`g++` 9 or newer), `make` and `git`. On WSL/Ubuntu:
  `sudo apt install git make g++`.
* [Visual Studio Code](https://code.visualstudio.com/download):
    * Primary editor.
* Nothing else. No LTspice, no MATLAB, no breadboard, no instrument.

---
