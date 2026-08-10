"""L01 figures: the divider, and what a load does to it.

The voltage divider is the only circuit in this course worth memorising, and DIVIDER_LOADING is
the reason it is worth understanding as well. A divider designed for 1.71 V delivers 1.09 V into
10 kilohms, and the number that predicts that is the Thevenin resistance, which is the two legs in
parallel rather than either of them.

That is also the first appearance of the idea the whole course runs on: a stage's output
resistance and the next stage's input resistance decide between them what actually arrives. L10's
gain budget loses 11 dB to the same arithmetic.
"""

from __future__ import annotations

import numpy as np
import schemdraw.elements as elm

import models
import style

SUPPLY = 10.0
UPPER = 33e3
LOWER = 6.8e3


def _divider(drawing, ax) -> None:
    """The divider, its unloaded output, and the resistance a load sees looking back."""
    ground_y = 1.0
    rail_y = 11.0
    column_x = 6.0
    tap_y = 6.0

    upper = elm.Resistor().at((column_x, rail_y)).down().length(2.6)
    lower = elm.Resistor().at((column_x, tap_y)).down().length(2.6)
    for element in (upper, lower):
        drawing.add(element)

    drawing.add(elm.Vdd().at((column_x, rail_y)))
    style.text(
        ax,
        f"{SUPPLY:.0f} V",
        (column_x + 0.8, rail_y + 0.4),
        halign="left",
        size=style.LABEL_SIZE,
    )
    style.wire(ax, (column_x, rail_y - 2.6), (column_x, tap_y))
    style.wire(ax, (column_x, tap_y - 2.6), (column_x, ground_y))
    drawing.add(elm.Ground().at((column_x, ground_y)))

    drawing.add(elm.Dot().at((column_x, tap_y)))
    style.wire(ax, (column_x, tap_y), (column_x + 4.2, tap_y))
    drawing.add(elm.Dot(open=True).at((column_x + 4.2, tap_y)))

    style.text(
        ax, "33k", (column_x - 0.8, rail_y - 1.3), halign="right", size=style.LABEL_SIZE
    )
    style.text(
        ax, "6.8k", (column_x - 0.8, tap_y - 1.3), halign="right", size=style.LABEL_SIZE
    )
    style.text(
        ax,
        f"{models.divider(SUPPLY, UPPER, LOWER):.2f} V",
        (column_x + 4.2, tap_y - 0.8),
        size=style.LABEL_SIZE,
        color=style.ACCENT_COLOR,
    )

    style.callout(
        ax,
        f"Looking back from here the divider is a\n"
        f"{models.divider(SUPPLY, UPPER, LOWER):.2f} V source behind "
        f"{models.divider_output_resistance(UPPER, LOWER) / 1e3:.1f} kilohms,\n"
        f"which is the two legs in parallel. Not 33k,\n"
        f"not 6.8k, and smaller than either.",
        (13.5, 9.4),
        (column_x + 2.6, tap_y),
    )
    style.callout(
        ax,
        f"Hang 10 kilohms on it and the output is\n"
        f"{models.divider(SUPPLY, UPPER, LOWER, 10e3):.2f} V, not "
        f"{models.divider(SUPPLY, UPPER, LOWER):.2f} V. The divider\n"
        f"you designed is not the divider you have.",
        (13.5, 3.0),
        (column_x + 4.2, tap_y),
    )


def _divider_loading(ax) -> None:
    """Output against the load hung on it, with the Thevenin resistance marked."""
    loads = np.logspace(2.0, 7.0, 500)
    output = [models.divider(SUPPLY, UPPER, LOWER, value) for value in loads]

    ax.plot(loads, output, color=style.ACCENT_COLOR, linewidth=style.CURVE_WIDTH)
    ax.axhline(
        models.divider(SUPPLY, UPPER, LOWER),
        color=style.MUTED_COLOR,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
    )

    ax.set_xscale("log")
    style.log_x_axis(ax, [1e2, 1e3, 1e4, 1e5, 1e6, 1e7])
    ax.set_xticklabels(["100", "1k", "10k", "100k", "1M", "10M"])
    ax.set_xlim(1e2, 1e7)
    ax.set_ylim(0.0, 2.0)

    style.style_axes(ax, "load resistance (ohm)", "output (V)")
    style.plot_title(ax, "A divider is only a divider until something uses it")

    thevenin = models.divider_output_resistance(UPPER, LOWER)
    style.marker(ax, thevenin, models.divider(SUPPLY, UPPER, LOWER, thevenin))
    style.annotate(
        ax,
        f"  a load equal to the Thevenin resistance,\n"
        f"  {thevenin / 1e3:.1f}k, halves the output",
        (thevenin, models.divider(SUPPLY, UPPER, LOWER, thevenin) - 0.06),
        color=style.ACCENT_COLOR,
        ha="left",
        va="top",
    )
    style.annotate(
        ax,
        f"unloaded: {models.divider(SUPPLY, UPPER, LOWER):.2f} V",
        (1.2e6, models.divider(SUPPLY, UPPER, LOWER) + 0.06),
        color=style.MUTED_COLOR,
        ha="left",
        va="bottom",
    )


DIVIDER = style.Figure(_divider, canvas=(0.0, 0.0, 24.0, 12.6))
DIVIDER_LOADING = style.Plot(_divider_loading, size=style.WIDE_SIZE)
