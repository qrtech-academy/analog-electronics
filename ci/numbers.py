#!/usr/bin/env python3
"""Check the numbers quoted in the appendices against diagrams/models.py.

    ci/numbers.py            Check every tagged value.
    ci/numbers.py --list     Print every tag and what it evaluates to.

Seven thousand lines of appendix quoting numbers that no longer exist is the specific way a
repository like this one rots, and it rots invisibly: nothing in a Markdown file goes red when a
constant changes underneath it. This is what goes red.

An appendix opts a number in by tagging it with the expression that produces it:

    The RF chain falls 15.45 dB short of its own resolution.
    <!-- value: 15.45 = quantization_snr(14) - CHAINS["RF"]["datasheet_snr"] -->

The expression is evaluated with `diagrams/models.py` as its namespace, so every function and
every reference-chain field in that module is available by name. If the result does not match the
quoted number to the precision the number was written to, this fails and says both values.

Tolerance is read from the quoted number itself: "15.45" is checked to two decimal places,
"15.4" to one, "15" to none. That is what a reader would assume, and it means tightening a quote
tightens its check without touching anything here.
"""

from __future__ import annotations

import importlib.util
import math
import re
import sys
from pathlib import Path

# Take this script's own directory off the import path, before anything imports numpy.
#
# Python puts a script's directory at the front of sys.path, so with this file named numbers.py
# any later `import numbers` finds it instead of the standard library's. numpy imports numbers on
# the way up, and the failure surfaces as "module 'numbers' has no attribute 'Integral'" from
# somewhere inside numpy, which points nowhere near here.
#
# Renaming the file would also fix it, and the name is worth keeping: it is what `make numbers`
# runs. So the path is cleaned instead.
_HERE = Path(__file__).resolve().parent
sys.path[:] = [e for e in sys.path if Path(e or ".").resolve() != _HERE]

SKIP_PARTS = {".git", ".venv", "libs", "build", "__pycache__", "temp"}

# <!-- value: 15.45 = quantization_snr(14) - CHAINS["RF"]["datasheet_snr"] -->
TAG = re.compile(r"<!--\s*value:\s*(?P<quoted>[-+0-9.eE]+)\s*=\s*(?P<expr>.+?)\s*-->")


def load_models(root: Path):
    """Import diagrams/models.py as a module, without requiring it to be on sys.path."""
    path = root / "diagrams" / "models.py"
    spec = importlib.util.spec_from_file_location("models", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tolerance_of(quoted: str) -> float:
    """Half a unit in the last place the number was written to.

    A quote of "15.45" claims two decimals and is checked to within 0.005; "15.4" claims one and
    is checked to within 0.05. Rounding the model's answer to the quoted precision and comparing
    for equality would do the same job, and this way the failure message can say how far out it
    was rather than only that it differed.
    """
    # Split the exponent off first. "1.5e3" claims one decimal on a mantissa, not three on a
    # value of 1500, and an rstrip of "eE+-0123456789" strips every character a fraction can
    # contain, so it always returned the empty string and the branch that used it was dead.
    mantissa = quoted.lower().split("e")[0]
    if "." not in mantissa:
        return 0.5
    return 0.5 * (10.0 ** -len(mantissa.split(".")[1]))


def main() -> int:
    """Check every tagged value, or list them."""
    listing = "--list" in sys.argv[1:]
    unknown = [arg for arg in sys.argv[1:] if arg != "--list"]
    if unknown:
        print(f"usage: {sys.argv[0]} [--list]", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parent.parent

    try:
        models = load_models(root)
    except Exception as error:  # noqa: BLE001
        # A missing or broken models.py is a skip rather than a failure: this check is about the
        # prose, and a reader who has not created the Python environment should not be told their
        # appendices are wrong.
        print(f"SKIP  cannot import diagrams/models.py ({error}).")
        return 0

    # Every name in models.py, plus the mathematics an expression is likely to want.
    namespace = {
        name: getattr(models, name) for name in dir(models) if not name.startswith("_")
    }
    namespace.update({"math": math, "abs": abs, "min": min, "max": max, "round": round})

    checked = 0
    stale = 0

    for path in sorted(root.rglob("*.md")):
        if SKIP_PARTS & set(path.relative_to(root).parts):
            continue

        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for match in TAG.finditer(line):
                quoted = match.group("quoted")
                expression = match.group("expr")
                where = f"{path.relative_to(root)}:{number}"

                try:
                    actual = float(
                        eval(expression, {"__builtins__": {}}, namespace)
                    )  # noqa: S307
                except Exception as error:  # noqa: BLE001
                    print(
                        f"{where}: cannot evaluate `{expression}`: {error}",
                        file=sys.stderr,
                    )
                    stale += 1
                    continue

                checked += 1
                expected = float(quoted)
                slack = tolerance_of(quoted)

                if listing:
                    print(f"{where}: {expression} = {actual:.6g}  (quoted {quoted})")
                elif abs(actual - expected) > slack:
                    print(
                        f"{where}: the appendix says {quoted}, but `{expression}` "
                        f"evaluates to {actual:.6g}",
                        file=sys.stderr,
                    )
                    stale += 1

    if stale:
        print(
            f"\nerror: {stale} stale value(s) out of {checked} checked.",
            file=sys.stderr,
        )
        return 1

    if checked == 0:
        print("Numbers: no appendix quotes a tagged value yet.")
        return 0

    print(f"Numbers: {checked} quoted value(s) still match diagrams/models.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
