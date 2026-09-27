"""Run with: python3 -m unittest discover -v"""
import unittest
from bmi_calculator import calculate_bmi, bmi_category, positive_number


class TestBMI(unittest.TestCase):
    def test_example(self):
        self.assertAlmostEqual(calculate_bmi(70, 1.75), 22.857142857, places=6)
        self.assertEqual(bmi_category(calculate_bmi(70, 1.75)), "Normal")

    def test_exact_boundaries(self):
        for number, expected in [(18.4999, "Underweight"), (18.5, "Normal"),
                                 (24.999, "Normal"), (25, "Overweight"),
                                 (29.999, "Overweight"), (30, "Obese")]:
            with self.subTest(number=number):
                self.assertEqual(bmi_category(number), expected)

    def test_bad_inputs(self):
        for value in ("", "hello", "-2", "0", "nan", "inf"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                positive_number(value, "Weight")
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)
        with self.assertRaises(ValueError):
            calculate_bmi(1e308, 1e-300)


if __name__ == "__main__":
    unittest.main()
