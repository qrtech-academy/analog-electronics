"""L09 figures: the differential pair, and what decides its common-mode rejection.

The pair is the first circuit in the course that is built to *reject* rather than amplify, and the
figures are about where that rejection comes from. It is not the matching of the two halves, which
is what everyone guesses; it is the tail.

CMRR_AGAINST_TAIL is the argument. The collector resistor cancels out of the ratio entirely, so no
choice of load improves rejection. The only lever is the resistance the tail presents, and that is
why every real pair is biased by a current source rather than a resistor: a resistor big enough to
give 80 dB would need a supply nobody has.
"""

from __future__ import annotations

import numpy as np
import schemdraw.elements as elm

import models
import style

TAIL_CURRENT = 2e-3
R_COLLECTOR = 10e3


def _differential_pair(drawing, ax) -> None:
    """The pair, its tail source, and the two inputs."""
    ground_y = 1.0
    rail_y = 13.0
    tail_y = 4.4

    leg = 0.7516666666666666
    rise = 0.6966666666666667

    left_base_x = 5.0
    right_base_x = 13.0
    base_y = 7.4

    # The right device is reversed so the two face each other and the tail node is between them.
    left = elm.BjtNpn().at((left_base_x, base_y))
    right = elm.BjtNpn().at((right_base_x, base_y)).reverse()
    left_load = elm.Resistor().at((left_base_x + leg, rail_y)).down().length(2.6)
    right_load = elm.Resistor().at((right_base_x + leg, rail_y)).down().length(2.6)
    tail = elm.SourceI().at((9.0, tail_y)).down().length(2.4)

    for element in (left, right, left_load, right_load, tail):
        drawing.add(element)

    left_x = left_base_x + leg
    # reverse() leaves the device column on the same side as an un-reversed part and moves
    # only the base, so the column is base_x + leg here too. Measured, not assumed.
    right_x = right_base_x + leg
    coll_y = base_y + rise
    emit_y = base_y - rise

    # Supply rail and the two loads.
    style.wire(ax, (left_x, rail_y), (right_x, rail_y))
    style.text(ax, "+V_CC", (9.0, rail_y + 0.7), size=style.LABEL_SIZE)
    style.wire(ax, (left_x, rail_y - 2.6), (left_x, coll_y))
    style.wire(ax, (right_x, rail_y - 2.6), (right_x, coll_y))

    # The two emitters onto one node, and the tail source below it.
    style.wire(ax, (left_x, emit_y), (left_x, tail_y))
    style.wire(ax, (right_x, emit_y), (right_x, tail_y))
    style.wire(ax, (left_x, tail_y), (right_x, tail_y))
    drawing.add(elm.Dot().at((9.0, tail_y)))
    style.wire(ax, (9.0, tail_y - 2.4), (9.0, ground_y))
    drawing.add(elm.Ground().at((9.0, ground_y)))

    # Inputs.
    drawing.add(elm.Dot(open=True).at((left_base_x - 3.4, base_y)))
    style.wire(ax, (left_base_x - 3.4, base_y), (left_base_x, base_y))
    style.text(ax, "v_1", (left_base_x - 3.4, base_y + 0.75), size=style.LABEL_SIZE)

    right_tie_x = right_base_x + 1.5
    drawing.add(elm.Dot(open=True).at((right_tie_x + 3.4, base_y)))
    style.wire(ax, (right_tie_x, base_y), (right_tie_x + 3.4, base_y))
    style.text(ax, "v_2", (right_tie_x + 3.4, base_y + 0.75), size=style.LABEL_SIZE)

    # Output, taken single-ended at the left collector, which is what feeds the next stage.
    out_y = 10.0
    style.wire(ax, (left_x, out_y), (left_x - 3.4, out_y))
    drawing.add(elm.Dot().at((left_x, out_y)))
    drawing.add(elm.Dot(open=True).at((left_x - 3.4, out_y)))
    style.text(
        ax, "v_out", (left_x - 3.8, out_y), halign="right", size=style.LABEL_SIZE
    )

    style.text(
        ax, "R_C", (left_x - 0.8, rail_y - 1.3), halign="right", size=style.LABEL_SIZE
    )
    style.text(
        ax, "R_C", (right_x + 0.8, rail_y - 1.3), halign="left", size=style.LABEL_SIZE
    )
    style.text(ax, "Q1", (left_x - 0.6, 6.0), halign="right", size=style.LABEL_SIZE)
    style.text(ax, "Q2", (right_x + 0.6, 6.0), halign="left", size=style.LABEL_SIZE)

    style.callout(
        ax,
        f"The tail carries both currents, so a common-mode\n"
        f"move sees it as a degeneration resistor of twice its\n"
        f"value. Everything the pair is for lives in making this\n"
        f"resistance large, and a resistor cannot get there.",
        (20.0, 3.0),
        (9.55, tail_y - 1.2),
    )
    style.callout(
        ax,
        f"Each side runs at half the tail current, so a "
        f"{TAIL_CURRENT * 1e3:.0f} mA\n"
        f"tail gives r_e = {models.diffpair_re(TAIL_CURRENT):.0f} ohms. "
        f"The differential gain is the\n"
        f"common-emitter result with a two in it: "
        f"{abs(models.diffpair_differential_gain(R_COLLECTOR, TAIL_CURRENT)):.0f}.",
        (20.0, 11.4),
        (right_x + 0.4, coll_y + 0.6),
    )


def _cmrr_against_tail(ax) -> None:
    """Common-mode rejection against the resistance the tail presents."""
    tails = np.logspace(3.0, 7.0, 400)

    rejection = [
        models.decibels(models.cmrr(R_COLLECTOR, TAIL_CURRENT, value))
        for value in tails
    ]

    ax.plot(
        tails,
        rejection,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
    )

    ax.set_xscale("log")
    style.log_x_axis(ax, [1e3, 1e4, 1e5, 1e6, 1e7])
    ax.set_xticklabels(["1k", "10k", "100k", "1M", "10M"])
    ax.set_xlim(1e3, 1e7)
    ax.set_ylim(20.0, 110.0)

    style.style_axes(ax, "resistance the tail presents (ohm)", "CMRR (dB)")
    style.plot_title(ax, "Rejection is a property of the tail, and nothing else")

    # What a plain resistor can reach, given the supply it would need.
    resistor = 50e3
    style.marker(
        ax, resistor, models.decibels(models.cmrr(R_COLLECTOR, TAIL_CURRENT, resistor))
    )
    style.annotate(
        ax,
        f"  a {resistor / 1e3:.0f}k resistor, which already drops\n"
        f"  {resistor * TAIL_CURRENT:.0f} V at {TAIL_CURRENT * 1e3:.0f} mA",
        # Below the curve, which is empty for every tail above about 10k.
        (5.5e4, 62.0),
        color=style.ACCENT_COLOR,
        ha="left",
        va="top",
    )

    mirror = models.early_resistance(TAIL_CURRENT / 2.0)
    style.marker(
        ax,
        mirror,
        models.decibels(models.cmrr(R_COLLECTOR, TAIL_CURRENT, mirror)),
        color=style.ACCENT_COLOR_3,
    )
    style.annotate(
        ax,
        f"  a current source: its r_o is {mirror / 1e3:.0f}k\n"
        f"  and it drops almost nothing",
        # Above the curve and to its left, the only band clear of it on this side.
        (9e4, 84.0),
        color=style.ACCENT_COLOR_3,
        ha="right",
        va="bottom",
    )

    style.annotate(
        ax,
        "R_C cancels out of the ratio: no choice of load\nchanges any point on this curve",
        (1.3e3, 103.0),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


DIFFERENTIAL_PAIR = style.Figure(_differential_pair, canvas=(0.0, 0.0, 32.0, 14.6))
CMRR_AGAINST_TAIL = style.Plot(_cmrr_against_tail, size=style.WIDE_SIZE)


def _mirror_loaded_pair(drawing, ax) -> None:
    """The pair with a current-mirror load, which is where both factors of two are won."""
    rail_y = 12.6
    mirror_y = 9.4
    pair_y = 4.6
    tail_y = 2.6

    leg = 0.7516666666666666
    rise = 0.6966666666666667

    left_x = 3.0
    right_x = 5.0
    left_column = left_x + leg
    right_column = right_x + leg

    # Devices before wires, and the reversed parts measured rather than assumed: reverse() leaves
    # the column at x + 0.752 and moves the base lead to x + 1.503.
    reference = elm.BjtPnp().at((left_x, mirror_y)).reverse()
    output = elm.BjtPnp().at((right_x, mirror_y))
    first = elm.BjtNpn().at((left_x, pair_y))
    second = elm.BjtNpn().at((right_x, pair_y)).reverse()
    tail = elm.SourceI().at((left_column + leg, tail_y)).down().length(1.6)
    for element in (reference, output, first, second, tail):
        drawing.add(element)

    # The mirror: emitters to the rail, bases tied, the left one diode-connected.
    style.wire(ax, (left_column - 1.2, rail_y), (right_column + 1.2, rail_y))
    style.wire(ax, (left_column, rail_y), (left_column, mirror_y + rise))
    style.wire(ax, (right_column, rail_y), (right_column, mirror_y + rise))
    style.text(ax, "+V_CC", (left_column - 1.2, rail_y + 0.7), halign="left")

    tie_left = left_x + (2.0 * leg)
    style.wire(ax, (tie_left, mirror_y), (right_x, mirror_y))
    style.wire(ax, (tie_left, mirror_y), (tie_left, mirror_y - rise))
    style.wire(ax, (tie_left, mirror_y - rise), (left_column, mirror_y - rise))
    drawing.add(elm.Dot().at((left_column, mirror_y - rise)))

    # The two collector nets.
    style.wire(ax, (left_column, mirror_y - rise), (left_column, pair_y + rise))
    style.wire(ax, (right_column, mirror_y - rise), (right_column, pair_y + rise))

    # The tail.
    style.wire(ax, (left_column, pair_y - rise), (left_column, tail_y))
    style.wire(ax, (left_column, tail_y), (right_column, tail_y))
    style.wire(ax, (right_column, tail_y), (right_column, pair_y - rise))
    drawing.add(elm.Dot().at((left_column + leg, tail_y)))
    style.wire(ax, (left_column + leg, tail_y - 1.6), (left_column + leg, 0.9))
    drawing.add(elm.Ground().at((left_column + leg, 0.9)))

    # Inputs and the single-ended output.
    drawing.add(elm.Dot(open=True).at((left_x - 2.4, pair_y)))
    style.wire(ax, (left_x - 2.4, pair_y), (left_x, pair_y))
    style.text(ax, "v+", (left_x - 2.4, pair_y + 0.8), size=style.LABEL_SIZE)

    second_base = right_x + (2.0 * leg)
    style.wire(ax, (second_base, pair_y), (second_base + 3.4, pair_y))
    drawing.add(elm.Dot(open=True).at((second_base + 3.4, pair_y)))
    style.text(
        ax,
        "v-",
        (second_base + 3.4, pair_y + 0.8),
        halign="right",
        size=style.LABEL_SIZE,
    )

    out_y = 7.2
    drawing.add(elm.Dot().at((right_column, out_y)))
    style.wire(ax, (right_column, out_y), (second_base + 3.4, out_y))
    drawing.add(elm.Dot(open=True).at((second_base + 3.4, out_y)))
    style.text(
        ax, "v_out", (second_base + 3.8, out_y), halign="left", size=style.LABEL_SIZE
    )

    style.text(
        ax, "Q1", (left_x - 0.3, pair_y - 0.9), halign="right", size=style.LABEL_SIZE
    )
    style.text(
        ax,
        "Q2",
        (second_base + 0.3, pair_y - 0.9),
        halign="left",
        size=style.LABEL_SIZE,
    )
    style.text(
        ax, "M1", (left_x - 0.3, mirror_y + 0.9), halign="right", size=style.LABEL_SIZE
    )
    style.text(
        ax,
        "M2",
        (right_column + 0.4, mirror_y + 0.9),
        halign="left",
        size=style.LABEL_SIZE,
    )

    mirror_load = models.parallel(
        models.early_resistance(TAIL_CURRENT / 2.0),
        models.early_resistance(TAIL_CURRENT / 2.0),
    )
    style.callout(
        ax,
        "M1 measures Q1's current and M2 copies it into\n"
        "the output node, so the left half is added rather\n"
        "than discarded. That is the factor of two a\n"
        "single-ended resistive output throws away.",
        (13.6, 11.0),
        (right_column + 0.35, mirror_y - rise - 0.4),
        halign="left",
    )
    style.callout(
        ax,
        f"And the load is now r_o in parallel with r_o,\n"
        f"{mirror_load / 1e3:.0f} kilohm rather than 10. Gain "
        f"{abs(models.diffpair_mirror_gain(TAIL_CURRENT, mirror_load)):.0f} against\n"
        f"{abs(models.diffpair_differential_gain(R_COLLECTOR, TAIL_CURRENT)):.0f}: "
        f"a factor of five from the load and\n"
        f"a factor of two from the mirror. Two mechanisms.",
        (13.6, 5.4),
        (right_column + 0.35, out_y),
        halign="left",
    )


def _diffpair_transfer(ax) -> None:
    """The pair's large-signal transfer, which the small-signal model cannot see."""
    swing = np.linspace(-0.150, 0.150, 800)
    difference = [models.diffpair_transfer(value, TAIL_CURRENT) for value in swing]

    ax.plot(
        swing * 1e3,
        np.array(difference) * 1e3,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="I_C1 - I_C2",
    )

    slope = TAIL_CURRENT / (2.0 * models.THERMAL_VOLTAGE)
    ax.plot(
        swing * 1e3,
        swing * slope * 1e3,
        color=style.MUTED_COLOR,
        linewidth=style.CONSTRUCTION_WIDTH,
        linestyle=(0, (5, 3)),
        label="the small-signal tangent",
    )

    linear = models.diffpair_linear_range(0.01)
    style.region(ax, -linear * 1e3, linear * 1e3, color=style.SHADE_COLOR)

    ax.set_xlim(-150.0, 150.0)
    ax.set_ylim(-TAIL_CURRENT * 1.15e3, TAIL_CURRENT * 1.15e3)
    style.style_axes(ax, "differential input (mV)", "difference current (mA)")
    style.plot_title(ax, "The pair is linear over nine millivolts")
    style.legend(ax, loc="upper left")

    style.annotate(
        ax,
        f"linear to 1 per cent\nwithin {linear * 1e3:.1f} mV,\nand that figure does\n"
        f"not depend on the tail",
        (0.0, -TAIL_CURRENT * 0.35e3),
        color=style.ACCENT_COLOR,
        ha="center",
        va="top",
    )
    style.annotate(
        ax,
        f"{100.0 * models.diffpair_transfer(0.1, TAIL_CURRENT) / TAIL_CURRENT:.0f} per cent "
        f"switched\nat 100 mV: the pair\nhard-limits, and that\nis where slew rate\ncomes from",
        (60.0, -TAIL_CURRENT * 0.15e3),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


MIRROR_LOADED_PAIR = style.Figure(_mirror_loaded_pair, canvas=(0.0, 0.0, 24.0, 13.5))
DIFFPAIR_TRANSFER = style.Plot(_diffpair_transfer, size=style.WIDE_SIZE)
