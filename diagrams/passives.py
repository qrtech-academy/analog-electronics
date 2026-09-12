"""L02 and L03 figures: reactance, the filter family, and what Q actually costs.

REACTANCE is the whole of L02 in one plot. A resistor is a horizontal line, a capacitor falls at
six decibels per octave and an inductor rises at the same rate, and every filter in the course is
the crossing of one of those lines with the resistor's.

RESONANCE_Q is the figure that stops Q being a number people admire. A Q of ten is a peak ten
times narrower than a Q of one, and it is also ten times the input appearing across the inductor
and the capacitor individually. That second half is what destroys parts: a 10 V input on a Q of
ten puts 100 V across a capacitor rated for 63.
"""

from __future__ import annotations

import numpy as np

import models
import style

# A kilohm rather than 100 ohms, so the three crossings are three different frequencies. At
# 100 ohms this network has Q = 1 and all three curves meet at one point, which is a pretty
# figure and a misleading one: it makes the RC corner and the LC resonance look like the same
# thing, and they are not.
RESISTANCE = 1000.0
INDUCTANCE = 10.0e-3
CAPACITANCE = 1.0e-6


def _reactance(ax) -> None:
    """The impedance of each passive against frequency, and where they cross."""
    frequency = np.logspace(1.0, 5.0, 600)

    ax.plot(
        frequency,
        [RESISTANCE for _ in frequency],
        color=style.MUTED_COLOR,
        linewidth=style.CURVE_WIDTH,
        label=f"R = {RESISTANCE:.0f} ohm",
    )
    ax.plot(
        frequency,
        [models.capacitor_reactance(f, CAPACITANCE) for f in frequency],
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label=f"C = {CAPACITANCE * 1e6:.0f} uF",
    )
    ax.plot(
        frequency,
        [models.inductor_reactance(f, INDUCTANCE) for f in frequency],
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        label=f"L = {INDUCTANCE * 1e3:.0f} mH",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    style.log_x_axis(ax, [10, 100, 1000, 10000, 100000])
    ax.set_xticklabels(["10", "100", "1k", "10k", "100k"])
    ax.set_xlim(10.0, 1e5)
    # Headroom above every curve, so the legend and the note have a strip of their own.
    ax.set_ylim(0.1, 1e5)
    ax.set_yticks([0.1, 1, 10, 100, 1000, 10000])
    ax.set_yticklabels(["0.1", "1", "10", "100", "1k", "10k"])

    style.style_axes(ax, "frequency (Hz)", "impedance magnitude (ohm)")
    style.plot_title(ax, "One horizontal line and two slopes")
    style.legend(ax, loc="upper left")

    resonance = models.lc_resonance(INDUCTANCE, CAPACITANCE)
    style.marker(
        ax,
        resonance,
        models.inductor_reactance(resonance, INDUCTANCE),
        color=style.ACCENT_COLOR_3,
    )
    style.annotate(
        ax,
        f"  L and C cross at {resonance:.0f} Hz:\n" f"  equal magnitude, opposite sign",
        (resonance, models.inductor_reactance(resonance, INDUCTANCE) * 1.4),
        color=style.ACCENT_COLOR_3,
        ha="left",
        va="bottom",
    )

    # Three crossings, three different meanings, and the figure is here to keep them apart.
    corner = models.rc_corner(RESISTANCE, CAPACITANCE)
    inductive = RESISTANCE / (2.0 * np.pi * INDUCTANCE)
    style.annotate(
        ax,
        f"R crosses C at {corner:.0f} Hz and L at {inductive / 1e3:.1f} kHz.\n"
        f"Those two are filter corners. The crossing\nmarked below is a resonance, and only the\n"
        f"resonance depends on neither resistor.",
        (1.4e3, 7e4),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _filter_family(ax) -> None:
    """Low-pass, high-pass and band-pass, on one pair of axes and one corner."""
    corner = models.rc_corner(1.0e3, 159.0e-9)
    frequency = np.logspace(-2.0, 2.0, 600) * corner

    lowpass = np.array([models.first_order_response(f, corner) for f in frequency])
    highpass = np.array(
        [models.first_order_response(f, corner, highpass=True) for f in frequency]
    )
    bandpass = np.array(
        [
            models.first_order_response(f, corner * 10.0)
            * models.first_order_response(f, corner / 10.0, highpass=True)
            for f in frequency
        ]
    )

    for values, colour, label in (
        (lowpass, style.ACCENT_COLOR, "low-pass"),
        (highpass, style.ACCENT_COLOR_2, "high-pass"),
        (bandpass, style.ACCENT_COLOR_3, "band-pass, two decades wide"),
    ):
        ax.plot(
            frequency / corner,
            20.0 * np.log10(np.abs(values)),
            color=colour,
            linewidth=style.CURVE_WIDTH,
            label=label,
        )

    ax.set_xscale("log")
    style.log_x_axis(ax, [0.01, 0.1, 1, 10, 100])
    ax.set_xlim(0.01, 100.0)
    # Headroom above the curves for the note; below them every band is crossed by something.
    ax.set_ylim(-45.0, 17.0)
    style.style_axes(ax, "frequency / corner", "magnitude (dB)")
    style.plot_title(ax, "Three filters, one corner each way")
    style.legend(ax, loc="lower center")

    style.annotate(
        ax,
        "a first-order band-pass is a high-pass\nand a low-pass in series, and it only\n"
        "reaches 0 dB if the two corners are\nwell apart",
        (0.012, 16.0),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _resonance_q(ax) -> None:
    """The band-pass peak for several Q, and the voltage that appears across the inductor."""
    resonance = models.lc_resonance(INDUCTANCE, CAPACITANCE)
    frequency = np.logspace(-1.0, 1.0, 800) * resonance

    # A one-ohm series resistance would give Q = 100 and a thousand volts across the capacitor.
    # That is arithmetically true and useless as an example; these three are resistances a design
    # would actually contain.
    for series, colour in (
        (100.0, style.MUTED_COLOR),
        (30.0, style.ACCENT_COLOR_2),
        (10.0, style.ACCENT_COLOR),
    ):
        q = models.series_rlc_q(series, INDUCTANCE, CAPACITANCE)
        response = [models.bandpass_response(f, resonance, q) for f in frequency]
        ax.plot(
            frequency / resonance,
            20.0 * np.log10(np.abs(response)),
            color=colour,
            linewidth=style.CURVE_WIDTH,
            label=f"R = {series:.0f} ohm, Q = {q:.1f}",
        )

    ax.set_xscale("log")
    style.log_x_axis(ax, [0.1, 1, 10])
    # Out to 13 rather than 10 purely so the note above has room to finish its lines.
    ax.set_xlim(0.1, 13.0)
    # A clear strip above every curve, for the legend and the note.
    ax.set_ylim(-40.0, 14.0)
    style.style_axes(ax, "frequency / resonance", "magnitude (dB)")
    style.plot_title(ax, "Q is the peak's sharpness, and the overshoot inside it")
    style.legend(ax, loc="upper left")

    high = models.series_rlc_q(10.0, INDUCTANCE, CAPACITANCE)
    style.annotate(
        ax,
        f"bandwidth is resonance / Q: "
        f"{resonance / high:.0f} Hz at Q = {high:.0f},\n"
        f"and Q times the input appears across L and C\n"
        f"individually, so 10 V in is {10.0 * high:.0f} V across a part\n"
        f"you probably rated for 63",
        (1.15, 12.5),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


REACTANCE = style.Plot(_reactance, size=style.WIDE_SIZE)
FILTER_FAMILY = style.Plot(_filter_family, size=style.WIDE_SIZE)
RESONANCE_Q = style.Plot(_resonance_q, size=style.WIDE_SIZE)
