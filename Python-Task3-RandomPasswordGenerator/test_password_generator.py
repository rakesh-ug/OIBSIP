"""Run with: python3 -m unittest discover -v"""
import unittest
from password_generator import CHARACTER_GROUPS, AMBIGUOUS, generate_password


class TestGenerator(unittest.TestCase):
    def test_all_groups_guaranteed(self):
        for _ in range(50):
            password = generate_password(24, list(CHARACTER_GROUPS))
            self.assertEqual(len(password), 24)
            for pool in CHARACTER_GROUPS.values():
                self.assertTrue(any(char in pool for char in password))

    def test_exclusion_and_freshness(self):
        samples = [
            generate_password(20, ["uppercase", "lowercase", "numbers", "symbols"], True)
            for _ in range(20)
        ]
        self.assertEqual(len(set(samples)), len(samples))
        self.assertTrue(all(not any(c in AMBIGUOUS for c in s) for s in samples))

    def test_bad_options(self):
        for length, groups in [(7, ["uppercase", "numbers"]),
                               (129, ["uppercase", "numbers"]),
                               (8, ["uppercase"]),
                               (8, []),
                               (8, ["uppercase", "oops"]),
                               (8, ["uppercase", "uppercase"])]:
            with self.subTest(length=length, groups=groups), self.assertRaises(ValueError):
                generate_password(length, groups)


if __name__ == "__main__":
    unittest.main()
