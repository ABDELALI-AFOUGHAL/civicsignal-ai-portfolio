# DemandPulse: leakage-safe demand forecasting with uncertainty

DemandPulse is a small, reproducible portfolio project for inventory planning. It generates a synthetic daily demand series with weekday seasonality, promotion shocks, and a trend; forecasts future demand using only observations available at prediction time; and exports prediction intervals plus a time-based backtest.

## Why this project

Instead of optimizing a single point estimate, the pipeline answers an operational question: **how much stock is needed to cover likely demand?** The baseline is deliberately transparent (seasonal naive forecast with a rolling residual interval), making it easy to audit and improve with gradient boosting later.

## Run

```bash
python3 demandpulse.py
python3 -m unittest discover -s tests -v
```

The script writes `demandpulse_predictions.csv` beside itself and prints MAE, RMSE, interval coverage, and average interval width on a final time-based holdout. It uses only the Python standard library and has no network or credential requirements.

## Data and method

The demo data is synthetic and contains no personal information. A real extension would ingest licensed SKU/day sales data, document stock-out censoring, and preserve product-level access controls. The forecast for day *t* uses the demand from seven days earlier (`t-7`), while uncertainty is estimated from prior one-week-ahead residuals only. The first 28 days are a warm-up period; the last 30% is held out chronologically.

The 90% interval is an empirical residual interval (5th–95th percentile), not a guarantee. Coverage can fail under promotions, stock-outs, or regime changes. Production use should add missingness checks, drift monitoring, intermittent-demand models, hierarchical reconciliation, and a human override.

## Files

- `demandpulse.py` — data generation, leakage-safe forecasting, metrics, CSV export, CLI.
- `tests/test_demandpulse.py` — deterministic unit tests for leakage, metrics, and interval behavior.
- `demandpulse_predictions.csv` — generated output after running the CLI (ignored as a build artifact in a larger repository).

## CV value

- Built a leakage-safe time-series backtest with a seasonal-naive baseline and empirical 90% prediction intervals.
- Evaluated operational uncertainty using MAE, RMSE, interval coverage, and width rather than a single accuracy score.
- Produced an auditable, dependency-free forecasting artifact and documented stock-out and distribution-shift limitations.
