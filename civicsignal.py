#!/usr/bin/env python3
"""CivicSignal: deterministic, explainable service-disruption early warning demo.

Runs with the Python standard library only, making the example reproducible offline.
"""
from __future__ import annotations
import csv, math, random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

@dataclass(frozen=True)
class Observation:
    day: date
    incidents: int
    rainfall_mm: float
    label: int


def make_demo_data(days: int = 120, seed: int = 7) -> list[Observation]:
    rng = random.Random(seed)
    start = date(2026, 1, 1)
    out = []
    for i in range(days):
        d = start + timedelta(days=i)
        rain = max(0.0, rng.gauss(4, 5))
        seasonal = 6 + (2 if d.weekday() >= 5 else 0)
        event = 1 if i in {43, 44, 45, 88, 89, 90} else 0
        incidents = max(0, int(round(seasonal + rain * .35 + rng.gauss(0, 1.8) + event * 16)))
        out.append(Observation(d, incidents, round(rain, 2), event))
    return out


def seasonal_score(rows: list[Observation], window: int = 14) -> list[float]:
    scores = []
    for i, row in enumerate(rows):
        history = rows[max(0, i-window):i]
        if len(history) < 5:
            scores.append(0.0); continue
        vals = [x.incidents for x in history]
        mean = sum(vals) / len(vals)
        std = math.sqrt(sum((x-mean)**2 for x in vals) / len(vals)) or 1.0
        scores.append((row.incidents - mean) / std)
    return scores


def metrics(labels: list[int], predictions: list[int]) -> dict[str, float]:
    """Return binary classification metrics, rejecting malformed inputs."""
    if len(labels) != len(predictions):
        raise ValueError("labels and predictions must have the same length")
    if any(value not in (0, 1) for value in [*labels, *predictions]):
        raise ValueError("labels and predictions must contain only 0 or 1")
    tp = sum(a == b == 1 for a, b in zip(labels, predictions))
    tn = sum(a == b == 0 for a, b in zip(labels, predictions))
    fp = sum(a == 0 and b == 1 for a, b in zip(labels, predictions))
    fn = sum(a == 1 and b == 0 for a, b in zip(labels, predictions))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = (tp + tn) / len(labels) if labels else 0.0
    return {
        "precision": precision, "recall": recall, "f1": f1, "accuracy": accuracy,
        "true_positives": tp, "true_negatives": tn,
        "false_positives": fp, "false_negatives": fn,
    }


def write_csv(rows: list[Observation], scores: list[float], path: Path) -> None:
    with path.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["date", "incidents", "rainfall_mm", "label", "z_score", "alert"])
        for row, score in zip(rows, scores):
            w.writerow([row.day, row.incidents, row.rainfall_mm, row.label, f"{score:.3f}", int(score >= 3)])


def main() -> None:
    root = Path(__file__).parent
    rows = make_demo_data(); scores = seasonal_score(rows)
    cutoff = int(len(rows) * .7)
    pred = [int(s >= 3) for s in scores[cutoff:]]
    labels = [r.label for r in rows[cutoff:]]
    result = metrics(labels, pred)
    out = root / "civicsignal_predictions.csv"; write_csv(rows, scores, out)
    print(f"Wrote {out.name} ({len(rows)} rows)")
    print("Time-based holdout metrics:", ", ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}" for k,v in result.items()))
    print("Latest alert:", "YES" if scores[-1] >= 3 else "NO", f"(z={scores[-1]:.2f})")

if __name__ == "__main__": main()
