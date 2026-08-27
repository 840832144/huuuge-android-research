import base64
import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "extract_lottery_facts.py"
SPEC = importlib.util.spec_from_file_location("extract_lottery_facts", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class LotteryFactsTests(unittest.TestCase):
    def test_big_integer_bytes_are_unsigned_big_endian(self):
        encoded = base64.b64encode((2_852_800_000).to_bytes(5, "big")).decode("ascii")
        self.assertEqual(MODULE.decode_big_integer(encoded), 2_852_800_000)
        self.assertEqual(MODULE.decode_big_integer("20000000"), 20_000_000)

    def test_reward_classification(self):
        self.assertEqual(MODULE.classify_reward({"chips_delta": "12"}), ("chips", 12))
        self.assertEqual(
            MODULE.classify_reward({"inventory_delta": {"id": 1, "amount": "3"}}),
            ("ticket_item", 3),
        )
        self.assertEqual(
            MODULE.classify_reward({"lottery_puzzle": {"color": 1, "delta": 2}}),
            ("puzzle_progress", 2),
        )

    def test_wilson_interval_contains_observed_rate(self):
        rate, low, high = MODULE.wilson_interval(148, 166)
        self.assertLess(low, rate)
        self.assertGreater(high, rate)
        self.assertAlmostEqual(rate, 148 / 166)

    def test_percentile_is_interpolated(self):
        self.assertEqual(MODULE.percentile([1.0, 2.0, 3.0, 4.0], 0.5), 2.5)


if __name__ == "__main__":
    unittest.main()
