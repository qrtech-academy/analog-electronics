# Appendix B - Nodal analysis, and what to build

The method that turns a circuit into a matrix, and the specification of the two components L01
asks you to write. [B.5](#b5-what-to-build) is the specification; everything before it is what you
need in order to write it.

---

## B.1 One unknown per node

Solving a circuit by hand means picking loops, choosing current directions, and writing equations
until there are as many as there are unknowns. It works, it is error-prone, and it does not
generalise into code, because the choices are yours rather than the circuit's.

Nodal analysis makes the choice for you. Take the node voltages as the unknowns, write the current
law at each node, and you have exactly as many equations as unknowns with nothing left to decide.

Ground is not an unknown, because its voltage is zero by definition. A circuit with $n$ nodes
therefore has $n - 1$ unknown voltages, and that is the first thing a reader gets wrong: five
nodes is four unknowns.

---

## B.2 The conductance stamp

At a node, the current law says the currents leaving through every attached element sum to the
current arriving from sources. For a resistor between nodes $a$ and $b$, the current leaving $a$
through it is

$$I_{a \to b} = \frac{V_a - V_b}{R} = G(V_a - V_b), \qquad G = \frac{1}{R}$$

Written into a matrix $\mathbf{G}\mathbf{v} = \mathbf{i}$, one resistor contributes exactly four
entries, and they are always the same four:

$$G_{aa} \mathrel{+}= G, \quad G_{bb} \mathrel{+}= G, \quad G_{ab} \mathrel{-}= G, \quad G_{ba} \mathrel{-}= G$$

That pattern is called a **stamp**, and it is the whole technique. You never derive an equation.
You walk the element list, add each element's stamp into the matrix, and solve.

Two things follow immediately, and both are tested by the shipped suite:

* **The diagonal accumulates.** Two resistors between the same pair of nodes stamp twice, and the
  result is the parallel combination without anyone computing a parallel combination. A solver
  that assigns one matrix row per *element* rather than per *node* gets this wrong, and gets it
  wrong quietly.
* **Ground is skipped.** A stamp entry whose row or column is ground is simply not written,
  because ground is not an unknown. That is why a resistor to ground contributes one entry rather
  than four.

A current source is easier still. It does not appear in $\mathbf{G}$ at all; it adds to the
right-hand side at the two nodes it touches.

---

## B.3 The trouble with a voltage source

A voltage source has no conductance. Its current is whatever the rest of the circuit demands, and
that means it cannot be stamped into $\mathbf{G}$ at all.

The fix is to stop pretending the unknowns are only voltages. Add the source's current as an extra
unknown, and add the constraint it satisfies as an extra equation:

$$V_p - V_n = V_{source}$$

The matrix grows by one row and one column per voltage source, and it is no longer purely a
conductance matrix. That is what the "modified" in **modified nodal analysis** refers to, and it
is the only modification there is.

The extra unknown is a current, and it is worth having for its own sake: it is what tells you how
much a supply is delivering, which is how L06 checks a bias point and how L10 checks a power
budget.

---

## B.4 Two conventions this course fixes

Sign conventions are arbitrary until they are not. These two are pinned by L01's test suite
because every component in the rest of the course reads them.

**A current source injects at its second node.** `addCurrentSource(from, to, current)` drives
current through itself from `from` to `to`, so it takes current out of `from` and pushes it into
`to`. One milliamp into a node with one kilohm to ground puts that node at $+1$ V.

**A voltage source reports the current leaving its positive terminal.** `sourceCurrents[k]` is the
current flowing out of source $k$'s positive terminal into the circuit. A 10 V source driving one
kilohm reports $+10$ mA.

That second one is the opposite sign to the raw modified-nodal unknown, which comes out as the
current flowing from the node *into* the source. Negating it is your job rather than the caller's,
and the suite checks that you did.

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

Nodes are mentioned rather than declared. There is no "add a node" call, because requiring one
would put a bookkeeping step in front of every exercise in the course.

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

[[nodiscard]] Solution solve(const net::Netlist& netlist);
}
```

Assemble the matrix from the stamps in [B.2](#b2-the-conductance-stamp) and
[B.3](#b3-the-trouble-with-a-voltage-source), solve it by Gaussian elimination with partial
pivoting, and fill in the result.

**`solved` is not decoration.** A network with a floating node, or one with two voltage sources
contradicting each other, has a singular matrix. A solver that returns zeros in that case will be
believed, and the reader will spend an hour looking for the fault in their circuit rather than in
their assumptions. Detect the singular pivot and say so. The suite has a test for exactly this.

### What good looks like

Around 120 lines for both, of which the elimination is about 20. If yours is much longer, you are
probably special-casing element kinds somewhere that a stamp would have handled.

---

## B.6 Why write a solver at all

It is a fair question in a course about amplifiers, and the answer is not that circuit simulation
is interesting.

It is that from L07 onwards this course computes every stage twice: once
from a closed form you can reason about, and once from a solver that knows nothing about
amplifiers. Where the two agree, the closed form is trustworthy and simpler. Where they disagree,
one of them is dropping a term, and finding out which is the exercise.

That only works if the solver is yours. A number from a tool you did not write is an authority
claim, and this course has none of those in it.

---

## B.7 What this appendix is blind to

* **Conditioning.** The networks here span three or four orders of magnitude in conductance and a
  direct solve handles them without complaint. In L04 a diode arrives and the spread becomes
  twelve orders of magnitude, at which point the pivoting stops being a formality.
* **Sparsity.** Every real simulator stores the matrix sparsely and orders it to limit fill-in.
  Nothing in this course is large enough for that to matter.
* **Anything time-varying.** This is a DC solve. L02 makes it complex, which covers the steady
  state at one frequency, and that is as far as the course goes: there is no transient analysis in
  it, so the ringing of an underdamped filter is something L03 computes rather than watches.

---
