#!/usr/bin/env python3
"""Build sanitized, report-specific Lottery fact tables from one finalized Session."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable


COLORS = ("BRONZE", "SILVER", "GOLD", "BLACK")
REGULAR_SPIN_REQUESTS_FIELD = "regular_spin_requests"
REGULAR_SPIN_RESPONSES_FIELD = "regular_spin_responses"
REGULAR_SPINS_FIELD = "regular_spins"
REGULAR_SPIN_COST_METRIC = "regular_spin_chip_cost"
CLAIM_COLUMNS = (
    "claim_type",
    "evidence_source",
    "evidence_level",
    "endpoint",
    "field_path",
    "sample_count",
    "limits",
)


def decode_big_integer(value: Any) -> int:
    """Decode protobuf JSON bytes used by Casino.Chips as unsigned big-endian."""
    text = str(value)
    if text.lstrip("-").isdigit():
        return int(text)
    return int.from_bytes(base64.b64decode(text), "big", signed=False)


def chip_value(reward: dict[str, Any]) -> int | None:
    value = (reward.get("big_chips_delta") or {}).get("value")
    if value is None:
        value = reward.get("chips_delta")
    return None if value is None else decode_big_integer(value)


def classify_reward(reward: dict[str, Any]) -> tuple[str, int | None]:
    if "chips_delta" in reward or "big_chips_delta" in reward:
        return "chips", chip_value(reward)
    if "inventory_delta" in reward:
        return "ticket_item", int(reward["inventory_delta"].get("amount", 0))
    if "lottery_puzzle" in reward:
        return "puzzle_progress", int(reward["lottery_puzzle"].get("delta", 0))
    if "collectibles_box" in reward or "collectibles_box_info" in reward:
        return "collectible_box", 1
    if "extra_item_boost" in reward:
        return "time_boost", 1
    if "charms_trade_token_delta" in reward:
        return "charms_token", int(reward.get("charms_trade_token_delta", 0))
    return "other", 1


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float, float]:
    if total <= 0:
        return 0.0, 0.0, 0.0
    rate = successes / total
    denominator = 1 + z * z / total
    center = (rate + z * z / (2 * total)) / denominator
    half = z * math.sqrt(rate * (1 - rate) / total + z * z / (4 * total * total)) / denominator
    return rate, max(0.0, center - half), min(1.0, center + half)


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def money_text(value: Any) -> str:
    """Return a stable two-decimal amount without accepting missing/invalid prices."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise RuntimeError("Purchase local_price is missing or invalid.") from exc
    if not amount.is_finite() or amount < 0:
        raise RuntimeError("Purchase local_price is missing or invalid.")
    return format(amount.quantize(Decimal("0.01")), "f")


def extract_purchase_facts(messages: list[dict[str, Any]], id_to_color: dict[int, str]) -> list[dict[str, Any]]:
    """Pair two-stage IAP messages locally and return identifier-free purchase facts."""
    pending_previews: list[dict[str, Any]] = []
    by_request: dict[str, dict[str, Any]] = {}
    facts: list[dict[str, Any]] = []

    for message in sorted(messages, key=lambda item: int(item["seq"])):
        direction = str(message["direction"])
        data = message["data"]
        request_id = data.get("request_id")

        if direction == "out" and data.get("lottery_ticket_color") in COLORS and not request_id:
            pending_previews.append({"ticket_color": data["lottery_ticket_color"]})
            continue

        if direction == "in" and request_id and "rewards_data" not in data:
            if not pending_previews:
                raise RuntimeError("Purchase initialization response has no preceding Lottery preview.")
            by_request[str(request_id)] = {"preview": pending_previews.pop(0)}
            continue

        if direction == "out" and request_id and "local_price" in data:
            state = by_request.get(str(request_id))
            if state is None:
                raise RuntimeError("Purchase checkout request cannot be linked to its preview.")
            state["checkout"] = data
            continue

        if direction == "in" and request_id and "rewards_data" in data:
            state = by_request.pop(str(request_id), None)
            if state is None or "checkout" not in state:
                raise RuntimeError("Purchase reward response cannot be linked to its checkout.")
            checkout = state["checkout"]
            currency = str(checkout.get("local_currency_code") or "").strip().upper()
            if not currency:
                raise RuntimeError("Purchase local_currency_code is missing.")

            ticket_quantities: Counter[str] = Counter()
            loyalty_points = 0
            other_reward_types: set[str] = set()
            for reward in ((data.get("rewards_data") or {}).get("reward") or []):
                inventory = reward.get("inventory_delta")
                if inventory and int(inventory.get("id", -1)) in id_to_color:
                    ticket_quantities[id_to_color[int(inventory["id"])]] += int(inventory.get("amount", 0))
                elif "loyalty_points" in reward:
                    loyalty_points += int(reward.get("loyalty_points", 0))
                    other_reward_types.add("loyalty_points")
                else:
                    category, _ = classify_reward(reward)
                    other_reward_types.add(category)

            preview_color = state["preview"]["ticket_color"]
            if set(ticket_quantities) != {preview_color} or ticket_quantities[preview_color] <= 0:
                raise RuntimeError("Purchase ticket grant does not match the preview color.")
            ticket_quantity = ticket_quantities[preview_color]
            price = money_text(checkout.get("local_price"))
            apparent_cost = Decimal(price) / Decimal(ticket_quantity)
            facts.append(
                {
                    "purchase_alias": f"Purchase-{len(facts) + 1}",
                    "success": data.get("status") == "OK",
                    "local_price": price,
                    "currency": currency,
                    "ticket_color": preview_color,
                    "ticket_quantity": ticket_quantity,
                    "loyalty_points": loyalty_points,
                    "other_reward_types": ";".join(sorted(other_reward_types)),
                    "bundle_has_other_rewards": bool(other_reward_types),
                    "apparent_cost_per_ticket": format(apparent_cost.quantize(Decimal("0.000001")), "f"),
                    "apparent_cost_limit": "bundle includes other rewards; full price cannot be assigned to tickets" if other_reward_types else "ticket-only bundle in decoded rewards",
                }
            )

    if pending_previews or by_request:
        raise RuntimeError("Purchase message chain is incomplete.")
    return facts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-dir", required=True, type=Path)
    parser.add_argument("--analysis-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--session-alias", default="LOT-20260827-A")
    args = parser.parse_args()

    session_dir = args.session_dir.resolve()
    analysis_dir = args.analysis_dir.resolve()
    output_dir = args.output_dir.resolve()
    manifest = read_json(session_dir / "manifest.json")
    if manifest.get("status") != "stopped":
        raise RuntimeError("Session manifest is not stopped.")

    with (session_dir / "index.csv").open(encoding="utf-8-sig", newline="") as handle:
        index_rows = list(csv.DictReader(handle))
    raw_count = len(list((session_dir / "raw").glob("*.rpc.bin")))
    json_count = len(list((session_dir / "json").glob("*.json")))
    if not (len(index_rows) == raw_count == json_count == int(manifest.get("message_count", -1))):
        raise RuntimeError("Index/raw/JSON/manifest counts differ.")
    if int(manifest.get("decoded_count", -1)) != json_count:
        raise RuntimeError("Decoded count is incomplete.")

    markers = [json.loads(line) for line in (session_dir / "markers.jsonl").read_text(encoding="utf-8-sig").splitlines() if line]
    marker_events = {item.get("event") for item in markers}
    required_markers = {"collector-start", "hooks-installed", "collector-ready", "collector-stop"}
    if not required_markers.issubset(marker_events):
        raise RuntimeError("Lifecycle evidence is incomplete.")

    def payload(row: dict[str, str]) -> dict[str, Any]:
        return read_json(Path(row["json_file"]))["data"]

    inventory_rows = list(csv.DictReader((analysis_dir / "rpc_inventory.csv").open(encoding="utf-8-sig", newline="")))
    field_rows = list(csv.DictReader((analysis_dir / "field_paths.csv").open(encoding="utf-8-sig", newline="")))

    lottery_configs: list[tuple[dict[str, str], dict[str, Any]]] = []
    for row in index_rows:
        if row["service"] == "AppClient" and row["method"] == "AddDciEvent":
            data = payload(row)
            if "lottery" in data:
                lottery_configs.append((row, data["lottery"]))
    if not lottery_configs:
        raise RuntimeError("No live Lottery config was found.")
    config = lottery_configs[0][1]

    id_to_color: dict[int, str] = {}
    for group in config.get("tickets_products") or []:
        color = group.get("ticket_color")
        for product in group.get("product") or []:
            for reward_data in product.get("reward_data") or []:
                inventory = (reward_data.get("reward") or {}).get("inventory_delta")
                if inventory and color in COLORS:
                    id_to_color[int(inventory["id"])] = color
    if set(id_to_color.values()) != set(COLORS):
        raise RuntimeError("Ticket ID/color mapping is incomplete.")
    color_to_id = {color: item_id for item_id, color in id_to_color.items()}

    toss_requests = [row for row in index_rows if row["service"] == "AppServer" and row["method"] == "LotteryToss" and row["direction"] == "out"]
    toss_responses = [row for row in index_rows if row["service"] == "AppServer" and row["method"] == "LotteryToss" and row["direction"] == "in"]
    if len(toss_requests) != len(toss_responses):
        raise RuntimeError("LotteryToss request/response counts differ.")

    toss_pairs: list[tuple[dict[str, str], dict[str, Any], dict[str, Any]]] = []
    for request_row, response_row in zip(toss_requests, toss_responses):
        request = payload(request_row)["data"]
        response = payload(response_row)
        if response.get("data", {}).get("ticket_color") != request.get("ticket_color"):
            raise RuntimeError("LotteryToss color pairing failed.")
        if int(response.get("data", {}).get("ticket_number", -1)) != int(request.get("ticket_number", -2)):
            raise RuntimeError("LotteryToss quantity pairing failed.")
        toss_pairs.append((request_row, request, response))

    spin_requests = [row for row in index_rows if row["service"] == "SlotsGameServer" and row["method"] == "Spin" and row["direction"] == "out"]
    spin_responses = [row for row in index_rows if row["service"] == "SlotsGameServer" and row["method"] == "Spin" and row["direction"] == "in"]
    free_spin_requests = [row for row in index_rows if row["service"] == "SlotsGameServer" and row["method"] == "FreeSpin" and row["direction"] == "out"]
    free_spin_responses = [row for row in index_rows if row["service"] == "SlotsGameServer" and row["method"] == "FreeSpin" and row["direction"] == "in"]
    if len(spin_requests) != len(spin_responses) or len(free_spin_requests) != len(free_spin_responses):
        raise RuntimeError("Spin request/response pairing failed.")
    bet_values = [int(payload(row)["bet"]) for row in spin_requests]
    base_bet = min(bet_values)

    initial_balances_by_id = {int(item["id"]): int(item["amount"]) for item in config.get("ticket_balance") or []}
    final_state = toss_pairs[-1][2]["state"]
    final_balances_by_id = {int(item["id"]): int(item["amount"]) for item in final_state.get("ticket_balance") or []}
    initial_balances = {id_to_color[item_id]: initial_balances_by_id.get(item_id, 0) for item_id in id_to_color}
    final_balances = {id_to_color[item_id]: final_balances_by_id.get(item_id, 0) for item_id in id_to_color}

    spent = Counter()
    free_grants = Counter()
    lottery_grants = Counter()
    reward_events: dict[tuple[str, str], list[int]] = defaultdict(list)
    action_stats: dict[str, Counter[str]] = {color: Counter() for color in COLORS}
    single_chip_values: dict[str, list[float]] = defaultdict(list)
    direct_chip_values: dict[str, list[int]] = defaultdict(list)
    board_chip_values: dict[str, list[int]] = defaultdict(list)

    for _, request, response in toss_pairs:
        color = request["ticket_color"]
        ticket_number = int(request["ticket_number"])
        stats = action_stats[color]
        stats["rpc_calls"] += 1
        stats["ticket_units"] += ticket_number
        stats["single_calls" if ticket_number == 1 else "bulk_calls"] += 1
        stats["status_ok"] += response.get("status") == "OK"
        spent[color] += ticket_number
        collected = ((response.get("state") or {}).get("free_ticket_state") or {}).get("ticket_collected") or []
        for collected_color in collected:
            free_grants[collected_color] += 1
            stats["free_ticket_grants"] += 1

        categories_in_call: set[str] = set()
        for reward in ((response.get("lottery_reward") or {}).get("reward") or []):
            category, quantity = classify_reward(reward)
            categories_in_call.add(category)
            stats[f"{category}_objects"] += 1
            if quantity is not None:
                reward_events[(color, category)].append(quantity)
            if category == "chips" and quantity is not None:
                direct_chip_values[color].append(quantity)
                if ticket_number == 1:
                    single_chip_values[color].append(quantity / base_bet)
            if category == "ticket_item":
                inventory = reward["inventory_delta"]
                reward_color = id_to_color.get(int(inventory["id"]), "UNKNOWN")
                lottery_grants[reward_color] += int(inventory["amount"])
        if ticket_number == 1:
            for category in categories_in_call:
                stats[f"single_{category}_hit_calls"] += 1

        completed = (response.get("state") or {}).get("puzzle_board_completed_reward") or []
        stats["board_completions"] += len(completed)
        for entry in completed:
            value = chip_value(entry.get("reward") or {})
            if value is not None:
                board_chip_values[color].append(value)
                reward_events[(color, "board_completion_chips")].append(value)

    purchase_messages = [
        {"seq": int(row["seq"]), "direction": row["direction"], "data": payload(row)}
        for row in index_rows
        if row["service"] == "AppServer" and row["method"] == "MakeInAppPurchase"
    ]
    purchase_facts = extract_purchase_facts(purchase_messages, id_to_color)
    purchase_grants = Counter()
    for fact in purchase_facts:
        if fact["success"]:
            purchase_grants[fact["ticket_color"]] += int(fact["ticket_quantity"])

    upgrade_linked = Counter()
    for color in COLORS:
        upgrade_linked[color] = (
            final_balances[color]
            - initial_balances[color]
            + spent[color]
            - purchase_grants[color]
            - free_grants[color]
            - lottery_grants[color]
        )

    # Locate positive absolute-state increments immediately following progress-level updates.
    upgrade_events: list[dict[str, Any]] = []
    last_observed: dict[int, int] | None = None
    last_observed_seq = 0
    effects: Counter[int] = Counter()
    recent_levels: list[tuple[int, str]] = []
    last_spin_bet: int | None = None
    current_segment = 0
    for row in index_rows:
        data = payload(row)
        key = (row["service"], row["method"], row["direction"])
        if key == ("AppServer", "JoinGame", "out"):
            current_segment += 1
            last_spin_bet = None
        elif key == ("SlotsGameServer", "Spin", "out"):
            last_spin_bet = int(data["bet"])
        if row["service"] == "AppClient" and row["method"] == "UpdateProgress" and "level" in data:
            recent_levels.append((int(row["seq"]), str(data["level"])))
        if key == ("AppServer", "LotteryToss", "out"):
            request = data["data"]
            effects[color_to_id[request["ticket_color"]]] -= int(request["ticket_number"])
        if key == ("AppServer", "MakeInAppPurchase", "in"):
            for reward in ((data.get("rewards_data") or {}).get("reward") or []):
                inventory = reward.get("inventory_delta")
                if inventory and int(inventory.get("id", -1)) in id_to_color:
                    effects[int(inventory["id"])] += int(inventory["amount"])

        observation = None
        source = None
        if row["service"] == "AppClient" and row["method"] == "AddDciEvent" and "lottery" in data:
            observation = {int(item["id"]): int(item["amount"]) for item in data["lottery"].get("ticket_balance") or []}
            source = "config"
        elif key == ("AppServer", "LotteryToss", "in"):
            for reward in ((data.get("lottery_reward") or {}).get("reward") or []):
                inventory = reward.get("inventory_delta")
                if inventory and int(inventory.get("id", -1)) in id_to_color:
                    effects[int(inventory["id"])] += int(inventory["amount"])
            for free_color in ((data.get("state") or {}).get("free_ticket_state") or {}).get("ticket_collected") or []:
                effects[color_to_id[free_color]] += 1
            observation = {int(item["id"]): int(item["amount"]) for item in (data.get("state") or {}).get("ticket_balance") or []}
            source = "toss_response"

        if observation is not None:
            if last_observed is not None:
                residual = {item_id: observation.get(item_id, 0) - last_observed.get(item_id, 0) - effects[item_id] for item_id in id_to_color}
                levels = [level for seq, level in recent_levels if last_observed_seq < seq <= int(row["seq"])]
                if source == "config" and levels:
                    for item_id, amount in residual.items():
                        if amount > 0:
                            upgrade_events.append(
                                {
                                    "level_after": levels[-1],
                                    "ticket_color": id_to_color[item_id],
                                    "ticket_quantity": amount,
                                    "slot_alias": f"Slot-{current_segment}",
                                    "normalized_bet": round((last_spin_bet or base_bet) / base_bet, 4),
                                }
                            )
            last_observed = observation
            last_observed_seq = int(row["seq"])
            effects = Counter()
            recent_levels = []

    if Counter({color: sum(event["ticket_quantity"] for event in upgrade_events if event["ticket_color"] == color) for color in COLORS}) != upgrade_linked:
        raise RuntimeError("Upgrade-linked ticket reconciliation failed.")

    free_state = config.get("free_ticket") or {}
    initial_progress = int(free_state.get("progress", 0))
    final_free_state = final_state.get("free_ticket_state") or {}
    final_progress = int(final_free_state.get("progress", 0))
    free_threshold = int(final_free_state.get("threshold", free_state.get("threshold", 0)))
    total_ticket_units = sum(spent.values())
    if (initial_progress + total_ticket_units) % free_threshold != final_progress:
        raise RuntimeError("Free-ticket progress does not reconcile.")
    if (initial_progress + total_ticket_units) // free_threshold != sum(free_grants.values()):
        raise RuntimeError("Free-ticket grant count does not reconcile.")

    capture_start = str(manifest.get("capture_start", ""))
    capture_end = str(manifest.get("capture_end", ""))
    duration_seconds = int((parse_time(capture_end) - parse_time(capture_start)).total_seconds())
    session_rows = [
        {
            "session_alias": args.session_alias,
            "instance_alias": "Research-1",
            "account_alias": "Account-A",
            "manifest_status": "stopped",
            "capture_start": capture_start,
            "capture_end": capture_end,
            "duration_seconds": duration_seconds,
            "game_version": manifest.get("game_version"),
            "version_code": manifest.get("version_code"),
            "source_revision": manifest.get("source_revision"),
            "descriptor_sha256": manifest.get("descriptor_sha256"),
            "agent_sha256": manifest.get("agent_sha256"),
            "total_rpc": len(index_rows),
            "decoded_rpc": json_count,
            "decode_rate": 1.0,
            "decode_errors": 0,
            "inventory_rows": len(inventory_rows),
            "field_path_rows": len(field_rows),
            "lottery_toss_requests": len(toss_requests),
            "lottery_toss_responses": len(toss_responses),
            REGULAR_SPIN_REQUESTS_FIELD: len(spin_requests),
            REGULAR_SPIN_RESPONSES_FIELD: len(spin_responses),
            "free_spin_requests": len(free_spin_requests),
            "free_spin_responses": len(free_spin_responses),
            "successful_purchase_count": sum(1 for fact in purchase_facts if fact["success"]),
            "lifecycle_complete": True,
            "evidence_completeness": "primary LotteryToss and Slots complete; CollectFreeTicket/MiniGameLotteryMachine/black-lottery missed-info absent",
        }
    ]
    write_csv(output_dir / "SESSION_SUMMARY.csv", session_rows, session_rows[0].keys())

    purchase_rows = [
        {
            "session_alias": args.session_alias,
            **fact,
            "claim_type": "Confirmed",
            "evidence_source": "Observed-live + Manual",
            "evidence_level": "L3",
            "endpoint": "AppServer.MakeInAppPurchase",
            "field_path": "local_price; local_currency_code; lottery_ticket_color; rewards_data.reward[]",
            "sample_count": 1,
            "limits": "request/product/order identifiers removed; User confirms the real-money purchases; apparent ticket cost does not subtract loyalty-point value",
        }
        for fact in purchase_facts
    ]
    write_csv(output_dir / "PURCHASES.csv", purchase_rows, purchase_rows[0].keys())

    action_rows: list[dict[str, Any]] = []
    for color in COLORS:
        stats = action_stats[color]
        single_total = stats["single_calls"]
        chip_hits = stats["single_chips_hit_calls"]
        rate, low, high = wilson_interval(chip_hits, single_total)
        values = single_chip_values[color]
        action_rows.append(
            {
                "session_alias": args.session_alias,
                "ticket_color": color,
                "rpc_calls": stats["rpc_calls"],
                "single_calls": single_total,
                "bulk_calls": stats["bulk_calls"],
                "ticket_units": stats["ticket_units"],
                "status_ok": stats["status_ok"],
                "single_chip_hit_calls": chip_hits,
                "single_chip_hit_rate": round(rate, 6),
                "wilson95_low": round(low, 6),
                "wilson95_high": round(high, 6),
                "single_chip_min_b0": round(min(values), 6) if values else "",
                "single_chip_p50_b0": round(statistics.median(values), 6) if values else "",
                "single_chip_mean_b0": round(statistics.mean(values), 6) if values else "",
                "single_chip_p90_b0": round(percentile(values, 0.9) or 0, 6) if values else "",
                "single_chip_max_b0": round(max(values), 6) if values else "",
                "puzzle_reward_objects": stats["puzzle_progress_objects"],
                "ticket_reward_objects": stats["ticket_item_objects"],
                "ticket_reward_quantity": sum(reward_events[(color, "ticket_item")]),
                "collectible_box_objects": stats["collectible_box_objects"],
                "time_boost_objects": stats["time_boost_objects"],
                "charms_token_objects": stats["charms_token_objects"],
                "free_ticket_grants": stats["free_ticket_grants"],
                "board_completions": stats["board_completions"],
                "board_completion_chips_b0": round(sum(board_chip_values[color]) / base_bet, 6),
                "claim_type": "Confirmed",
                "evidence_source": "Observed-live",
                "evidence_level": "L3",
                "endpoint": "AppServer.LotteryToss",
                "field_path": "data.ticket_*; lottery_reward.reward[]; state.*",
                "sample_count": stats["rpc_calls"],
                "limits": "single account/build; bulk calls are excluded from single-call hit-rate distribution",
            }
        )
    write_csv(
        output_dir / "LOTTERY_ACTION_STATS.csv",
        action_rows,
        tuple(key for key in action_rows[0].keys()),
    )

    # Segment regular and free spins without retaining game IDs.
    segment = 0
    active_segment = 0
    last_bet: int | None = None
    slot_stats: dict[tuple[int, int], Counter[str]] = defaultdict(Counter)
    for row in index_rows:
        key = (row["service"], row["method"], row["direction"])
        if key == ("AppServer", "JoinGame", "out"):
            segment += 1
            active_segment = segment
            last_bet = None
        elif key == ("AppServer", "LeaveGame", "out"):
            active_segment = 0
            last_bet = None
        elif key == ("SlotsGameServer", "Spin", "out"):
            last_bet = int(payload(row)["bet"])
            slot_stats[(active_segment, last_bet)][REGULAR_SPINS_FIELD] += 1
        elif key == ("SlotsGameServer", "FreeSpin", "out") and last_bet is not None:
            slot_stats[(active_segment, last_bet)]["free_spins"] += 1
    bet_rank = {bet: index + 1 for index, bet in enumerate(sorted(set(bet_values)))}
    slot_rows: list[dict[str, Any]] = []
    for (slot_segment, bet), stats in sorted(slot_stats.items()):
        linked_events = [event for event in upgrade_events if event["slot_alias"] == f"Slot-{slot_segment}" and event["normalized_bet"] == round(bet / base_bet, 4)]
        slot_rows.append(
            {
                "session_alias": args.session_alias,
                "slot_alias": f"Slot-{slot_segment}",
                "bet_tier": f"B{bet_rank[bet]}",
                "normalized_bet_b0": round(bet / base_bet, 6),
                REGULAR_SPINS_FIELD: stats[REGULAR_SPINS_FIELD],
                "free_spins": stats["free_spins"],
                "normalized_chip_cost_b0": round(stats[REGULAR_SPINS_FIELD] * bet / base_bet, 6),
                "direct_ticket_field_present": False,
                "direct_ticket_hit_count": "",
                "direct_ticket_quantity": "",
                "upgrade_linked_events": len(linked_events),
                "upgrade_linked_ticket_quantity": sum(event["ticket_quantity"] for event in linked_events),
                "claim_type": "Confirmed" if not linked_events else "Estimate",
                "evidence_source": "Observed-live" if not linked_events else "Observed-live + Manual",
                "evidence_level": "L3",
                "endpoint": "SlotsGameServer.Spin; AppClient.UpdateProgress; AppClient.AddDciEvent",
                "field_path": "bet; level; lottery.ticket_balance[]",
                "sample_count": stats[REGULAR_SPINS_FIELD],
                "limits": "SpinResponse has no direct ticket field; upgrade linkage is temporal/state reconciliation, not per-spin drop evidence",
            }
        )
    write_csv(output_dir / "SLOT_ITEM_DROP_STATS.csv", slot_rows, slot_rows[0].keys())

    reward_rows: list[dict[str, Any]] = []
    for (color, category), values in sorted(reward_events.items()):
        row = {
            "session_alias": args.session_alias,
            "ticket_color": color,
            "reward_category": category,
            "reward_objects": len(values),
            "quantity_sum": sum(values) if category != "chips" and category != "board_completion_chips" else "",
            "normalized_chip_sum_b0": round(sum(values) / base_bet, 6) if category in {"chips", "board_completion_chips"} else "",
            "normalized_chip_min_b0": round(min(values) / base_bet, 6) if category in {"chips", "board_completion_chips"} else "",
            "normalized_chip_median_b0": round(statistics.median(values) / base_bet, 6) if category in {"chips", "board_completion_chips"} else "",
            "normalized_chip_mean_b0": round(statistics.mean(values) / base_bet, 6) if category in {"chips", "board_completion_chips"} else "",
            "normalized_chip_max_b0": round(max(values) / base_bet, 6) if category in {"chips", "board_completion_chips"} else "",
            "source_kind": "conditional" if category == "board_completion_chips" else "random_or_pool_based",
            "claim_type": "Confirmed",
            "evidence_source": "Observed-live",
            "evidence_level": "L3",
            "endpoint": "AppServer.LotteryToss",
            "field_path": "lottery_reward.reward[]; state.puzzle_board_completed_reward[]",
            "sample_count": len(toss_pairs),
            "limits": "reward weights are not exposed; values are normalized by the minimum observed regular-spin bet B0",
        }
        reward_rows.append(row)
    write_csv(output_dir / "REWARD_OUTPUT_STATS.csv", reward_rows, reward_rows[0].keys())

    progression_rows: list[dict[str, Any]] = []

    def add_progress(metric: str, dimension: str, value: Any, unit: str, claim: str, source: str, level: str, endpoint: str, field_path: str, sample_count: int, limits: str) -> None:
        progression_rows.append(
            {
                "session_alias": args.session_alias,
                "metric": metric,
                "dimension": dimension,
                "value": value,
                "unit": unit,
                "claim_type": claim,
                "evidence_source": source,
                "evidence_level": level,
                "endpoint": endpoint,
                "field_path": field_path,
                "sample_count": sample_count,
                "limits": limits,
            }
        )

    add_progress("free_ticket_threshold", "ALL", free_threshold, "ticket units", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "state.free_ticket_state.threshold", len(toss_pairs), "constant in this Session")
    add_progress("free_ticket_initial_progress", "ALL", initial_progress, "progress", "Confirmed", "Static-config", "L2", "AppClient.AddDciEvent", "lottery.free_ticket.progress", len(lottery_configs), "single account/build")
    add_progress("free_ticket_final_progress", "ALL", final_progress, "progress", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "state.free_ticket_state.progress", len(toss_pairs), "single account/build")
    add_progress("free_ticket_granted", "BRONZE", free_grants["BRONZE"], "tickets", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "state.free_ticket_state.ticket_collected[]", len(toss_pairs), "grant is usage-threshold based in this Session")
    add_progress("bulk_play_cap", "ALL", int(config.get("bulk_play_cap", 0)), "ticket units", "Confirmed", "Static-config", "L2", "AppClient.AddDciEvent", "lottery.bulk_play_cap", len(lottery_configs), "configured cap; observed maximum may be lower")
    add_progress("observed_max_batch", "ALL", max(int(request["ticket_number"]) for _, request, _ in toss_pairs), "ticket units", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "data.ticket_number", len(toss_pairs), "single account/session")
    add_progress("board_completions", "ALL", sum(stats["board_completions"] for stats in action_stats.values()), "boards", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "state.puzzle_board_completed_reward[]", len(toss_pairs), "starting board state and full activity cycle are not known")
    for color in COLORS:
        add_progress("ticket_initial_balance", color, initial_balances[color], "tickets", "Confirmed", "Static-config", "L2", "AppClient.AddDciEvent", "lottery.ticket_balance[]", len(lottery_configs), "sanitized start snapshot")
        add_progress("ticket_acquired_purchase", color, purchase_grants[color], "tickets", "Confirmed", "Observed-live + Manual", "L3", "AppServer.MakeInAppPurchase", "local_price; local_currency_code; lottery_ticket_color; rewards_data.reward[].inventory_delta", sum(1 for fact in purchase_facts if fact["success"] and fact["ticket_color"] == color), "price and bundle composition are in PURCHASES.csv; bundle also grants loyalty points")
        add_progress("ticket_acquired_free_threshold", color, free_grants[color], "tickets", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "state.free_ticket_state.ticket_collected[]", len(toss_pairs), "only BRONZE was observed")
        add_progress("ticket_acquired_lottery_reward", color, lottery_grants[color], "tickets", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "lottery_reward.reward[].inventory_delta", len(toss_pairs), "gross immediate source; may originate from paid or earned toss inputs")
        add_progress("ticket_acquired_upgrade_linked", color, upgrade_linked[color], "tickets", "Estimate", "Observed-live + Manual", "L3", "AppClient.UpdateProgress + AppClient.AddDciEvent", "level; lottery.ticket_balance[]", len(upgrade_events), "repeated temporal/state reconciliation; no explicit ticket grant field in UpdateProgress")
        add_progress("ticket_spent", color, spent[color], "tickets", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "data.ticket_color; data.ticket_number", len(toss_pairs), "request/response pairs all status OK")
        add_progress("ticket_final_balance", color, final_balances[color], "tickets", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "state.ticket_balance[]", len(toss_pairs), "sanitized end snapshot")
    for event in upgrade_events:
        add_progress("upgrade_linked_event", event["ticket_color"], event["ticket_quantity"], "tickets", "Estimate", "Observed-live + Manual", "L3", "AppClient.UpdateProgress + AppClient.AddDciEvent", f"level={event['level_after']}; lottery.ticket_balance[]", 1, f"temporal correlation at {event['slot_alias']} / {event['normalized_bet']} B0; causal grant field absent")

    direct_chip_b0 = sum(sum(values) for values in direct_chip_values.values()) / base_bet
    board_chip_b0 = sum(sum(values) for values in board_chip_values.values()) / base_bet
    add_progress("scenario_conservative", "ALL", round(direct_chip_b0, 6), "B0 chips", "Estimate", "Observed-live", "L3", "AppServer.LotteryToss", "lottery_reward.reward[].big_chips_delta", len(toss_pairs), "same 933 observed ticket units; excludes all board-completion rewards")
    add_progress("scenario_current_observed", "ALL", round(direct_chip_b0 + board_chip_b0, 6), "B0 chips", "Confirmed", "Observed-live", "L3", "AppServer.LotteryToss", "direct reward + board completion reward", len(toss_pairs), "descriptive total, not an expectation or RTP")
    add_progress("scenario_optimistic", "ALL", "formula_only", "direct output + chosen board-completion frequency", "Decision proposal", "Inferred", "L0", "N/A", "N/A", 1, "one mixed-color Session cannot support a stable optimistic probability bound")
    write_csv(output_dir / "PROGRESSION_MODEL.csv", progression_rows, progression_rows[0].keys())

    spin_cost_b0 = sum(bet_values) / base_bet
    gross_acquired = sum(purchase_grants.values()) + sum(free_grants.values()) + sum(lottery_grants.values()) + sum(upgrade_linked.values())
    purchase_currencies = {fact["currency"] for fact in purchase_facts if fact["success"]}
    if len(purchase_currencies) != 1:
        raise RuntimeError("Successful purchases do not share one local currency.")
    purchase_currency = next(iter(purchase_currencies))
    total_real_money_spend = sum(Decimal(fact["local_price"]) for fact in purchase_facts if fact["success"])
    total_purchase_loyalty_points = sum(int(fact["loyalty_points"]) for fact in purchase_facts if fact["success"])
    return_rows: list[dict[str, Any]] = []

    def add_return(metric: str, value: Any, unit: str, numerator: str, denominator: str, claim: str, source: str, level: str, limits: str, sample_count: int | None = None) -> None:
        return_rows.append(
            {
                "session_alias": args.session_alias,
                "metric": metric,
                "value": value,
                "unit": unit,
                "numerator": numerator,
                "denominator": denominator,
                "claim_type": claim,
                "evidence_source": source,
                "evidence_level": level,
                "sample_count": len(toss_pairs) if sample_count is None else sample_count,
                "limits": limits,
            }
        )

    add_return(REGULAR_SPIN_COST_METRIC, round(spin_cost_b0, 6), "B0 chips", "sum regular-spin bet", "B0", "Confirmed", "Observed-live", "L3", "chip wager only; not a real-money payment", len(spin_requests))
    add_return("real_money_purchase_count", len(purchase_facts), "purchases", "successful linked purchase chains", "N/A", "Confirmed", "Observed-live + Manual", "L3", "all four purchases were confirmed by the User", len(purchase_facts))
    add_return("real_money_spend", money_text(total_real_money_spend), purchase_currency, "sum local_price", "N/A", "Confirmed", "Observed-live + Manual", "L3", "bundle prices include Lottery tickets and loyalty points", len(purchase_facts))
    add_return("purchased_ticket_units", sum(purchase_grants.values()), "tickets", "successful purchase grants", "N/A", "Confirmed", "Observed-live + Manual", "L3", "see PURCHASES.csv by ticket color", len(purchase_facts))
    add_return("purchase_loyalty_points", total_purchase_loyalty_points, "loyalty points", "successful purchase grants", "N/A", "Confirmed", "Observed-live + Manual", "L3", "other bundle value prevents assigning the full price to tickets", len(purchase_facts))
    add_return("lottery_direct_chip_output", round(direct_chip_b0, 6), "B0 chips", "direct Lottery chip rewards", "B0", "Confirmed", "Observed-live", "L3", "mixed ticket colors and three bulk calls")
    add_return("board_completion_chip_output", round(board_chip_b0, 6), "B0 chips", "board completion rewards", "B0", "Confirmed", "Observed-live", "L3", "five completions; one GOLD completion dominates")
    add_return("gross_chip_output", round(direct_chip_b0 + board_chip_b0, 6), "B0 chips", "direct + board completion chips", "B0", "Confirmed", "Observed-live", "L3", "gross output only")
    add_return("chip_reward_output_over_regular_spin_chip_cost_excluding_purchases", round((direct_chip_b0 + board_chip_b0) / spin_cost_b0, 6), "ratio", "gross Lottery chip output", "observed regular-spin chip cost", "Estimate", "Observed-live", "L3", "technical comparison only; excludes real-money purchases and is not RTP, ROI or paid return")
    add_return("ticket_units_spent", total_ticket_units, "tickets", "LotteryToss ticket_number", "N/A", "Confirmed", "Observed-live", "L3", "includes 590 units in three bulk calls")
    add_return("free_ticket_rebate", sum(free_grants.values()), "tickets", "ticket_collected count", "ticket units spent", "Confirmed", "Observed-live", "L3", "threshold rule is exact only for this build/session")
    add_return("net_ticket_consumption", total_ticket_units - sum(free_grants.values()), "tickets", "spent - threshold grants", "N/A", "Confirmed", "Observed-live", "L3", "gross source ledger, not monetary cost")
    add_return("gross_ticket_acquisition", gross_acquired, "tickets", "purchase + free + Lottery reward + upgrade-linked", "N/A", "Estimate", "Observed-live + Manual", "L3", "upgrade-linked component is temporally attributed")
    add_return("ticket_ledger_balance_check", sum(initial_balances.values()) + gross_acquired - total_ticket_units - sum(final_balances.values()), "tickets", "initial + acquired - spent - final", "N/A", "Confirmed", "Derived from Runtime", "L3", "must equal zero")
    write_csv(output_dir / "RETURN_MODEL.csv", return_rows, return_rows[0].keys())

    print(json.dumps(
        {
            "session_alias": args.session_alias,
            "rpc": len(index_rows),
            "decoded": json_count,
            "lottery_toss_calls": len(toss_pairs),
            "ticket_units": total_ticket_units,
            REGULAR_SPINS_FIELD: len(spin_requests),
            "free_spins": len(free_spin_requests),
            "successful_purchases": len(purchase_facts),
            "real_money_spend": f"{money_text(total_real_money_spend)} {purchase_currency}",
            "free_ticket_grants": sum(free_grants.values()),
            "upgrade_linked_ticket_quantity": sum(upgrade_linked.values()),
            "board_completions": sum(stats["board_completions"] for stats in action_stats.values()),
            "output_dir": str(output_dir),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
