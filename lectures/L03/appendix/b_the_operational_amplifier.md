# Appendix B - The operational amplifier, and what to build
Two rules, five circuits, and one circuit where the rules do not apply. The op-amp is a black box
until L10, where it is built out of the transistors of L05 to L09: you use it on trust for seven
lectures, then find out what you were trusting.

---

## B.1 What is inside, stated once
A differential amplifier with enormous gain, two inputs and one output:

$$V_{out} = A_{OL}\,(V_+ - V_-)$$

$A_{OL}$ is $10^5$ to $10^6$ at DC, and that is the entire model here. **A gain that large makes
the amplifier useless alone:** 100 microvolts of input difference saturates it. Everything below is
a consequence of the feedback, not of the amplifier.

---

## B.2 The two rules
**With negative feedback around it, and enough gain:**

1. **No current flows into either input.**
2. **No voltage appears between the inputs.**

Rule 1 is about the amplifier: its input impedance is large. Rule 2 is about the feedback: the
output moves to whatever makes the difference zero, leaving the output divided by $A_{OL}$. Rule 2
is the **virtual short**, and no current flows through it.

**Where they fail.** Rule 1 fails with bipolar inputs driven from a very high impedance, where the
input bias current develops a real voltage; L09 is where that current comes from. Rule 2 fails with
no feedback ([B.4](#b4-the-comparator-where-the-rules-do-not-apply)), with positive feedback, and
where $A_{OL}$ is no longer large, which is L04.

---

## B.3 The configurations, all from the two rules
Each is one line of algebra: rule 2 gives the voltage at the inverting input, rule 1 says whatever
current arrives there leaves through the feedback resistor.

**Non-inverting.** Feedback divider from output to inverting input, signal into the non-inverting
input. Gain cannot be less than one; the input impedance is the amplifier's own.

$$A = 1 + \frac{R_f}{R_g}$$

**Voltage follower.** Non-inverting with $R_f = 0$ and no $R_g$: gain exactly one, useless as an
amplifier and invaluable as the buffer
[A.3](./a_filters.md#a3-cascading-and-the-corner-you-did-not-design) needed.

**Inverting.** Signal through $R_{in}$, feedback through $R_f$, non-inverting input grounded. Gain
can be less than one.

$$A = -\frac{R_f}{R_{in}}$$

**Its input impedance is exactly $R_{in}$,** because rule 2 pins that input at ground, which is
usually the reason to prefer the non-inverting version.

**Summing.** Several inputs, each through its own resistor, into the inverting input.

$$V_{out} = -R_f \left( \frac{V_1}{R_1} + \frac{V_2}{R_2} + \dots \right)$$

They do not interact, because rule 2 holds their common node at ground: the natural
resistor-ladder digital-to-analogue converter.

**Difference.** Two inputs, two matched pairs of resistors.

$$V_{out} = \frac{R_f}{R_{in}} (V_2 - V_1)$$

**It rejects what is common to both inputs only as well as the two resistor ratios match.** A 1 per
cent mismatch limits rejection to about 46 dB. L09 meets the same limit from transistor matching.

---

## B.4 The comparator, where the rules do not apply
Take the feedback away and rule 2 goes with it: any positive difference drives the output to the
positive rail, any negative one to the negative rail. That is a **comparator**, a one-bit
analogue-to-digital converter. **Real inputs have noise,** so an input crossing the threshold
slowly with a millivolt of noise crosses it many times, and one wanted transition becomes a burst.

The fix is **positive** feedback, a fraction of the output back to the non-inverting input:

$$V_{th\pm} = \pm V_{supply} \frac{R_{lower}}{R_{upper} + R_{lower}}$$

The threshold now moves away from the input as soon as the output switches, so the input must
travel back across a gap to switch again. That gap is the **hysteresis** and the circuit is a
**Schmitt trigger**. With 12 V rails and 100 kilohm over 10 kilohm, thresholds of $\pm 1.09$ V.

<!-- value: 1.09 = schmitt_thresholds(12.0, 100e3, 10e3)[1] -->

**What hysteresis costs.** The circuit no longer says when the input crossed zero, but when it
crossed one of two levels that depend on where it has been. Make the gap just larger than the noise.

---

## B.5 What to build
Three pieces. The first is a netlist element, the other two are closed forms.

### An addition to `ael/net/netlist.hpp`
```cpp
/// A voltage-controlled voltage source: V(outPositive) - V(outNegative)
///                                    = gain * (V(inPositive) - V(inNegative)).
void addVcvs(Node outPositive, Node outNegative, Node inPositive, Node inNegative, double gain) noexcept;
[[nodiscard]] std::size_t vcvsCount() const noexcept;
```

The op-amp as far as a solver is concerned: finite gain, infinite input impedance, zero output
impedance. A gain of $10^5$ obeys the two rules; a gain of 100 lets them fail, as L04 does.

**The stamp is L01's voltage source with two more entries,** and the same extra unknown. Only the
constraint row differs: instead of $V_p - V_n = V$ it says

$$V_{op} - V_{on} - A(V_{ip} - V_{in}) = 0$$

so it has up to four entries and a right-hand side of zero, the two output-node entries being the
same $\pm 1$ as a voltage source's. About six lines, if L01's stamp was a small function.

### `ael/filter/response.hpp`
| Function                            | Returns                                                     |
| ----------------------------------- | ----------------------------------------------------------- |
| `rcCorner(r, c)`                    | The corner frequency of an RC section.                      |
| `lowpass(frequency, corner)`        | The complex first-order low-pass response.                  |
| `highpass(frequency, corner)`       | The complex first-order high-pass response.                 |
| `lcResonance(l, c)`                 | The resonant frequency.                                     |
| `seriesQ(r, l, c)`                  | Q of a series RLC taken across the resistor.                |
| `bandpass(frequency, resonance, q)` | The second-order band-pass response, unity at resonance.    |
| `cascadedCorner(r, c)`              | The 3 dB point of two identical sections cascaded directly. |

`cascadedCorner` is deliberately given no closed form here. Take the two poles from
[A.3](./a_filters.md#a3-cascading-and-the-corner-you-did-not-design), then locate the half-power
point of their product by bisection on a logarithmic axis. Twenty iterations is plenty; ten lines.

### `ael/opamp/ideal.hpp`
| Function                                  | Returns                                    |
| ----------------------------------------- | ------------------------------------------ |
| `nonInvertingGain(feedback, ground)`      | $1 + R_f/R_g$.                             |
| `invertingGain(feedback, input)`          | $-R_f/R_{in}$, negative.                   |
| `differenceGain(feedback, input)`         | $R_f/R_{in}$.                              |
| `schmittThresholds(supply, upper, lower)` | The lower and upper thresholds, as a pair. |

Three lines each, and worth having anyway: from here on they are what the solver gets checked
against.

---

## B.6 What this appendix is blind to
* **Everything real about an op-amp.** Offset voltage, input bias current, finite bandwidth, slew
  rate, output current limit, supply rejection and noise. L04 adds the gain and the bandwidth only.
* **Stability.** Wrapping feedback around an amplifier can make an oscillator. The condition is in
  L04 and the treatment is brief.
* **Single-supply operation.** Everything here assumes symmetric rails and signals around ground.
  Real designs often have neither.

---
