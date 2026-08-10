"""L05 figures: the transistor as a device, and as a switch.

The approach throughout: as little semiconductor physics as possible. A BJT is an exponential
with a current gain and a saturation voltage; a MOSFET is a square law with a threshold. No
depletion regions, no carrier transport.

BJT_OUTPUT carries the switch design on top of the device curves, because the two belong together:
the load line is the external circuit, the family of curves is the device, and a switch is the
statement that only the two ends of that line are ever used.

GM_COMPARISON is the figure the whole MOSFET half of the course leans on. A BJT's transconductance
is proportional to its current; a MOSFET's is proportional to the square root of it. At 1 mA the
two differ by about ten, which is exactly why the source factor sits near two where the emitter
factor sits near ten. This is where that correspondence comes from.

Two things that figure is blind to, both of which the lecture states:

* Below about 11 microamps the square law says the two devices have equal transconductance, and
  the curves cross. A real MOSFET does not follow the square law there; in weak inversion it
  conducts exponentially and its transconductance approaches I/(n kT/q), which is the BJT's
  result divided by a factor of one to two. So the curves converging is right and the crossing is
  an artifact of the model.
* The MOSFET's transconductance also depends on W/L, which this course holds fixed. A wide enough
  device beats the BJT at any current; it just costs area, and on a board it costs a bigger part.
"""

from __future__ import annotations

import numpy as np
import schemdraw.elements as elm

import models
import style

# The switch the lecture designs: 5 V logic driving a 100 mA load from a 5 V rail.
DRIVE = 5.0
SUPPLY = 5.0
LOAD_CURRENT = 0.1
R_LOAD = SUPPLY / LOAD_CURRENT
R_BASE = models.nearest_e12(models.switch_base_resistor(DRIVE, LOAD_CURRENT))


def _bjt_output(ax) -> None:
    """The output characteristics, with the switch's load line drawn across them."""
    vce = np.linspace(0.0, 6.0, 600)

    # A family of base currents spanning the load line's useful range.
    for base_current in [0.5e-3, 1.0e-3, 1.5e-3, 2.0e-3, 2.5e-3]:
        current = [
            models.bjt_collector_current(base_current, value) * 1e3 for value in vce
        ]
        ax.plot(
            vce,
            current,
            color=style.LINE_COLOR,
            linewidth=style.CURVE_WIDTH * 0.8,
            zorder=3,
        )
        style.annotate(
            ax,
            f"I_B = {base_current * 1e3:.1f} mA",
            (6.05, current[-1]),
            color=style.MUTED_COLOR,
            ha="left",
            va="center",
        )

    # The load line: the external circuit, which knows nothing about the device.
    ax.plot(
        [0.0, SUPPLY],
        [SUPPLY / R_LOAD * 1e3, 0.0],
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        zorder=4,
        label=f"load line, {R_LOAD:.0f} ohm from {SUPPLY:.0f} V",
    )

    style.region(ax, 0.0, models.VCE_SAT, color=style.SHADE_COLOR_2)

    # Headroom above the highest curve, so the legend and the region label have their own band
    # rather than sitting on the 2.5 mA trace.
    ax.set_xlim(0.0, 7.1)
    ax.set_ylim(0.0, 172.0)
    style.style_axes(ax, "collector-emitter voltage (V)", "collector current (mA)")
    style.plot_title(ax, "A switch uses only the two ends of the load line")
    style.legend(ax, loc="upper center")
    style.annotate(
        ax, "saturation", (0.28, 146.0), color=style.MUTED_COLOR, ha="left", va="center"
    )

    # The two states a switch actually occupies.
    ax.plot(
        [SUPPLY],
        [0.0],
        marker="o",
        markersize=7,
        color=style.ACCENT_COLOR,
        zorder=6,
        linestyle="none",
    )
    ax.plot(
        [models.VCE_SAT],
        [LOAD_CURRENT * 1e3],
        marker="o",
        markersize=7,
        color=style.ACCENT_COLOR,
        zorder=6,
        linestyle="none",
    )
    # The point about what lies between the two markers is made by the title and belongs to the
    # appendix in full. A figure carrying two sentences of prose stops being a figure.
    style.annotate(
        ax, "off", (4.88, 5.0), color=style.ACCENT_COLOR, ha="right", va="bottom"
    )
    style.annotate(
        ax,
        f"on: saturated, {LOAD_CURRENT * 1e3:.0f} mA",
        (0.55, 104.0),
        color=style.ACCENT_COLOR,
        ha="left",
    )


def _mosfet_regions(ax) -> None:
    """The MOSFET's output characteristics, and the boundary between its two regions."""
    vds = np.linspace(0.0, 5.0, 600)

    for vgs in (2.4, 2.6, 2.8, 3.0, 3.2):
        current = [models.mosfet_drain_current(vgs, value) * 1e3 for value in vds]
        ax.plot(
            vds,
            current,
            color=style.LINE_COLOR,
            linewidth=style.CURVE_WIDTH * 0.8,
            zorder=3,
        )
        style.annotate(
            ax,
            f"V_GS = {vgs:.1f} V",
            (5.05, current[-1]),
            color=style.MUTED_COLOR,
            ha="left",
            va="center",
        )

    # The locus V_DS = V_GS - V_TH, which is where each curve stops rising and flattens.
    overdrive = np.linspace(0.0, 1.4, 200)
    ax.plot(
        overdrive,
        0.5 * models.K_N * overdrive**2 * 1e3,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        zorder=4,
    )

    ax.set_xlim(0.0, 6.7)
    ax.set_ylim(0.0, 8.5)
    style.style_axes(ax, "drain-source voltage (V)", "drain current (mA)")
    style.plot_title(ax, f"The MOSFET, with V_TH = {models.VTH:.0f} V")

    # No legend: the only series worth naming is the boundary, and a legend box in the one corner
    # this figure leaves empty landed on the 2.4 V curve.
    style.annotate(
        ax,
        " V_DS = V_GS - V_TH",
        (1.42, 7.9),
        color=style.ACCENT_COLOR,
        ha="left",
        va="center",
    )
    style.annotate(ax, "triode", (0.15, 6.4), color=style.MUTED_COLOR, ha="left")
    style.annotate(ax, "saturation", (2.4, 6.6), color=style.MUTED_COLOR, ha="left")


def _gm_comparison(ax) -> None:
    """Transconductance against operating current, for both devices.

    The reason the source factor is two where the emitter factor is ten.
    """
    current = np.logspace(-5.0, -2.0, 400)

    bjt = [models.transconductance(value) * 1e3 for value in current]
    mosfet = [models.mosfet_transconductance(value) * 1e3 for value in current]

    ax.plot(
        current * 1e3,
        bjt,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="BJT: g_m = I_C / 26 mV",
    )
    ax.plot(
        current * 1e3,
        mosfet,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        label="MOSFET: g_m = sqrt(2 k I_D)",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    style.log_x_axis(ax, [0.01, 0.1, 1, 10])
    ax.set_xlim(0.01, 10.0)
    ax.set_ylim(0.1, 500.0)
    ax.set_yticks([0.1, 1, 10, 100])
    ax.set_yticklabels(["0.1", "1", "10", "100"])

    style.style_axes(ax, "operating current (mA)", "transconductance (mS)")
    style.plot_title(ax, "Why a MOSFET stage needs more current")
    style.legend(ax, loc="upper left")

    # The ratio goes as the square root of the current, so the BJT's advantage grows with current
    # and vanishes below about 11 microamps. Getting the direction of that backwards is easy and
    # the figure would still look plausible, which is why the crossing is marked rather than
    # described.
    ratio = models.transconductance(1e-3) / models.mosfet_transconductance(1e-3)
    crossover = models.THERMAL_VOLTAGE**2 * 2.0 * models.K_N

    # The gap between the curves at 1 mA is the whole message, and it is a large piece of empty
    # figure. Measuring it in place beats a sentence describing it: earlier drafts put the ratio
    # and the crossing in prose and the two blocks of text overlapped each other.
    top = models.transconductance(1e-3) * 1e3
    bottom = models.mosfet_transconductance(1e-3) * 1e3
    ax.annotate(
        "",
        xy=(1.0, top),
        xytext=(1.0, bottom),
        arrowprops={
            "arrowstyle": "<->",
            "color": style.ACCENT_COLOR_3,
            "linewidth": style.ACCENT_WIDTH,
            "shrinkA": 0,
            "shrinkB": 0,
        },
        zorder=6,
    )
    style.annotate(
        ax,
        f" {ratio:.0f}x at 1 mA",
        (1.0, (top * bottom) ** 0.5),
        color=style.ACCENT_COLOR_3,
        ha="left",
        va="center",
    )

    # The crossing is an artifact of the square law, not a property of the devices; the docstring
    # says why, and the lecture repeats it.
    ax.plot(
        [crossover * 1e3],
        [models.transconductance(crossover) * 1e3],
        marker="o",
        markersize=6,
        color=style.MUTED_COLOR,
        zorder=6,
        linestyle="none",
    )
    style.annotate(
        ax,
        f" equal at {crossover * 1e6:.0f} uA",
        (crossover * 1e3, models.transconductance(crossover) * 1e3 * 0.82),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _switch(drawing, ax) -> None:
    """The switch the load line above describes."""
    base_y = 5.0
    stage_x = 6.0
    device_x = stage_x + 0.7516666666666666
    collector_y = base_y + 0.6966666666666667
    emitter_y = base_y - 0.6966666666666667
    rail_y = 11.0
    ground_y = 1.0

    # Devices before wires; see diagrams/README.md.
    transistor = elm.BjtNpn().at((stage_x, base_y))
    load = elm.Resistor().at((device_x, rail_y)).down().length(2.6)
    base = elm.Resistor().at((1.4, base_y)).right().length(2.6)

    for element in (transistor, load, base):
        drawing.add(element)

    style.text(
        ax,
        f"{R_LOAD:.0f}",
        (device_x - 0.8, rail_y - 1.3),
        halign="right",
        size=style.LABEL_SIZE,
    )
    style.text(ax, f"{R_BASE:.0f}", (2.7, base_y + 0.9), size=style.LABEL_SIZE)

    style.wire(ax, (device_x, rail_y - 2.6), (device_x, collector_y))
    style.wire(ax, (device_x, emitter_y), (device_x, ground_y))
    style.wire(ax, (4.0, base_y), (stage_x, base_y))
    drawing.add(elm.Ground().at((device_x, ground_y)))

    # The supply, and the input the logic drives.
    style.wire(ax, (device_x, rail_y), (device_x, rail_y))
    drawing.add(elm.Vdd().at((device_x, rail_y)).label(f"{SUPPLY:.0f} V"))
    drawing.add(elm.Dot(open=True).at((1.4, base_y)))
    style.text(
        ax, f"{DRIVE:.0f} V logic", (1.1, base_y), halign="right", size=style.LABEL_SIZE
    )

    # This one sits below its resistor rather than out to the right with the others. A leader
    # coming in from the right at base height would cross the transistor, and one coming in from
    # below-right would cross the emitter wire on its way to ground; the column at device_x runs
    # the full height of the figure, so the only clear approach is straight up.
    #
    # The arrow is drawn from the text anchor and the box is painted over it, so the visible part
    # starts at the box edge. That is why a callout may point away from its own centre.
    style.callout(
        ax,
        f"Sized from a forced beta of 10,\n"
        f"not from h_FE: {LOAD_CURRENT * 1e3:.0f} mA needs\n"
        f"{LOAD_CURRENT / 10 * 1e3:.0f} mA of base drive, so {R_BASE:.0f} ohm.",
        (2.7, 2.3),
        (2.7, base_y - 0.45),
        halign="center",
    )
    style.callout(
        ax,
        f"{LOAD_CURRENT * 1e3:.0f} mA when the switch is on,\n"
        f"and V_CE is {models.VCE_SAT:.1f} V rather than zero.",
        (12.4, rail_y - 1.3),
        (device_x + 0.2, rail_y - 1.3),
    )


BJT_OUTPUT = style.Plot(_bjt_output, size=style.WIDE_SIZE)
MOSFET_REGIONS = style.Plot(_mosfet_regions)
GM_COMPARISON = style.Plot(_gm_comparison)
SWITCH = style.Figure(_switch, canvas=(-3.5, 0.0, 21.0, 12.5))
