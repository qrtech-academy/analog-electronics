"""L06 figures: the quiescent point, and what an emitter resistor does to it.

The schematic here is L06's worked common-emitter design: a 10 V supply, a 33k/6.8k divider,
1 kilohm in the emitter and 4.7 kilohm in the collector. The divider gives 1.71 V, not the 1.65 V
it looks like it ought to give, so the stage runs at 1.06 mA rather than 1 mA. No E12 pair
produces 1.65 V from 10 V, and 33k/6.8k is the right practical choice, so the values stay and the
arithmetic is done properly.

The plots are the correction to a tempting argument. It claims a 1 degree rise lifts the collector
current 10 %, which drops V_BE from 0.65 V to 0.55 V, which pulls the current back. The 10 % is
right for an undegenerated stage and the rest does not follow: a 100 mV fall in V_BE would cut the
current by a factor of 47, so the circuit never reaches that state. What actually happens is a
2 mV move, and the drift comes out at 0.2 %/K rather than 8 %/K, suppressed by exactly the emitter
factor. DRIFT_AGAINST_TEMPERATURE shows both curves; DRIFT_AGAINST_RE shows the suppression as a
function of the resistor, with the 220 mV design choice marked.
"""

from __future__ import annotations

import numpy as np
import schemdraw.elements as elm

import models
import style

# L06's worked stage.
SUPPLY = 10.0
R_UPPER = 33e3
R_LOWER = 6.8e3
R_COLLECTOR = 4.7e3
R_EMITTER = 1e3
I_C = models.divider_bias_current(SUPPLY, R_UPPER, R_LOWER, R_EMITTER)


# The layout grid. Named because the wires between the devices are computed from these, and a
# schematic whose coordinates are all literals cannot be adjusted without redrawing it by eye.
RAIL_Y = 13.0  # The supply rail.
GROUND_Y = 1.0  # The ground rail.
DIVIDER_X = 3.0  # The bias divider's column.
BASE_Y = 7.0  # The base node, which sets everything else vertically.
STAGE_X = 7.0  # Where the transistor's base sits.

# schemdraw places a BjtNpn's collector and emitter at these offsets from its base anchor, so the
# transistor's own column is the base column plus the horizontal part of that offset.
_C_OFFSET = (0.7516666666666666, 0.6966666666666667)
DEVICE_X = STAGE_X + _C_OFFSET[0]
COLLECTOR_Y = BASE_Y + _C_OFFSET[1]
EMITTER_Y = BASE_Y - _C_OFFSET[1]


def _divider_bias(drawing, ax) -> None:
    """The divider-biased common-emitter stage, with its quiescent voltages named."""
    # Every device first, then the wires. Adding a ground or a rail changes schemdraw's current
    # direction, and a transistor placed after one comes out mirrored while its anchor coordinates
    # still read correctly. The symptom is diagonal wires, and it is invisible from the code.
    transistor = elm.BjtNpn().at((STAGE_X, BASE_Y))

    # Values are placed by hand below rather than through schemdraw's own .label(), which centres
    # a vertical element's label on the wire and gives no way to choose a side. In a figure this
    # dense every label needs its own side, and four of them collided when schemdraw chose.
    upper = elm.Resistor().at((DIVIDER_X, RAIL_Y)).down().length(2.6)
    lower = elm.Resistor().at((DIVIDER_X, BASE_Y)).down().length(2.6)
    collector = elm.Resistor().at((DEVICE_X, RAIL_Y)).down().length(2.6)
    emitter = elm.Resistor().at((DEVICE_X, 4.6)).down().length(2.6)

    for element in (transistor, upper, lower, collector, emitter):
        drawing.add(element)

    # Component values, each on the side of its own column that faces open space.
    for value, (x, y), align in (
        ("33k", (DIVIDER_X - 0.7, RAIL_Y - 1.3), "right"),
        ("6.8k", (DIVIDER_X - 0.7, BASE_Y - 1.3), "right"),
        ("4.7k", (DEVICE_X - 0.8, RAIL_Y - 1.3), "right"),
        ("1k", (DEVICE_X - 0.8, 4.6 - 1.3), "right"),
    ):
        style.text(ax, value, (x, y), halign=align, size=style.LABEL_SIZE)

    # The supply rail, and the two branches hanging off it.
    style.wire(ax, (DIVIDER_X, RAIL_Y), (DEVICE_X, RAIL_Y))
    style.text(
        ax,
        f"+{SUPPLY:.0f} V",
        ((DIVIDER_X + DEVICE_X) / 2.0, RAIL_Y + 0.7),
        size=style.LABEL_SIZE,
    )

    # Divider: down from the upper resistor to the base node, then on down to ground.
    style.wire(ax, (DIVIDER_X, RAIL_Y - 2.6), (DIVIDER_X, BASE_Y))
    style.wire(ax, (DIVIDER_X, BASE_Y), (STAGE_X, BASE_Y))
    style.wire(ax, (DIVIDER_X, BASE_Y - 2.6), (DIVIDER_X, GROUND_Y))
    drawing.add(elm.Dot().at((DIVIDER_X, BASE_Y)))

    # Collector resistor down to the collector; emitter down through its resistor to ground.
    style.wire(ax, (DEVICE_X, RAIL_Y - 2.6), (DEVICE_X, COLLECTOR_Y))
    style.wire(ax, (DEVICE_X, EMITTER_Y), (DEVICE_X, 4.6))
    style.wire(ax, (DEVICE_X, 4.6 - 2.6), (DEVICE_X, GROUND_Y))

    # The ground rail.
    style.wire(ax, (DIVIDER_X, GROUND_Y), (DEVICE_X, GROUND_Y))
    drawing.add(elm.Ground().at(((DIVIDER_X + DEVICE_X) / 2.0, GROUND_Y)))

    # The output, taken at the collector, above the transistor so the leader does not cross it.
    out_y = COLLECTOR_Y + 1.4
    style.wire(ax, (DEVICE_X, out_y), (DEVICE_X + 4.0, out_y))
    drawing.add(elm.Dot().at((DEVICE_X, out_y)))
    drawing.add(elm.Dot(open=True).at((DEVICE_X + 4.0, out_y)))

    # The transistor's designator, clear of the emitter label below it.
    style.text(
        ax, "Q1", (STAGE_X - 0.5, BASE_Y - 1.5), size=style.LABEL_SIZE, halign="right"
    )

    # The three voltages the reader is asked to compute, in the accent ink because they are the
    # answer rather than the circuit.
    base_voltage = SUPPLY * R_LOWER / (R_UPPER + R_LOWER)
    style.text(
        ax,
        f"V_B = {base_voltage:.2f} V",
        (DIVIDER_X + 0.45, BASE_Y + 0.85),
        halign="left",
        size=style.LABEL_SIZE,
        color=style.ACCENT_COLOR,
    )
    style.text(
        ax,
        f"V_E = {base_voltage - models.VBE_ON:.2f} V",
        (DEVICE_X + 0.8, 4.35),
        halign="left",
        size=style.LABEL_SIZE,
        color=style.ACCENT_COLOR,
    )
    style.text(
        ax,
        f"V_C = {SUPPLY - I_C * R_COLLECTOR:.2f} V",
        (DEVICE_X + 4.0, out_y + 0.85),
        size=style.LABEL_SIZE,
        color=style.ACCENT_COLOR,
    )

    # The current arrow goes to the right of the collector column, where the only other thing is
    # the output wire two units below it.
    style.current_arrow(
        ax, (DEVICE_X + 1.5, RAIL_Y - 1.3), f"I_C = {I_C * 1e3:.2f} mA", length=1.6
    )


def _drift_against_temperature(ax) -> None:
    """Collector current against temperature, with the emitter resistor and without it."""
    rise = np.linspace(0.0, 30.0, 400)

    # Undegenerated: the base is held, so the whole of the V_BE drift lands on the exponential.
    without = np.exp(-models.VBE_TEMPCO * rise / models.THERMAL_VOLTAGE)

    # Degenerated: the emitter follows the base, and the current moves by the drift over R_E.
    with_re = 1.0 + (-models.VBE_TEMPCO * rise / R_EMITTER) / I_C

    ax.plot(
        rise,
        without,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        label="no emitter resistor",
    )
    ax.plot(
        rise,
        with_re,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label=f"{R_EMITTER / 1e3:.0f}k emitter resistor",
    )

    ax.set_yscale("log")
    ax.set_ylim(0.9, 20.0)
    ax.set_xlim(0.0, 30.0)
    ax.set_yticks([1, 2, 5, 10, 20])
    ax.set_yticklabels(["1", "2", "5", "10", "20"])

    style.style_axes(ax, "temperature rise (K)", "collector current, relative to 300 K")
    style.plot_title(ax, "What the emitter resistor is for")
    style.legend(ax, loc="upper left")

    style.annotate(
        ax,
        f"{models.drift_without_degeneration() * 100:.0f} %/K",
        (21.0, 9.0),
        color=style.ACCENT_COLOR_2,
        ha="center",
    )
    style.annotate(
        ax,
        f"{models.drift_with_degeneration(I_C, R_EMITTER) * 100:.1f} %/K",
        (21.0, 1.20),
        color=style.ACCENT_COLOR,
        ha="center",
    )


def _drift_against_re(ax) -> None:
    """Drift suppression against the emitter resistor, which is the emitter factor."""
    resistors = np.logspace(0.0, 4.0, 400)
    suppression = [models.drift_suppression(I_C, value) for value in resistors]
    factor = [models.emitter_factor(I_C, value) for value in resistors]

    ax.plot(
        resistors,
        suppression,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="drift suppression",
    )
    ax.plot(
        resistors,
        factor,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="emitter factor EF",
    )

    ax.set_yscale("log")
    style.log_x_axis(ax, [1, 10, 100, 1000, 10000])
    ax.set_ylim(1.0, 500.0)
    ax.set_yticks([1, 10, 100])
    ax.set_yticklabels(["1", "10", "100"])

    style.style_axes(ax, "emitter resistor (ohm)", "factor")
    style.plot_title(ax, "The suppression is the emitter factor")
    style.legend(ax, loc="upper left")

    # The design choice of L06 B.4: 220 mV across the resistor, taken to the nearest E12 value,
    # which is what a design actually uses and what makes the rule worth having.
    chosen = models.nearest_e12(models.degeneration_resistor(I_C))
    ax.set_xlim(1.0, 10000.0)
    style.marker(ax, chosen, models.emitter_factor(I_C, chosen))
    style.annotate(
        ax,
        f"220 mV rule: {chosen:.0f} ohm, EF = {models.emitter_factor(I_C, chosen):.0f}  ",
        (chosen, models.emitter_factor(I_C, chosen) * 1.35),
        color=style.ACCENT_COLOR,
        ha="right",
        va="bottom",
    )

    # The two curves part company below about 50 ohms, and the figure should say why rather than
    # leave a reader to wonder. The emitter factor is exact; the suppression is computed from a
    # linearisation that assumes the emitter voltage follows the base, and with almost no resistor
    # there is nothing for it to follow. Where a design actually sits, EF between 5 and 50, they
    # agree to better than a percent.
    style.annotate(
        ax,
        "the linearisation fails\nwhere there is no resistor",
        (1.15, 70.0),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


DIVIDER_BIAS = style.Figure(_divider_bias, canvas=(0.5, 0.0, 16.5, 14.6))
DRIFT_AGAINST_TEMPERATURE = style.Plot(_drift_against_temperature)
DRIFT_AGAINST_RE = style.Plot(_drift_against_re)
