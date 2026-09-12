# Appendix A - The bipolar transistor, and the switch
A practical treatment with as little semiconductor physics as possible. A transistor is an
exponential, a current gain, and a saturation voltage, and those three facts carry the whole of
Part 2.

---

## A.1 One equation, and one ratio
$$I_C = I_S\left(e^{V_{BE}/V_T} - 1\right), \qquad I_B = \frac{I_C}{\beta}$$

$I_S$ is around $10^{-14}$ A, $V_T$ is 26 mV, and $\beta$, also written $h_{FE}$, is between 50 and
300.

**That is the diode equation of [L04](../../L04/README.md)**, with the same $V_T$ and $I_S$,
because the base-emitter junction *is* a diode. Everything L04 established carries over:
* **60 mV per decade of current.** A transistor at 1 mA and 0.65 V needs 0.71 V for 10 mA.
* **The incremental resistance is $V_T/I$**, 26 ohm at 1 mA.

**That second one is the single most important number in this course.** From L07 it is $r_e$, the
intrinsic emitter resistance, and every gain, input resistance and output resistance in Part 2 is
written in terms of it. It arrives here as a property of a diode.

**The emitter carries both currents:**

$$I_E = I_C + I_B = I_C\left(1 + \frac{1}{\beta}\right)$$

which at $\beta = 50$ is 2 per cent more than $I_C$. That 2 per cent is why this course writes
$I_E \approx I_C$.

---

## A.2 Beta, and why this course assumes 50
$h_{FE}$ is the least trustworthy number on any datasheet. A 2N3904 is specified at 100 to 300 at
10 mA, and the same device at 0.1 mA and at 100 mA can differ by a factor of three.

**This course assumes $h_{FE} = 50$ everywhere,** below the specified minimum of most small-signal
parts, for one reason:

**A design that works at $h_{FE} = 50$ works at $h_{FE} = 300$. The reverse is not true.**

Hence the rule running through Part 2: **no design may depend on the value of beta.** Where beta
appears in a result, the design is arranged so the result is insensitive to it. There is exactly
one exception, the input resistance of an emitter follower in L08, and the lecture says so.

---

## A.3 Three regions
Two junctions, each forward or reverse biased, give four combinations, of which three are used.

| Region         | Base-emitter | Base-collector | Behaviour                           |
| -------------- | ------------ | -------------- | ----------------------------------- |
| Cutoff         | Reverse      | Reverse        | No current. An open switch.         |
| Forward active | Forward      | Reverse        | $I_C = \beta I_B$. An amplifier.    |
| Saturation     | Forward      | Forward        | $I_C < \beta I_B$. A closed switch. |

The fourth, reverse active, is a transistor used backwards; it works badly and nothing uses it on
purpose.

![Collector current against collector-emitter voltage for five base currents, with the fifty ohm load line drawn across them from five volts on the horizontal axis to a hundred milliamps on the vertical, and the two operating points of a switch marked at the ends of that line.](./images/bjt_output.png)

The curves are what the transistor allows, the straight line what the external circuit allows, and
the operating point is where they cross. **A switch uses only the two ends of that line;**
everything between them is where an amplifier lives and where a switch dissipates for nothing.

**Saturation is where the model stops being simple.** In the active region $I_C$ does not depend on
$V_{CE}$, so the transistor is a current source. Below about 0.2 V it does, steeply, so it is a
resistor instead. The simple model draws that knee as a corner and a real device rounds it off.

---

## A.4 Designing a switch
A switch must be **on hard**, meaning saturated, meaning a base current above $I_C/\beta$. Since
$\beta$ may not be trusted, it is chosen from a **forced beta** instead:

$$\beta_{forced} = \frac{I_C}{I_B}, \qquad \text{chosen as 10}$$

Ten times the base current the active region would need guarantees saturation for any device with
$h_{FE}$ above 10, which is every silicon transistor ever made.

![A switch: five volt logic through a base resistor into an NPN transistor, whose collector drives a fifty ohm load to a five volt rail and whose emitter is grounded, with annotations giving the base resistor as four hundred and seventy ohms and noting that the saturated collector-emitter voltage is not zero.](./images/switch.png)

For 100 mA of load current from a 5 V logic level:

$$I_B = \frac{100\ \text{mA}}{10} = 10\ \text{mA}, \qquad
R_B = \frac{5 - 0.7}{10\ \text{mA}} = 430\ \Omega$$

so 470 ohm from the E12 series, giving 9.1 mA and a forced beta of 11.

<!-- value: 470 = nearest_e12(switch_base_resistor(5.0, 0.1)) -->

**Note the 0.7 V, where every bias point in this course uses 0.65.** A forced beta of 10 drives the
base ten times harder than the active region would, and 60 mV a decade is what that costs: the
junction sits above the small-signal figure, and `baseResistor` uses 0.7 for exactly this reason.
At larger currents it moves again, which is why [C.5](./c_exercises.md#c5-design-a-relay-driver)
needs 0.8.

**What forced beta costs.** A tenth of the load current thrown away in the driver, and stored base
charge that must be removed before the device turns off. A hard-saturated transistor is slow to
turn off for exactly that reason, and a fast switch is deliberately kept out of deep saturation.

**What the saturation voltage costs.** 0.1 to 0.3 V across the device, so 10 to 30 mW at 100 mA. A
linear stage delivering the same current at half the supply dissipates 250 mW. **That ratio is the
entire reason switching exists.**

---

## A.5 What the model here is blind to
* **Bulk resistance.** The ideal transport model gives a saturation voltage of about 57 mV for the
  switch above; a real device gives 100 to 300 mV. **The model is optimistic, and the direction
  matters:** a design relying on the modelled figure runs hotter than predicted.
* **Speed.** Charge storage, transit time and junction capacitance are all absent, so nothing here
  says how fast a transistor switches. That is usually what decides the choice of part.
* **Breakdown.** Above some collector-emitter voltage the device conducts whatever the base does,
  and an inductive load will drive it there unless something is done about that.
* **Second breakdown.** A power transistor can fail at combinations of voltage and current that are
  individually within specification. Nothing here models it.

---
