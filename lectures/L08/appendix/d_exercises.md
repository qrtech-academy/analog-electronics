# Appendix D - Exercises

Eight, ending with the Cross-check. That one retires a model this course has used since L05, at
the exact calculation where it stops working.

Nothing here is set on [Appendix C](./c_power_amplifiers.md), which is reading.

Worked solutions are in [Appendix E](./e_solutions.md), in full.

---

## D.1 Recall: the stage that does nothing

1. Write the follower's gain, input resistance and output resistance.
2. The gain is always less than one. Where does the missing part go, and what is the only lever
   on it?
3. Which two of those three results depend on $h_{FE}$?
4. A follower has no voltage gain. Name two distinct things it is nevertheless used for.

---

## D.2 Recall: the three classes

1. Define class A, class B and class AB by what conducts when.
2. Give the maximum theoretical efficiency of class A and of class B.
3. What is crossover distortion, how wide is the band it occupies, and why is it more objectionable
   than its percentage suggests?
4. Class B has better efficiency and worse distortion than class AB. What does class AB give up
   to get the distortion back?

---

## D.3 Hand calculation: a follower at three currents

An emitter follower drives an 8 ohm loudspeaker. $\beta = 50$.

1. Its gain at 1 mA, at 10 mA and at 120 mA.
2. Its output resistance at each, driven from a 1 kilohm source.
3. The resistance looking into its base at each.
4. One of the three columns is nearly constant. Which, and why?

**Check yourself:** `gain`, `outputResistance`, `inputResistance`.

---

## D.4 Hand calculation: what the loudspeaker costs

The L07 stage: gain 38.5, output resistance 9.89 kilohm.

1. Its gain driving 8 ohm directly.
2. Its gain driving a follower biased at 120 mA, which drives the 8 ohm.
3. The same with a Darlington in place of the follower.
4. Repeat part 3 with $\beta = 20$ and with $\beta = 200$, and say in one sentence what that
   spread means for the design.

**Check yourself:** `loadedGain`, `inputResistance`, `darlingtonInputResistance`.

5. A Darlington's effective emitter resistance is twice a single transistor's, and $h_{FE}$ does
   not appear in that statement. Derive it.

---

## D.5 Design: a class-AB output stage

A stage is to idle at 100 mA and drive 8 ohm from $\pm 25$ V rails.

1. Size the emitter resistors by the 26 mV rule, and choose E12 values.
2. State the emitter factor you have bought and what fraction of the load your resistors now are.
3. Compute the bias voltage the stage needs, from the exponential rather than from 0.65 V.
4. State the maximum sine power into 8 ohm, ignoring saturation. Then say what you would actually
   specify the amplifier at, and why the two differ.

**Check yourself:** `degenerationResistor`, `biasVoltage`, `nearest_e12`.

---

## D.6 Design: thermal

The stage from [D.5](#d5-design-a-class-ab-output-stage), with the bias generator held at a fixed
voltage.

1. The fractional change in idle current per degree.
2. What the idle current becomes after a 30 degree rise, if nothing tracks.
3. Recompute part 1 with the emitter resistors removed, and state what they bought.
4. State where the bias generator must be mounted and what it is doing there. One sentence.

**Check yourself:** `driftPerDegree`.

---

## D.7 Code: the follower and the output stage

Implement `ael::follower` and `ael::output` to the specification in
[Appendix B.7](./b_the_output_stage.md#b7-what-to-build).

**`idleCurrent` may not use a constant base-emitter drop.** It is the inverse of an equation with
an exponential and a linear term in it and they do not separate. Bisect in the logarithm, or use
the Newton iteration with the step limiter you wrote in L04. A version that assumes 0.65 V will
pass one test in the shipped suite and fail four.

---

## D.8 Cross-check: the bias voltage a class-AB stage actually needs

The stage of [B.3](./b_the_output_stage.md#b3-class-ab-and-the-26-millivolt-rule): two
complementary followers, 0.22 ohm emitter resistors, idling at 120 mA. Find the bias voltage
between the two bases, three ways.

1. **By hand, with the constant-drop model.** Two base-emitter drops at 0.65 V, plus the two
   resistor drops.
2. **By hand, with the exponential.** $V_{BE} = V_T \ln(I_C/I_S)$ at the idle current, plus the
   two resistor drops.
3. **By your solver.** You do not need a PNP model for this. **At idle the stage is symmetric**:
   no current flows in the load, the output node sits at zero, and each device carries the same
   current from half the bias voltage. So simulate one half, an NPN with its base held at
   $V_{bias}/2$ and its emitter resistor returned to ground, and bisect on that base voltage
   until the collector current is 120 mA.

Then run it backwards, which is where the size of the disagreement shows: **apply leg 1's answer
to the real stage and ask your solver what idle current results.**

### What to expect

**Legs 2 and 3 agree to about 1 per cent**, at 1.619 and 1.604 V. **Leg 1 gives 1.353 V**, a
quarter of a volt below both.

**And 1.353 V applied to the stage gives an idle current of two or three milliamps, not 120.** A
factor of about fifty. The stage is in class B, the dead band is open, and every quiet passage is
distorted.

**Legs 2 and 3 differ by 14 mV and their idle currents differ by 31 per cent.** Say why, and note
that it is the same effect the exercise is about, one order of magnitude down.

**Explain, in your own words, why a model that was worth 1 per cent in L05 and 12 per cent in L06
is worth a factor of fifty here.** The answer is in what is being computed, not in the model.

**If your leg 3 needs no adjustment to reach 120 mA**, your solver's transistor is using a
constant drop somewhere, and you have measured leg 1 twice.

---
