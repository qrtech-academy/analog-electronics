# Appendix D - Solutions

In full, including the plausible wrong answers.

---

## D.1 Recall: the device in three facts

1. $I_C = I_S(e^{V_{BE}/V_T} - 1)$. **The diode of [L04](../../L04/README.md)** obeys the same
   equation, with the same $I_S$ and the same $V_T$, because the base-emitter junction is a diode.
2. **A decade**, a factor of ten, from $V_T \ln 10 = 59.9$ mV.
3. $V_T/I_C = 26$ ohm. **It is $r_e$**, the intrinsic emitter resistance, and from L07 onwards it
   is the quantity every result in Part 2 is written in terms of.
4. $I_E = I_C(1 + 1/50) = 1.02 I_C$. **Treating them as equal is a 2 per cent error**, which is
   smaller than the tolerance on any resistor in the circuit and far smaller than the spread in
   beta itself.

---

## D.2 Recall: the three regions

1. **Cutoff:** neither junction forward biased. **Forward active:** base-emitter forward,
   base-collector reverse. **Saturation:** both forward.
2. An amplifier lives in **forward active**. A switch uses **cutoff and saturation** and passes
   through active only in transit.
3. A **MOSFET's saturation** is where the channel is pinched off and the drain current no longer
   depends on drain voltage, so it is a current source. A **BJT's saturation** is where both
   junctions conduct and the device is a low resistance. **A MOSFET's saturation corresponds to a
   BJT's forward active region**, and a MOSFET's triode region corresponds to a BJT's saturation.
4. **The load line relies on the active region's current-source behaviour**: it is drawn across a
   family of curves that are flat, and the flatness is what makes the intersection well defined.
   **A switch relies on saturation's resistor behaviour**, because that is what makes the on-state
   drop small.

---

## D.3 Hand calculation: bias points from voltages

$V_{BE} = V_T \ln(I_C/I_S)$.

| $I_C$        | $V_{BE}$ | $I_B$         | $I_E$          |
| ------------ | -------- | ------------- | -------------- |
| 10 microamps | 0.539 V  | 0.2 microamps | 10.2 microamps |
| 1 mA         | 0.659 V  | 20 microamps  | 1.02 mA        |
| 10 mA        | 0.718 V  | 200 microamps | 10.2 mA        |

<!-- value: 0.659 = base_emitter_voltage(1e-3) -->

**The slope is 59.9 mV per decade**, so $V_{BE}$ against $\log I_C$ is a straight line of that
slope, and the three rows above are 60 mV apart per decade exactly.

**The plausible wrong answer** is to expect 0.7 V at 1 mA because that is the number everyone
quotes. It is 0.659 V for $I_S = 10^{-14}$ A. The 0.7 V figure corresponds to a few milliamps, and
the difference is why L06 computes bias currents with a constant drop and never computes anything
sensitive with one.

---

## D.4 Hand calculation: is it saturated

|     | Region                      | Why                                                                                                                  |
| --- | --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| a   | **Cutoff**                  | $V_{BE} = 0$, so the base-emitter junction is not conducting.                                                        |
| b   | **Forward active**          | $V_{BE} = 0.7$ forward, $V_{BC} = 0.7 - 3.0 = -2.3$ reverse.                                                         |
| c   | **Saturation**              | $V_{BE} = 0.8$ forward and $V_{BC} = +0.7$ also forward.                                                             |
| d   | **Forward active**          | $V_{BE} = 0.7$ forward, $V_{BC} = 2.7 - 5.0 = -2.3$ reverse. The emitter is not at ground, and that changes nothing. |
| e   | **Saturation, at its edge** | $V_{BC} = +0.7$, so the collector junction is fully forward biased and the collector is at the emitter potential.    |

**Row d is the one worth pausing on.** A reader who classifies by looking at $V_C$ alone will see
5 V and say active, which is right, and will say the same about a circuit whose emitter sits at
4.9 V, which would be wrong. **The region is decided by the two junction voltages, never by the
node voltages on their own.**

---

## D.5 Design: a relay driver

**1. A forced beta of 10**, for the same reason as [A.4](./a_the_bipolar_transistor.md#a4-designing-a-switch):
it guarantees saturation for any device whose $h_{FE}$ exceeds 10, which is all of them, and it
costs a tenth of the load current in base drive.

**2 and 3. The base resistor: 180 ohm.**

$$I_B = \frac{150\ \text{mA}}{10} = 15\ \text{mA}, \qquad
R_B = \frac{3.3 - 0.8}{15\ \text{mA}} = 167\ \Omega$$

Note the 0.8 V rather than 0.7: at 15 mA of base current the base-emitter drop is higher than the
textbook figure, and using 0.7 here would give a resistor 7 per cent too large.

The E12 neighbours are 150 and 180 ohm. **180 ohm** gives 13.9 mA and a forced beta of 10.8, which
is the right side to err on: it is the choice that draws less from the microcontroller pin, and
13.9 mA is already close to what many pins will supply.

**4. The design does not depend on $h_{FE}$ at all.** Nothing in the calculation used it. It stops
working only if $h_{FE}$ falls below the forced beta of 10.8, which no silicon transistor does.

**5. The coil is inductive**, so when the transistor turns off the current cannot stop instantly
and the collector flies up to whatever voltage is needed to keep it flowing. That will exceed the
transistor's breakdown voltage and destroy it, usually on the first operation. **A diode across
the coil**, cathode to the supply, gives the current a path and clamps the collector one diode
drop above the rail.

---

## D.6 Code: the two device models

Unpublished; the suite is the answer.

The hint that matters: **write the transport expressions and do not branch on region.** A model
with three cases has three sets of rounding behaviour and two seams, and the seams appear in L06
as small discontinuities in a bias curve that take an afternoon to trace. The transport form has
none, because saturation is what the equation does rather than a case it handles.

---

## D.7 Code: the transistor in the netlist

Unpublished. Two hints.

**Nine entries, not four.** Differentiate both transport expressions with respect to both junction
voltages, giving a two-by-two conductance matrix between the three terminals, plus the two
equivalent current sources that make the linearisation pass through the operating point. Stamping
it is mechanical once the derivatives are written down.

**Limit both junction voltages.** L04's diode circuit converged without limiting, slowly. This one
does not converge at all: both junctions are forward biased at the first solve, each drives the
other, and the iteration oscillates rather than merely crawling. Applying L04's limiter to both
$V_{BE}$ and $V_{BC}$ is the whole fix.

---

## D.8 Cross-check: the switch, and the model that agrees with itself

| Leg                                   | Collector current | $V_{CE}$      |
| ------------------------------------- | ----------------- | ------------- |
| 1. By hand, assuming 0.2 V saturation | 96.0 mA           | 0.2 V assumed |
| 2. By hand, transport model           | 98.9 mA           | 57 mV         |
| 3. By the solver                      | 98.9 mA           | 57 mV         |

**Legs 2 and 3 agree to five or six figures.** Same model, two methods.

**Leg 1 is 3 per cent lower, and leg 1 is closer to a bench.**

A real small-signal transistor carrying 100 mA saturates at 100 to 300 mV, not at 57 mV. The
transport model contains no bulk resistance: none in the collector material, none in the emitter,
none in the bond wires. At 1 mA those are negligible. At 100 mA they are most of the answer.

**So the two legs that agree are the two legs that are wrong**, and this is the point of the
exercise. Agreement between a closed form and a solver tells you the arithmetic is right. It says
nothing about whether the model contains the physics that decides the answer, and here it does
not.

The practical consequence is a heat calculation. Budgeting from 57 mV gives 5.7 mW in the
transistor; the real figure is nearer 20 mW. Both are small, so nothing burns; scale the same
error to a 5 A motor driver and the dissipation is 1 W predicted against 3.5 W actual, which is
the difference between a bare package and a heatsink.

**Sensitivity to beta.**

| $\beta_F$ | $I_C$    | $V_{CE}$ |
| --------- | -------- | -------- |
| 300       | 98.97 mA | 52 mV    |
| 50        | 98.86 mA | 57 mV    |
| 40        | 98.82 mA | 59 mV    |
| 8         | 72.0 mA  | 1.43 V   |

From 40 to 300, a factor of seven and a half in the parameter, the collector current moves by
0.15 per cent. **The design does not depend on beta**, which is what the forced-beta method was
for.

At $\beta_F = 8$, below the forced beta of 11, it collapses: the transistor cannot deliver the
current the base drive was supposed to guarantee, it leaves saturation, and the collector sits at
1.4 V dissipating 100 mW. **That is the cliff**, and every silicon transistor ever manufactured is
several times away from it.

**Diagnosing your own legs.**

Legs 2 and 3 should agree to five or six figures, and leg 1 should sit about 3 per cent below
them. Anything else is one of four things, and each says which line of your own code to look at:

* **Leg 3 comes back at 96.0 mA with $V_{CE}$ at exactly 0.2 V.** Your device model is branching
  on region and returning a fixed saturation voltage in one of the branches. The transport form
  has no such number anywhere in it; if 0.2 appears in your source, it was put there.
* **Leg 3 comes back at 100 mA exactly**, or at $5/50 = 100$ mA whatever you do to the base drive.
  The base-emitter drop is being taken as a constant, so the base current is whatever the 470 ohm
  allows rather than what the junction asks for, and the forced beta is not being enforced at all.
* **Leg 3 agrees with leg 2 but only to two or three figures.** The solve is stopping early.
  Tighten the convergence criterion; both legs are the same equations, so anything short of full
  convergence is the solver's tolerance and not physics.
* **Leg 3 will not converge, or oscillates.** The limiter is on one junction and not both. This is
  [C.7](./c_exercises.md#c7-code-the-transistor-in-the-netlist)'s warning arriving on schedule: a
  transistor forward-biases both junctions on the first solve and each drives the other.

**And a disagreement that is not a bug.** If leg 2 and leg 3 agree with each other but land near
0.2 V rather than 57 mV, you have added a bulk resistance to the model. That is a better model
than this course specifies, and the shipped suite will fail it. Take it out, or accept the
failure knowingly; what you must not do is leave it in and believe the suite.

---
