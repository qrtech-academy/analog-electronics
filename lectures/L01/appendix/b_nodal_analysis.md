# Appendix B - Nodal analysis, and what to build
The method that turns a circuit into a matrix, and the specification of the two components L01
asks you to write. [B.5](#b5-what-to-build) is the specification; everything before it is what you
need in order to write it.

---

## B.1 One unknown per node
Solving by hand means picking loops and current directions until the equations match the unknowns.
The choices are yours rather than the circuit's, so it does not generalise into code.

**Nodal analysis makes them for you:** node voltages are the unknowns, the current law at each
node supplies the equations, and the count comes out right. Ground is not one of them, so a
circuit with $n$ nodes has $n - 1$ unknowns. **Five nodes is four unknowns.**

---

## B.2 The conductance stamp
For a resistor between nodes $a$ and $b$, the current leaving $a$ through it is

$$I_{a \to b} = \frac{V_a - V_b}{R} = G(V_a - V_b), \qquad G = \frac{1}{R}$$

In $\mathbf{G}\mathbf{v} = \mathbf{i}$ one resistor contributes exactly four entries, always these
four:

$$G_{aa} \mathrel{+}= G, \quad G_{bb} \mathrel{+}= G, \quad G_{ab} \mathrel{-}= G, \quad G_{ba} \mathrel{-}= G$$

That pattern is a **stamp**, and it is the whole technique: never derive an equation, walk the
element list, add each stamp, solve. Two consequences, both tested by the shipped suite:
* **The diagonal accumulates.** Two resistors between the same pair of nodes stamp twice, giving
  the parallel combination without anyone computing one. A solver that assigns one matrix row per
  *element* rather than per *node* gets this wrong, and gets it wrong quietly.
* **Ground is skipped.** An entry whose row or column is ground is not written, which is why a
  resistor to ground contributes one entry rather than four.

A current source does not enter $\mathbf{G}$ at all; it adds to the right-hand side at its two
nodes.

---

## B.3 The trouble with a voltage source
A voltage source has no conductance: its current is whatever the circuit demands, so it cannot be
stamped. Add that current as an extra unknown and its constraint as an extra equation:

$$V_p - V_n = V_{source}$$

One extra row and column per source, and the matrix stops being purely a conductance matrix. That
is the whole of the "modified" in **modified nodal analysis**. The extra unknown says how much a
supply delivers, which is how L06 checks a bias point and L10 a power budget.

---

## B.4 Two conventions this course fixes
Pinned by L01's test suite, because every component in the rest of the course reads them.

**A current source injects at its second node.** `addCurrentSource(from, to, current)` takes
current out of `from` and pushes it into `to`. One milliamp into a node with one kilohm to ground
puts that node at $+1$ V.

**A voltage source reports the current leaving its positive terminal.** `sourceCurrents[k]` flows
out of source $k$'s positive terminal into the circuit; a 10 V source driving one kilohm reports
$+10$ mA.

**That is the opposite sign to the raw modified-nodal unknown,** which comes out as the current
flowing from the node into the source. Negating it is your job, and the suite checks that you did.

---

## B.5 What to build
Two headers. The paths are part of the specification: the test suite includes exactly these, and a
component written anywhere else stays dormant however correct it is.

### `ael/net/netlist.hpp`
A container. It holds elements and hands them to the solver, and it does nothing else.

| Member                                                            | Contract                                                            |
| ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| `using Node = std::size_t`                                        | A node index.                                                       |
| `constexpr Node Ground{0}`                                        | Node zero is ground, always.                                        |
| `addResistor(Node a, Node b, double resistance)`                  | Adds a resistor.                                                    |
| `addCurrentSource(Node from, Node to, double current)`            | Injects at `to`. See [B.4](#b4-two-conventions-this-course-fixes).  |
| `addVoltageSource(Node positive, Node negative, double voltage)`  | Fixes the difference.                                               |
| `nodeCount()`                                                     | Highest node index mentioned, plus one. An empty netlist returns 1. |
| `resistorCount()`, `voltageSourceCount()`, `currentSourceCount()` | Element counts, by kind.                                            |

Nodes are mentioned rather than declared: there is no "add a node" call, because that would put a
bookkeeping step in front of every exercise in the course.

The solver needs to read the elements back out. How you expose them is yours to decide; the tests
only require that `solve` can be handed a `const Netlist&`.

### `ael/mna/solver.hpp`
```cpp
namespace ael::mna
{
struct Solution
{
    std::vector<double> nodeVoltages{};    ///< Indexed by Node. [Ground] is always 0.
    std::vector<double> sourceCurrents{};  ///< One per voltage source, in insertion order.
    bool solved{false};                    ///< False if the network has no unique solution.
};

[[nodiscard]] Solution solve(const net::Netlist& netlist) noexcept;
}
```

Assemble from the stamps in [B.2](#b2-the-conductance-stamp) and
[B.3](#b3-the-trouble-with-a-voltage-source), then solve by Gaussian elimination with partial
pivoting.

**`solved` is not decoration.** A floating node, or two voltage sources contradicting each other,
gives a singular matrix. A solver that returns zeros there will be believed, and the reader spends
an hour looking for the fault in their circuit rather than in their assumptions. Detect the
singular pivot and say so. The suite has a test for exactly this.

### What good looks like
Around 120 lines for both, of which the elimination is about 20. If yours is much longer, you are
probably special-casing element kinds somewhere that a stamp would have handled.

---

## B.6 Why write a solver at all
**From L07 this course computes every stage twice:** once from a closed form you can reason about,
once from a solver that knows nothing about amplifiers. Where they agree, the closed form is
trustworthy and simpler. Where they disagree, one is dropping a term, and finding out which is the
exercise. That only works if the solver is yours; a number from a tool you did not write is an
authority claim.

---

## B.7 What this appendix is blind to
* **Conditioning.** A direct solve handles the three or four orders of magnitude here without
  complaint. L04 brings a diode and twelve orders, at which point pivoting stops being a formality.
* **Sparsity.** Real simulators store the matrix sparsely and order it to limit fill-in. Nothing
  in this course is large enough for that to matter.
* **Anything time-varying.** This is a DC solve; L02 makes it complex, which covers one frequency
  in steady state. There is no transient analysis, so an underdamped filter's ringing is something
  L03 computes rather than watches.

---
