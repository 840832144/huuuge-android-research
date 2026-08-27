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

    def test_purchase_chain_extracts_price_currency_ticket_and_other_reward(self):
        messages = [
            {"seq": 1, "direction": "out", "data": {"lottery_ticket_color": "BRONZE", "product_id": "private-product"}},
            {"seq": 2, "direction": "in", "data": {"status": "OK", "request_id": "private-request"}},
            {
                "seq": 3,
                "direction": "out",
                "data": {
                    "request_id": "private-request",
                    "local_price": 2.98,
                    "local_currency_code": "sgd",
                    "store_iap_id": "private-store-id",
                },
            },
            {
                "seq": 4,
                "direction": "in",
                "data": {
                    "status": "OK",
                    "request_id": "private-request",
                    "provider_purchase_id": "private-order",
                    "rewards_data": {
                        "reward": [
                            {"inventory_delta": {"id": 101, "amount": "588"}},
                            {"loyalty_points": "10"},
                        ]
                    },
                },
            },
        ]
        facts = MODULE.extract_purchase_facts(messages, {101: "BRONZE"})
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["purchase_alias"], "Purchase-1")
        self.assertEqual(facts[0]["local_price"], "2.98")
        self.assertEqual(facts[0]["currency"], "SGD")
        self.assertEqual(facts[0]["ticket_color"], "BRONZE")
        self.assertEqual(facts[0]["ticket_quantity"], 588)
        self.assertEqual(facts[0]["loyalty_points"], 10)
        self.assertTrue(facts[0]["bundle_has_other_rewards"])
        self.assertEqual(facts[0]["apparent_cost_per_ticket"], "0.005068")
        self.assertIn("full price cannot be assigned to tickets", facts[0]["apparent_cost_limit"])
        self.assertNotIn("request_id", facts[0])
        self.assertNotIn("product_id", facts[0])
        self.assertNotIn("provider_purchase_id", facts[0])

    def test_purchase_chain_fails_closed_when_checkout_is_missing(self):
        messages = [
            {"seq": 1, "direction": "out", "data": {"lottery_ticket_color": "GOLD"}},
            {"seq": 2, "direction": "in", "data": {"status": "OK", "request_id": "private-request"}},
            {
                "seq": 3,
                "direction": "in",
                "data": {
                    "status": "OK",
                    "request_id": "private-request",
                    "rewards_data": {"reward": [{"inventory_delta": {"id": 303, "amount": "79"}}]},
                },
            },
        ]
        with self.assertRaisesRegex(RuntimeError, "checkout"):
            MODULE.extract_purchase_facts(messages, {303: "GOLD"})

    def test_public_spin_names_use_regular_not_paid(self):
        public_names = (
            MODULE.REGULAR_SPIN_REQUESTS_FIELD,
            MODULE.REGULAR_SPIN_RESPONSES_FIELD,
            MODULE.REGULAR_SPINS_FIELD,
            MODULE.REGULAR_SPIN_COST_METRIC,
        )
        self.assertEqual(
            public_names,
            ("regular_spin_requests", "regular_spin_responses", "regular_spins", "regular_spin_chip_cost"),
        )
        self.assertTrue(all("paid" not in name for name in public_names))


if __name__ == "__main__":
    unittest.main()
