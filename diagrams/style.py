"""Shared drawing style and rendering plumbing for the lecture figures.

Every visual constant lives here, so restyling every figure at once is a single edit. Figure
modules only describe geometry and data; they never touch colors, line weights, or output size.

There are two kinds of figure, because this course draws two kinds of thing:

    Figure   A schematic, on a fixed canvas with equal aspect and no axes. Bias networks,
             small-signal models, current mirrors, differential pairs, output stages. Drawn with
             schemdraw where it is a circuit and with matplotlib patches where it is a diagram.
    Plot     A graph, with axes, ticks and labels. Output characteristics, load lines, Bode
             responses, collector current against temperature, the crossover region. Drawn with
             matplotlib.

Schematics dominate here, which is the opposite of the sibling courses: most of what this course
has to show is a transistor circuit.

One habit is deliberate and it is the best thing about these figures: a circuit is annotated in
place, with boxed notes pointing at the node being discussed, rather than described in a paragraph
underneath. `callout` is that.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")  # Render straight to file; there is no display in WSL or in CI.

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import NullFormatter  # noqa: E402
import schemdraw  # noqa: E402
from PIL import Image  # noqa: E402

schemdraw.use("matplotlib")

# ----------------------------------------------------------------------------------------
# Colors
#
# Three inks, never more, and they always mean the same thing: black is the circuit, red is what
# the figure is about, blue is what it is being compared against. Amber is a third series in the
# few plots that need one. Red/blue/amber rather than red/green/blue because red and green are the
# pair most colour vision deficiencies confuse.
# ----------------------------------------------------------------------------------------
LINE_COLOR = "black"

ACCENT_COLOR = "#c00000"  # The subject: the signal path, the quantity under discussion.
ACCENT_COLOR_2 = "#0050b3"  # The comparison: the same stage without the resistor.
ACCENT_COLOR_3 = "#b35c00"  # A third series, where a figure genuinely has one.

MUTED_COLOR = "#808080"  # Context that must not compete: construction lines, DC rails.
GRID_COLOR = "#d9d9d9"
SHADE_COLOR = "#f0d8d8"  # A region rather than a line: the active region, the swing.
SHADE_COLOR_2 = "#dce6f5"  # A second region, where two have to be told apart.
SHADE_ALPHA = 0.55

CALLOUT_FILL = "#fdf4f4"  # The pad behind an annotation box.

BACKGROUND = "white"

SERIES_COLORS = (ACCENT_COLOR, ACCENT_COLOR_2, ACCENT_COLOR_3, MUTED_COLOR)

# ----------------------------------------------------------------------------------------
# Line weights
# ----------------------------------------------------------------------------------------
WIRE_WIDTH = 2.0  # A single net.
BOX_WIDTH = 2.5  # A block boundary.
ACCENT_WIDTH = 2.0  # Anything drawn in an accent color.
CURVE_WIDTH = 2.2  # A plotted curve.
GRID_WIDTH = 0.8
CONSTRUCTION_WIDTH = 1.2  # A dashed line dropped to an axis to mark a value.
LEADER_WIDTH = 1.4  # The line from an annotation box to what it points at.

# ----------------------------------------------------------------------------------------
# Text. Identifiers, component designators, node names and C++ symbols are monospace so they read
# as the identifiers they are. Everything else, including axis labels, is the sans face.
# ----------------------------------------------------------------------------------------
FONT = "monospace"
PLOT_FONT = "DejaVu Sans"
FONT_SIZE = 15
LABEL_SIZE = 13
NOTE_SIZE = 11  # Inside a callout box, which carries a sentence rather than a symbol.
TICK_SIZE = 11
TITLE_SIZE = 17
TITLE_WEIGHT = "bold"

# ----------------------------------------------------------------------------------------
# Output geometry, in schemdraw units, for schematics.
#
# A schematic declares the canvas it is rendered onto rather than being cropped to its contents,
# so figures read as a sequence share one canvas and line up pixel for pixel. That matters more
# here than in the sibling courses: this material shows the same stage repeatedly with one thing
# changed, and a reader compares them by looking from one to the next.
# ----------------------------------------------------------------------------------------

# One amplifier stage, drawn tall because a stage runs from a supply rail down to ground.
CANVAS = (-1.0, -1.0, 13.0, 12.0)

# A stage with annotation boxes to the right of it, which is the usual layout here.
ANNOTATED_CANVAS = (-1.0, -1.0, 22.0, 12.0)

# Two stages side by side: with and without the resistor, BJT against MOSFET, before and after.
WIDE_CANVAS = (-1.0, -1.0, 24.0, 12.0)

INCHES_PER_UNIT = 0.5
DPI = 130

# The default size of a plot, in inches. Plots are sized in inches rather than in canvas units
# because their axes carry the scale, so there is nothing to line up between them.
PLOT_SIZE = (6.4, 4.2)
WIDE_SIZE = (8.6, 4.4)

# Line art on white uses a few hundred colors at most, so a palette beats 32-bit RGBA: a third of
# the file size, and lossless for a figure already inside 256 colors.
PALETTE_COLORS = 256

# A schematic builder: adds elements to the drawing, and may use the raw matplotlib axes for text,
# which schemdraw positions less predictably than we want here.
Builder = Callable[[schemdraw.Drawing, "plt.Axes"], None]

# A plot builder: draws onto a matplotlib axes that already has this course's styling.
Plotter = Callable[["plt.Axes"], None]


@dataclass(frozen=True)
class Figure:
    """One schematic: how to draw it, and the canvas it is drawn onto."""

    draw: Builder
    canvas: tuple[float, float, float, float] = field(default=CANVAS)


@dataclass(frozen=True)
class Plot:
    """One graph: how to draw it, and the page it is drawn onto.

    With `panels` greater than one the builder is handed a list of that many axes side by side,
    already styled, instead of a single axes. Two panels is the useful case and it comes up
    whenever the same circuit has to be read two ways, an output characteristic and the load line
    drawn on it, or a stage's gain and its drift against the same resistor value.
    """

    draw: Plotter
    size: tuple[float, float] = field(default=PLOT_SIZE)
    panels: int = 1
    stacked: bool = False


# The monospace text is fixed-pitch, so a string's width is its length times one character.
# DejaVu Sans Mono advances 0.602 em per character; 72 points to the inch.
CHAR_ASPECT = 0.602


# ----------------------------------------------------------------------------------------
# Schematic helpers
# ----------------------------------------------------------------------------------------


def text_width(string: str, size: float = FONT_SIZE) -> float:
    """Width of `string` in canvas units, for laying out around a label."""
    return len(string) * size * CHAR_ASPECT / (72 * INCHES_PER_UNIT)


def text_height(size: float = FONT_SIZE) -> float:
    """Cap-to-descender height of a line of text, in canvas units."""
    return size / (72 * INCHES_PER_UNIT)


def text(
    ax,
    string: str,
    pos: tuple[float, float],
    halign: str = "center",
    valign: str = "center",
    size: float = FONT_SIZE,
    weight: str = "normal",
    color: str = LINE_COLOR,
    family: str = FONT,
    backed: bool = False,
    rotation: float = 0.0,
) -> None:
    """Draw text at an exact point on the canvas.

    Goes through matplotlib rather than schemdraw so that a label's position is the point given
    and nothing else, and so that bold is available; schemdraw's text has no weight.

    `backed` puts an opaque pad behind the text. Needed wherever a label sits on top of a shaded
    region or a wire, because small type over a fill interleaves into something neither of them is.
    """
    ax.text(
        pos[0],
        pos[1],
        string,
        fontsize=size,
        family=family,
        weight=weight,
        color=color,
        ha=halign,
        va=valign,
        rotation=rotation,
        rotation_mode="anchor",
        zorder=8,
        bbox=(
            {
                "facecolor": BACKGROUND,
                "edgecolor": "none",
                "boxstyle": "round,pad=0.22",
                "alpha": 0.88,
            }
            if backed
            else None
        ),
    )


def title(ax, string: str, pos: tuple[float, float]) -> None:
    """Draw a figure's name above it."""
    text(ax, string, pos, size=TITLE_SIZE, weight=TITLE_WEIGHT)


def node_label(
    ax,
    string: str,
    pos: tuple[float, float],
    color: str = ACCENT_COLOR,
    offset: tuple[float, float] = (0.0, 0.5),
) -> None:
    """Name a node, in the accent ink, just off the point it names.

    Nodes get a colour because in this course they are what the reader is asked to compute. A
    figure with V_B, V_E and V_C picked out is a figure that says which three numbers the exercise
    wants.
    """
    text(
        ax,
        string,
        (pos[0] + offset[0], pos[1] + offset[1]),
        size=LABEL_SIZE,
        color=color,
        backed=True,
    )


def callout(
    ax,
    string: str,
    box: tuple[float, float],
    points_at: tuple[float, float],
    color: str = ACCENT_COLOR,
    width: float = 9.0,
    halign: str = "left",
) -> None:
    """A boxed note with a leader line to the thing it is about.

    This is the signature device of every schematic here, and the reason they teach as well as
    they do: the explanation sits next to the node, not in a paragraph below, so the reader never
    has to hold a circuit in their head while reading about it.

    `string` is wrapped by the caller with newlines; wrapping it here would need font metrics for
    a proportional face and would still be wrong at the edges. Keep lines to about `width` canvas
    units, which is what the default box is sized for.
    """
    ax.annotate(
        "",
        xy=points_at,
        xytext=box,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "linewidth": LEADER_WIDTH,
            "shrinkA": 6,
            "shrinkB": 4,
            "mutation_scale": 13,
        },
        zorder=6,
    )
    ax.text(
        box[0],
        box[1],
        string,
        fontsize=NOTE_SIZE,
        family=PLOT_FONT,
        color=LINE_COLOR,
        ha=halign,
        va="center",
        zorder=9,
        bbox={
            "facecolor": CALLOUT_FILL,
            "edgecolor": color,
            "linewidth": 1.1,
            "boxstyle": "round,pad=0.4",
        },
    )


def block(
    ax,
    lower_left: tuple[float, float],
    size: tuple[float, float],
    label: str,
    sub: str = "",
    color: str = LINE_COLOR,
    fill: str = BACKGROUND,
    sub_size: float = LABEL_SIZE,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Draw a labelled rectangle, and return the midpoints of its left and right edges.

    Returning the two ports is what makes a block diagram readable to write: each block hands the
    next one the point to wire to, so no figure module computes a wire endpoint from a box
    position and a width by hand.
    """
    x, y = lower_left
    width, height = size

    ax.add_patch(
        plt.Rectangle(
            (x, y),
            width,
            height,
            facecolor=fill,
            edgecolor=color,
            linewidth=BOX_WIDTH,
            zorder=3,
        )
    )

    centre = (x + width / 2.0, y + height / 2.0)
    if sub:
        text(ax, label, (centre[0], centre[1] + text_height() * 0.45), color=color)
        text(
            ax,
            sub,
            (centre[0], centre[1] - text_height() * 0.55),
            size=sub_size,
            color=MUTED_COLOR,
        )
    else:
        text(ax, label, centre, color=color)

    return (x, centre[1]), (x + width, centre[1])


def wire(
    ax,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = LINE_COLOR,
    width: float = WIRE_WIDTH,
    arrow: bool = False,
    label: str = "",
) -> None:
    """Draw a straight wire between two points.

    The arrow is off by default, which is the opposite of the sibling courses: this one draws
    circuits, where a wire is a connection rather than a flow, and arrowheads on a schematic mean
    a current direction and must be reserved for it.
    """
    if arrow:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={
                "arrowstyle": "-|>",
                "color": color,
                "linewidth": width,
                "shrinkA": 0,
                "shrinkB": 0,
                "mutation_scale": 16,
            },
            zorder=4,
        )
    else:
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            color=color,
            linewidth=width,
            solid_capstyle="round",
            zorder=4,
        )

    if label:
        mid = ((start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0)
        text(
            ax,
            label,
            (mid[0], mid[1] + text_height() * 0.6),
            size=LABEL_SIZE,
            color=color,
        )


def current_arrow(
    ax,
    at: tuple[float, float],
    label: str = "",
    length: float = 1.0,
    color: str = ACCENT_COLOR,
    down: bool = True,
) -> None:
    """Mark a current, with its direction, alongside the branch it flows in.

    Beside the wire rather than on it. An arrow drawn on top of a conductor reads as part of the
    conductor, and in a figure where three currents are named that becomes unreadable quickly.
    """
    sign = -1.0 if down else 1.0
    start = (at[0], at[1] - sign * length / 2.0)
    end = (at[0], at[1] + sign * length / 2.0)
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "linewidth": ACCENT_WIDTH,
            "shrinkA": 0,
            "shrinkB": 0,
            "mutation_scale": 14,
        },
        zorder=6,
    )
    if label:
        text(
            ax,
            label,
            (at[0] + 0.55, at[1]),
            halign="left",
            size=LABEL_SIZE,
            color=color,
        )


# ----------------------------------------------------------------------------------------
# Plot helpers
# ----------------------------------------------------------------------------------------


def style_axes(ax, xlabel: str = "", ylabel: str = "") -> None:
    """Apply this course's plot styling to an axes.

    Top and right spines go, because they are a box around data that needs no box. The grid stays,
    lightly, because almost every plot in this course is one a reader is expected to take a number
    off.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(LINE_COLOR)
    ax.spines["bottom"].set_color(LINE_COLOR)

    ax.grid(True, color=GRID_COLOR, linewidth=GRID_WIDTH, zorder=0)
    ax.set_axisbelow(True)

    ax.tick_params(labelsize=TICK_SIZE, colors=LINE_COLOR)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily(PLOT_FONT)

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=LABEL_SIZE, family=PLOT_FONT, color=LINE_COLOR)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=LABEL_SIZE, family=PLOT_FONT, color=LINE_COLOR)


def log_x_axis(ax, values) -> None:
    """Make the x axis logarithmic and label it with those values and nothing else.

    Matplotlib labels a log axis's minor ticks too, in scientific notation, and they collide with
    whatever you asked for. Suppressing them is one line and forgetting it is one unreadable
    figure, so it lives here rather than in each module that wants a decade axis.
    """
    ax.set_xscale("log")
    ax.set_xticks(list(values))
    ax.set_xticklabels([f"{value:g}" for value in values])
    ax.xaxis.set_minor_formatter(NullFormatter())


def plot_title(ax, string: str) -> None:
    """A title above a plot, in this course's face and weight."""
    ax.set_title(
        string,
        fontsize=LABEL_SIZE,
        family=PLOT_FONT,
        weight=TITLE_WEIGHT,
        color=LINE_COLOR,
        pad=8,
    )


def legend(ax, **kwargs) -> None:
    """A legend in this course's style: no frame, sans face, at the readable size."""
    handles, _ = ax.get_legend_handles_labels()
    if not handles:
        return
    box = ax.legend(frameon=False, fontsize=TICK_SIZE, **kwargs)
    for entry in box.get_texts():
        entry.set_fontfamily(PLOT_FONT)


def annotate(
    ax, string: str, pos: tuple[float, float], color: str = LINE_COLOR, **kwargs
) -> None:
    """A label placed in data coordinates on a plot."""
    ax.text(
        pos[0],
        pos[1],
        string,
        fontsize=TICK_SIZE,
        family=PLOT_FONT,
        color=color,
        **kwargs,
    )


def marker(ax, x: float, y: float, label: str = "", color: str = ACCENT_COLOR) -> None:
    """Mark one point on a plot, and drop construction lines to both axes.

    Used wherever the appendix quotes a number the reader should be able to find on the figure:
    the quiescent point, the corner frequency, the collector current at which a stage clips.
    """
    ax.plot([x], [y], marker="o", markersize=5, color=color, zorder=5, linestyle="none")
    ax.plot(
        [x, x],
        [ax.get_ylim()[0], y],
        color=color,
        linewidth=CONSTRUCTION_WIDTH,
        linestyle=(0, (4, 3)),
        zorder=1,
    )
    ax.plot(
        [ax.get_xlim()[0], x],
        [y, y],
        color=color,
        linewidth=CONSTRUCTION_WIDTH,
        linestyle=(0, (4, 3)),
        zorder=1,
    )
    if label:
        annotate(ax, label, (x, y), color=color, ha="left", va="bottom")


def region(
    ax,
    low: float,
    high: float,
    label: str = "",
    color: str = SHADE_COLOR,
    label_y: float = 0.94,
) -> None:
    """Shade a range of the x axis: the active region, the usable swing, the triode region.

    A shaded span rather than a pair of lines, because the thing being said is "everything in
    here", and two vertical lines say "these two values" instead.
    """
    ax.axvspan(low, high, color=color, alpha=SHADE_ALPHA, zorder=0, linewidth=0)
    if label:
        annotate(
            ax,
            label,
            ((low + high) / 2.0, label_y),
            ha="center",
            va="top",
            transform=ax.get_xaxis_transform(),
        )


# ----------------------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------------------


def _write(fig, paths: list[Path]) -> None:
    """Rasterize a matplotlib figure once and write it to every path.

    Rendering to memory rather than to disk is what lets the palette pass below run before
    anything is written, and lets one drawing become several identical files.
    """
    buffer = io.BytesIO()
    try:
        fig.savefig(buffer, format="png", dpi=DPI, facecolor=BACKGROUND)
    finally:
        # Close even on failure; matplotlib figures are a process-wide resource.
        plt.close(fig)

    # The background is opaque, so dropping the alpha channel costs nothing. Median cut is
    # deterministic, which keeps a rebuild byte-identical, and CI checks that it is.
    image = Image.open(buffer).convert("RGB").quantize(colors=PALETTE_COLORS)

    # One drawing, written to every lecture that embeds it, which is what keeps the copies
    # identical. Directories are created on demand so a new lecture needs no setup.
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path, "PNG", optimize=True)


def render(figure: Figure | Plot, paths: list[Path]) -> None:
    """Draw a figure or a plot and write it to every path in `paths`."""
    if isinstance(figure, Plot):
        _render_plot(figure, paths)
    else:
        _render_schematic(figure, paths)


def _render_schematic(figure: Figure, paths: list[Path]) -> None:
    """Draw a schematic onto its declared canvas."""
    # Size the page from the canvas, so one unit is INCHES_PER_UNIT inches in every figure.
    xmin, ymin, xmax, ymax = figure.canvas
    fig, ax = plt.subplots(
        figsize=((xmax - xmin) * INCHES_PER_UNIT, (ymax - ymin) * INCHES_PER_UNIT)
    )

    # Hand the builder a drawing that renders onto our axes, so it can mix schemdraw elements with
    # the direct matplotlib text and patches that `text`, `callout` and `block` draw.
    drawing = schemdraw.Drawing(canvas=ax)
    drawing.config(fontsize=FONT_SIZE, font=FONT, color=LINE_COLOR, lw=WIRE_WIDTH)
    figure.draw(drawing, ax)
    drawing.draw(show=False, canvas=ax)

    # Pin the view to the declared canvas instead of letting matplotlib fit the content, and drop
    # every margin so the saved pixels are exactly the canvas.
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    _write(fig, paths)


def _render_plot(plot: Plot, paths: list[Path]) -> None:
    """Draw a matplotlib plot, already carrying this course's axes styling."""
    shape = (plot.panels, 1) if plot.stacked else (1, plot.panels)
    fig, axes = plt.subplots(shape[0], shape[1], figsize=plot.size, squeeze=False)
    panels = [axes[row][col] for row in range(shape[0]) for col in range(shape[1])]
    for panel in panels:
        style_axes(panel)

    plot.draw(panels[0] if plot.panels == 1 else panels)
    fig.tight_layout(pad=0.6)
    _write(fig, paths)
