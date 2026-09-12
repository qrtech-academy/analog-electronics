# Appendix B - Rejection, the mirror, and what limits it
Where the rejection comes from, which is not where most people guess, and the load that wins two
independent factors at once.

---

## B.1 Common mode, and the tail doubled
Drive both bases with the same $v_{cm}$: both halves want more current, the tail cannot supply it,
so the tail node rises and the current barely changes. **The tail carries the sum of both
currents,** so a resistance $R_{tail}$ in the tail behaves as $2R_{tail}$ in one half's own
emitter, and it is L07's degenerated stage unchanged:

$$A_{cm} = -\frac{R_C}{2R_{tail} + r_e}$$

With 10 kilohm in the tail and a 2 mA pair, $-0.50$: a gain of *one half* for signals both inputs
share, against 192 for signals they do not.

<!-- value: 0.50 = abs(diffpair_common_mode_gain(10e3, 2e-3, 10e3)) -->

**Nothing new has been introduced:** the emitter factor of
[L07 A.5](../../L07/appendix/a_the_small_signal_model.md#a5-what-the-emitter-resistor-does-to-the-gain)
with $R_E = 2R_{tail}$. The pair is two old circuits wired so one input sees degeneration and the
other does not.

---

## B.2 CMRR, and the term that cancels
$$CMRR = \frac{A_{dm}}{A_{cm}} = \frac{R_C/2r_e}{R_C/(2R_{tail} + r_e)} = \frac{2R_{tail} + r_e}{2 r_e}$$

**Look at what happened to $R_C$.** It cancelled, exactly and completely.

$$\boxed{\;CMRR \approx \frac{R_{tail}}{r_e}\;}$$

<!-- value: 385 = cmrr(10e3, 2e-3, 10e3) -->

**No choice of collector resistor improves rejection, and neither does the gain.** Doubling $R_C$
doubles both gains and rejects exactly as badly. The instinct is universally the other way,
rejection feeling like it should be about matching or about gain: **it is about the tail and only
the tail.**

![Common-mode rejection ratio in decibels against the resistance the tail presents, on a logarithmic axis, rising 20 dB per decade, with the resistor-tail and current-source-tail regions marked and the supply voltage each would need annotated.](./images/cmrr_against_tail.png)

---

## B.3 Which makes it a supply-voltage question
A resistor in the tail carries the tail current, so a tail resistance implies a voltage,
$V_{tail} = I_{tail} R_{tail}$.

| Tail       | CMRR  | In decibels | Volts across it at 2 mA |
| ---------- | ----- | ----------- | ----------------------- |
| 1 kilohm   | 39    | 32 dB       | 2 V                     |
| 10 kilohm  | 385   | 52 dB       | 20 V                    |
| 100 kilohm | 3847  | 72 dB       | 200 V                   |
| 260 kilohm | 10000 | **80 dB**   | **520 V**               |
| 1 megohm   | 38462 | 92 dB       | 2000 V                  |

<!-- value: 52 = decibels(cmrr(10e3, 2e-3, 10e3)) -->

**80 dB of rejection from a resistor needs 520 V of supply,** and 80 dB is unremarkable. A current
source presents hundreds of kilohms of *incremental* resistance while dropping a volt or two of
*actual* voltage, because its resistance is $r_o$. **That is the whole reason the tail is a current
source,** and it generalises: **a current source has a large resistance without a large voltage
across it.**

**A cascoded mirror** raises $r_o$ by another $\beta$
([L07 B.5](../../L07/appendix/b_the_emitter_factor.md#b5-miller-and-the-cascode)): another 34 dB for
one transistor and 0.7 V of headroom, the usual integrated arrangement.

---

## B.4 The mirror load, and its two mechanisms
![A differential pair with a PNP current mirror as its load: the two mirror transistors' emitters to the positive rail, their bases tied, the left one diode-connected to the left pair collector, and the output taken at the right collector.](./images/mirror_loaded_pair.png)

Replace the collector resistors with a **current mirror**: two PNP devices, emitters to the rail,
bases tied, the left diode-connected. M1 carries whatever Q1 carries and M2 copies it into the
output node, so a differential input has the mirror pushing the output up while Q2 pulls it down.
**Both halves now drive the output.**

$$A_{dm} = -\frac{r_{o(n)} \parallel r_{o(p)}}{r_e}$$

<!-- value: 1923 = abs(diffpair_mirror_gain(2e-3, parallel(early_resistance(1e-3), early_resistance(1e-3)))) -->

**1923 against 192, and it is two separate factors:**

* **A factor of two from the mirror as a mirror.** The two in $R_C/2r_e$ came from throwing one
  collector away, and the mirror stops throwing it away. Nothing to do with resistance.
* **A factor of five from the load.** $r_o \parallel r_o$ is 50 kilohm where the resistor was 10.
  Nothing to do with mirroring.

**They multiply, and textbooks run them together.** Only the second is available to a resistively
loaded stage, and only the first survives when the next stage's input resistance dominates the
output node. **Third distinct job for one device:** stopping L07's degeneration boost being swamped,
giving the tail resistance without voltage, and recovering the discarded half.

---

## B.5 The other output, and why the answer changes completely
Everything above takes the output at **one collector**. Take the **difference between the two
collectors** instead and the rejection is set by something else entirely, 46 decibels away.

**Why.** A common-mode input moves both collectors down equally. Single-ended, that motion *is* the
output, so the tail alone decides its size. Differentially it appears on both collectors and
**subtracts out exactly**, provided the halves match, and what survives is the mismatch:

$$CMRR_{diff} = \frac{2R_{tail}}{\delta\, r_e}$$

| Output taken                | Limited by        | With a 10 kilohm tail |
| --------------------------- | ----------------- | --------------------- |
| One collector               | the tail alone    | 52 dB                 |
| Both, 5 per cent mismatch   | tail and matching | 84 dB                 |
| Both, 1 per cent mismatch   | tail and matching | 98 dB                 |
| Both, 0.1 per cent mismatch | tail and matching | 118 dB                |

<!-- value: 98 = decibels(cmrr_differential(2e-3, 10e3, 0.01)) -->

**Forty-six decibels, from 1 per cent resistors and where you put the voltmeter.** Same circuit.

**So "the CMRR of a differential pair" is not a statement about a circuit** unless it says which
output is taken: different limits, different fixes, two orders of magnitude apart at ordinary
tolerances.

**And it explains where integrated amplifiers get their 100 dB:** not exotic tails, but two devices
adjacent on one die matching to a fraction of a per cent, output differentially so that matching
becomes rejection. The same schematic in discrete parts, single-ended, gives 52 dB.

**Why this course still takes the single-ended output:** an operational amplifier's second stage
has one input, and taking the difference with a current mirror is
[B.4](#b4-the-mirror-load-and-its-two-mechanisms).

---

## B.6 Offset, matching, and why modern input stages are MOSFET
With both inputs at zero the output should sit at its quiescent value. It does not, and the
difference referred back to the input is the **input offset voltage**.

| Source                                                            | Size                            | Input-referred offset |
| ----------------------------------------------------------------- | ------------------------------- | --------------------- |
| 1 mV of $V_{BE}$ mismatch                                         | typical of two discrete devices | **1 mV**, directly    |
| 1 per cent of $R_C$ mismatch                                      | ordinary resistors              | 0.52 mV               |
| 20 microamps of base current through a 10 kilohm source imbalance |                                 | **200 mV**            |

<!-- value: 0.52 = diffpair_input_offset(0.01, 0.0, 10e3, 2e-3) * 1e3 -->

**The third row is not a misprint, and it dominates the others by two orders of magnitude.** 20
microamps through 10 kilohm is 200 mV, and it cancels only if the two sources match.

**The classical fix is to make the source resistances equal,** so the base currents produce the
same voltage and it becomes common-mode: hence the resistor textbook op-amp circuits put in the
non-inverting input. It leaves the *difference* between the base currents, and a 1 per cent beta
mismatch is 0.2 microamps, 2 mV through 10 kilohm.

**The modern fix is to have no base current.** A MOSFET gate draws nothing, so the row disappears
rather than being cancelled, and with it the requirement that the sources match.

**The trade, plainly:** a MOSFET input pair has a tenth of the gain at the same current, $r_s$ being
ten times $r_e$
([L07 B.6](../../L07/appendix/b_the_emitter_factor.md#b6-the-mosfet-in-one-substitution)), and none
of the input-current problem. **Almost every modern operational amplifier takes that trade** and
recovers the gain in the second stage. The third option, best of both for two more devices, is
**bipolar inputs with source followers in front of them**.

---

## B.7 What to build
### `ael/diffpair/pair.hpp`
| Function                                                                 | Returns                                                                                          |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `intrinsicEmitterResistance(tailCurrent)`                                | $V_T/(I_{tail}/2)$. **Half** the tail.                                                           |
| `differentialGain(load, tailCurrent, degeneration)`                      | $-R_C/(2(r_e + R_E))$, single-ended.                                                             |
| `commonModeGain(load, tailCurrent, tailResistance, degeneration)`        | $-R_C/(2R_{tail} + r_e + R_E)$.                                                                  |
| `commonModeRejection(load, tailCurrent, tailResistance, degeneration)`   | The ratio, as a plain number.                                                                    |
| `commonModeRejectionDifferential(tailCurrent, tailResistance, mismatch)` | [B.5](#b5-the-other-output-and-why-the-answer-changes-completely)'s figure, for both collectors. |
| `mirrorGain(tailCurrent, load)`                                          | $-R_{load}/r_e$: no factor of two.                                                               |
| `transfer(differentialInput, tailCurrent)`                               | $I_{tail}\tanh(v_d/2V_T)$.                                                                       |
| `linearRange(tolerance)`                                                 | The input at which `transfer` falls `tolerance` below its tangent.                               |
| `inputOffset(loadMismatch, vbeMismatch, load, tailCurrent)`              | Input-referred, from both causes.                                                                |
| `decibels(ratio)`                                                        | $20\log_{10}$, because every figure above is quoted both ways.                                   |

**`commonModeRejection` must be implemented as the ratio of the other two,** not as a separate
formula. The lecture's central claim is that $R_C$ cancels out of that ratio, and a shipped test
asks for the rejection at two very different loads and requires agreement to machine precision.

**`linearRange` must not have the tail current as a parameter.** If your derivation produced one,
it has a factor that should have cancelled.

### What good looks like
About sixty lines, of which `linearRange` is the only one that iterates.

---

## B.8 What this appendix is blind to
* **Temperature.** One temperature, both halves at it. Offset drifts about 3 microvolts per degree
  per millivolt of offset, the specification that matters in a precision amplifier.
* **The mirror's own mismatch,** which appears directly as offset and is why the mirror devices are
  matched as carefully as the input pair.
* **Noise,** the main reason to choose one pair over another in practice.
* **Common-mode input range.** The pair stops working as the inputs approach either rail, and the
  tail source needs a volt or two of its own.
* **Frequency, again.** The mirror adds a pole the resistive load does not.

---
