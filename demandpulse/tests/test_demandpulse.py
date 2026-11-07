import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from demandpulse import (  # noqa: E402
    Observation,
    metrics,
    rolling_residual_intervals,
    seasonal_forecast,
)


class DemandPulseTests(unittest.TestCase):
    def setUp(self):
        self.rows = [Observation(__import__('datetime').date(2026, 1, 1) + __import__('datetime').timedelta(days=i), i + 10, 0) for i in range(45)]

    def test_warmup_and_seasonal_lag(self):
        forecasts = seasonal_forecast(self.rows)
        self.assertIsNone(forecasts[27])
        self.assertEqual(forecasts[28], 31.0)
        self.assertEqual(forecasts[44], 47.0)

    def test_intervals_need_history(self):
        forecasts = seasonal_forecast(self.rows)
        intervals = rolling_residual_intervals(self.rows, forecasts)
        self.assertIsNone(intervals[28])
        self.assertIsNotNone(intervals[38])
        self.assertLessEqual(intervals[38][0], intervals[38][1])

    def test_metrics(self):
        result = metrics([10, 12], [9, 10], [(8, 11), (11, 13)])
        self.assertAlmostEqual(result["mae"], 1.5)
        self.assertAlmostEqual(result["rmse"], (2.5) ** 0.5)
        self.assertAlmostEqual(result["interval_coverage"], 1.0)


if __name__ == "__main__":
    unittest.main()
