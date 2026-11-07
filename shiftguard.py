#!/usr/bin/env python3
"""ShiftGuard: dependency-free data-drift monitor for ML feature streams."""
from __future__ import annotations
import math, random
from dataclasses import dataclass

@dataclass(frozen=True)
class DriftReport:
    feature: str
    psi: float
    status: str

def synthetic_stream(n: int = 240, seed: int = 11) -> tuple[list[dict[str,float]], list[dict[str,float]]]:
    rng = random.Random(seed)
    ref = [{"latency_ms": max(1, rng.gauss(180, 25)), "errors": max(0, rng.gauss(2, 1))} for _ in range(n)]
    cur = [{"latency_ms": max(1, rng.gauss(235, 35)), "errors": max(0, rng.gauss(4, 1.5))} for _ in range(n)]
    return ref, cur

def psi(reference: list[float], current: list[float], bins: int = 10) -> float:
    if not reference or not current or bins < 2: raise ValueError("non-empty samples and bins >= 2 required")
    lo, hi = min(reference), max(reference)
    if hi == lo: return 0.0
    edges = [lo + (hi-lo)*i/bins for i in range(bins+1)]
    def counts(values: list[float]) -> list[float]:
        out = [0]*bins
        for value in values:
            idx = min(bins-1, max(0, int((value-lo)/(hi-lo)*bins)))
            out[idx] += 1
        return [(x + 0.5) / (len(values) + 0.5*bins) for x in out]
    rp, cp = counts(reference), counts(current)
    return sum((c-r) * math.log(c/r) for r, c in zip(rp, cp))

def monitor(reference: list[dict[str,float]], current: list[dict[str,float]], threshold: float = .2) -> list[DriftReport]:
    if not reference or not current: raise ValueError("both datasets are required")
    return [DriftReport(k, psi([r[k] for r in reference], [r[k] for r in current]), "DRIFT" if psi([r[k] for r in reference], [r[k] for r in current]) >= threshold else "STABLE") for k in reference[0]]

def main() -> None:
    ref, cur = synthetic_stream(); reports = monitor(ref, cur)
    print(f"Compared {len(ref)} reference and {len(cur)} current records")
    for r in reports: print(f"{r.feature}: PSI={r.psi:.3f} [{r.status}]")

if __name__ == "__main__": main()
