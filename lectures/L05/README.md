# L05 - The transistor as a device and as a switch

## Agenda
* The bipolar transistor with as little semiconductor physics as can be managed, which is almost
  none.
* An exponential, a current gain, and a saturation voltage. That is the whole device.
* Why this course assumes $h_{FE} = 50$ everywhere, and what that assumption is worth.
* Active, saturation and cutoff, and which one a switch lives in.
* Designing a switch: the base resistor, forced beta, and the saturation voltage you pay for.
* The MOSFET: a threshold, a square law, and two regions.
* BJT against MOSFET, honestly, on gain, input impedance and current.
* Live-coding `ael::device::bjt` and `ael::device::mosfet`.

---

## Lecture plan
1. **What Part 2 is.** Six lectures on the transistor amplifier. The device arrives today, the
   operating point tomorrow, and the small-signal model the day after; nothing is designed until
   all three exist.
2. **The device, in one equation.** The collector current is an exponential in the base-emitter
   voltage, and the base current is that divided by beta. Everything else is consequence.
3. **Beta is not a parameter you may trust.** It varies by a factor of three between devices of
   the same part number and moves with temperature and current. This course assumes 50, the
   bottom of the range, and every design must work there.
4. **Three regions.** Cutoff, forward active, saturation. An amplifier lives in the second; a
   switch uses only the first and third.
5. **Designing a switch.** Choose the base current from a forced beta rather than from $h_{FE}$,
   and the design stops depending on the parameter you were told not to trust.
6. **The MOSFET.** A different device with the same three regions and a square law instead of an
   exponential. Its transconductance is about ten times lower at the same current, and that single
   fact drives every comparison between the two.
7. **Live coding.** The transport model, the region classifier, and the transistor as a netlist
   element the nonlinear solver of L04 can handle.

---

## Before the lecture
* Finish L04. This lecture puts a transistor into the netlist, and the solver that copes with it
  is L04's.
* Read [Appendix A](./appendix/a_the_bipolar_transistor.md), which is the BJT and the switch.
* Read [Appendix B](./appendix/b_the_mosfet_and_what_to_build.md) up to
  [B.4](./appendix/b_the_mosfet_and_what_to_build.md#b4-what-to-build).
* Be ready to answer: a diode's incremental resistance at 1 mA is 26 ohm. What is a transistor's
  base-emitter junction doing at the same current, and why is that number about to matter?

---

## After the lecture
* Write `ael::device::bjt` and `ael::device::mosfet`, and add the BJT to `ael::net::Netlist`, to
  the specification in [B.4](./appendix/b_the_mosfet_and_what_to_build.md#b4-what-to-build).
* Add rows to the report program for `ael::device::bjt` and `ael::device::mosfet`.
* Work through [Appendix C](./appendix/c_exercises.md), ending with the **Cross-check**.
* Compare against [Appendix D](./appendix/d_solutions.md).

---

## What you should be able to do afterwards
* Write down the collector current of a BJT from its base-emitter voltage, and the base current
  from the collector current.
* Say what 60 mV of extra base-emitter voltage does, and why that number is familiar.
* Classify an operating point as cutoff, active or saturated from two voltages.
* Design a switch from a load current and a logic level, without using $h_{FE}$ anywhere.
* Say what forced beta is, why it is used, and what it costs.
* Write down a MOSFET's drain current in both of its regions, and the boundary between them.
* Say why a MOSFET stage needs about ten times the current of a BJT stage for the same gain, and
  where that stops being true.

---

## Questions to test yourself
* Two transistors of the same part number have $h_{FE}$ of 80 and 300. Which of your designs
  should care, and which should not?
* A transistor has 1 mA of collector current. What is the incremental resistance of its
  base-emitter junction, and what will that quantity be called from L07 onwards?
* Why is a saturated transistor's collector-emitter voltage not zero, and what would make it
  smaller?
* A switch is designed with a forced beta of 10. What happens if the transistor turns out to have
  $h_{FE}$ of 300? What if it has 40?
* Why does a switch waste less power than a linear stage doing the same job, and where does the
  power actually go in each case?
* A MOSFET and a BJT both carry 1 mA. Which has the higher transconductance, by how much, and what
  would you have to do to the MOSFET to equalise them?
* At what current do a BJT and a MOSFET have equal transconductance, and why is the answer
  suspicious?

---

## Reference
* [Appendix A](./appendix/a_the_bipolar_transistor.md): the BJT, its regions, and the switch.
* [Appendix B](./appendix/b_the_mosfet_and_what_to_build.md): the MOSFET, the comparison, and what
  to build.
* [Appendix C](./appendix/c_exercises.md): the exercises, ending with the Cross-check.
* [Appendix D](./appendix/d_solutions.md): worked solutions, in full.
* [The L05 test suite](./exercises/test/README.md).
* *The Art of Electronics*, Horowitz and Hill, chapter 2, for the transistor introduced the same
  way, and chapter 3 for the MOSFET.

---

## Next lecture
* L06 puts the device to work as an amplifier, which first means holding it still. Biasing, the
  quiescent point, and what an emitter resistor actually buys.

---
