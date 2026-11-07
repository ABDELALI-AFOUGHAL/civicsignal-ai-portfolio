# Portfolio Projects — 7 November 2026

## Completed this run: ShiftGuard

**ShiftGuard** is a dependency-free data-drift monitor for ML feature streams. It generates a reproducible reference/current stream, computes Population Stability Index (PSI) with smoothed histogram bins, and emits a stable/drift status per feature. This demonstrates monitoring and responsible deployment—not just model training.

Run:

```bash
python3 shiftguard.py
```

CV bullet:

> Built ShiftGuard, a reproducible Python drift-monitoring pipeline using smoothed PSI across latency and error features, with explicit thresholds and operational DRIFT/STABLE reports.

Limitations: synthetic data is only a demo; production monitoring should version schemas, use training-period reference windows, alert on missingness and freshness, validate thresholds by model performance, and review subgroup drift. PSI is a screening signal, not proof that a model is unsafe.

## Existing project: CivicSignal

CivicSignal is a privacy-preserving early-warning demo for public-service disruptions. It generates synthetic transit-like observations, computes a leakage-safe rolling z-score, and evaluates alerts on a time-based holdout. Run `python3 civicsignal.py`; see [README](README.md) and the [detailed brief](ai-data-portfolio-project-2026-11-07.md) history in Git.
