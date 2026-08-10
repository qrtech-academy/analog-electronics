# Appendix D - Solutions

In full, including the plausible wrong answers. This is a self-study course and a reader with
nobody to ask cannot be left with an unanswered exercise.

---

## D.1 Recall: the convention

`addCurrentSource(from, to, current)` drives current through itself from `from` to `to`, so it
injects at `to`. `sourceCurrents[k]` is the current leaving voltage source $k$'s positive terminal
into the circuit.

**Every voltage negated is the voltage source, not the current source.** The reasoning is that the
divider has no current source in it. Its only source is the voltage source, so the only convention
it can be sensitive to is that one, and inverting it stamps the constraint as
$V_n - V_p = V_{source}$ rather than $V_p - V_n = V_{source}$.

There is a second, better test that does not require knowing the circuit: **a current-source
error negates some voltages and a voltage-source error negates all of them.** A network driven by
two sources of different kinds, with one convention inverted, comes out with the two contributions
subtracting rather than adding, which does not look like a global sign flip at all.

---

## D.2 Recall: two dividers

1. Two 1 megohm resistors give a Thevenin resistance of **500 kilohm**; two 10 ohm resistors give
   **5 ohm**. The parallel combination of two equal resistors is half of one of them.
2. **The megohm divider is the oscilloscope probe.** A probe must not load the circuit it
   measures, and its own accuracy is a ratio rather than an absolute value, so a high Thevenin
   resistance costs it nothing. The 10 ohm divider is inside the power supply, where the output
   has to hold its voltage against a load drawing real current, and 5 ohm of source resistance is
   what makes that possible.
3. Ten volts across 20 ohm total is 500 mA, so the divider dissipates **5 W**, split evenly as
   2.5 W in each resistor. That is a problem: it needs two wirewound parts and a heatsink to do
   the job of a component that should not have been there. A divider is a poor way to make a
   supply rail, and this is why.

---

## D.3 Hand calculation: the divider, three ways

**1. Unloaded.**

$$V_{out} = 10 \times \frac{6800}{33000 + 6800} = 1.71\ \text{V}$$

<!-- value: 1.71 = divider(10.0, 33e3, 6.8e3) -->

**2. Thevenin resistance.**

$$R_{th} = \frac{33000 \times 6800}{33000 + 6800} = 5.64\ \text{k}\Omega$$

<!-- value: 5.64 = divider_output_resistance(33e3, 6.8e3) / 1e3 -->

**3. Loaded with 10 kilohm, both ways.**

By substitution, the lower leg becomes $6800 \parallel 10000 = 4048\ \Omega$, so

$$V_{out} = 10 \times \frac{4048}{33000 + 4048} = 1.09\ \text{V}$$

<!-- value: 1.09 = divider(10.0, 33e3, 6.8e3, 10e3) -->

From the Thevenin equivalent, a 1.709 V source behind 5638 ohm driving 10 kilohm:

$$V_{out} = 1.709 \times \frac{10000}{5638 + 10000} = 1.09\ \text{V}$$

They agree because Thevenin's theorem says they must: the equivalent is *defined* as the network
that behaves identically at those two terminals, so any load gives the same answer through either
route. If they had disagreed, the Thevenin resistance would have been computed with the source
left alive.

**4. The load that halves the output** is a load equal to the Thevenin resistance, **5.64 kilohm**,
because the load and $R_{th}$ then form an equal divider. Note that this is smaller than the lower
leg, which is the point of the exercise: it is not obvious by eye.

---

## D.4 Hand calculation: node equations

**1. The two equations.** Currents leaving each node sum to the current injected:

$$\frac{V_1}{1000} + \frac{V_1 - V_2}{2200} = 1\ \text{mA}$$

$$\frac{V_2 - V_1}{2200} + \frac{V_2}{4700} = 0$$

**2. As a matrix.** With $G_1 = 1/1000$, $G_2 = 1/2200$ and $G_3 = 1/4700$:

$$\begin{bmatrix} G_1 + G_2 & -G_2 \\ -G_2 & G_2 + G_3 \end{bmatrix}
\begin{bmatrix} V_1 \\ V_2 \end{bmatrix} =
\begin{bmatrix} 1\ \text{mA} \\ 0 \end{bmatrix}$$

The four entries, by origin:

| Entry               | Contributions                                                        |
| ------------------- | -------------------------------------------------------------------- |
| $(1,1)$             | $G_1$ from the 1 kilohm to ground, plus $G_2$ from the 2.2 kilohm.   |
| $(2,2)$             | $G_3$ from the 4.7 kilohm to ground, plus $G_2$ from the 2.2 kilohm. |
| $(1,2)$ and $(2,1)$ | $-G_2$ each, both from the 2.2 kilohm bridging the two nodes.        |

The 1 kilohm and the 4.7 kilohm each contribute one entry rather than four, because their other
end is ground and ground is not an unknown.

**3. Solving** gives

$$V_1 = 0.873\ \text{V}, \qquad V_2 = 0.595\ \text{V}$$

**4. The resistance at node 2.** Killing the current source opens it, leaving the 2.2 kilohm in
series with the 1 kilohm, that pair in parallel with the 4.7 kilohm:

$$R = (2200 + 1000) \parallel 4700 = 1904\ \Omega$$

The ratio of node 2's voltage to the source current is $0.595 / 1\ \text{mA} = 595\ \Omega$, and
**that is not the same number.** If you expected it to be, the exercise has done its job.

The two agree only when the test current is injected *at the node being measured*. Here the source
injects at node 1 and the voltage is read at node 2, so the ratio is a transfer resistance rather
than an input resistance. Injecting 1 mA at node 2 instead gives 1.904 V there, and that ratio is
the 1904 ohm.

---

## D.5 Design: a reference divider

**The answer: 8.2 kilohm over 2.7 kilohm.**

| Quantity            | Value                                 |
| ------------------- | ------------------------------------- |
| Output              | 2.477 V, which is 0.92 per cent low   |
| Thevenin resistance | 2031 ohm, inside the 2.2 kilohm limit |
| Divider current     | 0.917 mA, inside the 1 mA limit       |

The reasoning. A 2.5 V output from 10 V needs a ratio of one to four, so the upper leg is three
times the lower. That fixes the ratio and leaves the magnitude free, and the two constraints pull
the magnitude in opposite directions: the Thevenin resistance wants the resistors small, and the
current budget wants them large. With $R_{upper} = 3R_{lower}$,

$$R_{th} = \frac{3R_{lower}^2}{4R_{lower}} = 0.75\,R_{lower} \le 2200 \implies R_{lower} \le 2933$$

$$I = \frac{10}{4R_{lower}} \le 1\ \text{mA} \implies R_{lower} \ge 2500$$

So the lower leg lies between 2500 and 2933 ohm, and the only E12 value in that window is 2.7
kilohm. The upper leg wants to be 8.1 kilohm, and the nearest E12 value is 8.2 kilohm.

**The plausible wrong answer is 10 kilohm over 3.3 kilohm.** Its ratio is better: it gives
2.481 V, an error of 0.75 per cent rather than 0.92. It is also the pair most people find first,
because 3.3 and 10 are a familiar-looking ratio. Its Thevenin resistance is **2481 ohm**, which
violates the limit by 13 per cent.

That is the lesson of the exercise. **The ratio sets the voltage and the magnitude sets the
Thevenin resistance, and they are independent.** Every pair on the one-to-four ratio line gives
2.48 V; 1 kilohm over 330 ohm gives the same voltage with a Thevenin resistance of 248 ohm and a
current of 7.5 mA. Choosing along that line is the design, and the voltage is the part that is
already decided.

Whether 0.92 per cent is acceptable depends on what the 2.5 V is for. As a comparator threshold,
comfortably. As a voltage reference for a converter, not remotely: E12 resistors are 5 per cent
parts, so the tolerance alone swamps it, and this whole approach is the wrong one.

---

## D.6 Code: the netlist

No solution is published for the code exercises, because the test suite is the solution: it tells
you whether you are right, which is what a solution would do, and it tells you nothing about how,
which is what a published implementation would spoil.

Two hints for the four tests, both of which catch people:

* **An empty netlist has one node, not zero.** Ground always exists.
* **`nodeCount()` is the highest index mentioned plus one,** not the number of distinct indices. A
  netlist whose only element runs between node 4 and ground has five nodes, three of which are
  isolated. That is deliberate: it keeps node numbering a property of the circuit rather than of
  the order you entered it.

---

## D.7 Code: the solver

Again no implementation, and three hints:

* **Stamp, do not derive.** If your code has a branch on how many elements touch a node, it is
  deriving. The stamp is unconditional.
* **The extra row per voltage source is symmetric.** The two entries you write into the matrix
  body, at $(p, k)$ and $(k, p)$, are both $+1$, and the two at $(n, k)$ and $(k, n)$ are both
  $-1$. If you write only one of each pair the matrix stops being symmetric and the answer is
  quietly wrong rather than singular.
* **Negate the source current on the way out.** The modified-nodal unknown is the current flowing
  from the positive node *into* the source; the contract reports the current leaving the positive
  terminal *into the circuit*. `Mna.VoltageSourceAndItsCurrent` is the test that catches it, and
  it is the single most commonly failed test in this lecture.

---

## D.8 Cross-check: the loaded divider

**All three legs give 1.0925 V.**

| Leg            | Value                                         |
| -------------- | --------------------------------------------- |
| By hand        | 1.09 V to three significant figures           |
| By closed form | 1.09254498714653 V                            |
| By solver      | The same, to about twelve significant figures |

<!-- value: 1.0925 = divider(10.0, 33e3, 6.8e3, 10e3) -->

The reconciliation:

**Legs 1 and 2 differ only by how many digits you wrote down.** They evaluate the same expression.
If they disagree at three significant figures, leg 1 has an arithmetic slip; the most common one
is computing $6800 \parallel 10000$ as $6800 \times 10000 / 10000$ by dropping a term in the
denominator, which gives 6800 and an answer of 1.71 V, the unloaded value.

**Legs 2 and 3 differ by rounding, and by nothing else.** The solver performs one elimination on a
three-by-three system in double precision, and the relative difference should be around
$10^{-13}$. It cannot be systematically different, because both are exact solutions of the same
linear system and that system has one solution.

**What a real disagreement would have meant.** Each of these has been seen:

* **Getting 1.71 V from the solver** means the load resistor is not in the circuit. Either
  `addResistor` was called with the same node twice, which stamps a resistor from a node to
  itself and contributes nothing, or the load was stamped between node 1 and node 1.
* **Getting 0.836 V** means the load was stamped across the *upper* leg rather than the lower one.
  It is a plausible-looking number, which is what makes it dangerous.
* **Getting 8.29 V** means the supply and output nodes were swapped, so you built the reciprocal
  divider.
* **Getting zeros with `solved` true** means the singular-matrix check is missing and the
  elimination divided by something near zero. This is the failure the shipped suite exists to
  prevent, and it is the one that costs the most time in the wild, because a zero looks like an
  answer.

**Why this one agrees, and why that is worth doing once.** Every leg here solves the same linear
problem, so agreement is guaranteed and the exercise is really about learning what agreement looks
like numerically. Keep the number $10^{-13}$ in mind. In L07 a closed form
and the solver disagree by a factor of ten, and the interesting part is that the closed form is
the one that is wrong.

---
