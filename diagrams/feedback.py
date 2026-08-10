"""L04 figures: feedback, the diode, and the solver that gets you through it.

GAIN_ERROR is the one result worth memorising from the whole of feedback: the closed-loop gain
falls short of the ideal by one part in (1 + T). It turns "how much open-loop gain do I need" from
a judgement into arithmetic, and the answer is usually "far more than you would guess", because
0.01 % accuracy needs a loop gain of ten thousand.

NEWTON_RAPHSON is the figure that earns the nonlinear solver. Plain Newton-Raphson on a diode,
started from zero volts, does not converge in a handful of steps; it overshoots to the supply and
then walks back one thermal voltage at a time, needing 168 iterations. Every simulator damps that
step, and the damped version arrives in seven. A reader who has seen both will believe the
limiting is necessary rather than decorative, which they will not if it is simply asserted.
"""

from __future__ import annotations

import numpy as np

import models
import style

SUPPLY = 5.0
SERIES = 1e3


def _gain_error(ax) -> None:
    """Closed-loop gain error against loop gain, for a few closed-loop gains."""
    open_loop = np.logspace(1.0, 7.0, 600)

    for closed, colour in (
        (10.0, style.ACCENT_COLOR),
        (100.0, style.ACCENT_COLOR_2),
        (1000.0, style.ACCENT_COLOR_3),
    ):
        beta = 1.0 / closed
        error = [models.gain_error(value, beta) * 100.0 for value in open_loop]
        ax.plot(
            open_loop,
            error,
            color=colour,
            linewidth=style.CURVE_WIDTH,
            label=f"closed-loop gain {closed:.0f}",
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    style.log_x_axis(ax, [10, 1e3, 1e5, 1e7])
    ax.set_xticklabels(["10", "1k", "100k", "10M"])
    ax.set_xlim(10.0, 1e7)
    ax.set_ylim(1e-4, 200.0)
    ax.set_yticks([1e-4, 1e-2, 1.0, 100.0])
    ax.set_yticklabels(["0.0001", "0.01", "1", "100"])

    style.style_axes(ax, "open-loop gain", "gain error (%)")
    style.plot_title(ax, "The error is one part in one plus the loop gain")
    style.legend(ax, loc="lower left")

    style.annotate(
        ax,
        "0.01 % accuracy needs a loop gain of ten thousand,\n"
        "which is why an operational amplifier has 120 dB it\n"
        "is going to throw away",
        (2e4, 60.0),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _diode_iv(ax) -> None:
    """The exponential, and the 0.7 V approximation laid over it."""
    voltage = np.linspace(0.0, 0.8, 600)
    current = np.array([models.diode_current(value) for value in voltage]) * 1e3

    ax.plot(
        voltage,
        current,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="the diode equation",
    )
    ax.plot(
        [0.0, models.VBE_ON, models.VBE_ON],
        [0.0, 0.0, 12.0],
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label=f"the {models.VBE_ON:.2f} V approximation",
    )

    ax.set_xlim(0.0, 0.8)
    ax.set_ylim(0.0, 12.0)
    style.style_axes(ax, "diode voltage (V)", "current (mA)")
    style.plot_title(ax, "Where the constant-drop model is a lie, and where it is not")
    style.legend(ax, loc="upper left")

    style.annotate(
        ax,
        "one decade of current per 60 mV:\nthe 'constant' drop moves 120 mV\nacross two decades",
        (0.06, 7.6),
        color=style.MUTED_COLOR,
        ha="left",
        va="top",
    )


def _newton_raphson(ax) -> None:
    """Newton-Raphson on the diode, with and without the step limiting a simulator applies."""
    limited = models.diode_newton(
        SUPPLY, SERIES, guess=0.0, iterations=12, limited=True
    )
    plain = models.diode_newton(SUPPLY, SERIES, guess=0.0, iterations=12, limited=False)

    ax.plot(
        range(len(limited)),
        limited,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        marker="o",
        markersize=4,
        label="with the limiting a simulator applies",
    )
    ax.plot(
        range(len(plain)),
        plain,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        marker="o",
        markersize=4,
        label="plain Newton-Raphson",
    )

    answer = limited[-1]
    ax.axhline(
        answer,
        color=style.MUTED_COLOR,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
    )

    ax.set_xlim(0.0, 12.0)
    # Room below the answer for the legend, which has nowhere else to go: the plain curve
    # owns the top of the figure and the limited one owns the bottom.
    ax.set_ylim(-1.5, 5.4)
    style.style_axes(ax, "iteration", "diode voltage (V)")
    style.plot_title(ax, "Why every simulator damps the step")
    style.legend(ax, loc="lower right")

    style.annotate(
        ax,
        f"the answer, {answer:.3f} V",
        (0.2, answer + 0.15),
        color=style.MUTED_COLOR,
        ha="left",
        va="bottom",
    )
    style.annotate(
        ax,
        "the first solve sees an open circuit and puts\n"
        "the whole supply across the diode; from there\n"
        "each step can only walk back one thermal\n"
        "voltage, so it needs 168 of them",
        (2.4, 4.35),
        color=style.ACCENT_COLOR_2,
        ha="left",
        va="top",
    )


GAIN_ERROR = style.Plot(_gain_error, size=style.WIDE_SIZE)
DIODE_IV = style.Plot(_diode_iv)
NEWTON_RAPHSON = style.Plot(_newton_raphson, size=style.WIDE_SIZE)
