# Portfolio Project: **CivicSignal — Auditable Early-Warning System for Local Service Disruptions**

## One-line pitch
Build a privacy-preserving pipeline that detects and explains emerging public-service disruptions (transit delays, outages, clinic closures, or severe weather impacts) from open data, while exposing uncertainty and possible reporting bias.

This is a strong AI/data project because it combines data engineering, time-series modelling, NLP, geospatial analysis, evaluation, and responsible AI rather than presenting a generic chatbot.

## Scope for 1–2 weeks

Choose **one city** and **one service domain** (public transit is easiest). Produce a daily batch pipeline and a small dashboard; do not promise real-time emergency response.

## Data sources

- City open-data API: service alerts, incidents, schedules, or 311 requests.
- Weather observations/alerts from [NOAA](https://www.noaa.gov/) or the relevant national meteorological service.
- Optional: GTFS static/realtime feeds from [MobilityDatabase](https://mobilitydatabase.org/).
- Optional text source: official agency notices. Avoid scraping private accounts or collecting personal identifiers.

Document licenses, timestamp coverage, missingness, and any geographic or language bias.

## Technical design

1. **Ingest:** Python, requests, and DuckDB; validate schemas with Pandera.
2. **Transform:** dbt or SQL models; deduplicate alerts, normalize timestamps, and create service-area features.
3. **Features:** rolling incident counts, anomaly scores, weather severity, route/zone concentration, and text embeddings for alert similarity.
4. **Models:** baseline seasonal z-score; compare with Isolation Forest or a lightweight temporal model. Use a small multilingual sentence-transformer only if the selected city needs it.
5. **Explainability:** show the top contributing signals, comparable historical events, confidence, and a clear “insufficient evidence” state.
6. **Serving:** Streamlit dashboard plus a scheduled GitHub Actions job; package with Docker.

## Evaluation

- **Detection:** precision, recall, F1, and average detection lead time against retrospectively labelled incidents.
- **Calibration:** reliability curve and Brier score for alert probabilities.
- **Operations:** pipeline success rate, data freshness, and runtime.
- **Robustness:** evaluate separately by neighborhood/route, weekday versus weekend, and high- versus low-reporting areas.
- **Responsible AI:** manually inspect false positives; never infer individual risk or use protected attributes.

## Deliverables

- Reproducible repository with `README`, data dictionary, architecture diagram, and one-command local run.
- Cleaned sample data or a downloader (not restricted raw data).
- Evaluation notebook comparing a transparent baseline with the ML model.
- Dashboard showing alert timeline, map/route view, evidence, uncertainty, and known limitations.
- Short model card covering intended use, out-of-scope use, bias risks, and monitoring plan.

## Suggested 10-day plan

- **Days 1–2:** select city/domain, confirm licenses, ingest one source, define label.
- **Days 3–4:** build validated DuckDB tables and baseline anomaly detector.
- **Days 5–6:** add weather/text features and compare one ML model.
- **Days 7–8:** evaluate by subgroup and create dashboard.
- **Day 9:** write model card and architecture documentation.
- **Day 10:** deploy demo, record a 90-second walkthrough, and polish CV bullets.

## CV bullets (replace placeholders with measured results)

- Built a reproducible DuckDB/Python pipeline combining **[N]** open-data records with weather and agency notices; added schema checks, deduplication, and freshness monitoring.
- Compared a seasonal baseline with Isolation Forest, achieving **[F1]** at **[precision]** precision and **[lead time]** average early-warning lead time on a time-based holdout.
- Shipped a Streamlit dashboard and model card that expose evidence, calibration, subgroup error rates, and an explicit insufficient-evidence state.

## Interview talking points

- Why a transparent seasonal baseline is necessary before using ML.
- How time-based splits prevent leakage from future alerts.
- Why calibration and false-positive review matter more than a single leaderboard score.
- How you would move from batch analysis to monitored production service safely.
