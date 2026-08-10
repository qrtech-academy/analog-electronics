"""L08 figures: followers, and the output stage they turn into.

The follower is the stage with no voltage gain, and the figures here are about why anyone builds
one anyway: it transforms impedance, by h_FE going in and down to r_e coming out.

FOLLOWER_INTO_LOAD is the figure that makes an output stage inevitable. A follower driving
8 ohms at 1 mA has a gain of 0.24, because r_e is 26 ohms and the load is 8. The only lever is
current: r_e falls as 1/I_C, so the gain climbs towards one as the stage is biased harder. An
output stage idles at about 120 mA, and this is why.

CROSSOVER is the other half. A complementary pair with no bias conducts nothing until the input
clears a diode drop, so the transfer curve has a flat dead band 1.3 V wide, centred exactly where
a music signal spends most of its time.
"""

from __future__ import annotations

import numpy as np
import schemdraw.elements as elm

import models
import style

SPEAKER = 8.0
QUIESCENT = 0.12


def _emitter_follower(drawing, ax) -> None:
    """The emitter follower, with what it does to impedance named at both ends."""
    ground_y = 1.0
    rail_y = 12.0
    base_x = 6.0
    base_y = 6.6

    leg = 0.7516666666666666
    rise = 0.6966666666666667

    transistor = elm.BjtNpn().at((base_x, base_y))
    load = elm.Resistor().at((base_x + leg, 4.4)).down().length(2.6)
    for element in (transistor, load):
        drawing.add(element)

    device_x = base_x + leg
    collector_y = base_y + rise
    emitter_y = base_y - rise

    drawing.add(elm.Vdd().at((device_x, rail_y)))
    style.wire(ax, (device_x, rail_y), (device_x, collector_y))
    style.wire(ax, (device_x, emitter_y), (device_x, 4.4))
    style.wire(ax, (device_x, 1.8), (device_x, ground_y))
    drawing.add(elm.Ground().at((device_x, ground_y)))

    drawing.add(elm.Dot(open=True).at((base_x - 3.6, base_y)))
    style.wire(ax, (base_x - 3.6, base_y), (base_x, base_y))
    style.text(ax, "v_in", (base_x - 3.6, base_y + 0.75), size=style.LABEL_SIZE)

    out_y = 3.6
    style.wire(ax, (device_x, out_y), (device_x + 3.4, out_y))
    drawing.add(elm.Dot().at((device_x, out_y)))
    drawing.add(elm.Dot(open=True).at((device_x + 3.4, out_y)))
    style.text(
        ax, "v_out", (device_x + 3.8, out_y), halign="left", size=style.LABEL_SIZE
    )

    style.text(ax, "R_E", (device_x - 0.8, 3.1), halign="right", size=style.LABEL_SIZE)
    style.text(
        ax, "Q1", (base_x - 0.5, base_y - 1.4), halign="right", size=style.LABEL_SIZE
    )

    style.callout(
        ax,
        "Looking in: h_FE times whatever\n"
        "hangs on the emitter. That multiplication\n"
        "is the whole point, and it is the one\n"
        "result in the course that leans on h_FE.",
        (base_x - 4.2, 9.6),
        (base_x - 1.6, base_y),
        halign="left",
    )
    style.callout(
        ax,
        "Looking back: r_e, plus whatever drives\n"
        "the base divided by h_FE. Tens of ohms out\n"
        "of a stage with tens of kilohms in.",
        (device_x + 4.2, 1.9),
        (device_x + 1.6, out_y),
        halign="left",
    )


def _follower_into_load(ax) -> None:
    """Follower gain into a loudspeaker, against the current it is biased at."""
    currents = np.logspace(-4.0, -0.3, 400)
    gain = [models.follower_gain(value, SPEAKER) for value in currents]

    ax.plot(
        currents * 1e3,
        gain,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label=f"{SPEAKER:.0f} ohm load",
    )
    ax.plot(
        currents * 1e3,
        [models.follower_gain(value, 1e3) for value in currents],
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="1 kilohm load",
    )

    ax.set_xscale("log")
    style.log_x_axis(ax, [0.1, 1, 10, 100, 500])
    ax.set_xlim(0.1, 500.0)
    ax.set_ylim(0.0, 1.05)

    style.style_axes(ax, "quiescent current (mA)", "voltage gain")
    style.plot_title(ax, "A follower into 8 ohms is a question about current")
    style.legend(ax, loc="lower center")

    style.marker(ax, QUIESCENT * 1e3, models.follower_gain(QUIESCENT, SPEAKER))
    style.annotate(
        ax,
        f"  {QUIESCENT * 1e3:.0f} mA: r_e = "
        f"{models.intrinsic_emitter_resistance(QUIESCENT):.2f} ohm,\n"
        f"  gain {models.follower_gain(QUIESCENT, SPEAKER):.3f}",
        (QUIESCENT * 1e3, models.follower_gain(QUIESCENT, SPEAKER) - 0.04),
        color=style.ACCENT_COLOR,
        ha="left",
        va="top",
    )
    style.annotate(
        ax,
        f"at 1 mA the gain into 8 ohms is only "
        f"{models.follower_gain(1e-3, SPEAKER):.2f}:\nr_e is "
        f"{models.intrinsic_emitter_resistance(1e-3):.0f} ohms and the load is "
        f"{SPEAKER:.0f}",
        (0.11, 0.76),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _crossover(ax) -> None:
    """The dead band a complementary pair has until it is biased out of it."""
    swing = np.linspace(-2.0, 2.0, 800)

    unbiased = [models.pushpull_output(value) for value in swing]
    biased = [
        models.pushpull_output(value, bias=2.0 * models.VBE_ON) for value in swing
    ]

    ax.plot(
        swing,
        unbiased,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="class B: no bias",
    )
    ax.plot(
        swing,
        biased,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="class AB: two diode drops of bias",
    )

    style.region(ax, -models.VBE_ON, models.VBE_ON, color=style.SHADE_COLOR)

    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.5, 1.5)
    style.style_axes(ax, "input (V)", "output (V)")
    style.plot_title(ax, "Crossover distortion, and the bias that removes it")
    style.legend(ax, loc="upper left")

    style.annotate(
        ax,
        f"neither device conducts across\n{2 * models.VBE_ON:.1f} V of input",
        (0.0, -1.35),
        color=style.ACCENT_COLOR,
        ha="center",
        va="bottom",
    )


EMITTER_FOLLOWER = style.Figure(_emitter_follower, canvas=(-6.0, 0.0, 22.0, 13.5))
FOLLOWER_INTO_LOAD = style.Plot(_follower_into_load, size=style.WIDE_SIZE)
CROSSOVER = style.Plot(_crossover)


def _class_ab(drawing, ax) -> None:
    """The class-AB output stage: two followers, two diodes, and two small resistors."""
    base_x = 6.0
    bias_x = 4.0
    upper_base_y = 8.4
    lower_base_y = 3.6
    out_y = 6.0

    leg = 0.7516666666666666
    rise = 0.6966666666666667
    device_x = base_x + leg

    upper = elm.BjtNpn().at((base_x, upper_base_y))
    lower = elm.BjtPnp().at((base_x, lower_base_y))
    upper_degeneration = elm.Resistor().at((device_x, 7.5)).down().length(1.5)
    lower_degeneration = elm.Resistor().at((device_x, 4.5)).up().length(1.5)
    speaker = elm.Resistor().at((device_x + 4.6, 5.4)).down().length(2.6)
    top_diode = elm.Diode().at((bias_x, upper_base_y)).down().length(2.4)
    bottom_diode = elm.Diode().at((bias_x, out_y)).down().length(2.4)
    for element in (
        upper,
        lower,
        upper_degeneration,
        lower_degeneration,
        speaker,
        top_diode,
        bottom_diode,
    ):
        drawing.add(element)

    drawing.add(elm.Vdd().at((device_x, 12.2)))
    style.wire(ax, (device_x, 12.2), (device_x, upper_base_y + rise))
    drawing.add(elm.Vss().at((device_x, 0.6)))
    style.wire(ax, (device_x, 0.6), (device_x, lower_base_y - rise))

    style.wire(ax, (device_x, upper_base_y - rise), (device_x, 7.5))
    style.wire(ax, (device_x, lower_base_y + rise), (device_x, 4.5))

    style.wire(ax, (bias_x, upper_base_y), (base_x, upper_base_y))
    style.wire(ax, (bias_x, lower_base_y), (base_x, lower_base_y))
    drawing.add(elm.Dot().at((bias_x, upper_base_y)))
    drawing.add(elm.Dot().at((bias_x, lower_base_y)))

    style.wire(ax, (device_x, out_y), (device_x + 4.6, out_y))
    drawing.add(elm.Dot().at((device_x, out_y)))
    style.wire(ax, (device_x + 4.6, out_y), (device_x + 4.6, 5.4))
    style.wire(ax, (device_x + 4.6, 2.8), (device_x + 4.6, 2.0))
    drawing.add(elm.Ground().at((device_x + 4.6, 2.0)))

    drawing.add(elm.Dot(open=True).at((bias_x - 3.0, upper_base_y)))
    style.wire(ax, (bias_x - 3.0, upper_base_y), (bias_x, upper_base_y))
    style.text(ax, "v_in", (bias_x - 3.0, upper_base_y + 0.8), size=style.LABEL_SIZE)

    style.text(
        ax,
        "Q1",
        (base_x - 0.3, upper_base_y - 0.8),
        halign="right",
        size=style.LABEL_SIZE,
    )
    style.text(
        ax,
        "Q2",
        (base_x - 0.3, lower_base_y + 0.8),
        halign="right",
        size=style.LABEL_SIZE,
    )
    style.text(ax, "0.22", (device_x + 0.5, 6.75), halign="left", size=style.LABEL_SIZE)
    style.text(ax, "0.22", (device_x + 0.5, 5.25), halign="left", size=style.LABEL_SIZE)
    style.text(ax, "8 ohm", (device_x + 5.2, 4.1), halign="left", size=style.LABEL_SIZE)

    style.callout(
        ax,
        "Two drops of bias, and the dead band closes.\n"
        "These diodes must sit on the same heatsink as\n"
        "Q1 and Q2. They are not setting a voltage, they\n"
        "are tracking one that moves 2 mV per degree.",
        (bias_x - 8.6, 1.2),
        (bias_x - 0.35, out_y),
        halign="left",
    )
    style.callout(
        ax,
        "26 mV across each at the idle current, so\n"
        "R_E equals r_e and the emitter factor is 2.\n"
        "Half the thermal sensitivity, and 0.22 ohm\n"
        "in series with 8 ohms costs 2.7 per cent.",
        (device_x + 2.4, 10.6),
        (device_x + 0.35, 6.75),
        halign="left",
    )


def _impedance_chain(ax) -> None:
    """What an 8 ohm load does to a stage's gain, and what each fix recovers."""
    unloaded = abs(models.ce_gain(10.0e3, 1.0e-3, 234.0))
    source = models.ce_output_resistance(10.0e3, 1.0e-3, 234.0)

    loads = np.logspace(0.0, 6.0, 500)
    ax.plot(
        loads,
        [100.0 * value / (source + value) for value in loads],
        color=style.MUTED_COLOR,
        linewidth=style.CURVE_WIDTH,
    )

    follower = models.follower_input_resistance(QUIESCENT, SPEAKER)
    darlington = models.darlington_input_resistance(QUIESCENT, SPEAKER)
    weak = models.darlington_input_resistance(QUIESCENT, SPEAKER, 20.0)
    strong = models.darlington_input_resistance(QUIESCENT, SPEAKER, 200.0)

    style.region(ax, weak, strong, color=style.SHADE_COLOR)

    # Unlabelled on purpose: each of these three points already carries a style.annotate below,
    # and a marker label on top of it overlaps the text it duplicates.
    for load in (SPEAKER, follower, darlington):
        style.marker(ax, load, 100.0 * load / (source + load))

    ax.set_xscale("log")
    style.log_x_axis(ax, [1, 10, 100, 1e3, 1e4, 1e5, 1e6])
    ax.set_xlim(1.0, 1.0e6)
    ax.set_ylim(0.0, 105.0)

    style.style_axes(
        ax, "resistance the driving stage sees (ohm)", "gain kept (per cent)"
    )
    style.plot_title(ax, "An 8 ohm load, and what it takes to survive one")

    style.annotate(
        ax,
        f"  8 ohm direct: {100.0 * SPEAKER / (source + SPEAKER):.2f} %\n"
        f"  of a gain of {unloaded:.0f}",
        (SPEAKER, 12.0),
        color=style.ACCENT_COLOR,
        ha="left",
        va="bottom",
    )
    style.annotate(
        ax,
        f"  one follower: {100.0 * follower / (source + follower):.0f} %",
        (follower, 4.0),
        color=style.ACCENT_COLOR,
        ha="left",
        va="center",
    )
    style.annotate(
        ax,
        f"a Darlington: {100.0 * darlington / (source + darlington):.0f} %",
        (darlington * 1.5, 72.0),
        color=style.ACCENT_COLOR,
        ha="left",
        va="top",
    )
    style.annotate(
        ax,
        "the shaded band is h_FE\nfrom 20 to 200: the answer\nspans 25 to 97 per cent",
        (weak * 0.75, 96.0),
        color=style.MUTED_COLOR,
        ha="right",
        va="top",
    )


CLASS_AB = style.Figure(_class_ab, canvas=(-5.0, 0.0, 22.0, 13.5))
IMPEDANCE_CHAIN = style.Plot(_impedance_chain, size=style.WIDE_SIZE)
