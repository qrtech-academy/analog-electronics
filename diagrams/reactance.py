"""L02 and L03 figures: reactance, the first-order response, and what cascading costs.

RC_BODE is the figure the whole frequency-domain half of Part I is built on: two straight lines
and a corner, with the phase already at 45 degrees where the magnitude has only fallen 3 dB. The
phase is the half people forget, and it is the half that decides whether a feedback loop
oscillates.

CASCADE_LOADING is the correction to the obvious guess. Two identical low-pass sections in a row
do not give you the same corner twice: the second section loads the first, and the pair rolls off
from a corner well below where either section alone would put it. Loaded and unloaded filters are
two different calculations, and this is both of them in one figure.
"""

from __future__ import annotations

import numpy as np

import models
import style

RESISTANCE = 1e3
CAPACITANCE = 159e-9


def _rc_bode(panels) -> None:
    """Magnitude and phase of a first-order low-pass, against normalised frequency."""
    magnitude_axis, phase_axis = panels

    corner = models.rc_corner(RESISTANCE, CAPACITANCE)
    frequency = np.logspace(-2.0, 2.0, 600) * corner
    response = np.array(
        [models.first_order_response(value, corner) for value in frequency]
    )

    magnitude_axis.plot(
        frequency / corner,
        20.0 * np.log10(np.abs(response)),
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="exact",
    )
    # The two asymptotes, which are what a reader should be able to draw from memory.
    magnitude_axis.plot(
        [0.01, 1.0, 100.0],
        [0.0, 0.0, -40.0],
        color=style.MUTED_COLOR,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="the two straight lines",
    )

    magnitude_axis.set_xscale("log")
    style.log_x_axis(magnitude_axis, [0.01, 0.1, 1, 10, 100])
    magnitude_axis.set_xlim(0.01, 100.0)
    magnitude_axis.set_ylim(-45.0, 8.0)
    style.style_axes(magnitude_axis, "frequency / corner", "magnitude (dB)")
    style.plot_title(magnitude_axis, "Two straight lines and a corner")
    style.legend(magnitude_axis, loc="lower left")
    style.marker(magnitude_axis, 1.0, -3.0, "  -3 dB at the corner")

    phase_axis.plot(
        frequency / corner,
        np.degrees(np.angle(response)),
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
    )
    phase_axis.set_xscale("log")
    style.log_x_axis(phase_axis, [0.01, 0.1, 1, 10, 100])
    phase_axis.set_xlim(0.01, 100.0)
    phase_axis.set_ylim(-100.0, 10.0)
    phase_axis.set_yticks([0, -45, -90])
    style.style_axes(phase_axis, "frequency / corner", "phase (degrees)")
    style.plot_title(phase_axis, "The half that decides stability")
    style.marker(phase_axis, 1.0, -45.0, "  45 degrees already")
    style.annotate(
        phase_axis,
        "6 degrees of lag\na decade below the corner",
        (0.011, -56.0),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _cascade_loading(ax) -> None:
    """One section, two sections buffered, and two sections cascaded directly."""
    corner = models.rc_corner(RESISTANCE, CAPACITANCE)
    frequency = np.logspace(-1.5, 1.5, 600) * corner

    single = np.array([models.first_order_response(f, corner) for f in frequency])

    # Buffered: two independent sections, so the responses simply multiply.
    buffered = single**2

    # Cascaded directly: the second section loads the first, and the poles split apart.
    low = corner * (3.0 - np.sqrt(5.0)) / 2.0
    high = corner * (3.0 + np.sqrt(5.0)) / 2.0
    loaded = np.array(
        [
            models.first_order_response(f, low) * models.first_order_response(f, high)
            for f in frequency
        ]
    )

    for values, colour, dashes, label in (
        (single, style.MUTED_COLOR, (0, (5, 3)), "one section"),
        (buffered, style.ACCENT_COLOR_2, None, "two sections, buffered"),
        (loaded, style.ACCENT_COLOR, None, "two sections, cascaded directly"),
    ):
        ax.plot(
            frequency / corner,
            20.0 * np.log10(np.abs(values)),
            color=colour,
            linewidth=style.CURVE_WIDTH,
            linestyle=dashes if dashes else "solid",
            label=label,
        )

    ax.set_xscale("log")
    style.log_x_axis(ax, [0.1, 1, 10])
    ax.set_xlim(0.03, 30.0)
    ax.set_ylim(-50.0, 6.0)
    style.style_axes(ax, "frequency / one section's corner", "magnitude (dB)")
    style.plot_title(
        ax, "Cascading two filters does not give you the same corner twice"
    )
    style.legend(ax, loc="lower left")

    actual = models.cascaded_corner(RESISTANCE, CAPACITANCE) / corner
    style.marker(ax, actual, -3.0)
    style.annotate(
        ax,
        f"  the pair is 3 dB down at {actual:.2f} of one\n"
        f"  section's corner, not at 1.0",
        (3.0, 2.0),
        color=style.ACCENT_COLOR,
        ha="left",
        va="top",
    )


RC_BODE = style.Plot(_rc_bode, size=(9.6, 4.0), panels=2)
CASCADE_LOADING = style.Plot(_cascade_loading, size=style.WIDE_SIZE)
