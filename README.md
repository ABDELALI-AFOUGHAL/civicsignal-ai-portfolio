# CivicSignal

A small, reproducible, privacy-preserving early-warning demo for public-service disruptions. It generates synthetic transit-like incident observations, computes a transparent rolling z-score, and evaluates alerts on a time-based holdout.

## Run

```bash
python3 civicsignal.py
```

The command writes `civicsignal_predictions.csv` and prints precision, recall, F1, accuracy, and the latest alert state. Run the regression tests with `python3 -m unittest -v`. A concise model card is included in [`MODEL_CARD.md`](MODEL_CARD.md). The demo intentionally uses synthetic data so no credentials, personal data, or restricted datasets are required. Replace `make_demo_data` with a licensed city open-data downloader for a real study.

## Method and limitations

The baseline compares each day's incident count with the previous 14 observations. A z-score ≥ 3 becomes an alert. This is deliberately interpretable and avoids leakage: only prior observations are used. Synthetic labels are not evidence of real-world performance; a real deployment needs historical retrospective labels, calibration checks, subgroup error analysis, data freshness monitoring, and human review of false positives.

## CV-ready summary

Built a standard-library Python pipeline that generates 120 timestamped service observations, applies a leakage-safe rolling anomaly baseline, evaluates a time-based holdout, and exports auditable evidence for each alert. Next step: connect a licensed open-data API and add DuckDB, schema validation, and a dashboard.
