# Appendix C - Exercises

Eight, ending with the Cross-check. Do them in order; the last one needs the code from the two
before it.

Worked solutions are in [Appendix D](./d_solutions.md), in full. Read them after you have your own
answers, including the ones you are unsure about, because being unsure and right is a different
thing from being unsure and wrong and the solutions say which is which.

---

## C.1 Recall: the convention

State the sign convention this course fixes for a current source and for a voltage source's
reported current. Then answer this: your solver comes back with a divider output of $-1.71$ V
instead of $+1.71$ V, and every voltage in the circuit is negated. Which of the two conventions
did you get backwards, and how do you know it was that one rather than the other?

---

## C.2 Recall: two dividers

A divider made of two 1 megohm resistors and a divider made of two 10 ohm resistors have the same
ratio.

1. What is the Thevenin resistance of each?
2. One of them is the front end of an oscilloscope probe and the other is inside a power supply.
   Which is which, and why?
3. A third divider uses two 10 ohm resistors across a 10 V supply. What is its power dissipation,
   and is that a problem?

---

## C.3 Hand calculation: the divider, three ways

For a 33 kilohm over 6.8 kilohm divider on a 10 V supply, by hand:

1. The unloaded output.
2. The Thevenin resistance.
3. The output with a 10 kilohm load, computed twice: once by substituting the parallel combination
   into the divider formula, and once from the Thevenin equivalent. Confirm they agree, and say
   why they must.
4. The load that would halve the output.

**Check yourself:** `divider`, `divider_output_resistance`.

---

## C.4 Hand calculation: node equations

A 1 mA current source injects into node 1. A 1 kilohm resistor runs from node 1 to ground, a
2.2 kilohm resistor from node 1 to node 2, and a 4.7 kilohm resistor from node 2 to ground.

1. Write the current-law equation at node 1 and at node 2. Do not solve them yet.
2. Write the two equations as a matrix, and identify each of the four entries as a stamp
   contribution from a named resistor.
3. Solve for both node voltages.
4. Kill the source and find the resistance looking into node 2. Now divide node 2's voltage from
   part 3 by the 1 mA source current. Those two numbers are both resistances and both about node
   2. Say whether they agree, and if not, say precisely what each one is a resistance *between*.

---

## C.5 Design: a reference divider

Design a divider giving 2.5 V from a 10 V supply, subject to:

* Thevenin resistance no greater than 2.2 kilohm, so the next stage does not load it.
* Divider current no greater than 1 mA, because the supply is a battery.
* E12 values only.

Give both resistors, the output voltage you actually achieve, the Thevenin resistance and the
current. Then state the percentage error in the output, and say whether you would accept it.

There is a tempting wrong answer to this one. Find the pair whose *ratio* is closest to correct,
check it against both constraints, and say what it violates.

**Check yourself:** `divider`, `divider_output_resistance`, `nearest_e12`.

---

## C.6 Code: the netlist

Implement `ael::net::Netlist` to the specification in
[Appendix B.5](./b_nodal_analysis.md#b5-what-to-build).

Four of L01's seventeen tests are for this. Getting them green needs no solver, so do this first
and confirm the suite goes from four passing to eight.

---

## C.7 Code: the solver

Implement `ael::mna::solve` to the same specification.

Assemble the stamps, solve by Gaussian elimination with partial pivoting, and detect a singular
matrix rather than returning zeros. All seventeen tests should pass.

Two of them are worth reading before you start rather than after you fail them:
`Mna.ParallelResistorsCombine`, which fails for a solver that indexes by element instead of by
node, and `Mna.FloatingNodeIsReportedRatherThanGuessed`, which fails for a solver that trusts its
own elimination.

---

## C.8 Cross-check: the loaded divider

The signature exercise of this course, and the shape every later one takes. Compute the same
number three ways and reconcile them.

Take the 33 kilohm over 6.8 kilohm divider on a 10 V supply, loaded with 10 kilohm.

1. **By hand.** Substitute the parallel combination into the divider formula. Write down the
   answer to three significant figures before doing anything else.
2. **By your closed form.** Whatever you wrote for [C.3](#c3-hand-calculation-the-divider-three-ways),
   as a function, evaluated on the same numbers.
3. **By your solver.** Build the netlist with four elements, one voltage source and three
   resistors, and read node 1 out of `ael::mna::solve`.

Then reconcile. State the difference between each pair, and say what would have to be true for
each difference to be non-zero.

### What to expect

**Legs 1 and 2 should agree to every digit you wrote down.** They are the same formula evaluated
by two different pieces of hardware. A disagreement here is an arithmetic slip in leg 1 or a typo
in leg 2, and it is not interesting except that finding it is faster than finding it later.

**Legs 2 and 3 should agree to about twelve significant figures.** Both are solving the same
linear problem in double precision, one by algebra you did in advance and one by elimination. The
difference is rounding and nothing else, and it should be somewhere around $10^{-13}$ relative.

**A difference of a few per cent means one of them is not solving the circuit you think it is.**
The usual cause is the load stamped between the wrong pair of nodes, which quietly gives you a
different circuit rather than an error. The second usual cause is the supply node and the output
node swapped, which gives you the reciprocal divider.

**A difference of exactly a factor of two, or exactly the unloaded answer, means the load is not
in the circuit at all.** Check `resistorCount()`.

This exercise is deliberately one where all three legs agree. That is worth doing once, so that
you know what agreement looks like before L07, where a closed form and the
solver disagree by a factor of ten and the closed form is the one that is wrong.

---
