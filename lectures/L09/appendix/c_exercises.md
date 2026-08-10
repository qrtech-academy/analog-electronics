# Appendix C - Exercises

Eight, ending with the Cross-check. That one asks a design lever to keep helping, and finds that
past a certain point it stops.

Worked solutions are in [Appendix D](./d_solutions.md), in full.

---

## C.1 Recall: the pair and its tail

1. What does the tail current fix, and what do the inputs decide?
2. A pair has a 2 mA tail. What is $r_e$ on each side? Show the step that is easy to get wrong.
3. Describe what the tail *node* does for a differential input and for a common-mode input.
4. Why does a resistance $R_{tail}$ in the tail behave as $2R_{tail}$ to one half of the pair?

---

## C.2 Recall: the two factors of two

1. The differential gain to one collector is $-R_C/2r_e$. Account for the two.
2. There is a second factor of two available. Where, and what recovers it?
3. Which of the two is a property of what "differential" means, and which is a choice?
4. A current-mirror load raises the gain by a factor of ten in this lecture. Split that into its
   two independent causes and say what each is worth.

---

## C.3 Hand calculation: the pair, resistively loaded

A pair with a 2 mA tail, $R_C = 10$ kilohm, $\beta = 50$, and a 10 kilohm tail resistor.

1. $r_e$, the differential gain to one collector, and the gain to both.
2. The common-mode gain to one collector.
3. CMRR, as a ratio and in decibels.
4. Recompute all of parts 1 to 3 with $R_C = 100$ kilohm. Which numbers changed and which did not?

**Check yourself:** `differentialGain`, `commonModeGain`, `commonModeRejection`.

---

## C.4 Hand calculation: the large signal

Same pair.

1. The difference current at $v_d = 5$ mV, 26 mV and 100 mV.
2. What fraction of the tail has moved at each.
3. The input at which the small-signal answer is 1 per cent optimistic.
4. Repeat part 3 for a 20 mA tail. Explain the result.

**Check yourself:** `transfer`, `linearRange`.

---

## C.5 Design: a pair to a rejection requirement

An instrumentation front end needs 80 dB of common-mode rejection at a 2 mA tail, with a
single-ended output.

1. What tail resistance does that require?
2. What voltage would a resistor of that value drop, and what supply does that imply?
3. State the arrangement you would actually use, and what its incremental resistance has to be.
4. Now suppose you may take the output differentially instead. What matching would give you 80 dB
   with a 10 kilohm resistor tail? Comment on which of the two designs you would build.

**Check yourself:** `commonModeRejection`, `commonModeRejectionDifferential`, `decibels`.

---

## C.6 Design: offset

The same pair, driven from a source of 10 kilohm on one input and 1 kilohm on the other.

1. The base current in each input, and the offset voltage the *imbalance* produces.
2. The offset from a 1 per cent collector-resistor mismatch, referred to the input.
3. The offset from 1 mV of $V_{BE}$ mismatch, referred to the input.
4. Rank the three, then say what single change removes the largest one entirely and what it costs.

**Check yourself:** `inputOffset`.

---

## C.7 Code: the pair

Implement `ael::diffpair` to the specification in
[Appendix B.7](./b_rejection_and_the_mirror.md#b7-what-to-build).

**`commonModeRejection` must be the ratio of your own two gain functions**, not a separate
formula. The lecture's central claim is that $R_C$ cancels out of that ratio, and writing it as a
ratio is what makes your code demonstrate the claim rather than restate it.

**`linearRange` must not take the tail current as an argument.** If your derivation produced one,
something cancelled that you did not cancel.

---

## C.8 Cross-check: common-mode rejection, and the lever that reverses

The pair of [C.3](#c3-hand-calculation-the-pair-resistively-loaded): 2 mA tail, 10 kilohm collector
resistors, 10 kilohm tail resistor to a negative rail. Find its CMRR, four ways.

1. **By hand.** $(2R_{tail} + r_e)/2r_e$.
2. **By your closed form, twice**, once with $R_C = 10$ kilohm and once with $R_C = 100$ kilohm.
3. **By your solver.** Apply a small differential input, measure the change at one collector;
   apply a small common-mode input, measure the change at the same collector; divide.
4. **Then replace the tail resistor with an ideal current source and repeat leg 3.**

### What to expect

**Legs 1, 2 and 3 agree to about a decibel**, at 52, 52 and 51. **Leg 2 gives the same number
twice**, because the collector resistor cancels; if yours does not, `commonModeRejection` is not a
ratio of your two gains.

**Leg 4 is the exercise, and it does not return infinity.** An ideal current source has infinite
incremental resistance, so the expected answer is that the common-mode gain is zero. What you will
get is a small, **stable, positive** common-mode gain and a CMRR of about **101 dB**.

That number is not noise: check it by changing your perturbation size by three decades and
watching it stay put. **Find out where it comes from.** Two experiments settle it:

* Set the Early voltage to $10^9$ and repeat. The common-mode gain should collapse to your
  solver's arithmetic floor.
* Set $\beta$ to 5000 and repeat. It should fall by about a hundred.

**Then sweep the tail.** Put the ideal source in parallel with a resistor and step that resistor
from 1 megohm to 10. The closed form says CMRR rises without limit. Report what the solver says,
and where the maximum is.

**Finally, answer this.** L05's Cross-check had two legs that agreed with each other and were both
wrong about a real device. This one has a leg that is exactly right about the model and answers a
question nobody asked. **What is the single statement about models that covers both?**

**If leg 3 gives a CMRR near 1**, you have applied the common-mode input to only one base.

**If leg 3's differential gain is 385 rather than 192**, you have measured the difference between
the two collectors rather than one of them, which is
[B.5](./b_rejection_and_the_mirror.md#b5-the-other-output-and-why-the-answer-changes-completely)'s
question rather than this one.

---
