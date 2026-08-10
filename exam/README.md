# Written Examinations

Two complete four-hour papers for **Analog Electronics**, with worked solutions.

```text
paper_a.md              Paper A, questions only. Hand this out.
paper_a_solutions.md    Paper A, model answers with marks.
paper_b.md              Paper B, questions only.
paper_b_solutions.md    Paper B, model answers with marks.
```

---

## What these are for

The course as written has **no exam and nothing is marked**. Assessment is the exercises in every
lecture, the shipped test suite each component comes with, and the Cross-check that closes every
one of the ten lectures.

These papers do not replace any of that. **They are here for students to check their own knowledge,
and nothing else.** They gate nothing, they are not a qualification, and no part of the course
requires them. Nothing in the repository depends on them and `make test` does not know they exist.
What they check is the half the test suites cannot: whether you can still produce the derivation
with the appendix out of the room.

**Take one only once the course is over.** Every paper has one question per lecture, so sitting one
partway through examines material nobody has taught you yet. The intended point is after L10, once
the capstone's report prints a row for every stage.

---

## The two papers

Both cover the whole course, one question per lecture, and question N carries the same lecture and
the same mark in both. They share no question, so the topics below are Paper A's; Paper B's ten
are different. Either can be used alone; use both as a main sitting and a resit, or in alternate
years.

| Question | Topic                                                               | Lecture | Marks   |
| -------- | ------------------------------------------------------------------- | ------- | ------- |
| 1        | A divider, its Thevenin resistance, and a load that takes a third   | L01     | 10      |
| 2        | One capacitor, two corners, and the resistance nobody drew          | L02     | 9       |
| 3        | Two sections, one buffer, and the factor of 1.72                    | L03     | 11      |
| 4        | Loop gain, the error it divides, and a diode that will not converge | L04     | 10      |
| 5        | Sixty millivolts a decade, and a switch that ignores beta           | L05     | 10      |
| 6        | A bias point that loads itself, and drift that is a loop gain       | L06     | 9       |
| 7        | The emitter factor, and the node it belongs to                      | L07     | 11      |
| 8        | Eight ohms, two Darlingtons, and a bias that is not two drops       | L08     | 10      |
| 9        | The tail, the 520 volts, and the resistor that cancels              | L09     | 11      |
| 10       | A gain budget, and the two stages that amplify nothing              | L10     | 9       |
|          |                                                                     |         | **100** |

**The weighting is the course's own.** Ten lectures in two parts of four and six, and the paper
puts 40 marks on Part 1 and 60 on Part 2, because that is the split the course was designed with
and the transistors are the point of it.

The three at 11 are L03, L07 and L09, because each asks for two separate derivations rather than
one: a cascade's corner and the buffer that fixes it; the emitter factor and the node it belongs
to; the two gains of a pair and the ratio in which the load cancels. The three at 9 are L02, whose
examinable content is one reactance and one corner; L06, which is a droop and a suppression factor;
and L10, which is a multiplication and one observation about it.

**Paper A leans towards the numbers this repository publishes and checks**: 1.7085 V from a 33k
and a 6.8k, a Thevenin resistance of 5.638 kilohm and a third of the output lost to a 10 kilohm
load; a 1001 Hz corner that becomes 151 Hz; a cascade at 375 Hz where a buffer would give 644;
0.01 per cent of gain error from a loop gain of ten thousand; a diode at 0.6965 V that takes 168
Newton iterations without limiting and 7 with it; 290 ohm becoming 270 and a forced beta of 9.3;
a base that droops 105 mV and a collector current of 0.934 mA rather than 1.06; an output
resistance of 9.89 kilohm where the tempting rule says 100; a Darlington's 21.08 kilohm against a
single follower's 411; 51.7 dB of rejection and the 520 V it would take to reach 80; and an
open-loop gain of 119.9 dB where the stage gains multiply to 131.4.

**Paper B leans towards the results the course derives**: why a divider's output resistance is the
parallel combination and not either resistor; why a corner moves when nothing in the filter
changed; why two identical sections do not give twice the roll-off at the same corner; why every
feedback result is a function of the loop gain rather than of the open-loop gain; why saturation is
not a case a transport model handles but a thing the equation does; why a thermal argument that
moves $V_{BE}$ by 100 mV describes a circuit that does not exist; why the emitter factor multiplies
the resistance looking into the collector and not the stage's output resistance; why a model worth
1 per cent in one calculation is worth a factor of sixty in another; why the collector resistor
cancels out of a rejection ratio; and why two stages with no voltage gain are worth more decibels
than either gain stage.

Neither paper asks a candidate to write C++. The toolkit is how the course teaches; it is not what
the course is about, and a written paper that asked for an `ael::ssm` implementation would be
examining typing.

---

## Conventions the papers assume

Both papers state these in their own rubric, so a candidate never has to have read this file.

* **The thermal voltage is 26 mV** and every $r_e$ in both papers follows from it. The physical
  value is 25.85 mV at 300 K, and 25.87 mV at the 300.15 K that L06 makes the device model's
  default; the course rounds, says so, and marks to the rounded figure.
* **Beta is 50**, and it is a worst case rather than a typical one. Where a question wants the
  spread it gives the two values.
* **The constant-drop model is 0.65 V**, except where a question names the exponential, and then
  $V_{BE} = V_T \ln(I_C/I_S)$ with $I_S = 10^{-14}$ A. Several answers turn on knowing which of
  the two a calculation needs.
* **Component values land on E12** wherever a question asks for a design, and the answer is the
  E12 value with the resulting error stated. A design quoted to four figures has not been
  designed.
* **Twenty for amplitudes, ten for powers.** Both produce a number in dB carrying no label. Every
  gain in this course is a voltage ratio, so it is $20\log_{10}$ throughout, and a candidate who
  uses ten has halved every answer in decibels.
* **A number pinned by a rule is pinned.** The 220 mV degeneration rule, the 26 mV output-stage
  rule, $r_e = V_T/I_C$, the emitter factor as $(r_e + R_E)/r_e$, and $r_o = V_A/I_C$ with
  $V_A = 100$ V each fix an answer exactly.
* **An assertion without arithmetic scores nothing** where a question asks which of two terms
  dominates, or by how much, which is several of them.

---

## Marking

Every solution is written to be marked by somebody who has read the appendices and has not written
the toolkit, so each carries the reasoning rather than the answer alone. Marks are shown per part.

* **Method carries the marks.** A correct rule with an arithmetic slip in it is worth more than a
  correct number with no working, and several questions consume their own earlier answers. Follow
  through an error rather than penalising it twice.
* **The named traps are worth full marks on their own.** Several parts exist entirely to see
  whether a candidate avoids one specific mistake. The list, in the order the papers meet them:

| Trap                                                        | Where    | What it looks like                                               |
| ----------------------------------------------------------- | -------- | ---------------------------------------------------------------- |
| A divider's output resistance taken as the lower resistor   | L01      | 6.8 kilohm where the answer is 5.638                             |
| A loaded divider computed without reforming the divider     | L01      | 1.71 V quoted for a node sitting at 1.09                         |
| An RC corner computed from the resistor that is drawn       | L02      | 1001 Hz where the circuit gives 151                              |
| Two cascaded sections given the single-section corner       | L03      | 1001 Hz where the answer is 375                                  |
| A feedback result computed from the open-loop gain alone    | L04      | An error that does not move when the feedback network does       |
| Newton started at zero on an exponential                    | L04      | 168 iterations, or no convergence at all                         |
| A saturated transistor assumed to obey $\beta$              | L05      | A base current 5 times smaller than the design needs             |
| A switch designed from the datasheet's $h_{FE}$             | L05      | A design that works on one device and not the next               |
| A divider bias computed unloaded                            | L06      | 1.06 mA where the stage sits at 0.934                            |
| The thermal argument that moves $V_{BE}$ by 100 mV          | L06      | A factor of 47 described as 10 per cent                          |
| The emitter factor applied to the stage's output resistance | L07      | 100 kilohm where a parallel combination cannot exceed 10         |
| $r_e$ read from the tail current rather than one side       | L07, L09 | Every gain out by a factor of two                                |
| A Miller capacitance left unmultiplied                      | L07      | A bandwidth 385 times too optimistic                             |
| A Darlington's $r_e$ not doubled                            | L08      | An input resistance 2.6 per cent low, and an identity that fails |
| A class-AB bias taken as two constant drops                 | L08      | 2 mA of idle current where 120 was wanted                        |
| A larger collector resistor prescribed to improve CMRR      | L09      | Both gains doubled and the rejection unchanged                   |
| An ideal current source read as infinite rejection          | L09      | 101 dB reported from a mechanism nobody designed                 |
| A gain budget computed without loading                      | L10      | 131 dB claimed for a 120 dB amplifier                            |
| An open-loop DC solve expected to converge mid-rail         | L10      | A solver blamed for an amplifier's own arithmetic                |

* **The discussion parts are not decoration.** "Say what this establishes" and "say what it does
  not" is where the course's actual content is, and a paper marked only on the arithmetic would
  pass a candidate who has understood none of it. Four of the hardest things in this course carry
  almost no arithmetic at all: that a source resistance and a load resistance form a divider and
  that this one subtraction decides six separate results; that a model's accuracy is a property of
  the calculation it appears in rather than of the model; that an idealisation can delete the very
  quantity a design is about; and that the stages with no gain are the ones that make the gain
  usable.

---
