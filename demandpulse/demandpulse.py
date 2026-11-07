#!/usr/bin/env python3
"""DemandPulse: deterministic, leakage-safe demand forecasting demo."""
from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


@dataclass(frozen=True)
class Observation:
    day: date
    demand: int
    promotion: int


def make_demo_data(days: int = 180, seed: int = 23) -> list[Observation]:
    """Create realistic-looking, non-sensitive daily demand observations."""
    rng = random.Random(seed)
    start = date(2026, 1, 1)
    rows: list[Observation] = []
    for i in range(days):
        day = start + timedelta(days=i)
        promotion = int(i in {35, 36, 37, 92, 93, 94, 145, 146})
        weekday = 8 if day.weekday() < 5 else 5
        trend = i * 0.025
        demand = max(0, round(weekday + trend + promotion * 7 + rng.gauss(0, 1.5)))
        rows.append(Observation(day, demand, promotion))
    return rows


def seasonal_forecast(rows: list[Observation], lag: int = 7, warmup: int = 28) -> list[float | None]:
    """Forecast using only the value observed exactly one seasonal lag ago."""
    forecasts: list[float | None] = []
    for i, row in enumerate(rows):
        del row
        forecasts.append(float(rows[i - lag].demand) if i >= warmup else None)
    return forecasts


def rolling_residual_intervals(rows: list[Observation], forecasts: list[float | None], window: int = 28) -> list[tuple[float, float] | None]:
    """Build empirical 90% intervals from residuals strictly before each day."""
    intervals: list[tuple[float, float] | None] = []
    for i, forecast in enumerate(forecasts):
        if forecast is None:
            intervals.append(None)
            continue
        residuals = [rows[j].demand - forecasts[j] for j in range(max(0, i - window), i) if forecasts[j] is not None]
        if len(residuals) < 10:
            intervals.append(None)
            continue
        residuals.sort()
        lo = residuals[max(0, math.floor(0.05 * (len(residuals) - 1)))]
        hi = residuals[min(len(residuals) - 1, math.ceil(0.95 * (len(residuals) - 1)))]
        intervals.append((max(0.0, forecast + lo), max(0.0, forecast + hi)))
    return intervals


def metrics(actual: list[int], forecasts: list[float], intervals: list[tuple[float, float]]) -> dict[str, float]:
    errors = [a - f for a, f in zip(actual, forecasts)]
    coverage = sum(lo <= a <= hi for a, (lo, hi) in zip(actual, intervals)) / len(actual)
    return {
        "mae": sum(abs(e) for e in errors) / len(errors),
        "rmse": math.sqrt(sum(e * e for e in errors) / len(errors)),
        "interval_coverage": coverage,
        "average_interval_width": sum(hi - lo for lo, hi in intervals) / len(intervals),
    }


def write_csv(rows: list[Observation], forecasts: list[float | None], intervals: list[tuple[float, float] | None], path: Path) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "demand", "promotion", "forecast", "lower_90", "upper_90"])
        for row, forecast, interval in zip(rows, forecasts, intervals):
            writer.writerow([row.day, row.demand, row.promotion, "" if forecast is None else f"{forecast:.2f}",
                             "" if interval is None else f"{interval[0]:.2f}",
                             "" if interval is None else f"{interval[1]:.2f}"])


def main() -> None:
    root = Path(__file__).parent
    rows = make_demo_data()
    forecasts = seasonal_forecast(rows)
    intervals = rolling_residual_intervals(rows, forecasts)
    cutoff = int(len(rows) * 0.7)
    scored = [(r.demand, f, iv) for r, f, iv in zip(rows[cutoff:], forecasts[cutoff:], intervals[cutoff:]) if f is not None and iv is not None]
    actual, point, bands = zip(*scored)
    result = metrics(list(actual), list(point), list(bands))
    output = root / "demandpulse_predictions.csv"
    write_csv(rows, forecasts, intervals, output)
    print(f"Wrote {output.name} ({len(rows)} rows)")
    print("Time-based holdout:", ", ".join(f"{key}={value:.3f}" for key, value in result.items()))


if __name__ == "__main__":
    main()
