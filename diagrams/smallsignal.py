"""L07 figures: the r_e model, the emitter factor, and which node it belongs to.

EF_ATTRIBUTION is the most important figure in the course, and it is the one that settles which
resistance the emitter factor multiplies.

The tempting answer is that a degeneration resistor raises the *stage's* output resistance by the
emitter factor, R_out = R_C * EF. It does not, and it cannot: the stage's output resistance is R_C
in parallel with the resistance looking into the collector, and a parallel combination is smaller
than either part. What EF raises is the resistance looking into the collector, which is a
different node and is invisible from outside the stage whenever R_C is small enough to swamp it.

Drawn against the emitter resistor, on one pair of axes, the three curves say the whole thing:

* Looking into the collector rises with EF, which is the factor arriving where it belongs.
* With a 10k resistive load the stage's output resistance is flat. Degeneration buys nothing.
* With a current-mirror load it rises, because there is no longer a resistor swamping it.

So the factor is right about the transistor and wrong about the stage, and getting the node right
is what explains why mirror loads exist at all.
"""

from __future__ import annotations

import numpy as np
import schemdraw.elements as elm

import models
import style

I_C = 1e-3
R_COLLECTOR = 10e3


def _ef_attribution(ax) -> None:
    """Where the emitter factor's boost actually lands."""
    resistors = np.logspace(0.0, 3.7, 400)

    into_collector = [
        models.resistance_into_collector(I_C, value) for value in resistors
    ]
    resistive = [
        models.ce_output_resistance(R_COLLECTOR, I_C, value) for value in resistors
    ]
    mirror_load = models.early_resistance(I_C)
    mirrored = [
        models.ce_output_resistance(mirror_load, I_C, value) for value in resistors
    ]
    claimed = [R_COLLECTOR * models.emitter_factor(I_C, value) for value in resistors]

    ax.plot(
        resistors,
        np.array(into_collector) / 1e3,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="looking into the collector",
    )
    ax.plot(
        resistors,
        np.array(mirrored) / 1e3,
        color=style.ACCENT_COLOR_3,
        linewidth=style.CURVE_WIDTH,
        label="stage, current-mirror load",
    )
    ax.plot(
        resistors,
        np.array(resistive) / 1e3,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        label=f"stage, {R_COLLECTOR / 1e3:.0f}k resistive load",
    )
    ax.plot(
        resistors,
        np.array(claimed) / 1e3,
        color=style.MUTED_COLOR,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="the tempting R_C x EF",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    style.log_x_axis(ax, [1, 10, 100, 1000])
    ax.set_xlim(1.0, 5000.0)
    # The floor is well below the lowest curve so the note underneath it has clear air.
    ax.set_ylim(2.5, 3000.0)
    ax.set_yticks([10, 100, 1000])
    ax.set_yticklabels(["10", "100", "1000"])

    style.style_axes(ax, "emitter resistor (ohm)", "resistance (kilohm)")
    style.plot_title(ax, "What the emitter factor actually multiplies")
    style.legend(ax, loc="upper left")

    # The worked point of L07 B.3, 234 ohms for EF = 10.
    chosen = 234.0
    style.annotate(
        ax,
        f"at EF = {models.emitter_factor(I_C, chosen):.0f} the stage with a resistive load\n"
        f"has not moved: {models.ce_output_resistance(R_COLLECTOR, I_C, chosen) / 1e3:.1f}k "
        f"against {models.ce_output_resistance(R_COLLECTOR, I_C, 0.0) / 1e3:.1f}k",
        (60.0, 2.9),
        color=style.ACCENT_COLOR_2,
        ha="left",
        va="bottom",
    )


def _gain_against_ef(ax) -> None:
    """What the emitter factor costs, on the same axis as what it buys.

    Gain falls as 1/EF exactly. That is the other half of the trade, and it is the half the
    obvious reading gets right: a stage with EF = 10 has given up a decade of gain.
    """
    resistors = np.logspace(0.0, 3.7, 400)

    resistive = [abs(models.ce_gain(R_COLLECTOR, I_C, value)) for value in resistors]
    factor = [models.emitter_factor(I_C, value) for value in resistors]

    ax.plot(
        resistors,
        resistive,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label=f"gain, {R_COLLECTOR / 1e3:.0f}k load",
    )
    ax.plot(
        resistors,
        factor,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="emitter factor EF",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    style.log_x_axis(ax, [1, 10, 100, 1000])
    ax.set_xlim(1.0, 5000.0)
    ax.set_ylim(0.7, 700.0)
    ax.set_yticks([1, 10, 100])
    ax.set_yticklabels(["1", "10", "100"])

    style.style_axes(ax, "emitter resistor (ohm)", "gain, and emitter factor")
    style.plot_title(ax, "Gain falls by exactly the factor EF rises")
    # Centre-left is the one band both curves leave empty: the gain is still near its ceiling
    # there and the emitter factor is still near one.
    style.legend(ax, loc="center left")

    chosen = 234.0
    style.marker(ax, chosen, abs(models.ce_gain(R_COLLECTOR, I_C, chosen)))
    style.annotate(
        ax,
        f"EF = {models.emitter_factor(I_C, chosen):.0f}: gain "
        f"{abs(models.ce_gain(R_COLLECTOR, I_C, 0.0)):.0f} becomes "
        f"{abs(models.ce_gain(R_COLLECTOR, I_C, chosen)):.0f}  ",
        (chosen, abs(models.ce_gain(R_COLLECTOR, I_C, chosen)) * 1.5),
        color=style.ACCENT_COLOR,
        ha="right",
        va="bottom",
    )


def _re_model(drawing, ax) -> None:
    """The small-signal schematic of a common-emitter stage, in the r_e model.

    What A.3's construction produces: the supply shorted to ground, the coupling capacitors
    gone, the bias divider gone, and the transistor replaced by a current source and the one
    resistance the whole course is built on.
    """
    # Two columns sharing a ground rail. The left one is the input branch, and the current the
    # input drives through it is the same current the source on the right delivers; that equality
    # is the entire model, and the label on the source is where it is stated.
    input_x = 4.0
    output_x = 14.0
    ground_y = 1.0
    base_y = 9.6
    collector_y = 7.4
    rail_y = 10.6

    # Devices first, then the wires; see diagrams/README.md.
    re_element = elm.Resistor().at((input_x, base_y)).down().length(2.4)
    emitter = elm.Resistor().at((input_x, 6.2)).down().length(2.4)
    collector = elm.Resistor().at((output_x, rail_y)).down().length(2.6)
    source = elm.SourceI().at((output_x, collector_y)).down().length(3.0)

    for element in (re_element, emitter, collector, source):
        drawing.add(element)

    # Input branch: v_in onto the base node, down through r_e and R_E to ground. The short link
    # between the two resistors is a wire like any other and is easy to leave out; without it the
    # figure shows two floating branches and says nothing.
    drawing.add(elm.Dot(open=True).at((input_x, base_y)))
    # Above the terminal, not left of it: the r_e callout owns the space to the left.
    style.text(ax, "v_in", (input_x, base_y + 0.75), size=style.LABEL_SIZE)
    style.wire(ax, (input_x, base_y - 2.4), (input_x, 6.2))
    style.wire(ax, (input_x, 3.8), (input_x, ground_y))

    # Output branch: the supply rail, now a short to ground, down through R_C to the collector
    # node, and the transistor's current pulled from that node to ground.
    drawing.add(elm.Ground().at((output_x, rail_y)))
    style.wire(ax, (output_x, rail_y - 2.6), (output_x, collector_y))
    style.wire(ax, (output_x, collector_y - 3.0), (output_x, ground_y))

    # One ground rail under both columns.
    style.wire(ax, (input_x, ground_y), (output_x, ground_y))
    drawing.add(elm.Ground().at(((input_x + output_x) / 2.0, ground_y)))

    # The output, taken at the collector node.
    style.wire(ax, (output_x, collector_y), (18.5, collector_y))
    drawing.add(elm.Dot().at((output_x, collector_y)))
    drawing.add(elm.Dot(open=True).at((18.5, collector_y)))
    style.text(ax, "v_out", (18.9, collector_y), halign="left", size=style.LABEL_SIZE)

    # Both left-column values sit on the right of their resistors, because the space to the left
    # of that column is the only place the r_e callout can go: the output column runs the full
    # height of the figure, so a leader coming in from the right would cross it.
    style.text(
        ax,
        "r_e",
        (input_x + 0.8, base_y - 1.2),
        halign="left",
        size=style.LABEL_SIZE,
        color=style.ACCENT_COLOR,
    )
    style.text(ax, "R_E", (input_x + 0.8, 5.0), halign="left", size=style.LABEL_SIZE)
    style.text(
        ax, "R_C", (output_x - 0.8, rail_y - 1.3), halign="right", size=style.LABEL_SIZE
    )

    style.callout(
        ax,
        "The supply is a short to ground here.\n"
        "A rail that does not move carries no signal,\n"
        "so every DC source becomes ground.",
        (22.0, rail_y),
        (output_x + 0.35, rail_y - 0.35),
    )
    style.callout(
        ax,
        "The one equation in the model: the current\n"
        "the input drives through r_e and R_E is the\n"
        "current the collector delivers. Divide the two\n"
        "and the gain is -R_C / (r_e + R_E).",
        (22.0, collector_y - 1.5),
        (output_x + 0.55, collector_y - 1.5),
    )
    style.callout(
        ax,
        "r_e = 26 mV / I_C.\n"
        "Not a resistor: it is the\n"
        "slope of the device's own\n"
        "exponential at the Q-point,\n"
        "so it moves when the\n"
        "current does.",
        (input_x - 1.4, base_y - 1.2),
        (input_x - 0.35, base_y - 1.2),
        halign="right",
    )


def _miller_bandwidth(ax) -> None:
    """What the Miller effect costs, and what the cascode gets back.

    The base-collector capacitance is a few picofarads and looks harmless. Across an inverting
    stage it is multiplied by the gain, and it is the reason a stage with a gain of 385 rolls off
    at a hundred kilohertz while the device itself is good to hundreds of megahertz.
    """
    gains = np.logspace(0.0, 3.0, 400)
    source = 1e3

    with_miller = [
        models.input_pole(source, models.miller_capacitance(gain)) / 1e6
        for gain in gains
    ]
    without = models.input_pole(source, models.C_BC) / 1e6

    ax.plot(
        gains,
        with_miller,
        color=style.ACCENT_COLOR,
        linewidth=style.CURVE_WIDTH,
        label="input pole, C_bc multiplied by the gain",
    )
    ax.axhline(
        without,
        color=style.ACCENT_COLOR_2,
        linewidth=style.CURVE_WIDTH,
        linestyle=(0, (5, 3)),
        label="input pole if C_bc were not multiplied",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    style.log_x_axis(ax, [1, 10, 100, 1000])
    ax.set_xlim(1.0, 1000.0)
    ax.set_ylim(0.02, 200.0)
    ax.set_yticks([0.1, 1, 10, 100])
    ax.set_yticklabels(["0.1", "1", "10", "100"])

    style.style_axes(ax, "stage gain", "input corner frequency (MHz)")
    style.plot_title(ax, f"The Miller effect, driven from {source / 1e3:.0f} kilohm")
    style.legend(ax, loc="lower left")

    plain = abs(models.ce_gain(R_COLLECTOR, I_C))
    corner = models.input_pole(source, models.miller_capacitance(plain))
    style.marker(ax, plain, corner / 1e6)
    style.annotate(
        ax,
        f"gain {plain:.0f}: {models.C_BC * 1e12:.0f} pF becomes "
        f"{models.miller_capacitance(plain) * 1e9:.1f} nF,\n"
        f"and the corner falls to {corner / 1e3:.0f} kHz  ",
        # Above the un-multiplied line, which is the one band both curves leave empty. Next to
        # the marker it sat on the falling curve.
        (1.3, 160.0),
        color=style.ACCENT_COLOR,
        ha="left",
        va="top",
    )


def _current_mirror(drawing, ax) -> None:
    """A common-emitter stage with a current mirror as its load."""
    ground_y = 1.0
    rail_y = 13.0
    mirror_y = 10.2
    amp_y = 4.6

    # Base anchors. A schemdraw transistor's device column sits LEG to the right of its base, and
    # `.reverse()` moves the base to the far side of that column rather than mirroring the whole
    # element. Both facts are measured here rather than assumed: the first attempt at this figure
    # assumed reverse() put the base where the un-reversed one has it, and the reference leg came
    # out disconnected from its own transistor.
    LEG = 0.7516666666666666
    RISE = 0.6966666666666667

    ref_base_x = 3.0
    out_base_x = 9.0

    # Devices before wires; see diagrams/README.md.
    ref_device = elm.BjtPnp().at((ref_base_x, mirror_y)).reverse()
    out_device = elm.BjtPnp().at((out_base_x, mirror_y))
    amp = elm.BjtNpn().at((out_base_x, amp_y))
    ref_resistor = elm.Resistor().at((ref_base_x + LEG, 6.6)).down().length(2.6)

    for element in (ref_device, out_device, amp, ref_resistor):
        drawing.add(element)

    ref_x = ref_base_x + LEG  # Q2's device column.
    out_x = out_base_x + LEG  # Q3's and Q1's device column.
    ref_tie_x = ref_base_x + 1.5  # Where reverse() leaves Q2's base.

    emit_y = mirror_y + RISE
    coll_y = mirror_y - RISE
    amp_coll_y = amp_y + RISE
    amp_emit_y = amp_y - RISE

    # The supply rail, with both mirror emitters onto it.
    style.wire(ax, (ref_x, rail_y), (out_x, rail_y))
    style.wire(ax, (ref_x, rail_y), (ref_x, emit_y))
    style.wire(ax, (out_x, rail_y), (out_x, emit_y))
    style.text(
        ax, "+V_CC", ((ref_x + out_x) / 2.0, rail_y + 0.7), size=style.LABEL_SIZE
    )

    # The reference leg, and the diode connection that makes Q2 set the current: its base is tied
    # to its own collector, so the pair share a base-emitter voltage and therefore a current.
    style.wire(ax, (ref_x, coll_y), (ref_x, 6.6))
    style.wire(ax, (ref_x, 4.0), (ref_x, ground_y))
    style.wire(ax, (ref_tie_x, mirror_y), (ref_tie_x, 8.5))
    style.wire(ax, (ref_tie_x, 8.5), (ref_x, 8.5))
    drawing.add(elm.Dot().at((ref_x, 8.5)))

    # The bases tied together.
    style.wire(ax, (ref_tie_x, mirror_y), (out_base_x, mirror_y))
    drawing.add(elm.Dot().at((ref_tie_x, mirror_y)))

    # The output leg: Q3's collector straight down onto Q1's collector.
    style.wire(ax, (out_x, coll_y), (out_x, amp_coll_y))
    style.wire(ax, (out_x, amp_emit_y), (out_x, ground_y))

    # Ground rail, input, output.
    style.wire(ax, (ref_x, ground_y), (out_x, ground_y))
    drawing.add(elm.Ground().at(((ref_x + out_x) / 2.0, ground_y)))

    drawing.add(elm.Dot(open=True).at((out_base_x - 4.0, amp_y)))
    style.wire(ax, (out_base_x - 4.0, amp_y), (out_base_x, amp_y))
    # Above the terminal, not left of it: the reference leg's column runs down through that space.
    style.text(ax, "v_in", (out_base_x - 4.0, amp_y + 0.75), size=style.LABEL_SIZE)

    out_y = 7.4
    style.wire(ax, (out_x, out_y), (out_x + 5.0, out_y))
    drawing.add(elm.Dot().at((out_x, out_y)))
    drawing.add(elm.Dot(open=True).at((out_x + 5.0, out_y)))
    style.text(ax, "v_out", (out_x + 5.4, out_y), halign="left", size=style.LABEL_SIZE)

    style.text(ax, "Q2", (ref_x - 0.8, 11.4), halign="right", size=style.LABEL_SIZE)
    style.text(ax, "Q3", (out_x - 0.8, 11.4), halign="right", size=style.LABEL_SIZE)
    style.text(ax, "Q1", (out_x - 0.8, 3.2), halign="right", size=style.LABEL_SIZE)
    style.text(ax, "R_REF", (ref_x - 0.8, 5.3), halign="right", size=style.LABEL_SIZE)

    # Both callouts approach from the right, one above the output wire and one below it, so
    # neither leader crosses it.
    style.callout(
        ax,
        "Q2 sets the current, Q3 copies it.\n"
        "Q3 is a load with no resistance you chose:\n"
        "what it presents is its own r_o.",
        (18.5, 11.0),
        (out_x + 0.4, coll_y),
    )
    style.callout(
        ax,
        f"This is where the emitter factor finally pays.\n"
        f"With a resistor the boost was swamped; here the\n"
        f"load is r_o, so the gain becomes -(r_o1 || r_o2) / r_e\n"
        f"and reaches "
        f"{abs(models.ce_gain_exact(models.early_resistance(I_C), I_C)):.0f} "
        f"instead of {abs(models.ce_gain(R_COLLECTOR, I_C)):.0f}.",
        (18.5, 4.4),
        (out_x + 0.4, 6.2),
    )


def _cascode(drawing, ax) -> None:
    """The cascode, drawn as what it is: degeneration by another transistor's r_o."""
    ground_y = 1.0
    rail_y = 13.0
    stage_x = 8.0
    device_x = stage_x + 0.7516666666666666

    lower = elm.BjtNpn().at((stage_x, 4.2))
    upper = elm.BjtNpn().at((stage_x, 8.4))
    load = elm.Resistor().at((device_x, rail_y)).down().length(2.6)

    for element in (lower, upper, load):
        drawing.add(element)

    lower_c = 4.2 + 0.6966666666666667
    lower_e = 4.2 - 0.6966666666666667
    upper_c = 8.4 + 0.6966666666666667
    upper_e = 8.4 - 0.6966666666666667

    style.wire(ax, (device_x, rail_y), (device_x, rail_y))
    style.text(ax, "+V_CC", (device_x, rail_y + 0.7), size=style.LABEL_SIZE)
    style.wire(ax, (device_x, rail_y - 2.6), (device_x, upper_c))
    style.wire(ax, (device_x, upper_e), (device_x, lower_c))
    style.wire(ax, (device_x, lower_e), (device_x, ground_y))
    drawing.add(elm.Ground().at((device_x, ground_y)))

    drawing.add(elm.Dot(open=True).at((stage_x - 4.0, 4.2)))
    style.wire(ax, (stage_x - 4.0, 4.2), (stage_x, 4.2))
    style.text(ax, "v_in", (stage_x - 4.4, 4.2), halign="right", size=style.LABEL_SIZE)

    drawing.add(elm.Dot(open=True).at((stage_x - 4.0, 8.4)))
    style.wire(ax, (stage_x - 4.0, 8.4), (stage_x, 8.4))
    style.text(
        ax, "V_BIAS", (stage_x - 4.4, 8.4), halign="right", size=style.LABEL_SIZE
    )

    out_y = (rail_y - 2.6 + upper_c) / 2.0
    style.wire(ax, (device_x, out_y), (device_x + 4.5, out_y))
    drawing.add(elm.Dot().at((device_x, out_y)))
    drawing.add(elm.Dot(open=True).at((device_x + 4.5, out_y)))
    style.text(
        ax, "v_out", (device_x + 4.9, out_y), halign="left", size=style.LABEL_SIZE
    )

    style.text(ax, "Q2", (stage_x - 0.5, 7.2), halign="right", size=style.LABEL_SIZE)
    style.text(ax, "Q1", (stage_x - 0.5, 3.0), halign="right", size=style.LABEL_SIZE)

    style.callout(
        ax,
        "Q1's collector barely moves now, because Q2\n"
        "holds it. No voltage swing there means no Miller\n"
        "multiplication, and the input capacitance stays\n"
        "at C_bc instead of C_bc times the gain.",
        (17.0, 5.2),
        (device_x + 0.4, (upper_e + lower_c) / 2.0),
    )
    style.callout(
        ax,
        f"Nothing new: Q2 is a degenerated stage whose\n"
        f"emitter resistor is Q1's r_o, so the emitter factor\n"
        f"applies unchanged. It would be "
        f"{models.emitter_factor(I_C, models.early_resistance(I_C)):.0f}, but the\n"
        f"boost caps at h_FE, so R_out reaches "
        f"{models.cascode_output_resistance(I_C) / 1e6:.1f} M.",
        # Below the output wire, not above it: the tap sits between the load resistor and Q2's
        # collector, so a leader coming in from above crosses it on the way to the device.
        (17.0, 8.2),
        (device_x + 0.4, upper_c),
    )


def _re_to_rs(drawing, ax) -> None:
    """The two stages side by side, and the one substitution that connects them.

    No textbook names the quantity that makes this correspondence work. Naming r_s is the whole
    of this course's MOSFET treatment: draw the same stage, write r_s for r_e, and every gain and
    output-resistance result carries over with nothing else changed.
    """
    rail_y = 12.0
    ground_y = 1.0

    bjt_base_x = 4.0
    bjt_y = 6.0
    fet_x = 16.0
    fet_drain_y = 6.697

    # Devices before wires; see diagrams/README.md.
    bjt = elm.BjtNpn().at((bjt_base_x, bjt_y))
    fet = elm.NFet().at((fet_x, fet_drain_y)).reverse()
    load_c = elm.Resistor().at((bjt_base_x + 0.7517, rail_y)).down().length(2.6)
    load_d = elm.Resistor().at((fet_x, rail_y)).down().length(2.6)
    degen_e = elm.Resistor().at((bjt_base_x + 0.7517, 4.0)).down().length(2.6)
    degen_s = elm.Resistor().at((fet_x, 4.0)).down().length(2.6)

    for element in (bjt, fet, load_c, load_d, degen_e, degen_s):
        drawing.add(element)

    bjt_x = bjt_base_x + 0.7517
    bjt_coll = bjt_y + 0.6967
    bjt_emit = bjt_y - 0.6967
    fet_source_y = fet_drain_y - 1.5
    fet_gate_y = fet_drain_y - 0.75

    # Each stage gets its own rails. One rail spanning both would say these are two halves of a
    # single circuit, which is the opposite of the point.
    for column, gate_y, gate_x, source_y in (
        (bjt_x, bjt_y, bjt_base_x, bjt_emit),
        (fet_x, fet_gate_y, fet_x - 1.37, fet_source_y),
    ):
        drawing.add(elm.Vdd().at((column, rail_y)))
        style.wire(ax, (column, rail_y - 2.6), (column, source_y + 1.394))
        style.wire(ax, (column, source_y), (column, 4.0))
        style.wire(ax, (column, 1.4), (column, ground_y))
        drawing.add(elm.Ground().at((column, ground_y)))

        drawing.add(elm.Dot(open=True).at((gate_x - 3.0, gate_y)))
        style.wire(ax, (gate_x - 3.0, gate_y), (gate_x, gate_y))
        style.text(ax, "v_in", (gate_x - 3.0, gate_y + 0.75), size=style.LABEL_SIZE)

        # On the wire between the load resistor and the device, not partway up the resistor: the
        # output node is the collector or drain, and a tap drawn inside the resistor body says
        # the output is taken from the middle of a component.
        out_y = 8.5
        style.wire(ax, (column, out_y), (column + 3.2, out_y))
        drawing.add(elm.Dot().at((column, out_y)))
        drawing.add(elm.Dot(open=True).at((column + 3.2, out_y)))
        style.text(
            ax, "v_out", (column + 3.6, out_y), halign="left", size=style.LABEL_SIZE
        )

    del bjt_coll

    style.title(ax, "common emitter", (bjt_x, rail_y + 1.6))
    style.title(ax, "common source", (fet_x, rail_y + 1.6))

    for label, (x, y), align, color in (
        ("R_C", (bjt_x - 0.8, rail_y - 1.3), "right", style.LINE_COLOR),
        ("R_E", (bjt_x - 0.8, 2.7), "right", style.LINE_COLOR),
        ("r_e", (bjt_x + 0.9, bjt_y - 0.1), "left", style.ACCENT_COLOR),
        ("R_D", (fet_x - 0.8, rail_y - 1.3), "right", style.LINE_COLOR),
        ("R_S", (fet_x - 0.8, 2.7), "right", style.LINE_COLOR),
        ("r_s", (fet_x + 0.9, fet_gate_y - 0.1), "left", style.ACCENT_COLOR),
    ):
        style.text(ax, label, (x, y), halign=align, size=style.LABEL_SIZE, color=color)

    style.callout(
        ax,
        "One substitution, and the whole of the left column carries over:\n"
        "write r_s = 1/g_m wherever r_e appears. The gain is -R_D/(r_s + R_S),\n"
        "the source factor is (r_s + R_S)/r_s, and the 220 mV rule is unchanged.\n"
        "\n"
        "The exception is input resistance. A gate draws no current, so there is\n"
        "no h_FE(r_e + R_E) term to carry over; Z_in is the bias network alone.",
        (10.4, -2.4),
        (fet_x - 0.5, fet_gate_y - 0.6),
        halign="center",
    )


EF_ATTRIBUTION = style.Plot(_ef_attribution, size=style.WIDE_SIZE)
RE_TO_RS = style.Figure(_re_to_rs, canvas=(-1.0, -5.0, 25.0, 15.0))
MILLER_BANDWIDTH = style.Plot(_miller_bandwidth, size=style.WIDE_SIZE)
CURRENT_MIRROR = style.Figure(_current_mirror, canvas=(0.0, 0.0, 31.0, 14.6))
CASCODE = style.Figure(_cascode, canvas=(0.0, 0.0, 28.0, 14.6))
GAIN_AGAINST_EF = style.Plot(_gain_against_ef)
RE_MODEL = style.Figure(_re_model, canvas=(-7.0, 0.0, 30.5, 12.4))
