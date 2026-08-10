# Appendix B - The operational amplifier, and what to build

Two rules, five circuits, and one circuit where the rules do not apply at all.

The op-amp is a black box in this lecture and stays one until L10, where it is built out of the
transistors of L05 to L09. That inversion is deliberate: you use it on trust for seven lectures,
and then you find out what you were trusting.

---

## B.1 What is inside, stated once

An operational amplifier is a differential amplifier with enormous gain. It has two inputs and one
output, and

$$V_{out} = A_{OL}\,(V_+ - V_-)$$

where $A_{OL}$, the open-loop gain, is typically $10^5$ to $10^6$ at DC. That is the entire model
for this lecture.

With a gain that large the amplifier is useless on its own: 100 microvolts of input difference
saturates it. It becomes useful only when feedback is wrapped around it, and everything below is a
consequence of the feedback rather than of the amplifier.

---

## B.2 The two rules

**With negative feedback around it, and enough gain:**

1. **No current flows into either input.**
2. **No voltage appears between the inputs.**

Rule 1 is a statement about the amplifier: its input impedance is large. Rule 2 is a statement
about the feedback: the output moves to whatever it must in order to make the difference zero, and
with $A_{OL}$ of $10^5$ the difference that remains is the output divided by $10^5$, which is
microvolts.

Rule 2 is often called the **virtual short**, and the name is a good one as long as it is
remembered that no current flows through it. The two inputs are at the same voltage and are not
connected.

**What each rule assumes, and where it fails.** Rule 1 fails for an amplifier with bipolar inputs
driven from a very high impedance, because the input bias current then develops a real voltage;
L09 is where that current comes from. Rule 2 fails in three places, and all three matter later:
when there is no feedback at all ([B.4](#b4-the-comparator-where-the-rules-do-not-apply)), when
the feedback is positive rather than negative, and when the frequency is high enough that
$A_{OL}$ is no longer large, which is L04.

---

## B.3 The configurations, all from the two rules

Each of these is one line of algebra once the rules are applied, and the line is always the same:
apply rule 2 to find the voltage at the inverting input, then apply rule 1 to say that whatever
current arrives there must leave through the feedback resistor.

**Non-inverting.** Feedback divider from the output back to the inverting input, signal into the
non-inverting input.

$$A = 1 + \frac{R_f}{R_g}$$

The gain cannot be less than one. The input impedance is the amplifier's own, which is enormous.

**Voltage follower.** The non-inverting configuration with $R_f = 0$ and $R_g$ absent, giving a
gain of exactly one. Useless as an amplifier and invaluable as a buffer, which is what
[A.3](./a_filters.md#a3-cascading-and-the-corner-you-did-not-design) needed.

**Inverting.** Signal in through $R_{in}$ to the inverting input, feedback through $R_f$, the
non-inverting input grounded.

$$A = -\frac{R_f}{R_{in}}$$

The gain can be less than one. The input impedance is exactly $R_{in}$, because rule 2 holds the
inverting input at ground, and that is usually the reason to prefer the non-inverting version.

**Summing.** Several inputs, each through its own resistor, into the inverting input.

$$V_{out} = -R_f \left( \frac{V_1}{R_1} + \frac{V_2}{R_2} + \dots \right)$$

The inputs do not interact, because rule 2 holds their common node at ground whatever any of them
does. That independence is why a summing amplifier is the natural way to build a resistor-ladder
digital-to-analogue converter.

**Difference.** Two inputs, two matched pairs of resistors.

$$V_{out} = \frac{R_f}{R_{in}} (V_2 - V_1)$$

and it only rejects what is common to both inputs to the extent that the two resistor ratios
match. A 1 per cent mismatch limits the rejection to about 46 dB, which is usually the reason a
difference amplifier disappoints. L09 meets the same limit again, set by transistor matching
rather than resistor matching.

---

## B.4 The comparator, where the rules do not apply

Take the feedback away and rule 2 goes with it. The amplifier then does what its gain says: any
positive difference drives the output to the positive rail, any negative difference to the
negative rail. That is a **comparator**, and it is a one-bit analogue-to-digital converter.

The problem is that real inputs have noise on them. An input crossing the threshold slowly, with a
millivolt of noise, crosses it many times, and the output produces a burst of transitions where
one was wanted.

The fix is **positive** feedback, taking a fraction of the output back to the non-inverting input:

$$V_{th\pm} = \pm V_{supply} \frac{R_{lower}}{R_{upper} + R_{lower}}$$

Now the threshold moves away from the input as soon as the output switches, so the input has to
travel back across a gap before it can switch again. That gap is the **hysteresis**, and the
circuit is a **Schmitt trigger**.

With 12 V rails and a 100 kilohm over 10 kilohm divider the thresholds are at $\pm 1.09$ V, a gap
of 2.18 V.

<!-- value: 1.09 = schmitt_thresholds(12.0, 100e3, 10e3)[1] -->

**What hysteresis costs.** The circuit no longer tells you when the input crossed zero; it tells
you when the input crossed one of two levels that depend on where it has been. For a clean
threshold that is a real loss of accuracy, and the design question is always to make the gap
larger than the noise and no larger.

---

## B.5 What to build

Three pieces. The first is a netlist element, and the other two are closed forms.

### An addition to `ael/net/netlist.hpp`

```cpp
/// A voltage-controlled voltage source: V(outPositive) - V(outNegative)
///                                    = gain * (V(inPositive) - V(inNegative)).
void addVcvs(Node outPositive, Node outNegative, Node inPositive, Node inNegative, double gain);
[[nodiscard]] std::size_t vcvsCount() const noexcept;
```

This is the op-amp, as far as a solver is concerned: an amplifier with a finite gain, an infinite
input impedance and a zero output impedance. Give it a gain of $10^5$ and it behaves like the two
rules; give it a gain of 100 and you can watch the rules fail, which is what
L04 does.

**The stamp is L01's voltage source with two more entries.** It needs an extra unknown, its
current, exactly as a voltage source does. The difference is only in the constraint row: instead
of $V_p - V_n = V$, the row says

$$V_{op} - V_{on} - A(V_{ip} - V_{in}) = 0$$

so the row has up to four entries and the right-hand side is zero. The two output-node entries in
the matrix body are the same $\pm 1$ as a voltage source's. If you wrote L01's voltage-source
stamp as a small function, this is about six lines.

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

`cascadedCorner` is the interesting one, and it is deliberately not given a closed form here. Find
the two poles from [A.3](./a_filters.md#a3-cascading-and-the-corner-you-did-not-design), then
locate the half-power point of their product numerically, by bisection on a logarithmic axis.
Twenty iterations is plenty and the function is ten lines.

### `ael/opamp/ideal.hpp`

| Function                                  | Returns                                    |
| ----------------------------------------- | ------------------------------------------ |
| `nonInvertingGain(feedback, ground)`      | $1 + R_f/R_g$.                             |
| `invertingGain(feedback, input)`          | $-R_f/R_{in}$, negative.                   |
| `differenceGain(feedback, input)`         | $R_f/R_{in}$.                              |
| `schmittThresholds(supply, upper, lower)` | The lower and upper thresholds, as a pair. |

These are three lines each and they are worth having anyway, because from here on they are what
the solver gets checked against.

---

## B.6 What this appendix is blind to

* **Everything real about an op-amp.** Offset voltage, input bias current, finite bandwidth, slew
  rate, output current limit, supply rejection and noise are all absent. L04 adds the finite gain
  and the bandwidth; the rest this course never covers.
* **Stability.** Wrapping feedback around an amplifier can make an oscillator. The condition is in
  L04 and the treatment is brief.
* **Single-supply operation.** Everything here assumes symmetric rails and signals around ground.
  Real designs often have neither, and the arithmetic changes more than people expect.

---
