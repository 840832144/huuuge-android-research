from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


SLOT_APP_METHODS = {
    "GetJackpotValues",
    "GetPlayerList",
    "JoinGame",
    "LeaveGame",
    "ListGames",
    "QueryGame",
    "QueryGamePlayer",
}
ECONOMY_TERMS = (
    "Offer",
    "Purchase",
    "Shop",
    "Reward",
    "Gift",
    "Diamonds",
)
PROGRESSION_TERMS = ("Charms", "Fame", "Loyalty", "Progress")
EVENT_TERMS = ("BattlePass", "MiniPass", "Vault", "Milestone", "Collection", "Conquest")
MISSION_TERMS = ("Mission", "Quest", "Task")


def classify(service: str, method: str) -> str:
    combined = f"{service}.{method}"
    if "Lottery" in combined or "Draw" in combined or "Ticket" in combined:
        return "lottery"
    if service.startswith("Slots") or (service == "AppServer" and method in SLOT_APP_METHODS):
        return "slots"
    if any(term in combined for term in EVENT_TERMS):
        return "passes/events"
    if any(term in combined for term in MISSION_TERMS):
        return "missions/quests"
    if any(term in combined for term in ECONOMY_TERMS):
        return "offers/economy"
    if any(term in combined for term in PROGRESSION_TERMS):
        return "clubs/VIP/progression"
    return "other/unknown"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def scalar_type(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    return type(value).__name__


def collect_field_paths(value: object, prefix: str = "") -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    if isinstance(value, dict):
        if prefix and not value:
            found.add((prefix, "object"))
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            found.update(collect_field_paths(child, child_prefix))
    elif isinstance(value, list):
        array_prefix = f"{prefix}[]"
        if not value:
            found.add((array_prefix, "array(empty)"))
        for child in value:
            found.update(collect_field_paths(child, array_prefix))
    elif prefix:
        found.add((prefix, scalar_type(value)))
    return found


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def write_inventory(rows: list[dict[str, str]], path: Path) -> list[dict[str, object]]:
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row["service"],
            row["method"],
            row["rpc_type"],
            row["direction"],
            row["payload_type"],
        )
        groups[key].append(row)

    inventory: list[dict[str, object]] = []
    for key, group in groups.items():
        service, method, rpc_type, direction, payload_type = key
        payload_sizes = [int(row["payload_bytes"]) for row in group]
        decoded = sum(row["decoded"] == "1" for row in group)
        inventory.append(
            {
                "domain": classify(service, method),
                "service": service,
                "method": method,
                "rpc_type": rpc_type,
                "direction": direction,
                "payload_type": payload_type,
                "count": len(group),
                "decoded_count": decoded,
                "undecoded_count": len(group) - decoded,
                "first_seen": min(row["time"] for row in group),
                "last_seen": max(row["time"] for row in group),
                "payload_bytes_total": sum(payload_sizes),
                "payload_bytes_min": min(payload_sizes),
                "payload_bytes_max": max(payload_sizes),
            }
        )
    inventory.sort(key=lambda item: (str(item["domain"]), str(item["service"]), str(item["method"]), str(item["rpc_type"])))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(inventory[0]))
        writer.writeheader()
        writer.writerows(inventory)
    return inventory


def write_field_paths(rows: list[dict[str, str]], path: Path) -> tuple[int, int]:
    observations: Counter[tuple[str, str, str, str, str]] = Counter()
    missing_json = 0
    for row in rows:
        json_path = Path(row["json_file"])
        if not json_path.is_file():
            missing_json += 1
            continue
        message = json.loads(json_path.read_text(encoding="utf-8-sig"))
        for field_path, value_type in collect_field_paths(message.get("data", {})):
            observations[(row["service"], row["method"], row["payload_type"], field_path, value_type)] += 1

    field_rows = []
    for (service, method, payload_type, field_path, value_type), count in observations.items():
        field_rows.append(
            {
                "domain": classify(service, method),
                "service": service,
                "method": method,
                "payload_type": payload_type,
                "field_path": field_path,
                "value_type": value_type,
                "messages_seen": count,
            }
        )
    field_rows.sort(key=lambda item: (item["domain"], item["service"], item["method"], item["payload_type"], item["field_path"]))

    fieldnames = [
        "domain",
        "service",
        "method",
        "payload_type",
        "field_path",
        "value_type",
        "messages_seen",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(field_rows)
    return len(field_rows), missing_json


def write_summary(
    rows: list[dict[str, str]],
    inventory: list[dict[str, object]],
    field_path_count: int,
    missing_json: int,
    output: Path,
    args: argparse.Namespace,
) -> None:
    decoded = sum(row["decoded"] == "1" for row in rows)
    endpoint_names = {f'{row["service"]}.{row["method"]}' for row in rows}
    domains = Counter(classify(row["service"], row["method"]) for row in rows)
    domain_endpoints: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        domain_endpoints[classify(row["service"], row["method"])].add(f'{row["service"]}.{row["method"]}')

    descriptor_line = "not recorded"
    if args.descriptors:
        descriptor_line = f"`{sha256(args.descriptors)}`"

    lines = [
        f"# Sanitized RPC discovery summary — {args.session.name}",
        "",
        "This report contains aggregate metadata and protobuf field names only. Raw wrappers, decoded values, account identifiers, signatures, and local file paths are intentionally excluded from version control.",
        "",
        "## Session facts",
        "",
        f"- Capture start: `{min(row['time'] for row in rows)}`",
        f"- Capture end: `{max(row['time'] for row in rows)}`",
        f"- Messages: **{len(rows)}**",
        f"- Decoded: **{decoded}/{len(rows)}**",
        f"- Unique service/method endpoints: **{len(endpoint_names)}**",
        f"- Inventory rows (direction/type-specific): **{len(inventory)}**",
        f"- Sanitized protobuf field-path/type observations: **{field_path_count}**",
        f"- Missing decoded JSON files during summary: **{missing_json}**",
        f"- Game: `{args.game_version}` (`versionCode={args.version_code}`)",
        f"- Instrumentation: Frida/Gadget `{args.frida_version}`, `{args.device}`",
        f"- Descriptor SHA-256: {descriptor_line}",
        "",
        "## Heuristic domain coverage",
        "",
        "Domain labels are deterministic discovery heuristics based on service/method names; they are not claims about server-side business ownership.",
        "",
        "| Domain | Messages | Unique endpoints |",
        "|---|---:|---:|",
    ]
    for domain in sorted(domains):
        lines.append(f"| {domain} | {domains[domain]} | {len(domain_endpoints[domain])} |")

    lines.extend(["", "## Observed endpoints by domain", ""])
    endpoint_counts = Counter(f'{row["service"]}.{row["method"]}' for row in rows)
    for domain in sorted(domain_endpoints):
        lines.append(f"### {domain}")
        lines.append("")
        for endpoint in sorted(domain_endpoints[domain], key=lambda item: (-endpoint_counts[item], item)):
            lines.append(f"- `{endpoint}` — {endpoint_counts[endpoint]}")
        lines.append("")

    lines.extend(
        [
            "## Sanitized schema coverage",
            "",
            "The companion `field_paths.csv` inventories observed decoded `data` paths and scalar types without retaining values. It is discovery evidence only; no business meaning or single-system numerical model is asserted in this session summary.",
            "",
            "## Limitations / next capture improvements",
            "",
            "- This session predates first-class `manifest.json` generation; version and hash facts here were supplied during post-capture summarization.",
            "- No action markers were recorded, so RPC bursts cannot be mapped to precise clicks beyond method semantics and timestamps.",
            "- No Lottery, Battle Pass, Collection Event, or Conquest endpoint was observed in this session.",
            "- Raw and decoded value-bearing captures remain local and are required for later numerical extraction.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a sanitized service/method and field-path inventory from a live_decode capture")
    parser.add_argument("session", type=Path, help="Capture session directory containing index.csv and json/")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--descriptors", type=Path)
    parser.add_argument("--game-version", default="unknown")
    parser.add_argument("--version-code", default="unknown")
    parser.add_argument("--frida-version", default="unknown")
    parser.add_argument("--device", default="unknown")
    args = parser.parse_args()

    args.session = args.session.resolve()
    index_path = args.session / "index.csv"
    if not index_path.is_file():
        raise SystemExit(f"Missing capture index: {index_path}")
    with index_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"Capture index has no messages: {index_path}")
    for row in rows:
        parse_time(row["time"])

    args.out_dir.mkdir(parents=True, exist_ok=True)
    inventory_path = args.out_dir / "rpc_inventory.csv"
    fields_path = args.out_dir / "field_paths.csv"
    summary_path = args.out_dir / "summary.md"
    inventory = write_inventory(rows, inventory_path)
    field_count, missing_json = write_field_paths(rows, fields_path)
    write_summary(rows, inventory, field_count, missing_json, summary_path, args)
    print(f"Wrote {summary_path}")
    print(f"Wrote {inventory_path} ({len(inventory)} rows)")
    print(f"Wrote {fields_path} ({field_count} rows, {missing_json} missing JSON files)")


if __name__ == "__main__":
    main()
