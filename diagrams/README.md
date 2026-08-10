# Diagrams

Every figure in the lectures is generated from this directory. Nothing is drawn by hand, and no
figure is copied in from anywhere.

```bash
python3 -m venv .venv                                # once
.venv/bin/pip install -r diagrams/requirements.txt   # once

make diagrams                        # redraw every figure into the lecture trees
make diagrams FIGURE=divider_bias    # redraw one
.venv/bin/python diagrams/build.py --list
.venv/bin/python diagrams/build.py --outdir /tmp/preview   # preview, repo untouched
```

---

## Why every figure is generated

No figure in this course is a bitmap somebody drew once. A rasterised schematic cannot be
relabelled, cannot be corrected, and cannot be checked against the numbers the appendix quotes; it
can only be redrawn from scratch when any of those turn out to be needed, which they always do.

So the topology, the component values and the content of every callout are what the appendix
needs, and every pixel is generated from the code in this directory. `ci/schematic.py` then reads
the coordinates back out of the capstone and asserts the circuit is wired the way L10 says.

---

## The files

| File             | What it holds                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| `style.py`       | Every visual constant, both figure kinds, and the render pass. Figure modules never name a colour.    |
| `models.py`      | The physics. Numbers an appendix tags with `<!-- value: ... -->` are checked here by `ci/numbers.py`. |
| `build.py`       | The registry: figure name to builder and output paths.                                                |
| `circuits.py`    | L01: the divider, and what a load does to it.                                                         |
| `reactance.py`   | L02 and L03: the first-order response, and what cascading costs.                                      |
| `passives.py`    | L02 and L03: reactance against frequency, the filter family, and Q.                                   |
| `feedback.py`    | L04: gain error, the diode, and why a solver damps its step.                                          |
| `device.py`      | L05: both devices, the switch and its load line, and the transconductance gap between them.           |
| `bias.py`        | L06: the quiescent point and thermal drift.                                                           |
| `smallsignal.py` | L07: the r_e model, what the emitter factor costs, and where its boost lands.                         |
| `follower.py`    | L08: the follower, why an output stage needs current, and crossover.                                  |
| `diffpair.py`    | L09: the pair, and why rejection is a property of the tail.                                           |
| `opamp.py`       | L10: the three stages, and the gain budget loading takes a third of.                                  |

`models.py` is also this course's copy of calculations the reader implements in C++. Where the
two disagree, that is the exercise.

---

## Rules that cost time when broken

**Place every device before any wire, ground or rail.** schemdraw's `.reverse()` is relative to
the drawing's current direction, and adding a `Ground` changes that direction; a transistor added
afterwards comes out mirrored while its anchor coordinates still read correctly. The symptom is
diagonal wires across the figure.

**Do not use schemdraw's `.label()` on a vertical element.** It centres the text on the wire and
gives no way to choose a side. Place values with `style.text` and an explicit side. Four labels
collided the first time this was done the easy way.

**Look at every figure you generate.** Render to `--outdir` and open the PNG. Colliding labels,
clipped text and a wire crossing a device are invisible from the code and obvious in the image.
Every figure currently here needed at least one layout pass after it first rendered correctly.

---

## Determinism

The dependency pins in `requirements.txt` are exact and `style.py` quantises to a fixed palette, so
a rebuild is byte-identical. CI redraws every figure and runs
`git diff --exit-code -- 'lectures/*/appendix/images/*.png'`, which is what catches a figure module
edited without its PNG re-committed. Check it locally the same way:

```bash
make diagrams && git diff --exit-code -- 'lectures/*/appendix/images/*.png'
```

---
