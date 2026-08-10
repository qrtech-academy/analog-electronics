# Appendix B - The complex stamps, and what to build

The frequency domain costs about thirty lines, and only because the L01 solver was written in a
way that lets it. [B.4](#b4-what-to-build) is the specification.

---

## B.1 Nothing about the method changes

The whole of [L01 Appendix B](../../L01/appendix/b_nodal_analysis.md) survives intact. One unknown
per node, one current-law equation per node, one stamp per element, Gaussian elimination.

What changes is the number field. The unknowns are complex, the conductances are complex, and the
arithmetic is complex. Kirchhoff's current law does not care: it says the currents at a node sum
to zero, and that is as true of phasors as of real currents, because the common $e^{j\omega t}$
divides out of every term.

So the correct way to write L02 is to not write it. Template the L01 solver on its scalar type and
instantiate it twice.

```cpp
template <typename T>
[[nodiscard]] std::vector<T> solveLinearSystem(std::vector<std::vector<T>> matrix);
```

If your L01 elimination was written against `double` in a way that makes this hard, the usual
culprit is the pivot search, which needs `std::abs` rather than `std::fabs` and needs to compare
magnitudes rather than values. `std::abs` of a `std::complex` is its magnitude and is already what
you want.

---

## B.2 The two new stamps

A capacitor between nodes $a$ and $b$ at angular frequency $\omega$ has admittance $j\omega C$,
and stamps exactly like a resistor of that conductance:

$$Y_{aa} \mathrel{+}= j\omega C, \quad Y_{bb} \mathrel{+}= j\omega C, \quad Y_{ab} \mathrel{-}= j\omega C, \quad Y_{ba} \mathrel{-}= j\omega C$$

An inductor has admittance $1/(j\omega L)$ and stamps the same way.

That is the entire electrical content of this lecture. Two lines of code each, and they are the
same two lines as the resistor with a different scalar.

**One trap.** At zero frequency an inductor's admittance is infinite and a capacitor's is zero. A
sweep that includes DC therefore divides by zero in the inductor stamp and produces a singular
matrix in any circuit whose only path to ground is through a capacitor. This course's sweeps start
above zero and the specification below says so; a real simulator does the DC operating point
separately, for exactly this reason.

---

## B.3 What a sweep is for

A single frequency answers one question. A sweep answers the question people actually have, which
is what shape the response is, and it is the input to every Bode plot in the rest of the course.

Sweeps are logarithmic, because responses are. A linear sweep from 10 Hz to 100 kHz spends 99 per
cent of its points above 1 kHz and shows a first-order corner as a single kink at the left-hand
edge.

---

## B.4 What to build

### Additions to `ael/net/netlist.hpp`

| Member                                             | Contract                                  |
| -------------------------------------------------- | ----------------------------------------- |
| `addCapacitor(Node a, Node b, double capacitance)` | Adds a capacitor, in farads.              |
| `addInductor(Node a, Node b, double inductance)`   | Adds an inductor, in henries.             |
| `capacitorCount()`, `inductorCount()`              | Element counts, matching the L01 pattern. |

The L01 members and both L01 sign conventions are unchanged, and L01's suite still has to pass.
That is not a courtesy; L10 links every suite in the course at once, so a change here that broke
L01 would be found eventually and painfully.

### `ael/ac/sweep.hpp`

```cpp
namespace ael::ac
{
struct Point
{
    double frequency{0.0};                              ///< Hertz.
    std::vector<std::complex<double>> nodeVoltages{};   ///< Indexed by Node. [Ground] is 0.
    bool solved{false};
};

/// Solve at one frequency. Voltage sources are phasors of their own value at zero phase.
[[nodiscard]] Point solveAt(const net::Netlist& netlist, double frequency);

/// Logarithmically spaced points from `first` to `last` inclusive. Both must be positive.
[[nodiscard]] std::vector<Point> sweep(const net::Netlist& netlist, double first, double last,
                                       std::size_t points);
}
```

Three details the suite checks, and each one has a reason:

* **A voltage source is a phasor of its own value at zero phase.** There is no separate AC
  amplitude. It keeps the netlist to one concept, and it means a divider built for L01 can be
  swept without being rebuilt.
* **`sweep` is logarithmic and inclusive at both ends.** With `points` equal to 1 it returns one
  point at `first`. With `first` equal to `last` it returns `points` identical points rather than
  dividing by zero.
* **`sweep` throws or returns empty for a non-positive frequency**, rather than producing infinity
  in the inductor stamp. Which of the two you choose is yours; the suite accepts an empty result.

### What good looks like

Around forty new lines, of which about ten are the two stamps and about twenty are the sweep's
frequency generation. If `solveAt` duplicates the elimination from L01, stop and template that
instead; the duplication is the thing this lecture is actually teaching against.

---

## B.5 Reading a complex answer

`nodeVoltages[n]` is a phasor. Two lines turn it into what a plot wants:

```cpp
const double magnitudeDb{20.0 * std::log10(std::abs(v))};
const double phaseDegrees{std::arg(v) * 180.0 / M_PI};
```

**The phase sign is the single most common defect** in a first AC solver, and it is invisible in a
magnitude plot. A low-pass filter must produce a *negative* phase: the output lags. If yours comes
out positive at every frequency, the likely cause is a capacitor stamped as $1/(j\omega C)$ where
the admittance is wanted, which is the impedance rather than the admittance and therefore the
reciprocal of the right answer.

The suite tests the phase at the corner for exactly this reason.

---

## B.6 What this appendix is blind to

* **DC.** The sweep starts above zero and the stamps break at zero. L01's solver is still the one
  that answers a DC question, and from L05 onwards the two are used together: the DC solve finds
  an operating point, and the AC solve describes small movements around it.
* **Nonlinearity.** Everything here assumes superposition, which a diode or a transistor breaks.
  L04 is where that is confronted.
* **Noise, and anything statistical.** A phasor describes a deterministic sinusoid. The thermal
  noise that decides how small a signal an amplifier can usefully handle is not in this course at
  all.

---
