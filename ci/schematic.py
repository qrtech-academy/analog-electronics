#!/usr/bin/env python3
"""Extract the netlist from the capstone schematic and check it is the circuit that was intended.

Two figures in this course came out silently detached from assumed schemdraw anchor geometry, and
the capstone amplifier of L10 has eleven transistors, so looking at it is not a check. This reads
the coordinates the figure builder actually emitted, unions them into nets (treating a point that
lies *on* a wire as joined to it, not only a shared endpoint), and asserts the nets the circuit is
supposed to have -- including the pairs that must **not** be joined.

Run it from the repository root:

    .venv/bin/python ci/schematic.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Drop this script's own directory from the import path before importing anything else. It is
# `ci/`, which contains `numbers.py`, and that shadows the standard library's `numbers` module for
# every package matplotlib and schemdraw pull in.
_HERE = str(Path(__file__).resolve().parent)
sys.path[:] = [entry for entry in sys.path if entry not in ("", ".", _HERE)]
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "diagrams"))

import schemdraw  # noqa: E402

import opamp  # noqa: E402
import style  # noqa: E402

TOLERANCE = 1.0e-6


def capture(builder):
    """Run a figure builder with the drawing and the axes stubbed, recording what it emitted."""
    wires: list[tuple] = []
    elements: list = []

    def spy(_ax, first, second, **_kwargs):
        wires.append((tuple(first), tuple(second)))

    style.wire = opamp.style.wire = spy
    for name in ("text", "callout", "block", "current_arrow"):
        setattr(style, name, lambda *a, **k: None)
        setattr(opamp.style, name, lambda *a, **k: None)

    # A real schemdraw drawing, not a stub. schemdraw applies `.reverse()` to an element's
    # anchors only when the drawing places it, so a stub reports every reversed device
    # un-reversed. The first version of this checker did that and reported the mirror's bases as
    # disconnected when they were not.
    real = schemdraw.Drawing()

    class Drawing:
        def add(self, element):
            real.add(element)
            elements.append(element)
            return element

    class Axes:
        def __getattr__(self, _name):
            return lambda *a, **k: None

    builder(Drawing(), Axes())
    return wires, elements


class Nets:
    """Union-find over coordinates, with points on a wire joined to that wire."""

    def __init__(self, wires):
        self.parent: dict = {}
        self.wires = wires
        for first, second in wires:
            self.union(self.key(first), self.key(second))

        # A wire that ends part-way along another wire is a T-junction, not a break. Without this
        # every connection to a supply rail reads as detached, which is how the first version of
        # this checker reported six failures against a schematic that was correct.
        for first, second in wires:
            for endpoint in (first, second):
                self.attach(endpoint)

    @staticmethod
    def key(point):
        return (round(point[0], 4), round(point[1], 4))

    def find(self, point):
        self.parent.setdefault(point, point)
        while self.parent[point] != point:
            self.parent[point] = self.parent[self.parent[point]]
            point = self.parent[point]
        return point

    def union(self, first, second):
        self.parent[self.find(first)] = self.find(second)

    def attach(self, point):
        """Join a terminal to every wire it lies on, endpoint or not."""
        key = self.key(point)
        for first, second in self.wires:
            if self.on_segment(point, first, second):
                self.union(key, self.key(first))

    @staticmethod
    def on_segment(point, first, second):
        cross = (second[0] - first[0]) * (point[1] - first[1]) - (
            second[1] - first[1]
        ) * (point[0] - first[0])
        if abs(cross) > TOLERANCE:
            return False
        dot = (point[0] - first[0]) * (second[0] - first[0]) + (point[1] - first[1]) * (
            second[1] - first[1]
        )
        length = (second[0] - first[0]) ** 2 + (second[1] - first[1]) ** 2
        return -TOLERANCE <= dot <= length + TOLERANCE

    def same(self, first, second):
        return self.find(self.key(first)) == self.find(self.key(second))


def terminals(elements, names):
    """Absolute terminal positions. schemdraw anchors are local, so the placement is added back."""
    devices = [
        element
        for element in elements
        if type(element).__name__ in ("BjtNpn", "BjtPnp")
    ]
    if len(devices) != len(names):
        raise SystemExit(f"expected {len(names)} transistors, found {len(devices)}")

    result = {}
    for name, element in zip(names, devices):
        result[name] = {
            anchor: tuple(element.absanchors[anchor])
            for anchor in ("base", "collector", "emitter")
        }
    return result


def main() -> int:
    wires, elements = capture(opamp._amplifier)
    nets = Nets(wires)

    device = terminals(
        elements, ["M1", "M2", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9"]
    )
    for anchors in device.values():
        for point in anchors.values():
            nets.attach(point)

    checks = [
        ("M1 is diode-connected", "M1", "base", "M1", "collector", True),
        ("the mirror bases are tied", "M1", "base", "M2", "base", True),
        ("M1 loads Q1", "M1", "collector", "Q1", "collector", True),
        ("M2 loads Q2", "M2", "collector", "Q2", "collector", True),
        ("the mirror emitters are on +V_CC", "M1", "emitter", "M2", "emitter", True),
        ("the pair emitters are tied", "Q1", "emitter", "Q2", "emitter", True),
        ("the pair drives the buffer", "Q2", "collector", "Q3", "base", True),
        ("the buffer is a Darlington", "Q3", "emitter", "Q4", "base", True),
        ("the buffer collectors are tied", "Q3", "collector", "Q4", "collector", True),
        ("the buffer drives stage 3", "Q4", "emitter", "Q5", "base", True),
        ("stage 3 drives the output stage", "Q5", "collector", "Q6", "base", True),
        ("the upper output is a Darlington", "Q6", "emitter", "Q7", "base", True),
        ("the upper collectors are tied", "Q6", "collector", "Q7", "collector", True),
        ("the lower output is a Darlington", "Q8", "emitter", "Q9", "base", True),
        ("the lower collectors are tied", "Q8", "collector", "Q9", "collector", True),
        ("the output devices are on +V_CC", "Q6", "collector", "M1", "emitter", True),
        ("stage 3's emitter is on -V_EE", "Q5", "emitter", "Q8", "collector", True),
        ("the bias diodes are not shorted", "Q6", "base", "Q8", "base", False),
        (
            "the emitter resistors are not shorted",
            "Q7",
            "emitter",
            "Q9",
            "emitter",
            False,
        ),
        ("the rails are not shorted", "M1", "emitter", "Q9", "collector", False),
        ("the Miller capacitor is not a wire", "Q5", "collector", "Q5", "base", False),
        ("the tail source is not a wire", "Q1", "emitter", "Q9", "collector", False),
    ]

    failures = 0
    for label, first, first_anchor, second, second_anchor, expected in checks:
        joined = nets.same(device[first][first_anchor], device[second][second_anchor])
        ok = joined == expected
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}")

    print()
    if failures:
        print(f"{failures} problem(s) in the capstone schematic")
        return 1
    print(f"capstone schematic: {len(checks)} net assertions hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
