"""Fast structural validation for the experiment matrix."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REQUIRED_VARIANTS = {
    "standard",
    "shared_lie",
    "shared_strang",
    "shared_parallel",
    "shared_heun",
    "shared_learned_dt",
}
REQUIRED_BENCHMARKS = {
    "modular_addition",
    "sequence_copy",
    "associative_recall",
    "tiny_shakespeare",
}


def main(path: str) -> None:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    variants = set(data.get("variants", []))
    benchmarks = set(data.get("benchmarks", {}))
    missing_variants = REQUIRED_VARIANTS - variants
    missing_benchmarks = REQUIRED_BENCHMARKS - benchmarks
    if missing_variants or missing_benchmarks:
        raise SystemExit(
            f"invalid matrix; missing variants={sorted(missing_variants)}, "
            f"missing benchmarks={sorted(missing_benchmarks)}"
        )
    for name, cfg in data["benchmarks"].items():
        if cfg.get("enabled") and not cfg.get("primary_metric"):
            raise SystemExit(f"enabled benchmark {name!r} lacks primary_metric")
    print(f"valid: {len(variants)} variants, {len(benchmarks)} benchmarks")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/validate_matrix.py PATH")
    main(sys.argv[1])

