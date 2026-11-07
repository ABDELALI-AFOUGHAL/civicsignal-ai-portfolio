import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from civicsignal import Observation, make_demo_data, metrics, seasonal_score, write_csv


class CivicSignalTests(unittest.TestCase):
    def test_demo_data_is_deterministic_and_well_formed(self):
        rows = make_demo_data(days=50, seed=3)
        self.assertEqual(rows, make_demo_data(days=50, seed=3))
        self.assertEqual(rows[0].day, date(2026, 1, 1))
        self.assertEqual(len(rows), 50)
        self.assertTrue(all(row.incidents >= 0 and row.rainfall_mm >= 0 for row in rows))

    def test_scores_use_only_prior_history(self):
        rows = [Observation(date(2026, 1, i + 1), 10, 0.0, 0) for i in range(6)]
        rows[-1] = Observation(rows[-1].day, 20, 0.0, 1)
        scores = seasonal_score(rows, window=5)
        self.assertEqual(scores[:5], [0.0] * 5)
        self.assertEqual(scores[-1], 10.0)

    def test_metrics_counts_and_validation(self):
        result = metrics([1, 0, 1, 0], [1, 1, 0, 0])
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["true_negatives"], 1)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["false_negatives"], 1)
        self.assertAlmostEqual(result["f1"], 0.5)
        with self.assertRaises(ValueError):
            metrics([1], [])
        with self.assertRaises(ValueError):
            metrics([2], [0])

    def test_csv_export_has_audit_columns(self):
        rows = make_demo_data(days=7)
        scores = seasonal_score(rows)
        with TemporaryDirectory() as tmp:
            output = Path(tmp) / "predictions.csv"
            write_csv(rows, scores, output)
            lines = output.read_text().splitlines()
        self.assertEqual(lines[0], "date,incidents,rainfall_mm,label,z_score,alert")
        self.assertEqual(len(lines), 8)


if __name__ == "__main__":
    unittest.main()
