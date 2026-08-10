# Appendix D - Solutions

In full, including the plausible wrong answers. The Cross-check here is the first in the course
where the closed form is **qualitatively** wrong: it says a design lever always helps, and past a
certain point that lever makes things worse.

---

## D.1 Recall: the pair and its tail

1. The tail fixes the **sum** of the two collector currents. The inputs decide only the
   **division** of that sum.
2. **26 ohm.** Each side carries half the tail, so $r_e = V_T/(I_{tail}/2) = 26/1 = 26$ ohm. The
   easy mistake is $26/2 = 13$, from reading the tail current instead of the side current.
3. For a **differential** input the tail node barely moves, because the sum is unchanged. For a
   **common-mode** input the tail node moves with the inputs, because the sum cannot change and
   something has to give.
4. Because the tail carries **both** currents. If one half's current rises by $i$ and the other's
   rises by $i$ too, the tail carries $2i$, so the voltage it develops is $2iR_{tail}$, and one
   half sees that as $2R_{tail}$ in its own emitter.

---

## D.2 Recall: the two factors of two

1. One two is the **input split**: a differential input of $v_d$ puts $v_d/2$ on each base. The
   other two is not in that formula at all, which is the point of question 2.
2. In the **output**. Taking one collector discards the other half. Taking the difference between
   the two collectors gives $-R_C/r_e$, twice as much. A **current-mirror load** recovers it while
   keeping a single-ended output.
3. The input split is what "differential" means and cannot be avoided. The output is a choice.
4. **A factor of two from the mirror as a mirror**, which recovers the discarded half, and **a
   factor of five from the load**, because $r_o \parallel r_o$ is 50 kilohm where the resistor was
   10. Neither depends on the other.

---

## D.3 Hand calculation: the pair, resistively loaded

|                           | $R_C = 10$ k | $R_C = 100$ k |
| ------------------------- | ------------ | ------------- |
| $r_e$                     | 26 ohm       | 26 ohm        |
| $A_{dm}$, one collector   | $-192$       | $-1923$       |
| $A_{dm}$, both collectors | $-385$       | $-3846$       |
| $A_{cm}$, one collector   | $-0.499$     | $-4.99$       |
| CMRR                      | **385**      | **385**       |
| CMRR in decibels          | **51.7 dB**  | **51.7 dB**   |

<!-- value: 51.7 = decibels(cmrr(10e3, 2e-3, 10e3)) -->

**Every gain went up by ten and the rejection did not move at all.** That is the lecture's central
result, and doing it twice with a pencil is more convincing than the algebra: $R_C$ appears in the
numerator of both gains and cancels out of the ratio exactly.

**The plausible wrong answer** is that more gain means better rejection. It is a common-mode
*gain*, not a common-mode error, and raising the differential gain raises it by exactly as much.

---

## D.4 Hand calculation: the large signal

| $v_d$  | Difference current | Fraction of the tail |
| ------ | ------------------ | -------------------- |
| 5 mV   | 0.192 mA           | 9.6 per cent         |
| 26 mV  | 0.924 mA           | 46 per cent          |
| 100 mV | 1.916 mA           | **96 per cent**      |

<!-- value: 9.6 = 100 * diffpair_transfer(5e-3, 2e-3) / 2e-3 -->

**The small-signal answer is 1 per cent optimistic at 9.1 mV**, and that is the pair's honest
linear range.

**At a 20 mA tail it is still 9.1 mV.** The tail multiplies the whole curve and cancels out of the
ratio between the tanh and its tangent, so **linearity does not improve with current**. Biasing
the pair ten times harder buys ten times the transconductance and not one millivolt of range.

That is worth pausing on, because it is the opposite of the pattern the rest of the course has
established. In L08 a follower's every problem was solved by more current. Here more current
solves nothing, and the only lever on linearity is **degeneration**: emitter resistors trade gain
for range one for one, exactly as in L07.

---

## D.5 Design: a pair to a rejection requirement

1. **260 kilohm.** From $CMRR = (2R_{tail} + r_e)/2r_e = 10^4$ with $r_e = 26$ ohm.
2. **520 V.** 260 kilohm carrying 2 mA. There is no such supply in an audio amplifier, and if
   there were, the pair would need 520 V of headroom below its emitters.
3. **A current source**, whose incremental resistance must be at least 260 kilohm while it drops a
   volt or two.

   **And a simple mirror is not enough.** Its output resistance is $r_o = V_A/I_{tail} = 50$
   kilohm at 2 mA, giving 1923, which is **66 dB**. It falls 14 dB short.

   <!-- value: 66 = decibels(early_resistance(2e-3) / diffpair_re(2e-3)) -->

   **A cascoded mirror gives 2.5 megohm**, from [L07's](../../L07/appendix/b_the_emitter_factor.md#b5-miller-and-the-cascode)
   $\beta r_o$ ceiling, and that is **100 dB** with 20 dB to spare. One extra transistor and about
   0.7 V of headroom.

   <!-- value: 100 = decibels(cascode_output_resistance(2e-3) / diffpair_re(2e-3)) -->

4. **7.7 per cent.** With a differential output and a plain 10 kilohm resistor tail,
   $CMRR_{diff} = 2R_{tail}/\delta r_e = 10^4$ needs only $\delta = 0.077$.

   **Which is the design to build, and it is not close.** Ordinary 1 per cent resistors and a
   resistor tail give 98 dB differentially; reaching 80 dB single-ended needs a cascoded current
   source. If the next stage can accept a differential input, take one.

   **The reason the answer is usually the other one** is that the next stage usually cannot. An
   operational amplifier's second stage has one input, so the difference has to be taken
   somewhere, and taking it with a current mirror is
   [B.4](./b_rejection_and_the_mirror.md#b4-the-mirror-load-and-its-two-mechanisms).

---

## D.6 Design: offset

| Source                                    | Input-referred offset |
| ----------------------------------------- | --------------------- |
| Base current through the source imbalance | **180 mV**            |
| 1 mV of $V_{BE}$ mismatch                 | 1.00 mV               |
| 1 per cent of $R_C$ mismatch              | 0.52 mV               |

<!-- value: 0.52 = diffpair_input_offset(0.01, 0.0, 10e3, 2e-3) * 1e3 -->

20 microamps through 10 kilohm is 200 mV; through 1 kilohm it is 20 mV; the difference is 180 mV
and the amplifier cannot tell it from signal.

**The ranking is not close: the first is 180 times the second.** Any effort spent on matched
resistors or matched devices before fixing the source imbalance is wasted.

**The single change that removes it: MOSFET inputs.** A gate draws no current, so the row
disappears rather than being reduced. The cost is gain: $r_s$ is ten times $r_e$
([L07 B.6](../../L07/appendix/b_the_emitter_factor.md#b6-the-mosfet-in-one-substitution)), so the
pair's transconductance falls by ten and its gain with it.

**The classical alternative** is to make the two source resistances equal, which turns the 180 mV
into a common-mode voltage that the pair rejects. It works, it is why textbook op-amp circuits put
a resistor in the non-inverting input matching the parallel feedback network, and it leaves the
*difference* between the two base currents: a 1 per cent beta mismatch leaves 0.2 microamps, which
through 10 kilohm is **2 mV**. Better than 180 and worse than either of the other two rows.

---

## D.7 Code: the pair

Unpublished; the suite is the answer.

The two hints worth repeating. **`commonModeRejection` is the ratio of your own two gain
functions**, so that the cancellation of $R_C$ is something your code does rather than something
you asserted. And **`linearRange` takes no tail current**, because the tail cancels; a signature
with one in it is a derivation that stopped early.

---

## D.8 Cross-check: common-mode rejection, and the lever that reverses

| Leg                                  | CMRR                     |
| ------------------------------------ | ------------------------ |
| 1. By hand, $(2R_{tail} + r_e)/2r_e$ | 385, **51.7 dB**         |
| 2. Closed form, $R_C = 10$ k         | 385, 51.7 dB             |
| 2. Closed form, $R_C = 100$ k        | **385, 51.7 dB**         |
| 3. Solver, 10 kilohm tail            | about 347, **50.8 dB**   |
| 4. Solver, ideal current-source tail | about 111000, **101 dB** |

**Legs 1, 2 and 3 agree to about one decibel**, and the residue is nameable rather than slop:

* The 10 kilohm tail resistor delivers **1.935 mA**, not 2, because the tail node sits about
  0.65 V below ground and the drop across the resistor is 19.35 V rather than 20. Each side
  carries half of that, so $r_e$ is 26.9 ohm rather than 26.
* The device's thermal voltage is $kT/q = 25.87$ mV where the closed form uses 26.
* $r_o$ loads the collector resistor: 10 kilohm in parallel with about 116 kilohm is 9.2.

Put those three together and the differential gain comes to $-172$, against the solver's $-169$.

**The last two per cent is the fourth thing, and it is the base current again.** The tail sets
each side's *emitter* current at 0.968 mA, and `intrinsicEmitterResistance` is written from it,
but the gain is set by the transconductance, which is the *collector* current over $V_T$. The
collector gets $\beta/(\beta+1)$ of the emitter current, so it carries 0.950 mA and the resistance
that matters is $25.87\ \text{mV}/0.950\ \text{mA} = 27.2$ ohm rather than 26.9. Then

$$A_d = \frac{-9.2\ \text{k}\Omega}{2 \times 27.2\ \Omega} = -169$$

and nothing is unexplained. **It is the same $1/\beta$ that L06's divider turned on**, arriving at
a different node and costing two per cent instead of twelve.

### Leg 4 does not return infinity, and that is the exercise

An ideal current source has infinite incremental resistance, so the expectation is that the
common-mode gain is zero and the rejection is infinite. **It is not.** The solver gives a
common-mode gain of $+1.57\times10^{-3}$: small, stable to four figures across four decades of
perturbation size, and **positive**, where the resistor tail gave a negative one.

**It is a real effect and it is not the one the design is about.** The Early effect makes the
collector current depend on $V_{CE}$ while the base current does not, so $h_{FE}$ rises with
$V_{CE}$. An ideal current source fixes the **emitter** current, not the collector current, and
the split between them moves when a common-mode input shifts the tail node and with it $V_{CE}$.

**Two checks confirm the mechanism**, and both are worth running:

| Change                                  | Common-mode gain                                          |
| --------------------------------------- | --------------------------------------------------------- |
| As specified, $V_A = 100$, $\beta = 50$ | $1.57\times10^{-3}$                                       |
| $V_A = 10^9$                            | $4\times10^{-10}$, which is the solver's arithmetic floor |
| $\beta = 5000$                          | $1.6\times10^{-5}$, a hundred times smaller               |

It scales as $1/\beta V_A$, exactly as that account predicts.

### And then the lever reverses

The two mechanisms have **opposite signs**. The resistive one gives a negative common-mode gain
and the beta one a positive one, so at some tail resistance they cancel. Sweep it:

| Tail           | Common-mode gain    | CMRR       |
| -------------- | ------------------- | ---------- |
| 1 megohm       | $-3.3\times10^{-3}$ | 94.5 dB    |
| 2 megohm       | $-8.7\times10^{-4}$ | 106 dB     |
| 3 megohm       | $-6.0\times10^{-5}$ | 129 dB     |
| **3.2 megohm** | $+4.2\times10^{-5}$ | **132 dB** |
| 5 megohm       | $+5.9\times10^{-4}$ | 109 dB     |
| 10 megohm      | $+1.1\times10^{-3}$ | 104 dB     |
| infinite       | $+1.6\times10^{-3}$ | 101 dB     |

**Past about 3 megohm, more tail resistance makes the rejection worse.** The closed form says it
rises without limit; the circuit has a maximum and then declines to a floor.

**Nothing in [B.2](./b_rejection_and_the_mirror.md#b2-cmrr-and-the-term-that-cancels) is wrong.**
That expression describes one mechanism correctly and is silent about the other, and where the
other dominates the expression stops describing the circuit. Two hundred kilohms of tail is well
inside the region where the closed form is right, which is why it is the formula to design with;
several megohms is not, which is why a cascoded tail does not give the 130 dB its resistance
suggests.

### The general statement, which is what the exercise asks for

[L05's Cross-check](../../L05/appendix/c_exercises.md#c8-cross-check-the-switch-and-the-model-that-agrees-with-itself)
had two legs that agreed with each other and were both wrong about a real device. This one has a
leg that is exactly right about the model and answers a question nobody asked.

**Both are the same failure: a model is only informative about the quantities it contains.** The
transport model contained no bulk resistance, so it could not be wrong about saturation voltage.
It simply had nothing to say, and said 57 mV confidently. The ideal current source contains no
output resistance, so it cannot be wrong about common-mode rejection, and it returned 101 dB,
which is a plausible number produced by an unrelated mechanism.

**The dangerous case is not the one that returns infinity or NaN.** It is the one that returns a
number a designer would accept.

### Diagnosing your own legs

* **CMRR near 1 in leg 3** means the common-mode input went to only one base.
* **A differential gain of 385 rather than 192** means you measured the difference between the two
  collectors, which is [B.5](./b_rejection_and_the_mirror.md#b5-the-other-output-and-why-the-answer-changes-completely)'s
  question, not this one.
* **Leg 4 returning something above 200 dB** means your Early effect is missing, and L07's suite
  should have said so.
* **Legs 2 giving two different numbers** means `commonModeRejection` is not a ratio of your two
  gains.

---
