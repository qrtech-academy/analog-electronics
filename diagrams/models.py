"""The models every figure is drawn from and every quoted number is checked against.

Two rules govern this file, and between them they are most of what keeps the course honest.

**Every number an appendix quotes is computed here.** An appendix opts a number in by tagging it,
and `ci/numbers.py` evaluates the tag against this module:

    A 1 mA stage has an intrinsic emitter resistance of 26 ohms.
    <!-- value: 26.0 = intrinsic_emitter_resistance(1e-3) -->

So a constant changed here goes red in every appendix that quoted it, which is the failure mode a
repository like this one otherwise has no defence against.

**Every function here is one the reader also writes in C++.** This module is not a reference
implementation to be consulted; it is this course's copy of a calculation the reader is asked to
implement as part of `ael`. Where the two disagree the exercise is to find out which is wrong, and
that only works if this file is as answerable as the reader's is.

Which numbers are matched to reality, and which are merely representative:

* **Matched.** The thermal voltage, the temperature coefficient of V_BE, and the E12 series are
  physical or standardised, and are right.
* **Representative.** h_FE = 50, the Early voltage of 100 V, and the MOSFET transconductance
  parameters are this course's working assumptions. Real devices spread over a factor of five on
  the first and a factor of ten on the second. They are stated as assumptions in the lectures
  rather than presented as data, and every result that leans hard on one says so.

Nothing in this file is measured. There is no bench in this course.
"""

from __future__ import annotations

import math

# ----------------------------------------------------------------------------------------
# Physical constants
# ----------------------------------------------------------------------------------------

# The thermal voltage kT/q. At 300 K it is 25.85 mV; this course uses 26 mV throughout, because
# every rule of thumb built on it is quoted to two significant figures and 26 divides nicely.
# THERMAL_VOLTAGE_EXACT is here so that the one exercise that asks how much the approximation
# costs has something to compare against; the answer is 0.6 %.
THERMAL_VOLTAGE = 0.026
THERMAL_VOLTAGE_EXACT = 0.02585

# How the base-emitter voltage of a conducting BJT moves with temperature, at a fixed collector
# current. Around -2 mV/K for a silicon junction, and the sign matters: V_BE *falls* as the device
# heats, which is why a stage biased from a stiff divider sees its current rise.
VBE_TEMPCO = -2.0e-3

# The forward drop of a conducting silicon junction, at the currents this course works at.
VBE_ON = 0.65

# ----------------------------------------------------------------------------------------
# Device assumptions
#
# These are deliberate rather than careless. h_FE is taken at the bottom of its range because a
# design that works at h_FE = 50 works at h_FE = 250, and the reverse is not true.
# ----------------------------------------------------------------------------------------

HFE = 50.0
EARLY_VOLTAGE = 100.0

# A MOSFET's transconductance at 1 mA, an order of magnitude below a BJT's at the same current.
# That single fact is why the source factor is around two where the emitter factor is around ten.
NMOS_GM_AT_1MA = 4.0e-3

# The voltage this course drops across a degeneration resistor. Chosen because 220 mV over the
# decade of collector currents used here lands on an E12 value every time: 220 ohms at 1 mA,
# 22 at 10 mA, 12 at 20 mA.
DEGENERATION_DROP = 0.220

E12 = (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2)


# ----------------------------------------------------------------------------------------
# The intrinsic resistances
# ----------------------------------------------------------------------------------------


def intrinsic_emitter_resistance(collector_current: float) -> float:
    """r_e, the resistance the emitter presents from inside the transistor.

    This is the quantity the whole course is built on. It is not a resistor; it is the slope of
    the device's own exponential at the operating point, which is why it depends on nothing but
    the current and the temperature.
    """
    return THERMAL_VOLTAGE / collector_current


def transconductance(collector_current: float) -> float:
    """g_m for a BJT, which is exactly the reciprocal of r_e.

    g_m is the more standard quantity and r_e the easier one to reason with. Both are here
    because the course reasons in r_e and connects to other literature through g_m.
    """
    return 1.0 / intrinsic_emitter_resistance(collector_current)


def intrinsic_source_resistance(gm: float) -> float:
    """r_s, the MOSFET's counterpart to r_e.

    No textbook gives this quantity a name. This course does, for one reason: with r_s defined,
    every common-emitter result becomes the common-source result by substituting r_s for r_e, and
    nothing else changes. That substitution is the whole of the MOSFET half of the course.

    It is a name for 1/g_m and not a new model. Anyone reading a textbook afterwards will find
    g_m and should recognise it immediately.
    """
    return 1.0 / gm


def early_resistance(
    collector_current: float, early_voltage: float = EARLY_VOLTAGE
) -> float:
    """r_o, the transistor's own output resistance, from the Early effect.

    Large but not infinite, and the difference is what decides how much gain a stage with a
    current-mirror load can actually reach.
    """
    return early_voltage / collector_current


def base_resistance(collector_current: float, hfe: float = HFE) -> float:
    """r_pi, the resistance looking into the base, excluding any external emitter resistor."""
    return hfe * intrinsic_emitter_resistance(collector_current)


# ----------------------------------------------------------------------------------------
# The emitter factor and the source factor
#
# The organising device of this course's whole transistor treatment.
# ----------------------------------------------------------------------------------------


def emitter_factor(collector_current: float, emitter_resistor: float) -> float:
    """EF: the factor by which a degeneration resistor raises the total emitter resistance.

    One number that answers two questions at once. It is exactly the factor by which the stage's
    voltage gain falls, and it is very nearly the factor by which the resistance looking into the
    collector rises. A design with EF = 10 has given up a decade of gain and bought a decade of
    everything degeneration buys.
    """
    return (
        emitter_resistor + intrinsic_emitter_resistance(collector_current)
    ) / intrinsic_emitter_resistance(collector_current)


def source_factor(gm: float, source_resistor: float) -> float:
    """SF: the emitter factor, for a MOSFET.

    Identical in form once r_s is written for r_e, which is the point of naming r_s at all. It
    comes out around two where a BJT's comes out around ten, for the same 220 mV across the
    resistor, purely because a MOSFET's transconductance is about ten times lower.
    """
    return (
        source_resistor + intrinsic_source_resistance(gm)
    ) / intrinsic_source_resistance(gm)


def degeneration_resistor(
    collector_current: float, drop: float = DEGENERATION_DROP
) -> float:
    """The emitter or source resistor that drops `drop` volts at the operating current."""
    return drop / collector_current


def nearest_e12(value: float) -> float:
    """The nearest E12 value to `value`, on a logarithmic distance.

    Logarithmic rather than linear because component series are geometric: 8.2 is nearer to 9 than
    10 is, even though the linear distances say otherwise.
    """
    if value <= 0.0:
        raise ValueError("component values are positive")

    decade = 10.0 ** math.floor(math.log10(value))
    candidates = [step * decade for step in E12] + [10.0 * decade]
    return min(candidates, key=lambda option: abs(math.log(value / option)))


# ----------------------------------------------------------------------------------------
# The common-emitter stage
# ----------------------------------------------------------------------------------------


def ce_gain(
    collector_resistor: float,
    collector_current: float,
    emitter_resistor: float = 0.0,
    load: float | None = None,
) -> float:
    """Voltage gain of a common-emitter stage, negative because the stage inverts.

    The result the reader implements first. It ignores r_o, which for a resistively loaded stage
    costs under a percent and for a mirror-loaded stage is the entire
    answer; `ce_gain_exact` is the version that does not ignore it.
    """
    total_collector = (
        collector_resistor if load is None else parallel(collector_resistor, load)
    )
    return -total_collector / (
        emitter_resistor + intrinsic_emitter_resistance(collector_current)
    )


def ce_gain_exact(
    collector_resistor: float,
    collector_current: float,
    emitter_resistor: float = 0.0,
    load: float | None = None,
    early_voltage: float = EARLY_VOLTAGE,
) -> float:
    """Common-emitter gain with the transistor's own output resistance included."""
    total_collector = parallel(
        collector_resistor, early_resistance(collector_current, early_voltage)
    )
    if load is not None:
        total_collector = parallel(total_collector, load)
    return -total_collector / (
        emitter_resistor + intrinsic_emitter_resistance(collector_current)
    )


def ce_input_resistance(
    collector_current: float, emitter_resistor: float = 0.0, hfe: float = HFE
) -> float:
    """Resistance looking into the base, excluding the bias divider."""
    return hfe * (intrinsic_emitter_resistance(collector_current) + emitter_resistor)


def resistance_into_collector(
    collector_current: float,
    emitter_resistor: float = 0.0,
    hfe: float = HFE,
    early_voltage: float = EARLY_VOLTAGE,
) -> float:
    """Resistance looking into the collector, with the collector resistor removed.

    **This is the quantity the emitter factor multiplies**, and getting that attribution right
    is the correction at the centre of L07.

    It is tempting to write the stage's output resistance as R_C * EF. It cannot be: the stage's
    output resistance is R_C in parallel with this, and a parallel combination is smaller than
    either part, so no amount of degeneration pushes it above R_C. What degeneration raises is the
    resistance looking into the collector, which is what this returns, and the boost is invisible
    from outside the stage until the collector resistor is large enough not to swamp it.

    That is exactly why a current-mirror load exists, and it is the reason L09's mirror-loaded
    pair reaches the gain it does. See `ce_output_resistance`.
    """
    degenerated = parallel(emitter_resistor, base_resistance(collector_current, hfe))
    return (
        early_resistance(collector_current, early_voltage)
        * (1.0 + transconductance(collector_current) * degenerated)
        + degenerated
    )


def ce_output_resistance(
    collector_resistor: float,
    collector_current: float,
    emitter_resistor: float = 0.0,
    hfe: float = HFE,
    early_voltage: float = EARLY_VOLTAGE,
) -> float:
    """Output resistance of a common-emitter stage, seen at the collector node.

    Pass the mirror's own output resistance as `collector_resistor` to get the mirror-loaded case,
    which is where degeneration finally pays.
    """
    return parallel(
        collector_resistor,
        resistance_into_collector(
            collector_current, emitter_resistor, hfe, early_voltage
        ),
    )


# ----------------------------------------------------------------------------------------
# The cascode, and the Miller effect it answers
# ----------------------------------------------------------------------------------------

# The base-collector capacitance of a small-signal BJT. Representative rather than measured; a
# 2N3904 specifies about 4 pF at 5 V and it rises as the reverse bias falls.
C_BC = 4.0e-12


def cascode_output_resistance(
    collector_current: float, hfe: float = HFE, early_voltage: float = EARLY_VOLTAGE
) -> float:
    """Resistance looking into the collector of a cascode pair.

    There is nothing new here, and that is the point worth teaching. A cascode is a degenerated
    stage whose degeneration resistor happens to be another transistor's output resistance, so the
    emitter factor applies unchanged with $R_E = r_o$. It comes out enormous, and then runs into
    the ceiling every degenerated stage has: the base resistance shunts the degeneration, so the
    boost can never exceed h_FE however large the degeneration is.

    That ceiling is why a cascode buys about a factor of fifty here and not a factor of ten
    thousand, and it is the same ceiling `resistance_into_collector` already models.
    """
    return resistance_into_collector(
        collector_current,
        early_resistance(collector_current, early_voltage),
        hfe,
        early_voltage,
    )


def miller_capacitance(gain: float, feedback_capacitance: float = C_BC) -> float:
    """The base-collector capacitance as the input sees it.

    A capacitor bridging input to output, across a stage that inverts by |G|, presents
    $C(1 + |G|)$ at the input, because the far end moves the other way by |G| times as much. On a
    stage with a gain of 385 a 4 pF capacitor becomes 1.5 nF, which is what closes the bandwidth
    down long before the device runs out of speed.
    """
    return feedback_capacitance * (1.0 + abs(gain))


def input_pole(source_resistance: float, capacitance: float) -> float:
    """The corner frequency an input capacitance makes with the resistance driving it."""
    return 1.0 / (2.0 * math.pi * source_resistance * capacitance)


# ----------------------------------------------------------------------------------------
# Bias and temperature
# ----------------------------------------------------------------------------------------


def divider_bias_current(
    supply: float,
    upper: float,
    lower: float,
    emitter_resistor: float,
    vbe: float = VBE_ON,
) -> float:
    """Collector current of a divider-biased stage, assuming the divider is stiff.

    Stiff means the base current is negligible against the divider current, which is the
    assumption the whole design method rests on and the one an exercise is built on breaking.
    """
    base_voltage = supply * lower / (upper + lower)
    return (base_voltage - vbe) / emitter_resistor


def loaded_bias_base_current(
    supply: float,
    upper: float,
    lower: float,
    emitter_resistor: float,
    vbe: float = VBE_ON,
    hfe: float = HFE,
) -> float:
    """Base current of a divider-biased stage once the base is allowed to load the divider.

    The closed form of the fixed point A.3 solves by iteration. The emitter resistor carries the
    *emitter* current, so it appears as (hfe + 1) R_E referred to the base; dropping that term is
    the one simplification this section cannot afford, because its whole subject is the base
    current it would drop.
    """
    thevenin_voltage = supply * lower / (upper + lower)
    thevenin_resistance = parallel(upper, lower)
    return (thevenin_voltage - vbe) / (
        thevenin_resistance + (hfe + 1.0) * emitter_resistor
    )


def loaded_bias_current(
    supply: float,
    upper: float,
    lower: float,
    emitter_resistor: float,
    vbe: float = VBE_ON,
    hfe: float = HFE,
) -> float:
    """Collector current of a divider-biased stage, with the base current's droop included."""
    return hfe * loaded_bias_base_current(
        supply, upper, lower, emitter_resistor, vbe, hfe
    )


def loaded_bias_droop(
    supply: float,
    upper: float,
    lower: float,
    emitter_resistor: float,
    vbe: float = VBE_ON,
    hfe: float = HFE,
) -> float:
    """How far the base current pulls the divider's output below its unloaded value, in volts."""
    base_current = loaded_bias_base_current(
        supply, upper, lower, emitter_resistor, vbe, hfe
    )
    return base_current * parallel(upper, lower)


def loaded_bias_error(
    supply: float,
    upper: float,
    lower: float,
    emitter_resistor: float,
    vbe: float = VBE_ON,
    hfe: float = HFE,
) -> float:
    """Fraction by which the stiff-divider prediction overstates the actual collector current."""
    predicted = divider_bias_current(supply, upper, lower, emitter_resistor, vbe)
    actual = loaded_bias_current(supply, upper, lower, emitter_resistor, vbe, hfe)
    return (predicted - actual) / predicted


def bias_stiffness(
    supply: float,
    upper: float,
    lower: float,
    emitter_resistor: float,
    vbe: float = VBE_ON,
    hfe: float = HFE,
) -> float:
    """Divider current over base current. Ten is the usual rule of thumb."""
    base_current = loaded_bias_base_current(
        supply, upper, lower, emitter_resistor, vbe, hfe
    )
    return (supply / (upper + lower)) / base_current


def drift_without_degeneration(temperature_rise: float = 1.0) -> float:
    """Fractional change in collector current per degree, at a fixed base-emitter voltage.

    The exponential moved by 2 mV of V_BE drift, which is about 8 % per degree. Quoting it as
    "about 10 %" is close enough, and for the undegenerated case it is the right ballpark.
    """
    return math.exp(-VBE_TEMPCO * temperature_rise / THERMAL_VOLTAGE) - 1.0


def drift_with_degeneration(
    collector_current: float, emitter_resistor: float, temperature_rise: float = 1.0
) -> float:
    """Fractional change in collector current per degree, with an emitter resistor.

    With the base held by a stiff divider, V_BE falling 2 mV/K lifts the emitter by the same 2 mV,
    and the current rises by that over the emitter resistor. On a 1 mA stage with 1 kilohm that is
    2 microamps per degree: 0.2 %/K, against 8 %/K without the resistor.

    The ratio between the two is the loop gain, 1 + R_E/r_e, which is the emitter factor. So the
    resistor suppresses drift by exactly the factor it costs in gain, and that trade is the
    whole content of L06 B.3.
    """
    delta = -VBE_TEMPCO * temperature_rise / emitter_resistor
    return delta / collector_current


def drift_suppression(collector_current: float, emitter_resistor: float) -> float:
    """How many times smaller the drift is with the emitter resistor than without.

    Equal to the emitter factor, to within the linearisation.
    """
    return drift_without_degeneration() / drift_with_degeneration(
        collector_current, emitter_resistor
    )


# ----------------------------------------------------------------------------------------
# Followers
# ----------------------------------------------------------------------------------------


def follower_gain(collector_current: float, emitter_resistor: float) -> float:
    """Emitter-follower voltage gain: just under one, and the shortfall is the point."""
    re = intrinsic_emitter_resistance(collector_current)
    return emitter_resistor / (emitter_resistor + re)


def follower_output_resistance(
    collector_current: float, source_resistance: float = 0.0, hfe: float = HFE
) -> float:
    """Output resistance of an emitter follower.

    Approximately r_e, which is the whole reason the stage exists: a few tens of ohms out of a
    device whose input resistance is tens of kilohms. A driving source's resistance divided by
    h_FE adds to it, which is what limits how much transformation one follower can do.
    """
    return intrinsic_emitter_resistance(collector_current) + source_resistance / hfe


def follower_input_resistance(
    collector_current: float, load: float, hfe: float = HFE
) -> float:
    """Resistance looking into a follower's base, with `load` on its emitter.

    The load, multiplied by h_FE. That multiplication is the stage's entire purpose and also its
    weakness: it is proportional to a parameter the course refuses to trust anywhere else.
    """
    return hfe * (intrinsic_emitter_resistance(collector_current) + load)


# ----------------------------------------------------------------------------------------
# The differential pair
#
# Single-ended output throughout, taken at one collector, because that is what feeds the next
# stage in the operational amplifier L10 builds. Taking both collectors doubles every gain here
# and leaves every ratio unchanged.
# ----------------------------------------------------------------------------------------


def diffpair_re(tail_current: float) -> float:
    """r_e of one side of a pair, which runs at half the tail current."""
    return intrinsic_emitter_resistance(tail_current / 2.0)


def diffpair_differential_gain(
    collector_resistor: float, tail_current: float, emitter_resistor: float = 0.0
) -> float:
    """Gain from a differential input to one collector.

    The common-emitter result with a factor of two in it, because a differential input of v is
    half of v on each base.
    """
    return -collector_resistor / (2.0 * (diffpair_re(tail_current) + emitter_resistor))


def diffpair_common_mode_gain(
    collector_resistor: float,
    tail_current: float,
    tail_resistance: float,
    emitter_resistor: float = 0.0,
) -> float:
    """Gain from a common-mode input to one collector.

    Both sides move together, so the tail resistance carries the sum of the two currents and acts
    like a degeneration resistor of twice its value. Everything the pair is for lives in making
    this number small, and the only lever is the tail.
    """
    return -collector_resistor / (
        2.0 * tail_resistance + diffpair_re(tail_current) + emitter_resistor
    )


def cmrr(
    collector_resistor: float,
    tail_current: float,
    tail_resistance: float,
    emitter_resistor: float = 0.0,
) -> float:
    """Common-mode rejection ratio, as a plain ratio rather than in decibels.

    The collector resistor cancels, which is worth noticing: CMRR is a property of the tail and
    the operating current, and no choice of load improves it.
    """
    return abs(
        diffpair_differential_gain(collector_resistor, tail_current, emitter_resistor)
        / diffpair_common_mode_gain(
            collector_resistor, tail_current, tail_resistance, emitter_resistor
        )
    )


def diffpair_transfer(differential_input: float, tail_current: float) -> float:
    """Difference between the two collector currents, for any differential input.

    The pair divides its tail current between two exponentials, and the algebra of that is a
    hyperbolic tangent:

        I_C1 - I_C2 = I_tail * tanh(v_d / 2 V_T)

    Two things follow that the small-signal model cannot say. The pair is **linear only over a few
    millivolts**, because tanh is, and it **hard-limits** rather than clipping softly, because tanh
    saturates. Both matter: the first is the distortion of an operational amplifier's input stage
    and the second is where its slew rate comes from.
    """
    return tail_current * math.tanh(differential_input / (2.0 * THERMAL_VOLTAGE))


def diffpair_linear_range(tolerance: float = 0.01) -> float:
    """Differential input at which the tanh has fallen `tolerance` below its tangent at zero.

    Independent of the tail current, because the tail scales the whole curve and cancels. That
    independence is worth noticing: biasing the pair harder buys gain and buys no linearity at all.
    """
    low, high = 0.0, 0.5
    for _ in range(200):
        middle = 0.5 * (low + high)
        slope = math.tanh(middle / (2.0 * THERMAL_VOLTAGE)) / (
            middle / (2.0 * THERMAL_VOLTAGE)
        )
        if slope > (1.0 - tolerance):
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def cmrr_differential(
    tail_current: float, tail_resistance: float, load_mismatch: float
) -> float:
    """Common-mode rejection when the output is the *difference* between the two collectors.

    A different circuit from `cmrr`, and much better. With a single-ended output the common-mode
    motion of the collector is the output, so the tail alone sets the rejection and matching does
    not enter at first order. Take both collectors and that motion is identical on each, so it
    subtracts out exactly when the halves match; what survives is the *mismatch* in the loads
    acting on it.

        CMRR_diff = 2 R_tail / (delta * r_e)

    So the two arrangements are limited by different things, and saying "the CMRR of a
    differential pair" without saying which output is being taken is not a statement about a
    circuit.
    """
    return (2.0 * tail_resistance) / (load_mismatch * diffpair_re(tail_current))


def diffpair_input_offset(
    load_mismatch: float,
    vbe_mismatch: float,
    collector_resistor: float,
    tail_current: float,
) -> float:
    """Input-referred offset voltage from a load mismatch and a V_BE mismatch.

    The V_BE mismatch appears at the input one for one, because it *is* an input voltage. The load
    mismatch appears at the output as delta * R_C * I_C and has to be divided by the gain to get
    back to the input, which is why an ordinary 1 per cent resistor pair costs about half of what
    a millivolt of device mismatch costs.
    """
    output = load_mismatch * collector_resistor * (tail_current / 2.0)
    referred = output / abs(
        diffpair_differential_gain(collector_resistor, tail_current)
    )
    return referred + abs(vbe_mismatch)


def diffpair_mirror_gain(tail_current: float, load: float) -> float:
    """Differential gain to a single output, with a current mirror as the active load.

    The factor of two in `diffpair_differential_gain` is the price of throwing one collector away.
    A mirror does not throw it away: it turns the idle side's current around and adds it to the
    output node, so the gain is the full common-emitter result rather than half of it.

    That doubling is a second, independent reason to use a mirror here, and it is separate from
    the large r_o that L07's correction is about. The lecture separates them.
    """
    return -load / diffpair_re(tail_current)


def loaded_gain(
    unloaded_gain: float, output_resistance: float, load_resistance: float
) -> float:
    """A stage's gain once the next stage's input resistance is hung on its output.

    This is not a correction term. In a multi-stage amplifier it is usually the dominant effect:
    a common-emitter stage with 50 kilohms of output resistance driving a following base of
    1.3 kilohms keeps 2.5 % of the gain it had on paper. Every follower in an operational
    amplifier is there to stop exactly that, and a gain budget computed without it is not wrong by
    a few percent, it is wrong by a factor of forty.
    """
    return unloaded_gain * load_resistance / (output_resistance + load_resistance)


def darlington_emitter_resistance(output_current: float, hfe: float = HFE) -> float:
    """Effective r_e of a Darlington pair, referred to its input.

    Exactly **twice** a single transistor's, and the reason is worth doing once. The output device
    runs at the output current and contributes r_e. The input device runs at the output device's
    *base* current, which is h_FE times smaller, so its own r_e is h_FE times larger; but it is
    seen through the second device's current gain, so it contributes r_e1/h_FE. The two h_FEs
    cancel and the answer is 2 V_T/I, whatever h_FE is.
    """
    del hfe
    return 2.0 * intrinsic_emitter_resistance(output_current)


def darlington_follower_gain(
    output_current: float, load: float, hfe: float = HFE
) -> float:
    """Voltage gain of a Darlington emitter follower, which is a little worse than a single one.

    Twice the intrinsic emitter resistance in the divider, so the shortfall from one is doubled.
    """
    effective = darlington_emitter_resistance(output_current, hfe)
    return load / (effective + load)


def darlington_input_resistance(
    output_current: float, load: float, hfe: float = HFE
) -> float:
    """Resistance looking into a Darlington pair's base, with `load` on the output emitter.

    Two transistors, so h_FE squared. That is the whole reason an output stage is not a single
    follower: 8 ohms multiplied by 50 is 400 ohms, which would flatten the stage driving it.

    The resistance the square multiplies is the pair's **effective** emitter resistance, which is
    twice one device's. Writing h_FE^2 (r_e + R) instead is out by 2.6 per cent into 8 ohms and by
    2 per cent into a following base, and it also breaks the identity that makes the expression
    derivable: this is h_FE times (r_e of the input device, plus the input resistance of the
    output device on its own).
    """
    return hfe * hfe * (darlington_emitter_resistance(output_current, hfe) + load)


# ----------------------------------------------------------------------------------------
# The capstone amplifier
#
# Four stages, all bipolar, on plus and minus fifteen volts. Every number below comes from a
# function already in this module; nothing new is modelled here, and that is the point of the
# lecture. What L10 adds is the *accounting*, and the accounting is where the eleven decibels go.
# ----------------------------------------------------------------------------------------

OPAMP_TAIL = 2.0e-3  # Input pair tail current.
OPAMP_BUFFER_CURRENT = 1.0e-3  # The Darlington buffer between stages one and two.
OPAMP_STAGE2_CURRENT = 1.0e-3  # The common-emitter voltage-gain stage.
OPAMP_IDLE = 0.120  # Output stage idle current.
OPAMP_LOAD = 8.0  # Loudspeaker.
OPAMP_CLOSED_LOOP = 20.0  # What the capstone is asked to deliver, closed loop.


def opamp_budget() -> dict[str, float]:
    """Every gain in the capstone amplifier, loaded and unloaded.

    Four stages: a mirror-loaded differential pair, a Darlington emitter follower that exists only
    so the pair is not loaded, a common-emitter stage with a current-source load, and a class-AB
    Darlington output.

    Two of the four have no voltage gain at all. They are more than half the transistor count.
    """
    pair_load = parallel(
        early_resistance(OPAMP_TAIL / 2.0), early_resistance(OPAMP_TAIL / 2.0)
    )
    stage2_load = parallel(
        early_resistance(OPAMP_STAGE2_CURRENT),
        early_resistance(OPAMP_STAGE2_CURRENT),
    )

    stage2_input = ce_input_resistance(OPAMP_STAGE2_CURRENT)
    buffer_input = darlington_input_resistance(OPAMP_BUFFER_CURRENT, stage2_input)
    output_input = darlington_input_resistance(OPAMP_IDLE, OPAMP_LOAD)

    stage1_unloaded = abs(diffpair_mirror_gain(OPAMP_TAIL, pair_load))
    stage1 = abs(loaded_gain(stage1_unloaded, pair_load, buffer_input))
    buffer = darlington_follower_gain(OPAMP_BUFFER_CURRENT, stage2_input)
    stage2_unloaded = abs(ce_gain(stage2_load, OPAMP_STAGE2_CURRENT))
    stage2 = abs(loaded_gain(stage2_unloaded, stage2_load, output_input))
    output = darlington_follower_gain(OPAMP_IDLE, OPAMP_LOAD)

    return {
        "pair_load": pair_load,
        "stage2_load": stage2_load,
        "stage2_input": stage2_input,
        "buffer_input": buffer_input,
        "output_input": output_input,
        "stage1_unloaded": stage1_unloaded,
        "stage1": stage1,
        "buffer": buffer,
        "stage2_unloaded": stage2_unloaded,
        "stage2": stage2,
        "output": output,
        "open_loop": stage1 * buffer * stage2 * output,
        "unloaded": stage1_unloaded * stage2_unloaded,
    }


def intrinsic_gain(early_voltage: float = EARLY_VOLTAGE) -> float:
    """Gain of a stage loaded by a current source, which does not depend on the current.

    Both of this amplifier's gain stages come to V_A/(2 V_T), and neither depends on how hard it
    is biased. The load is r_o against r_o, which falls as 1/I; the transconductance rises as I;
    the current cancels exactly.

    So **gain cannot be bought with supply current**, which is the opposite of the pattern L08
    established for followers, and it is why every stage in every operational amplifier lands
    within a few decibels of the same figure. The only lever is r_o, and the only way to raise
    that is a cascode.
    """
    return early_voltage / (2.0 * THERMAL_VOLTAGE)


def cascoded_intrinsic_gain(
    collector_current: float, hfe: float = HFE, early_voltage: float = EARLY_VOLTAGE
) -> float:
    """The same stage with cascoded loads, where the ceiling is h_FE times higher."""
    load = parallel(
        cascode_output_resistance(collector_current, hfe, early_voltage),
        cascode_output_resistance(collector_current, hfe, early_voltage),
    )
    return load / intrinsic_emitter_resistance(collector_current)


def opamp_buffer_worth() -> float:
    """Decibels of open-loop gain the Darlington buffer is worth, by removing it.

    The buffer has a voltage gain of 0.96 and is therefore the least impressive stage in the
    amplifier. Take it out and let the pair drive stage 3 directly, and the open loop falls by
    more than thirty decibels, which is more than any two-transistor gain stage in this course can
    deliver. That comparison is L10's whole argument and it is quoted in three figure captions, so
    it is computed here rather than written out as a literal.
    """
    budget = opamp_budget()
    without = (
        loaded_gain(
            budget["stage1_unloaded"], budget["pair_load"], budget["stage2_input"]
        )
        * budget["stage2"]
        * budget["output"]
    )
    return decibels(budget["open_loop"] / abs(without))


def opamp_output_worth() -> float:
    """The same measurement for the output stage: a single follower in place of the Darlington."""
    budget = opamp_budget()
    single = follower_gain(OPAMP_IDLE, OPAMP_LOAD)
    without = (
        budget["stage1"]
        * budget["buffer"]
        * abs(
            loaded_gain(
                budget["stage2_unloaded"],
                budget["stage2_load"],
                follower_input_resistance(OPAMP_IDLE, OPAMP_LOAD),
            )
        )
        * single
    )
    return decibels(budget["open_loop"] / without)


def opamp_open_loop_gain() -> float:
    """The capstone's open-loop gain, with every stage loaded by the next."""
    return opamp_budget()["open_loop"]


def opamp_unloaded_gain() -> float:
    """What the two gain stages would give if nothing loaded anything. It is not what you get."""
    return opamp_budget()["unloaded"]


def opamp_loading_loss() -> float:
    """Decibels lost to loading, which is the whole subject of L10."""
    return decibels(opamp_unloaded_gain()) - decibels(opamp_open_loop_gain())


# ----------------------------------------------------------------------------------------
# Feedback
# ----------------------------------------------------------------------------------------


def loop_gain(open_loop_gain: float, feedback_fraction: float) -> float:
    """The loop gain, which is what every feedback result is actually a function of."""
    return abs(open_loop_gain) * feedback_fraction


def closed_loop_gain(open_loop_gain: float, feedback_fraction: float) -> float:
    """Closed-loop gain of a negative-feedback amplifier."""
    return abs(open_loop_gain) / (1.0 + loop_gain(open_loop_gain, feedback_fraction))


def gain_error(open_loop_gain: float, feedback_fraction: float) -> float:
    """How far the closed-loop gain falls short of the ideal 1/beta, as a fraction.

    Returns a positive number: the shortfall. It is 1/(1 + T) to a very good approximation, which
    is the single most useful result in the whole of feedback, because it turns "how much open-loop
    gain do I need" into arithmetic.
    """
    ideal = 1.0 / feedback_fraction
    return (ideal - closed_loop_gain(open_loop_gain, feedback_fraction)) / ideal


# ----------------------------------------------------------------------------------------
# Output stages
# ----------------------------------------------------------------------------------------


def pushpull_output(
    input_voltage: float, bias: float = 0.0, vbe: float = VBE_ON, load: float = 8.0
) -> float:
    """Output of a complementary follower pair, as a function of its input.

    With no bias, neither device conducts until the input exceeds a diode drop, and the output
    sits at zero through a dead band two drops wide. That flat is crossover distortion, and it is
    worst exactly where a music signal spends most of its time.

    `bias` is the voltage forced between the two bases. At two diode drops the dead band closes.
    """
    del load
    half = bias / 2.0
    if input_voltage > vbe - half:
        return input_voltage - (vbe - half)
    if input_voltage < -(vbe - half):
        return input_voltage + (vbe - half)
    return 0.0


def quiescent_emitter_resistor(quiescent_current: float) -> float:
    """The emitter resistor that drops one thermal voltage at the quiescent current.

    The rule for an output stage: put 26 mV across each output emitter resistor, so
    that the resistor and the device's own r_e are equal and the pair is stable against thermal
    runaway without giving away efficiency.
    """
    return THERMAL_VOLTAGE / quiescent_current


def class_ab_bias(quiescent_current: float, emitter_resistor: float) -> float:
    """The voltage a class-AB bias generator has to produce for a stated idle current.

    Two base-emitter drops at the *idle current* plus the two resistor drops, and the first of
    those is the trap. The constant-drop model this course has used since L05 puts V_BE at 0.65 V,
    which is right at a milliamp and wrong by 130 mV at 120. Here that is not a few per cent, it
    is a factor of a hundred and sixty-eight, because what is being computed is a current from a
    voltage across a *junction* rather than across a resistor.
    """
    return 2.0 * (
        base_emitter_voltage(quiescent_current) + (quiescent_current * emitter_resistor)
    )


def class_ab_idle_current(bias: float, emitter_resistor: float) -> float:
    """The idle current a class-AB output stage settles at for a stated bias voltage.

    The inverse of `class_ab_bias`, and it has no closed form because the exponential and the
    linear term do not separate. Bisection in the logarithm, which is how the reader's solver
    finds it too.
    """
    low, high = 1.0e-12, 100.0
    for _ in range(200):
        middle = math.sqrt(low * high)
        if class_ab_bias(middle, emitter_resistor) < bias:
            low = middle
        else:
            high = middle
    return math.sqrt(low * high)


def class_ab_drift(quiescent_current: float, emitter_resistor: float) -> float:
    """Fractional change in idle current per degree, with the bias voltage held fixed.

    Both junctions drift by VBE_TEMPCO, so the bias generator is effectively 4 mV too generous per
    degree, and that surplus lands on 2(r_e + R_E). The emitter resistors divide it by the emitter
    factor, exactly as in L06, and the 26 mV rule makes that factor two.

    A bias generator mounted on the output devices' heatsink drifts the same way and cancels this
    to first order, which is the whole reason it is mounted there.
    """
    return (2.0 * abs(VBE_TEMPCO)) / (
        2.0
        * (intrinsic_emitter_resistance(quiescent_current) + emitter_resistor)
        * quiescent_current
    )


# ----------------------------------------------------------------------------------------
# Large-signal device behaviour
#
# What L05 needs to draw a characteristic curve, and what the reader's ael::device implements.
# ----------------------------------------------------------------------------------------

# The collector-emitter voltage below which a BJT stops behaving like a current source. Not a
# sharp edge in a real device; the course uses one because every design decision it informs is a
# decision about staying well clear of it.
VCE_SAT = 0.2

# The MOSFET the course uses. The threshold is representative; the transconductance parameter is
# then fixed by requiring g_m to come out at NMOS_GM_AT_1MA at 1 mA, so the square law here and
# the small-signal numbers elsewhere describe the same device rather than two different ones.
VTH = 2.0
K_N = 8.0e-3


def bjt_collector_current(
    base_current: float,
    vce: float,
    hfe: float = HFE,
    early_voltage: float = EARLY_VOLTAGE,
) -> float:
    """Collector current of a BJT, across saturation and the active region.

    In saturation the device is a resistor and the current is whatever the external circuit
    allows, so the model ramps linearly to the active-region value at VCE_SAT. That is a
    simplification and the lecture says so: a real device's knee is soft, and the ramp here is
    straight only because nothing in this course depends on its shape.
    """
    active = hfe * base_current * (1.0 + vce / early_voltage)
    if vce <= 0.0:
        return 0.0
    if vce < VCE_SAT:
        return active * vce / VCE_SAT
    return active


def mosfet_drain_current(
    vgs: float, vds: float, vth: float = VTH, k: float = K_N
) -> float:
    """Drain current of an n-channel MOSFET: cutoff, triode and saturation.

    The square law, which real short-channel devices have long since stopped obeying. It is right enough for the design decisions in this course
    and wrong enough that the lecture says where.
    """
    overdrive = vgs - vth
    if overdrive <= 0.0:
        return 0.0
    if vds < overdrive:
        return k * (overdrive * vds - 0.5 * vds * vds)
    return 0.5 * k * overdrive * overdrive


def mosfet_transconductance(
    drain_current: float, vth: float = VTH, k: float = K_N
) -> float:
    """g_m of a MOSFET at an operating current, from the square law.

    Proportional to the square root of the current, where a BJT's is proportional to the current
    itself. That single difference is why a MOSFET stage needs ten times the current for the same
    gain, and why the source factor sits at two where the emitter factor sits at ten.
    """
    del vth
    return math.sqrt(2.0 * k * drain_current)


def switch_base_resistor(
    drive_voltage: float,
    load_current: float,
    forced_beta: float = 10.0,
    # A saturated switch is sized from the textbook 0.7 V rather than from VBE_ON. The base is
    # being driven ten times harder than the active region needs, so the junction sits well above
    # the 0.65 V the small-signal stages use. Appendix A.4 and ael::device::bjt::baseResistor both
    # use 0.7, and this has to agree with them.
    vbe: float = 0.7,
) -> float:
    """The base resistor that saturates a switch carrying `load_current`.

    Sized from a forced beta rather than the device's h_FE, which is the whole trick: driving ten
    times the base current the active region would need is what guarantees saturation across every
    device in the bin and every temperature, and it costs almost nothing.
    """
    return (drive_voltage - vbe) / (load_current / forced_beta)


# ----------------------------------------------------------------------------------------
# Circuit theory
#
# What L01 and L02 need, and the first components the reader writes.
# ----------------------------------------------------------------------------------------


def divider(
    supply: float, upper: float, lower: float, load: float | None = None
) -> float:
    """Output of a resistive divider, with an optional load across the lower leg.

    The divider is the only circuit worth memorising, and the load is the reason it is worth
    understanding rather than memorising: hang a load on it and the lower leg becomes the parallel
    combination, so the ratio you designed is not the ratio you get.
    """
    bottom = lower if load is None else parallel(lower, load)
    return supply * bottom / (upper + bottom)


def divider_output_resistance(upper: float, lower: float) -> float:
    """Thevenin resistance of a divider, which is what decides how much a load disturbs it.

    The two legs in parallel, which surprises people: it does not depend on which way round they
    are, and it is always smaller than either.
    """
    return parallel(upper, lower)


def rc_corner(resistance: float, capacitance: float) -> float:
    """The corner frequency of an RC section, where the reactance equals the resistance."""
    return 1.0 / (2.0 * math.pi * resistance * capacitance)


def first_order_response(
    frequency: float, corner: float, highpass: bool = False
) -> complex:
    """Complex response of a first-order RC section at one frequency.

    Returned as a complex number rather than a magnitude, because the phase is half the content
    of a first-order response and dropping it is how a reader ends up surprised by an oscillator.
    """
    ratio = frequency / corner
    if highpass:
        return 1j * ratio / (1.0 + 1j * ratio)
    return 1.0 / (1.0 + 1j * ratio)


def capacitor_reactance(frequency: float, capacitance: float) -> float:
    """The magnitude of a capacitor's impedance, which falls as the frequency rises."""
    return 1.0 / (2.0 * math.pi * frequency * capacitance)


def inductor_reactance(frequency: float, inductance: float) -> float:
    """The magnitude of an inductor's impedance, which rises as the frequency rises."""
    return 2.0 * math.pi * frequency * inductance


def lc_resonance(inductance: float, capacitance: float) -> float:
    """The frequency at which an inductor and a capacitor have equal and opposite reactance.

    Equal in magnitude and opposite in sign, so in series they cancel to nothing and in parallel
    they add to infinity. Everything an LC circuit does follows from that one crossing.
    """
    return 1.0 / (2.0 * math.pi * math.sqrt(inductance * capacitance))


def series_rlc_q(resistance: float, inductance: float, capacitance: float) -> float:
    """Q of a series RLC, taking the output across the resistor.

    Q is the reactance at resonance divided by the resistance, and it is two things at once: how
    sharp the peak is, and how much the voltage across L and C overshoots the input. A Q of ten
    means ten times the input appears across the inductor, which is how a filter designed on paper
    destroys a capacitor in practice.
    """
    return math.sqrt(inductance / capacitance) / resistance


def bandpass_response(frequency: float, resonance: float, q: float) -> complex:
    """Complex response of a second-order bandpass, normalised to unity at resonance."""
    ratio = frequency / resonance
    return (1j * ratio / q) / (1.0 - ratio * ratio + 1j * ratio / q)


def cascaded_corner(resistance: float, capacitance: float) -> float:
    """The corner of two identical RC low-pass sections cascaded directly, with no buffer.

    Not the corner of one section, and not that corner divided by two. The second section loads
    the first, and the combined response has its half-power point at a frequency lower than the
    naive answer by a factor that falls out of solving the loaded network. This returns the real
    answer; the exercise is to predict it before running it.
    """
    single = rc_corner(resistance, capacitance)

    # The loaded pair has poles at (3 +/- sqrt(5))/2 times the single-section corner. The
    # half-power point is where the product of the two first-order magnitudes falls to 1/sqrt(2).
    low = single * (3.0 - math.sqrt(5.0)) / 2.0
    high = single * (3.0 + math.sqrt(5.0)) / 2.0

    def magnitude(frequency: float) -> float:
        return 1.0 / math.sqrt(
            (1.0 + (frequency / low) ** 2) * (1.0 + (frequency / high) ** 2)
        )

    lower_bound, upper_bound = single * 1e-3, single * 10.0
    for _ in range(200):
        middle = math.sqrt(lower_bound * upper_bound)
        if magnitude(middle) > 1.0 / math.sqrt(2.0):
            lower_bound = middle
        else:
            upper_bound = middle
    return math.sqrt(lower_bound * upper_bound)


def schmitt_thresholds(
    supply: float, upper: float, lower: float
) -> tuple[float, float]:
    """The two thresholds of a Schmitt trigger built from positive feedback on a comparator.

    Two numbers where a comparator has one, and the gap between them is the whole point: a
    comparator with a noisy input near its threshold chatters, and hysteresis wider than the noise
    is the only cure that does not slow the circuit down.
    """
    fraction = lower / (upper + lower)
    return (-supply * fraction, supply * fraction)


# ----------------------------------------------------------------------------------------
# The diode, and solving for it
# ----------------------------------------------------------------------------------------

SATURATION_CURRENT = 1e-14


def diode_current(
    voltage: float, saturation: float = SATURATION_CURRENT, ideality: float = 1.0
) -> float:
    """The diode equation, which is the first nonlinearity in the course."""
    return saturation * (math.exp(voltage / (ideality * THERMAL_VOLTAGE)) - 1.0)


def base_emitter_voltage(
    collector_current: float, saturation: float = SATURATION_CURRENT
) -> float:
    """The base-emitter voltage a BJT needs for a given collector current.

    The diode equation inverted, and the reason the familiar 0.7 V is not a constant: it is
    0.659 V at 1 mA and 0.718 V at 10 mA, sixty millivolts apart because that is what a decade
    costs.
    """
    return THERMAL_VOLTAGE * math.log((collector_current / saturation) + 1.0)


def diode_newton(
    supply: float,
    resistance: float,
    saturation: float = SATURATION_CURRENT,
    guess: float = 0.0,
    iterations: int = 12,
    limited: bool = True,
) -> list[float]:
    """Newton-Raphson on a diode in series with a resistor, returning every iterate.

    The whole of nonlinear circuit simulation is this loop: linearise at the current guess, solve
    the linear circuit, use the answer as the next guess.

    **Plain Newton-Raphson does not work here, and finding out why is the exercise.** Started at
    zero volts the diode looks like an open circuit, so the first solve puts the whole supply
    across it. At 5 V the exponential's slope is astronomical, and from there each iteration can
    only walk back by about one thermal voltage: roughly 170 steps to reach the answer, from a
    method advertised as quadratic.

    `limited` applies the damping every real simulator applies, which is to take the step in the
    logarithm rather than in the voltage whenever the step is large and increasing. That is not a
    trick to make the demonstration work; it is what SPICE does, for exactly this reason.

    Returns the sequence of diode voltages, starting with `guess`, so a figure can plot the path
    rather than only the answer.
    """
    voltage = guess
    path = [voltage]
    for _ in range(iterations):
        current = diode_current(voltage, saturation)
        conductance = (current + saturation) / THERMAL_VOLTAGE

        # The linearised diode is a conductance in parallel with a current source; solving the
        # resulting linear circuit for the node voltage is one line.
        equivalent = current - conductance * voltage
        proposed = (supply / resistance - equivalent) / (conductance + 1.0 / resistance)

        if limited and proposed > voltage:
            step = proposed - voltage
            if step > 2.0 * THERMAL_VOLTAGE:
                proposed = voltage + THERMAL_VOLTAGE * math.log(
                    1.0 + step / THERMAL_VOLTAGE
                )

        voltage = proposed
        path.append(voltage)
    return path


# ----------------------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------------------


def parallel(*resistances: float) -> float:
    """The parallel combination, which appears in almost every result in the course."""
    total = 0.0
    for resistance in resistances:
        if resistance <= 0.0:
            return 0.0
        total += 1.0 / resistance
    return 1.0 / total


def decibels(ratio: float) -> float:
    """A voltage ratio in decibels, taking the magnitude so an inverting gain is admissible."""
    return 20.0 * math.log10(abs(ratio))
