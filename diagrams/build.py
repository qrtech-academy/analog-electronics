#!/usr/bin/env python3
"""Regenerate the lecture figures.

    python3 diagrams/build.py                    # every figure, into the lecture trees
    python3 diagrams/build.py divider_bias       # one figure
    python3 diagrams/build.py --outdir /tmp/x    # preview, without touching the repo
    python3 diagrams/build.py --list             # what can be built

Adding a figure: write a builder in a module next to this one, then add an entry to FIGURES below
naming every path that should receive it. A figure listed with more than one path is one that
several lectures embed, and writing all the copies from a single source is what keeps them
identical.

The generated PNGs stay committed: GitHub renders the lectures straight from the repository, so
nothing here runs during a normal build. CI has its own job that redraws every figure and diffs it
byte for byte, which is what catches a figure module edited without its PNG re-committed.

**Look at what you generate.** Colliding labels, clipped text and wires crossing a device are
invisible from the code and obvious in the PNG. Render to --outdir and open it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bias  # noqa: E402
import circuits  # noqa: E402
import device  # noqa: E402
import diffpair  # noqa: E402
import feedback  # noqa: E402
import follower  # noqa: E402
import opamp  # noqa: E402
import passives  # noqa: E402
import reactance  # noqa: E402
import smallsignal  # noqa: E402
import style  # noqa: E402

# Root directory.
ROOT = Path(__file__).resolve().parent.parent


def images(lecture: str) -> Path:
    """The image directory of one lecture's appendix, e.g. `images("L06")`."""
    return ROOT / "lectures" / lecture / "appendix/images"


# figure name -> (figure, output paths).
FIGURES: dict[str, tuple[style.Figure | style.Plot, list[Path]]] = {
    # L01 - Circuits, units, and the nodal solver.
    "divider": (circuits.DIVIDER, [images("L01") / "divider.png"]),
    "divider_loading": (
        circuits.DIVIDER_LOADING,
        [images("L01") / "divider_loading.png"],
    ),
    # L02 - Reactance, phasors, and frequency response.
    "reactance": (passives.REACTANCE, [images("L02") / "reactance.png"]),
    "rc_bode": (reactance.RC_BODE, [images("L02") / "rc_bode.png"]),
    # L03 - Passive filters and the operational amplifier.
    "filter_family": (passives.FILTER_FAMILY, [images("L03") / "filter_family.png"]),
    "resonance_q": (passives.RESONANCE_Q, [images("L03") / "resonance_q.png"]),
    "cascade_loading": (
        reactance.CASCADE_LOADING,
        [images("L03") / "cascade_loading.png"],
    ),
    # L04 - Feedback, active filters, and the diode.
    "gain_error": (feedback.GAIN_ERROR, [images("L04") / "gain_error.png"]),
    "diode_iv": (feedback.DIODE_IV, [images("L04") / "diode_iv.png"]),
    "newton_raphson": (
        feedback.NEWTON_RAPHSON,
        [images("L04") / "newton_raphson.png"],
    ),
    # L05 - The transistor as a device and as a switch.
    "bjt_output": (device.BJT_OUTPUT, [images("L05") / "bjt_output.png"]),
    "switch": (device.SWITCH, [images("L05") / "switch.png"]),
    "mosfet_regions": (device.MOSFET_REGIONS, [images("L05") / "mosfet_regions.png"]),
    "gm_comparison": (device.GM_COMPARISON, [images("L05") / "gm_comparison.png"]),
    # L06 - Biasing, and what an emitter resistor actually buys.
    "divider_bias": (bias.DIVIDER_BIAS, [images("L06") / "divider_bias.png"]),
    "drift_against_temperature": (
        bias.DRIFT_AGAINST_TEMPERATURE,
        [images("L06") / "drift_against_temperature.png"],
    ),
    "drift_against_re": (
        bias.DRIFT_AGAINST_RE,
        [images("L06") / "drift_against_re.png"],
    ),
    # L07 - Small-signal analysis: r_e, the emitter factor, and the cascode.
    "re_model": (smallsignal.RE_MODEL, [images("L07") / "re_model.png"]),
    "ef_attribution": (
        smallsignal.EF_ATTRIBUTION,
        [images("L07") / "ef_attribution.png"],
    ),
    "gain_against_ef": (
        smallsignal.GAIN_AGAINST_EF,
        [images("L07") / "gain_against_ef.png"],
    ),
    "current_mirror": (
        smallsignal.CURRENT_MIRROR,
        [images("L07") / "current_mirror.png"],
    ),
    "miller_bandwidth": (
        smallsignal.MILLER_BANDWIDTH,
        [images("L07") / "miller_bandwidth.png"],
    ),
    "cascode": (smallsignal.CASCODE, [images("L07") / "cascode.png"]),
    "re_to_rs": (smallsignal.RE_TO_RS, [images("L07") / "re_to_rs.png"]),
    # L08 - Followers and output stages.
    "emitter_follower": (
        follower.EMITTER_FOLLOWER,
        [images("L08") / "emitter_follower.png"],
    ),
    "follower_into_load": (
        follower.FOLLOWER_INTO_LOAD,
        [images("L08") / "follower_into_load.png"],
    ),
    "crossover": (follower.CROSSOVER, [images("L08") / "crossover.png"]),
    "class_ab": (follower.CLASS_AB, [images("L08") / "class_ab.png"]),
    "impedance_chain": (
        follower.IMPEDANCE_CHAIN,
        [images("L08") / "impedance_chain.png"],
    ),
    # L09 - The differential amplifier.
    "differential_pair": (
        diffpair.DIFFERENTIAL_PAIR,
        [images("L09") / "differential_pair.png"],
    ),
    "mirror_loaded_pair": (
        diffpair.MIRROR_LOADED_PAIR,
        [images("L09") / "mirror_loaded_pair.png"],
    ),
    "diffpair_transfer": (
        diffpair.DIFFPAIR_TRANSFER,
        [images("L09") / "diffpair_transfer.png"],
    ),
    "cmrr_against_tail": (
        diffpair.CMRR_AGAINST_TAIL,
        [images("L09") / "cmrr_against_tail.png"],
    ),
    # L10 - Building an operational amplifier, and the capstone.
    "opamp_stages": (opamp.OPAMP_STAGES, [images("L10") / "opamp_stages.png"]),
    "amplifier": (opamp.AMPLIFIER, [images("L10") / "amplifier.png"]),
    "gain_budget": (opamp.GAIN_BUDGET, [images("L10") / "gain_budget.png"]),
}


def main() -> int:
    """Build the figures named on the command line, or all of them.

    Exit code 0 on success; argparse exits 2 on an unknown figure or a bad option.
    """
    # The summary line of this file is the usage description.
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "figures",
        nargs="*",
        metavar="FIGURE",
        help="Figures to build. Default: all of them.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        help="Write <FIGURE>.png here instead of into the lecture trees.",
    )
    parser.add_argument(
        "--list", action="store_true", help="List the known figures and exit."
    )
    args = parser.parse_args()

    if args.list:
        for name in FIGURES:
            print(name)
        return 0

    # Check every name before drawing anything, so a typo fails at once instead of halfway through
    # a rebuild with some figures already written.
    names = args.figures or list(FIGURES)
    unknown = [name for name in names if name not in FIGURES]
    if unknown:
        parser.error(
            f"unknown figure(s): {', '.join(unknown)}\nknown: {', '.join(FIGURES)}"
        )

    for name in names:
        # --outdir replaces the lecture paths with one preview file, which is what makes it safe to
        # look at a change before it lands in the lecture trees.
        figure, paths = FIGURES[name]
        if args.outdir:
            paths = [args.outdir / f"{name}.png"]

        # Report paths relative to the repo where they are inside it, absolute otherwise.
        style.render(figure, paths)
        for path in paths:
            print(f"wrote {path.relative_to(ROOT) if ROOT in path.parents else path}")

    return 0


# Run only when executed as a script, never on import, and hand the return value to the shell as
# the exit status.
if __name__ == "__main__":
    raise SystemExit(main())
