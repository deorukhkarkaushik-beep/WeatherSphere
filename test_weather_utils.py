import csv
import unittest
from pathlib import Path

from weather_utils import rain_risk_advisory


class RainRiskAdvisoryTests(unittest.TestCase):
    def test_probability_bands_include_their_lower_boundaries(self):
        self.assertEqual(rain_risk_advisory(0.0)[0], "Low")
        self.assertEqual(rain_risk_advisory(0.25)[0], "Watch")
        self.assertEqual(rain_risk_advisory(0.50)[0], "Elevated")
        self.assertEqual(rain_risk_advisory(0.75)[0], "High")

    def test_rejects_probabilities_outside_zero_to_one(self):
        for probability in (-0.01, 1.01, float("nan")):
            with self.subTest(probability=probability):
                with self.assertRaises(ValueError):
                    rain_risk_advisory(probability)

    def test_bundled_dataset_has_expected_schema_and_rows(self):
        dataset_path = Path(__file__).with_name("weather_dataset.csv")
        with dataset_path.open(newline="", encoding="utf-8") as dataset_file:
            reader = csv.DictReader(dataset_file)
            rows = list(reader)

        self.assertEqual(
            reader.fieldnames,
            [
                "Temperature",
                "Humidity",
                "Wind_Speed",
                "Pressure",
                "Rain",
                "Next_Temperature",
            ],
        )
        self.assertEqual(len(rows), 3000)
        self.assertEqual({row["Rain"] for row in rows}, {"0", "1"})


if __name__ == "__main__":
    unittest.main()
