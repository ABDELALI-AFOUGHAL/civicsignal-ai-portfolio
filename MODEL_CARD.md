# CivicSignal model card

## Intended use

CivicSignal is an offline demonstration of a transparent, daily anomaly screen for aggregate public-service incident counts. It is designed to help an analyst prioritize records for human review, not to make enforcement, safety, eligibility, or individual-level decisions.

## Method

The baseline computes a rolling z-score against the previous 14 observations. The current observation is never included in its own reference window. Scores are converted to alerts at `z >= 3`; the first five observations are marked as insufficient evidence (`0.0`). Synthetic data is generated with a fixed seed for reproducibility.

## Evaluation

The command evaluates a chronological 70/30 holdout and reports precision, recall, F1, and accuracy. These metrics are descriptive only: the labels are synthetic event flags and do not establish real-world performance. Before deployment, use retrospectively reviewed labels, report confidence intervals, inspect false positives, and measure detection lead time and calibration.

## Limitations and risks

- Counts can reflect reporting volume, staffing, or access differences rather than true disruption severity.
- A fixed threshold may behave differently across routes, neighborhoods, seasons, or reporting systems.
- Rainfall is generated as a feature in the demo but is not used by the baseline detector.
- The model can miss gradual changes and cannot distinguish data-quality failures from genuine incidents.
- Do not infer individual risk, protected characteristics, or causal effects from its output.

## Monitoring and safeguards

For a real study, document data license and coverage, validate schema and freshness, monitor missingness and score distributions, evaluate weekday/weekend and geographic slices where legally and ethically appropriate, and require human review before any operational response. Log each score with the historical window and data timestamp so alerts remain auditable.
