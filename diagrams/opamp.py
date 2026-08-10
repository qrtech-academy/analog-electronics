"""L10 figures: the operational amplifier from L03, opened up and accounted for.

The course used an op-amp as a black box in L03 and L04 on the promise that L10 would build one.
These two figures are that promise being kept: the block diagram says which stage is responsible
for which specification, and the budget says where the open-loop gain actually comes from.

GAIN_BUDGET carries the lesson. Two stages of about 66 dB each should give 131 dB, and the
amplifier delivers 120. The missing 11 dB is not a rounding error and it is not distributed evenly:
it is one stage being loaded by the next. That is why there is a follower between stages one and
two, why the output stage is a Darlington rather than a single transistor, and why a gain budget
written without loading is not slightly optimistic but wrong by a factor of three.
"""

from __future__ import annotations


import schemdraw.elements as elm

import models
import style

TAIL = 2e-3
STAGE2_CURRENT = 1e-3
QUIESCENT = 0.12
SPEAKER = 8.0
CLOSED_LOOP = 20.0


def _budget() -> dict[str, float]:
    """Every number both figures quote. One source, in models, shared with the prose and tests."""
    return models.opamp_budget()


def _opamp_stages(drawing, ax) -> None:
    """What each stage is responsible for, which is the only way to size any of them."""
    del drawing

    numbers = _budget()

    y = 6.0
    height = 3.0
    width = 5.4
    gap = 1.6

    blocks = (
        (
            "differential pair",
            "gain, and every input\nspecification there is",
            f"x{numbers['stage1']:.0f}",
        ),
        (
            "Darlington follower",
            "no gain at all: it is here\nso stage 1 is not loaded",
            f"x{numbers['buffer']:.2f}",
        ),
        (
            "common emitter",
            "most of the open-loop gain,\nand the compensation pole",
            f"x{numbers['stage2']:.0f}",
        ),
        (
            "class-AB output",
            "no gain either: current,\nand a low output resistance",
            f"x{numbers['output']:.2f}",
        ),
    )

    x = 0.0
    previous_right = None
    for title, role, gain in blocks:
        # style.block's `sub` is positioned for a single line and overlaps the title as soon as
        # the text wraps, so the role is drawn separately with room of its own.
        left, right = style.block(ax, (x, y), (width, height), title)
        style.text(
            ax,
            role,
            (x + width / 2.0, y + height / 2.0 - 1.0),
            size=11,
            color=style.MUTED_COLOR,
            family=style.PLOT_FONT,
        )
        if previous_right is not None:
            style.wire(ax, previous_right, left, arrow=True)
        style.text(
            ax,
            gain,
            (x + width / 2.0, y + height + 0.9),
            size=style.FONT_SIZE,
            color=style.ACCENT_COLOR,
        )
        previous_right = right
        x += width + gap

    style.text(
        ax,
        "v_in",
        (-1.2, y + height / 2.0),
        halign="right",
        size=style.LABEL_SIZE,
    )
    style.wire(ax, (-1.0, y + height / 2.0), (0.0, y + height / 2.0), arrow=True)
    style.wire(
        ax, previous_right, (previous_right[0] + 1.6, previous_right[1]), arrow=True
    )
    style.text(
        ax,
        "v_out",
        (previous_right[0] + 1.9, previous_right[1]),
        halign="left",
        size=style.LABEL_SIZE,
    )

    style.text(
        ax,
        f"open loop {models.decibels(numbers['open_loop']):.0f} dB, "
        f"closed loop {CLOSED_LOOP:.0f} with "
        f"{models.gain_error(numbers['open_loop'], 1.0 / CLOSED_LOOP) * 100:.4f} % error. "
        f"The two stages with no gain are worth {models.opamp_buffer_worth():.0f} dB each.",
        (x / 2.0 - gap / 2.0, y - 2.0),
        size=style.FONT_SIZE,
        weight=style.TITLE_WEIGHT,
    )


def _gain_budget(ax) -> None:
    """Where the open-loop gain comes from, and what loading takes back."""
    numbers = _budget()

    steps = (
        (
            "differential pair,\nunloaded",
            models.decibels(numbers["stage1_unloaded"]),
            style.ACCENT_COLOR,
        ),
        (
            "loaded by the\nDarlington buffer",
            models.decibels(numbers["stage1"] / numbers["stage1_unloaded"]),
            style.ACCENT_COLOR_2,
        ),
        ("the buffer itself", models.decibels(numbers["buffer"]), style.ACCENT_COLOR_2),
        (
            "common emitter,\nunloaded",
            models.decibels(numbers["stage2_unloaded"]),
            style.ACCENT_COLOR,
        ),
        (
            "loaded by the\noutput stage",
            models.decibels(numbers["stage2"] / numbers["stage2_unloaded"]),
            style.ACCENT_COLOR_2,
        ),
        ("output follower", models.decibels(numbers["output"]), style.ACCENT_COLOR_2),
    )

    running = 0.0
    for index, (label, delta, colour) in enumerate(steps):
        ax.barh(index, delta, left=running, height=0.55, color=colour, zorder=3)
        end = running + delta
        ax.text(
            max(running, end) + 1.5 if delta > 0 else min(running, end) - 1.5,
            index,
            f"{delta:+.1f} dB",
            fontsize=style.TICK_SIZE,
            family=style.PLOT_FONT,
            color=colour,
            va="center",
            ha="left" if delta > 0 else "right",
        )
        running = end
        del label

    total = models.decibels(numbers["open_loop"])
    ax.barh(len(steps), total, height=0.55, color=style.LINE_COLOR, zorder=3)
    ax.text(
        total + 1.5,
        len(steps),
        f"{total:.0f} dB",
        fontsize=style.TICK_SIZE,
        family=style.PLOT_FONT,
        color=style.LINE_COLOR,
        va="center",
        ha="left",
    )

    ax.set_yticks(list(range(len(steps) + 1)))
    ax.set_yticklabels([label for label, _, _ in steps] + ["open loop"])
    ax.invert_yaxis()
    # A clear band above the bars for the note; without it the note lands on two of them.
    ax.set_ylim(len(steps) + 0.8, -1.9)
    ax.set_xlim(0.0, 150.0)

    style.style_axes(ax, "gain (dB)", "")
    style.plot_title(ax, "Two stages of 66 dB give 120, not 131")

    style.annotate(
        ax,
        f"Loading costs {models.opamp_loading_loss():.1f} dB of the "
        f"{models.decibels(numbers['unloaded']):.0f} the two gain stages\n"
        f"would give on their own. Both of the stages that fix it have a\n"
        f"gain below one, and each is worth about {models.opamp_buffer_worth():.0f} dB of loop gain.",
        (2.0, -1.35),
        color=style.MUTED_COLOR,
        ha="left",
        va="center",
    )


OPAMP_STAGES = style.Figure(_opamp_stages, canvas=(-4.5, 2.0, 30.5, 12.0))
GAIN_BUDGET = style.Plot(_gain_budget, size=style.WIDE_SIZE)


LEG = 0.7516666666666666
RISE = 0.6966666666666667
REVERSED_BASE = 1.5033333333333332


def _amplifier(drawing, ax) -> None:
    """The whole amplifier, one transistor at a time.

    Every anchor here is computed from LEG, RISE and REVERSED_BASE rather than guessed, because
    two circuits earlier in this course came out silently detached from assuming otherwise. A
    reversed part keeps its device column at x + LEG and moves only its base lead, to
    x + REVERSED_BASE.
    """
    numbers = _budget()

    rail_y = 14.6
    vee_y = 1.4
    out_y = 8.5

    def npn(x, y, reverse=False):
        # `.right()` is not decoration. schemdraw carries a current direction from one added
        # element to the next, so a transistor placed after a `.down()` resistor inherits `down`
        # and is drawn rotated, with its terminals nowhere near where the wiring below expects
        # them. Pin every device.
        element = elm.BjtNpn().at((x, y)).right()
        if reverse:
            element = element.reverse()
        drawing.add(element)
        return (
            (x + LEG, y + RISE),
            (x + LEG, y - RISE),
            (
                (x + REVERSED_BASE) if reverse else x,
                y,
            ),
        )

    def pnp(x, y, reverse=False):
        element = elm.BjtPnp().at((x, y)).right()
        if reverse:
            element = element.reverse()
        drawing.add(element)
        return (
            (x + LEG, y - RISE),
            (x + LEG, y + RISE),
            (
                (x + REVERSED_BASE) if reverse else x,
                y,
            ),
        )

    # ---- Stage 1: the mirror-loaded pair ------------------------------------------------
    mirror_y = 11.9
    pair_y = 7.4

    m1_c, m1_e, m1_b = pnp(2.4, mirror_y, reverse=True)
    m2_c, m2_e, m2_b = pnp(4.4, mirror_y)
    q1_c, q1_e, q1_b = npn(2.4, pair_y)
    q2_c, q2_e, q2_b = npn(4.4, pair_y, reverse=True)

    for anchor in (m1_e, m2_e):
        style.wire(ax, anchor, (anchor[0], rail_y))
    style.wire(ax, m1_b, m2_b)
    style.wire(ax, m1_b, (m1_b[0], m1_c[1]))
    style.wire(ax, (m1_b[0], m1_c[1]), m1_c)
    drawing.add(elm.Dot().at(m1_c))
    style.wire(ax, m1_c, q1_c)
    style.wire(ax, m2_c, q2_c)
    style.wire(ax, q1_e, (q1_e[0], 4.9))
    style.wire(ax, (q1_e[0], 4.9), (q2_e[0], 4.9))
    style.wire(ax, q2_e, (q2_e[0], 4.9))
    tail_x = q1_e[0] + LEG
    drawing.add(elm.Dot().at((tail_x, 4.9)))
    drawing.add(elm.SourceI().at((tail_x, 4.9)).down().length(1.7))
    style.wire(ax, (tail_x, 3.2), (tail_x, vee_y))

    drawing.add(elm.Dot(open=True).at((0.4, pair_y)))
    style.wire(ax, (0.4, pair_y), q1_b)
    style.text(ax, "v+", (0.4, pair_y + 0.8), size=style.LABEL_SIZE)
    drawing.add(elm.Dot(open=True).at((q2_b[0] + 1.0, pair_y - 2.0)))
    style.wire(ax, q2_b, (q2_b[0] + 1.0, pair_y))
    style.wire(ax, (q2_b[0] + 1.0, pair_y), (q2_b[0] + 1.0, pair_y - 2.0))
    style.text(
        ax, "v-", (q2_b[0] + 1.3, pair_y - 2.0), halign="left", size=style.LABEL_SIZE
    )

    # ---- Stage 2: the Darlington buffer ------------------------------------------------
    buffer_y = 9.6
    q3_c, q3_e, q3_b = npn(8.2, buffer_y)
    q4_c, q4_e, q4_b = npn(10.0, buffer_y)

    style.wire(ax, m2_c, (q3_b[0], m2_c[1]))
    style.wire(ax, (q3_b[0], m2_c[1]), q3_b)
    drawing.add(elm.Dot().at(m2_c))

    style.wire(ax, q3_e, (q3_e[0], buffer_y - 1.4))
    style.wire(ax, (q3_e[0], buffer_y - 1.4), (q4_b[0], buffer_y - 1.4))
    style.wire(ax, (q4_b[0], buffer_y - 1.4), q4_b)
    for anchor in (q3_c, q4_c):
        style.wire(ax, anchor, (anchor[0], 12.9))
    style.wire(ax, (q3_c[0], 12.9), (q4_c[0], 12.9))
    style.wire(ax, (q4_c[0], 12.9), (q4_c[0], rail_y))

    style.wire(ax, q4_e, (q4_e[0], 6.6))
    drawing.add(elm.SourceI().at((q4_e[0], 6.6)).down().length(1.7))
    style.wire(ax, (q4_e[0], 4.9), (q4_e[0], vee_y))
    drawing.add(elm.Dot().at((q4_e[0], 7.4)))

    # ---- Stage 3: the common-emitter voltage gain ---------------------------------------
    stage2_y = 5.6
    q5_c, q5_e, q5_b = npn(14.2, stage2_y)

    base_x = q5_b[0] - 1.9
    style.wire(ax, (q4_e[0], 7.4), (base_x, 7.4))
    style.wire(ax, (base_x, 7.4), (base_x, q5_b[1]))
    style.wire(ax, (base_x, q5_b[1]), q5_b)
    style.wire(ax, q5_e, (q5_e[0], vee_y))

    drive_y = 11.4
    style.wire(ax, q5_c, (q5_c[0], drive_y))
    drawing.add(elm.SourceI().at((q5_c[0], rail_y - 1.2)).down().length(1.7))
    style.wire(ax, (q5_c[0], rail_y), (q5_c[0], rail_y - 1.2))
    style.wire(ax, (q5_c[0], rail_y - 2.9), (q5_c[0], drive_y))
    drawing.add(elm.Dot().at((q5_c[0], drive_y)))

    miller_y = 9.2
    drawing.add(
        elm.Capacitor()
        .at((q5_c[0], miller_y))
        .left()
        .length(1.9)
        .label("C_c", loc="top")
    )
    style.wire(ax, (q5_c[0] - 1.9, miller_y), (q5_c[0] - 1.9, 7.4))
    style.wire(ax, (q5_c[0] - 1.9, 7.4), (base_x, 7.4))
    drawing.add(elm.Dot().at((q5_c[0] - 1.9, 7.4)))

    # ---- Stage 4: the class-AB Darlington output ----------------------------------------
    upper_y = 11.4
    lower_y = 5.6
    bias_x = 17.4

    q6_c, q6_e, q6_b = npn(19.0, upper_y)
    q7_c, q7_e, q7_b = npn(20.8, upper_y)
    q8_c, q8_e, q8_b = pnp(19.0, lower_y)
    q9_c, q9_e, q9_b = pnp(20.8, lower_y)

    drawing.add(elm.Diode().at((bias_x, upper_y)).down().length(2.9))
    drawing.add(elm.Diode().at((bias_x, upper_y - 2.9)).down().length(2.9))
    style.wire(ax, (q5_c[0], drive_y), (bias_x, drive_y))
    style.wire(ax, (bias_x, upper_y), q6_b)
    style.wire(ax, (bias_x, lower_y), q8_b)
    drawing.add(elm.Dot().at((bias_x, upper_y)))
    drawing.add(elm.Dot().at((bias_x, lower_y)))

    style.wire(ax, q6_e, (q6_e[0], upper_y - 1.4))
    style.wire(ax, (q6_e[0], upper_y - 1.4), (q7_b[0], upper_y - 1.4))
    style.wire(ax, (q7_b[0], upper_y - 1.4), q7_b)
    for anchor in (q6_c, q7_c):
        style.wire(ax, anchor, (anchor[0], 13.2))
    style.wire(ax, (q6_c[0], 13.2), (q7_c[0], 13.2))
    style.wire(ax, (q7_c[0], 13.2), (q7_c[0], rail_y))

    style.wire(ax, q8_e, (q8_e[0], lower_y + 1.4))
    style.wire(ax, (q8_e[0], lower_y + 1.4), (q9_b[0], lower_y + 1.4))
    style.wire(ax, (q9_b[0], lower_y + 1.4), q9_b)
    for anchor in (q8_c, q9_c):
        style.wire(ax, anchor, (anchor[0], 3.8))
    style.wire(ax, (q8_c[0], 3.8), (q9_c[0], 3.8))
    style.wire(ax, (q9_c[0], 3.8), (q9_c[0], vee_y))

    style.wire(ax, q7_e, (q7_e[0], q7_e[1] - 0.4))
    drawing.add(
        elm.Resistor().at((q7_e[0], q7_e[1] - 0.4)).down().length(q7_e[1] - 0.4 - out_y)
    )
    style.wire(ax, q9_e, (q9_e[0], q9_e[1] + 0.4))
    drawing.add(
        elm.Resistor().at((q9_e[0], q9_e[1] + 0.4)).up().length(out_y - (q9_e[1] + 0.4))
    )
    drawing.add(elm.Dot().at((q7_e[0], out_y)))

    speaker_x = q7_e[0] + 3.4
    style.wire(ax, (q7_e[0], out_y), (speaker_x, out_y))
    drawing.add(elm.Resistor().at((speaker_x, out_y)).down().length(2.6))
    style.wire(ax, (speaker_x, out_y - 2.6), (speaker_x, 4.6))
    drawing.add(elm.Ground().at((speaker_x, 4.6)))
    drawing.add(elm.Dot(open=True).at((speaker_x + 2.0, out_y)))
    style.wire(ax, (speaker_x, out_y), (speaker_x + 2.0, out_y))
    style.text(
        ax, "v_out", (speaker_x + 2.3, out_y), halign="left", size=style.LABEL_SIZE
    )

    # ---- Rails ---------------------------------------------------------------------------
    style.wire(ax, (1.4, rail_y), (speaker_x + 0.6, rail_y))
    style.wire(ax, (1.4, vee_y), (speaker_x + 0.6, vee_y))
    style.text(ax, "+V_CC", (speaker_x - 1.0, rail_y + 0.7), halign="right")
    style.text(ax, "-V_EE", (1.4, vee_y - 0.8), halign="left")

    # ---- Labels --------------------------------------------------------------------------
    for label, position in (
        ("M1", (2.0, mirror_y + 1.0)),
        ("M2", (5.6, mirror_y + 1.0)),
        ("Q1", (2.0, pair_y - 1.1)),
        ("Q2", (6.2, pair_y - 1.1)),
        ("Q3", (8.55, 11.7)),
        ("Q4", (10.35, 11.7)),
        ("Q5", (13.5, stage2_y - 1.1)),
        ("Q6", (18.7, upper_y + 1.1)),
        ("Q7", (20.5, upper_y + 1.1)),
        ("Q8", (18.7, lower_y - 1.1)),
        ("Q9", (20.5, lower_y - 1.1)),
    ):
        style.text(ax, label, position, size=style.LABEL_SIZE)

    style.text(
        ax,
        "8 ohm",
        (speaker_x + 0.5, out_y - 1.3),
        halign="left",
        size=style.LABEL_SIZE,
    )
    style.text(
        ax, "0.22", (q7_e[0] + 0.4, out_y + 1.1), halign="left", size=style.LABEL_SIZE
    )
    style.text(
        ax, "0.22", (q9_e[0] + 0.4, out_y - 1.1), halign="left", size=style.LABEL_SIZE
    )

    style.callout(
        ax,
        f"Stage 1. Mirror-loaded pair, "
        f"{numbers['stage1_unloaded']:.0f} unloaded.\n"
        f"The mirror recovers the half a single-ended\n"
        f"output would throw away, and presents r_o\n"
        f"rather than a resistor. L09.",
        (0.4, 17.4),
        (m2_c[0], mirror_y - RISE - 0.8),
        halign="left",
    )
    style.callout(
        ax,
        f"Stage 2. No gain: {numbers['buffer']:.2f}.\n"
        f"Its input resistance is "
        f"{numbers['buffer_input'] / 1e6:.1f} megohm\n"
        f"against stage 3's {numbers['stage2_input'] / 1e3:.1f} kilohm, and\n"
        f"that is worth {models.opamp_buffer_worth():.0f} dB of loop gain.",
        (7.6, 17.4),
        (q4_e[0], 7.9),
        halign="left",
    )
    style.callout(
        ax,
        f"Stage 3. {numbers['stage2_unloaded']:.0f} unloaded, "
        f"{numbers['stage2']:.0f} loaded.\n"
        f"C_c is the Miller capacitor: it is here to\n"
        f"make this pole dominant, which is the only\n"
        f"reason the closed loop is stable.",
        (13.0, 2.0),
        (q5_c[0] - 1.9, miller_y - 0.4),
        halign="left",
    )
    style.callout(
        ax,
        f"Stage 4. No gain either: {numbers['output']:.3f}.\n"
        f"Darlingtons, so the input resistance is\n"
        f"{numbers['output_input'] / 1e3:.0f} kilohm rather than 0.4, and that\n"
        f"is worth another {models.opamp_output_worth():.0f} dB.",
        (22.4, 2.0),
        (q7_e[0], out_y - 1.0),
        halign="left",
    )


AMPLIFIER = style.Figure(_amplifier, canvas=(-0.5, 0.0, 34.0, 19.0))
