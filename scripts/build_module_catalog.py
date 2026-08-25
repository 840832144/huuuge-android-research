from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from google.protobuf import descriptor_pb2


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESCRIPTORS = ROOT / "artifacts" / "live_probe" / "huuuge_descriptors.pb"
DEFAULT_SPECS = ROOT / "artifacts" / "module_catalog" / "module_specs.json"
DEFAULT_LIVE_INVENTORY = ROOT / "artifacts" / "analysis" / "20260825_182300" / "rpc_inventory.csv"
DEFAULT_LIVE_FIELDS = ROOT / "artifacts" / "analysis" / "20260825_182300" / "field_paths.csv"
DEFAULT_OUT = ROOT / "artifacts" / "module_catalog"


SCALAR_TYPES = {
    descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE: "double",
    descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT: "float",
    descriptor_pb2.FieldDescriptorProto.TYPE_INT64: "int64",
    descriptor_pb2.FieldDescriptorProto.TYPE_UINT64: "uint64",
    descriptor_pb2.FieldDescriptorProto.TYPE_INT32: "int32",
    descriptor_pb2.FieldDescriptorProto.TYPE_FIXED64: "fixed64",
    descriptor_pb2.FieldDescriptorProto.TYPE_FIXED32: "fixed32",
    descriptor_pb2.FieldDescriptorProto.TYPE_BOOL: "bool",
    descriptor_pb2.FieldDescriptorProto.TYPE_STRING: "string",
    descriptor_pb2.FieldDescriptorProto.TYPE_BYTES: "bytes",
    descriptor_pb2.FieldDescriptorProto.TYPE_UINT32: "uint32",
    descriptor_pb2.FieldDescriptorProto.TYPE_SFIXED32: "sfixed32",
    descriptor_pb2.FieldDescriptorProto.TYPE_SFIXED64: "sfixed64",
    descriptor_pb2.FieldDescriptorProto.TYPE_SINT32: "sint32",
    descriptor_pb2.FieldDescriptorProto.TYPE_SINT64: "sint64",
}
LABELS = {
    descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL: "optional",
    descriptor_pb2.FieldDescriptorProto.LABEL_REQUIRED: "required",
    descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED: "repeated",
}


@dataclass(frozen=True)
class MessageInfo:
    full_name: str
    proto_file: str
    descriptor: descriptor_pb2.DescriptorProto


@dataclass(frozen=True)
class Endpoint:
    service_index: int
    service: str
    method_index: int
    method: str
    request_type: str
    response_type: str


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_type(name: str) -> str:
    return name.lstrip(".")


def walk_messages(
    proto_file: str,
    package: str,
    messages: Iterable[descriptor_pb2.DescriptorProto],
    parent: str = "",
) -> Iterable[MessageInfo]:
    for message in messages:
        local = f"{parent}.{message.name}" if parent else message.name
        full_name = f"{package}.{local}" if package else local
        yield MessageInfo(full_name, proto_file, message)
        yield from walk_messages(proto_file, package, message.nested_type, local)


def load_descriptor_set(path: Path) -> tuple[
    descriptor_pb2.FileDescriptorSet,
    dict[str, MessageInfo],
    list[Endpoint],
]:
    descriptor_set = descriptor_pb2.FileDescriptorSet()
    descriptor_set.ParseFromString(path.read_bytes())
    messages: dict[str, MessageInfo] = {}
    endpoints: list[Endpoint] = []
    for file_descriptor in descriptor_set.file:
        for info in walk_messages(file_descriptor.name, file_descriptor.package, file_descriptor.message_type):
            messages[info.full_name] = info
        if file_descriptor.name == "Services.proto":
            for service_index, service in enumerate(file_descriptor.service):
                for method_index, method in enumerate(service.method):
                    endpoints.append(
                        Endpoint(
                            service_index,
                            service.name,
                            method_index,
                            method.name,
                            normalize_type(method.input_type),
                            normalize_type(method.output_type),
                        )
                    )
    return descriptor_set, messages, endpoints


def matches_any(patterns: list[str], value: str) -> bool:
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in patterns)


def assign_endpoint(specs: list[dict[str, Any]], endpoint: Endpoint) -> str:
    combined = f"{endpoint.service}.{endpoint.method}"
    for spec in specs:
        if matches_any(spec.get("priority_endpoint_patterns", []), combined):
            return spec["id"]
    # Exact service ownership wins over broad cross-cutting method keywords.
    for spec in specs:
        if endpoint.service in spec.get("services", []):
            return spec["id"]
    message_pair = f"{endpoint.request_type} {endpoint.response_type}"
    for spec in specs:
        if matches_any(spec.get("endpoint_patterns", []), combined):
            return spec["id"]
        if matches_any(spec.get("endpoint_message_patterns", []), message_pair):
            return spec["id"]
    return "other_protocol"


def message_matches_spec(spec: dict[str, Any], info: MessageInfo) -> bool:
    if info.proto_file in spec.get("proto_files", []):
        return True
    return matches_any(spec.get("message_patterns", []), info.full_name)


def semantic_role(path: str) -> str:
    name = path.lower()
    tail = re.split(r"[.\[\]]+", name)[-1] or name
    if re.search(r"(^|_)(id|ids|uuid|key)$", tail) or tail in {
        "game",
        "event",
        "mission",
        "offer",
        "product",
        "player",
        "theme",
        "tile",
    }:
        return "entity/id"
    if re.search(r"time|timestamp|expire|expiry|reset|duration|cooldown|deadline|created_at|start_at|end_at|start_time|end_time|ttl", name):
        return "timing/reset/expiry"
    if re.search(r"segment|eligib|limit|limitation|restriction|unlock|minimum|maximum|allowed|country|cap$|required_level|level_required|available", name):
        return "segment/eligibility/limit"
    if re.search(r"reward|prize|payout|win|grant|gift|bonus|winnings|award", name):
        return "reward/output"
    if re.search(r"cost|price|bet|stake|fee|requirement|threshold|consume|spend|input|ticket|token|quantity|amount", name):
        return "cost/input"
    if re.search(r"balance|cash|chips|currency|coin|diamond|gem|credit", name):
        return "currency/balance"
    if re.search(r"progress|status|state|level|tier|rank|stage|phase|points|iteration|completed|tutorial|active|count", name):
        return "progression/state"
    return "other"


def field_type(field: descriptor_pb2.FieldDescriptorProto) -> str:
    if field.type_name:
        return normalize_type(field.type_name)
    return SCALAR_TYPES.get(field.type, f"type_{field.type}")


def flow_role(service: str) -> str:
    if service.endswith("Client") or service in {"AppClient", "PurchaseClient", "RaceClient"}:
        return "server update/request -> client response/ack"
    if service == "GameHost":
        return "game process -> host request/response"
    if service.startswith("ProxyTest") or service.startswith("Htf"):
        return "diagnostic/test request -> response"
    return "client request -> server response/update"


def scalar_value_type(value: Any) -> str:
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


def walk_scalar_values(value: Any, prefix: str = "") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            yield from walk_scalar_values(child, child_prefix)
    elif isinstance(value, list):
        array_prefix = f"{prefix}[]"
        if not value:
            yield array_prefix, "array(empty)", []
        for child in value:
            yield from walk_scalar_values(child, array_prefix)
    elif prefix:
        yield prefix, scalar_value_type(value), value


def value_fingerprint(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def collect_live_value_stats(session: Path | None) -> dict[tuple[str, str], dict[str, Any]]:
    if session is None or not (session / "json").is_dir():
        return {}
    stats: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "message_sequences": set(),
            "occurrences": 0,
            "nonempty": 0,
            "fingerprints": set(),
            "types": set(),
        }
    )
    for path in sorted((session / "json").glob("*.json")):
        message = json.loads(path.read_text(encoding="utf-8-sig"))
        payload_type = message.get("payload_type", "")
        sequence = message.get("seq")
        per_message: dict[str, list[tuple[str, Any]]] = defaultdict(list)
        for field_path, value_type, value in walk_scalar_values(message.get("data", {})):
            per_message[field_path].append((value_type, value))
        for field_path, values in per_message.items():
            entry = stats[(payload_type, field_path)]
            entry["message_sequences"].add(sequence)
            for value_type, value in values:
                entry["occurrences"] += 1
                entry["types"].add(value_type)
                entry["fingerprints"].add(value_fingerprint(value))
                if value not in (None, "", [], {}):
                    entry["nonempty"] += 1
    return stats


def live_variability(entry: dict[str, Any] | None) -> str:
    if not entry:
        return "not-assessed"
    distinct = len(entry["fingerprints"])
    messages = len(entry["message_sequences"])
    if messages <= 1:
        return "single-observation"
    if distinct <= 1:
        return "constant-in-session"
    return "varying-in-session"


def list_apk_assets(apk: Path | None) -> list[str]:
    if apk is None or not apk.is_file():
        return []
    with zipfile.ZipFile(apk) as archive:
        return sorted(name for name in archive.namelist() if name.lower().endswith(".zpk"))


def completion(summary: dict[str, Any]) -> tuple[int, str]:
    score = 0
    if summary["schema_message_count"] or summary["schema_endpoint_count"]:
        score += 30
    if summary["asset_count"]:
        score += 5
    if summary["live_sample_count"]:
        score += 30
    elif summary["crosscutting_live_sample_count"]:
        score += 20
    if summary["live_endpoint_count"] >= 3:
        score += 10
    if summary["live_field_path_count"] >= 10:
        score += 10
    if summary["live_request_count"] and summary["live_response_count"]:
        score += 5
    score = min(score, 90)
    if score >= 75:
        label = "substantial live structure"
    elif score >= 55:
        label = "partial live structure"
    elif summary["schema_message_count"] or summary["schema_endpoint_count"]:
        label = "schema skeleton"
    else:
        label = "inferred/static skeleton"
    return score, label


def md_join(items: Iterable[str], empty: str = "none identified") -> str:
    values = sorted(set(item for item in items if item))
    return ", ".join(f"`{item}`" for item in values) if values else empty


def build_catalog(args: argparse.Namespace) -> dict[str, Any]:
    descriptor_set, messages, endpoints = load_descriptor_set(args.descriptors)
    specs = json.loads(args.specs.read_text(encoding="utf-8"))
    spec_by_id = {spec["id"]: spec for spec in specs}
    if len(spec_by_id) != len(specs):
        raise RuntimeError("module_specs.json contains duplicate module ids")
    required_crosscutting = {"economy", "rewards", "other_protocol"}
    if not required_crosscutting <= set(spec_by_id):
        raise RuntimeError(f"module_specs.json must define {sorted(required_crosscutting)}")

    endpoint_modules = {endpoint: assign_endpoint(specs, endpoint) for endpoint in endpoints}
    endpoint_lookup = {(endpoint.service, endpoint.method): endpoint for endpoint in endpoints}
    live_inventory = read_csv(args.live_inventory)
    live_fields = read_csv(args.live_fields)
    value_stats = collect_live_value_stats(args.capture_session)
    apk_assets = list_apk_assets(args.apk)

    live_by_endpoint: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {"REQUEST": 0, "RESPONSE": 0})
    live_directions: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in live_inventory:
        key = (row["service"], row["method"])
        live_by_endpoint[key][row["rpc_type"]] += int(row["count"])
        live_directions[key].add(row["direction"])

    module_messages: dict[str, set[str]] = defaultdict(set)
    module_endpoints: dict[str, list[Endpoint]] = defaultdict(list)
    for endpoint in endpoints:
        module_id = endpoint_modules[endpoint]
        module_endpoints[module_id].append(endpoint)
        module_messages[module_id].update((endpoint.request_type, endpoint.response_type))
    for spec in specs:
        for name, info in messages.items():
            if message_matches_spec(spec, info):
                module_messages[spec["id"]].add(name)
    assigned_messages = set().union(*module_messages.values()) if module_messages else set()
    module_messages["other_protocol"].update(set(messages) - assigned_messages)

    assets_by_module: dict[str, list[str]] = defaultdict(list)
    for spec in specs:
        for asset in apk_assets:
            if any(term.lower() in asset.lower() for term in spec.get("asset_terms", [])):
                assets_by_module[spec["id"]].append(asset)

    live_path_rows: list[dict[str, Any]] = []
    crosscutting_sequences: dict[str, set[int]] = defaultdict(set)
    crosscutting_estimates: dict[str, dict[str, int]] = defaultdict(dict)
    for row in live_fields:
        endpoint = endpoint_lookup.get((row["service"], row["method"]))
        primary_module = endpoint_modules[endpoint] if endpoint else "other_protocol"
        role = semantic_role(row["field_path"])
        modules = {primary_module}
        live_path_identity = f'{row["payload_type"]}.{row["field_path"]}'
        for spec in specs:
            if matches_any(spec.get("live_path_patterns", []), live_path_identity):
                modules.add(spec["id"])
        if role in {"currency/balance", "cost/input"}:
            modules.add("economy")
        if role == "reward/output":
            modules.update(("economy", "rewards"))
        stats = value_stats.get((row["payload_type"], row["field_path"]))
        message_count = len(stats["message_sequences"]) if stats else int(row["messages_seen"])
        for module_id in modules:
            if module_id not in spec_by_id:
                continue
            if stats:
                if module_id != primary_module:
                    crosscutting_sequences[module_id].update(stats["message_sequences"])
            if module_id != primary_module:
                previous = crosscutting_estimates[module_id].get(row["payload_type"], 0)
                crosscutting_estimates[module_id][row["payload_type"]] = max(previous, message_count)
            live_path_rows.append(
                {
                    "module_id": module_id,
                    "record_kind": "live_path",
                    "proto_file": messages.get(row["payload_type"], MessageInfo("", "", descriptor_pb2.DescriptorProto())).proto_file,
                    "message_type": row["payload_type"],
                    "field_number": "",
                    "field_name": row["field_path"].split(".")[-1].replace("[]", ""),
                    "field_path": row["field_path"],
                    "cardinality": "observed",
                    "field_type": row["value_type"],
                    "semantic_role": role,
                    "evidence_status": "observed-live",
                    "live_message_count": message_count,
                    "live_occurrence_count": stats["occurrences"] if stats else "",
                    "live_nonempty_count": stats["nonempty"] if stats else "",
                    "live_distinct_count": len(stats["fingerprints"]) if stats else "",
                    "variability": live_variability(stats),
                    "source_session": args.session_id,
                }
            )

    schema_field_rows: list[dict[str, Any]] = []
    live_paths_by_message: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in live_fields:
        live_paths_by_message[row["payload_type"]].append(row)
    for spec in specs:
        module_id = spec["id"]
        for message_name in sorted(module_messages[module_id]):
            info = messages.get(message_name)
            if not info:
                continue
            for field in info.descriptor.field:
                path_prefixes = (field.name, f"{field.name}.", f"{field.name}[]")
                matching_live = [
                    row for row in live_paths_by_message.get(message_name, [])
                    if row["field_path"] == path_prefixes[0]
                    or row["field_path"].startswith(path_prefixes[1])
                    or row["field_path"].startswith(path_prefixes[2])
                ]
                schema_field_rows.append(
                    {
                        "module_id": module_id,
                        "record_kind": "schema_field",
                        "proto_file": info.proto_file,
                        "message_type": message_name,
                        "field_number": field.number,
                        "field_name": field.name,
                        "field_path": field.name,
                        "cardinality": LABELS.get(field.label, str(field.label)),
                        "field_type": field_type(field),
                        "semantic_role": semantic_role(field.name),
                        "evidence_status": "observed-live" if matching_live else "schema-only",
                        "live_message_count": max((int(row["messages_seen"]) for row in matching_live), default=0),
                        "live_occurrence_count": "",
                        "live_nonempty_count": "",
                        "live_distinct_count": "",
                        "variability": "see-live-path" if matching_live else "not-observed",
                        "source_session": args.session_id if matching_live else "",
                    }
                )

    field_rows = schema_field_rows + live_path_rows
    field_rows.sort(key=lambda row: (
        row["module_id"], row["record_kind"], row["message_type"], str(row["field_path"]), str(row["field_number"])
    ))

    endpoint_rows: list[dict[str, Any]] = []
    for endpoint in endpoints:
        module_id = endpoint_modules[endpoint]
        counts = live_by_endpoint[(endpoint.service, endpoint.method)]
        total = counts["REQUEST"] + counts["RESPONSE"]
        endpoint_rows.append(
            {
                "module_id": module_id,
                "service_index": endpoint.service_index,
                "service": endpoint.service,
                "method_index": endpoint.method_index,
                "method": endpoint.method,
                "request_type": endpoint.request_type,
                "response_type": endpoint.response_type,
                "flow_role": flow_role(endpoint.service),
                "request_live_count": counts["REQUEST"],
                "response_live_count": counts["RESPONSE"],
                "total_live_count": total,
                "live_directions": ";".join(sorted(live_directions[(endpoint.service, endpoint.method)])),
                "evidence_status": "observed-live" if total else "schema-only",
                "source_session": args.session_id if total else "",
            }
        )
    endpoint_rows.sort(key=lambda row: (row["module_id"], int(row["service_index"]), int(row["method_index"])))

    module_summaries: dict[str, dict[str, Any]] = {}
    for spec in specs:
        module_id = spec["id"]
        owned_endpoints = module_endpoints[module_id]
        observed_endpoints = [
            endpoint for endpoint in owned_endpoints
            if sum(live_by_endpoint[(endpoint.service, endpoint.method)].values())
        ]
        primary_samples = sum(
            sum(live_by_endpoint[(endpoint.service, endpoint.method)].values())
            for endpoint in owned_endpoints
        )
        module_field_rows = [row for row in live_path_rows if row["module_id"] == module_id]
        crosscut_samples = (
            len(crosscutting_sequences[module_id])
            if crosscutting_sequences[module_id]
            else sum(crosscutting_estimates[module_id].values())
        )
        related_proto_files = {
            messages[name].proto_file for name in module_messages[module_id] if name in messages
        }
        related_proto_files.update(spec.get("proto_files", []))
        if owned_endpoints:
            related_proto_files.add("Services.proto")
        services = {endpoint.service for endpoint in owned_endpoints}
        request_count = sum(live_by_endpoint[(endpoint.service, endpoint.method)]["REQUEST"] for endpoint in owned_endpoints)
        response_count = sum(live_by_endpoint[(endpoint.service, endpoint.method)]["RESPONSE"] for endpoint in owned_endpoints)
        summary = {
            "module_id": module_id,
            "title": spec["title"],
            "summary": spec["summary"],
            "schema_message_count": len(module_messages[module_id]),
            "schema_endpoint_count": len(owned_endpoints),
            "live_endpoint_count": len(observed_endpoints),
            "live_sample_count": primary_samples,
            "crosscutting_live_sample_count": crosscut_samples,
            "live_field_path_count": len({(row["message_type"], row["field_path"]) for row in module_field_rows}),
            "live_request_count": request_count,
            "live_response_count": response_count,
            "proto_files": sorted(related_proto_files),
            "services": sorted(services),
            "asset_count": len(assets_by_module[module_id]),
            "assets": assets_by_module[module_id],
        }
        if primary_samples:
            summary["status"] = "live-confirmed"
        elif crosscut_samples:
            summary["status"] = "live-confirmed (cross-cutting/config only)"
        elif summary["schema_message_count"] or summary["schema_endpoint_count"]:
            summary["status"] = "schema-only / live sample pending"
        else:
            summary["status"] = "inferred/static / live sample pending"
        summary["completion_score"], summary["completion_label"] = completion(summary)
        module_summaries[module_id] = summary

    module_rows: list[dict[str, Any]] = []
    for spec in specs:
        summary = module_summaries[spec["id"]]
        module_rows.append(
            {
                "module_id": spec["id"],
                "module": spec["title"],
                "status": summary["status"],
                "completion_score": summary["completion_score"],
                "completion_label": summary["completion_label"],
                "schema_proto_count": len(summary["proto_files"]),
                "schema_message_count": summary["schema_message_count"],
                "schema_endpoint_count": summary["schema_endpoint_count"],
                "live_endpoint_count": summary["live_endpoint_count"],
                "live_sample_count": summary["live_sample_count"],
                "crosscutting_live_sample_count": summary["crosscutting_live_sample_count"],
                "live_field_path_count": summary["live_field_path_count"],
                "proto_files": ";".join(summary["proto_files"]),
                "services": ";".join(summary["services"]),
                "zpk_asset_count": summary["asset_count"],
                "next_action": spec["next_actions"][0],
            }
        )

    write_csv(
        args.out_dir / "modules.csv",
        module_rows,
        [
            "module_id", "module", "status", "completion_score", "completion_label",
            "schema_proto_count", "schema_message_count", "schema_endpoint_count",
            "live_endpoint_count", "live_sample_count", "crosscutting_live_sample_count",
            "live_field_path_count", "proto_files", "services", "zpk_asset_count", "next_action",
        ],
    )
    write_csv(
        args.out_dir / "endpoints.csv",
        endpoint_rows,
        [
            "module_id", "service_index", "service", "method_index", "method", "request_type",
            "response_type", "flow_role", "request_live_count", "response_live_count",
            "total_live_count", "live_directions", "evidence_status", "source_session",
        ],
    )
    write_csv(
        args.out_dir / "fields.csv",
        field_rows,
        [
            "module_id", "record_kind", "proto_file", "message_type", "field_number", "field_name",
            "field_path", "cardinality", "field_type", "semantic_role", "evidence_status",
            "live_message_count", "live_occurrence_count", "live_nonempty_count",
            "live_distinct_count", "variability", "source_session",
        ],
    )

    for spec in specs:
        write_module_dossier(
            args.out_dir / f'{spec["id"]}.md',
            spec,
            module_summaries[spec["id"]],
            module_endpoints[spec["id"]],
            module_messages[spec["id"]],
            messages,
            live_by_endpoint,
            [row for row in live_path_rows if row["module_id"] == spec["id"]],
            args.session_id,
        )

    write_index(
        args.out_dir / "MODULE_INDEX.md",
        specs,
        module_summaries,
        descriptor_set,
        endpoints,
        live_inventory,
        len(messages),
        len(set().union(*module_messages.values())),
        args,
    )
    return {
        "modules": len(specs),
        "live_confirmed": sum(summary["status"].startswith("live-confirmed") for summary in module_summaries.values()),
        "schema_only": sum(summary["status"].startswith("schema-only") for summary in module_summaries.values()),
        "inferred_static": sum(summary["status"].startswith("inferred/static") for summary in module_summaries.values()),
        "endpoints": len(endpoint_rows),
        "fields": len(field_rows),
        "schema_messages": len(messages),
        "assigned_schema_messages": len(set().union(*module_messages.values())),
    }


def write_module_dossier(
    path: Path,
    spec: dict[str, Any],
    summary: dict[str, Any],
    endpoints: list[Endpoint],
    message_names: set[str],
    messages: dict[str, MessageInfo],
    live_by_endpoint: dict[tuple[str, str], dict[str, int]],
    live_paths: list[dict[str, Any]],
    session_id: str,
) -> None:
    observed_endpoints = [
        endpoint for endpoint in endpoints
        if sum(live_by_endpoint[(endpoint.service, endpoint.method)].values())
    ]
    schema_fields: dict[str, list[str]] = defaultdict(list)
    for message_name in sorted(message_names):
        info = messages.get(message_name)
        if not info:
            continue
        for field in info.descriptor.field:
            role = semantic_role(field.name)
            schema_fields[role].append(f"{message_name}.{field.name} ({field_type(field)}, {LABELS.get(field.label, field.label)})")

    lines = [
        f"# {spec['title']}",
        "",
        spec["summary"],
        "",
        "## Catalog status",
        "",
        f"- Evidence status: **{summary['status']}**",
        f"- Structural completeness: **{summary['completion_score']}/100 — {summary['completion_label']}**",
        f"- Primary live samples: **{summary['live_sample_count']}** from `{session_id}`",
        f"- Cross-cutting live samples: **{summary['crosscutting_live_sample_count']}**",
        f"- Live endpoints / schema endpoints: **{summary['live_endpoint_count']} / {summary['schema_endpoint_count']}**",
        f"- Live populated field paths: **{summary['live_field_path_count']}**",
        "",
        "## Schema scope",
        "",
        f"- Proto files: {md_join(summary['proto_files'])}",
        f"- Services: {md_join(summary['services'])}",
        f"- Related message types: **{summary['schema_message_count']}**",
        "",
    ]
    for name in sorted(message_names):
        if name in messages:
            lines.append(f"- `{name}` ({messages[name].proto_file})")

    lines.extend(["", "## RPC and flow structure", "", spec["flow"], ""])
    if endpoints:
        lines.extend([
            "| Service.method | Request | Response/update | Live req | Live resp | Evidence |",
            "|---|---|---|---:|---:|---|",
        ])
        for endpoint in sorted(endpoints, key=lambda item: (item.service_index, item.method_index)):
            counts = live_by_endpoint[(endpoint.service, endpoint.method)]
            status = "observed-live" if sum(counts.values()) else "schema-only"
            lines.append(
                f"| `{endpoint.service}.{endpoint.method}` | `{endpoint.request_type}` | "
                f"`{endpoint.response_type}` | {counts['REQUEST']} | {counts['RESPONSE']} | {status} |"
            )
    else:
        lines.append("No dedicated RPC endpoint is assigned yet; the dossier is based on shared schema/static structure.")

    lines.extend(["", "## Structural fields", ""])
    role_order = [
        "entity/id", "progression/state", "cost/input", "currency/balance", "reward/output",
        "timing/reset/expiry", "segment/eligibility/limit", "other",
    ]
    role_titles = {
        "entity/id": "Entity identifiers",
        "progression/state": "Progression / state",
        "cost/input": "Cost / input",
        "currency/balance": "Currency / balance",
        "reward/output": "Reward / output",
        "timing/reset/expiry": "Timing / reset / expiry",
        "segment/eligibility/limit": "Segment / eligibility / limit",
        "other": "Other structural fields",
    }
    for role in role_order:
        values = sorted(set(schema_fields[role]))
        lines.extend([f"### {role_titles[role]}", ""])
        if values:
            for value in values[:40]:
                lines.append(f"- `{value}`")
            if len(values) > 40:
                lines.append(f"- … {len(values) - 40} more rows in `fields.csv`")
        else:
            lines.append("- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.")
        lines.append("")

    lines.extend(["## Live-session coverage", ""])
    if observed_endpoints:
        lines.append(f"Observed endpoint samples in `{session_id}`:")
        lines.append("")
        for endpoint in sorted(observed_endpoints, key=lambda item: -sum(live_by_endpoint[(item.service, item.method)].values())):
            counts = live_by_endpoint[(endpoint.service, endpoint.method)]
            lines.append(
                f"- `{endpoint.service}.{endpoint.method}` — {counts['REQUEST'] + counts['RESPONSE']} "
                f"({counts['REQUEST']} request, {counts['RESPONSE']} response)"
            )
    else:
        lines.append("No primary endpoint for this module appeared in the current session; live sample pending.")
    if live_paths:
        lines.extend([
            "",
            "Populated field-path evidence (values withheld):",
            "",
            "| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |",
            "|---|---:|---:|---:|---|",
        ])
        ranked = sorted(
            live_paths,
            key=lambda row: (-int(row["live_message_count"] or 0), row["message_type"], row["field_path"]),
        )
        for row in ranked[:40]:
            lines.append(
                f"| `{row['message_type']}.{row['field_path']}` | {row['live_message_count']} | "
                f"{row['live_nonempty_count'] or 'n/a'} | {row['live_distinct_count'] or 'n/a'} | {row['variability']} |"
            )
        if len(ranked) > 40:
            lines.append(f"| … | | | | {len(ranked) - 40} more rows in `fields.csv` |")

    lines.extend([
        "",
        "## Evidence ledger",
        "",
        "### Observed-live",
        "",
    ])
    if observed_endpoints or live_paths:
        lines.append(
            f"- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `{session_id}`."
        )
        lines.append("- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.")
    else:
        lines.append("- None in the current session.")
    lines.extend([
        "",
        "### Schema-only",
        "",
        "- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.",
        "- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.",
        "",
        "### Inferred",
        "",
        f"- Flow interpretation: {spec['flow']}",
        "- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.",
        "",
        "## Static / additional evidence channels",
        "",
    ])
    if summary["assets"]:
        for asset in summary["assets"]:
            lines.append(f"- ZPK asset: `{asset}`")
    else:
        lines.append("- No module-specific ZPK filename match was found in the current base APK inventory.")
    for item in spec.get("static_evidence", []):
        lines.append(f"- {item}")
    lines.append("- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.")

    lines.extend(["", "## Missing data and next user actions", ""])
    for action in spec["next_actions"]:
        lines.append(f"- {action}")
    lines.extend([
        "- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.",
        "- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.",
        "",
        "This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(
    path: Path,
    specs: list[dict[str, Any]],
    summaries: dict[str, dict[str, Any]],
    descriptor_set: descriptor_pb2.FileDescriptorSet,
    endpoints: list[Endpoint],
    live_inventory: list[dict[str, str]],
    schema_message_count: int,
    assigned_message_count: int,
    args: argparse.Namespace,
) -> None:
    live = [summary for summary in summaries.values() if summary["status"].startswith("live-confirmed")]
    schema_only = [summary for summary in summaries.values() if summary["status"].startswith("schema-only")]
    inferred = [summary for summary in summaries.values() if summary["status"].startswith("inferred/static")]
    live_messages = sum(int(row["count"]) for row in live_inventory)
    lines = [
        "# Huuuge Module Structure Catalog",
        "",
        "This is the broad structural map of the Huuuge client. It combines recovered protobuf descriptors, service/method relationships, sanitized live-session counts/field presence, and APK ZPK filenames. It does not publish captured values or make final numerical conclusions.",
        "",
        "## Catalog snapshot",
        "",
        f"- Independent module dossiers: **{len(specs)}**",
        f"- Live-confirmed modules: **{len(live)}**",
        f"- Schema-only / live pending modules: **{len(schema_only)}**",
        f"- Inferred/static-only modules: **{len(inferred)}**",
        f"- Recovered proto files: **{len(descriptor_set.file)}**",
        f"- Descriptor message types: **{schema_message_count}**; assigned to at least one dossier: **{assigned_message_count}**",
        f"- Descriptor service methods: **{len(endpoints)}**",
        f"- Current live session: `{args.session_id}`, **{live_messages}** sanitized message samples",
        f"- Descriptor SHA-256: `{sha256(args.descriptors)}`",
        "",
        "Status meanings:",
        "",
        "- **live-confirmed** — at least one primary module endpoint appeared in the session.",
        "- **live-confirmed (cross-cutting/config only)** — populated fields appeared inside a shared/config message, but no dedicated module endpoint was exercised.",
        "- **schema-only / live sample pending** — descriptor structure exists, but this session did not exercise it.",
        "- **inferred/static / live sample pending** — current evidence is shared/static or organizational rather than a dedicated observed RPC family.",
        "",
        "## Recovered schema and static backbone",
        "",
        f"Recovered files: {md_join(file_descriptor.name for file_descriptor in descriptor_set.file)}",
        "",
        "- `Services.proto` supplies the 34-service / 356-method RPC relationship map used by `endpoints.csv`.",
        "- `libClawApp.so` supplies the recovered descriptors and preserves C++/Lua integration evidence; module-specific Lua/native ownership remains a future mapping layer.",
        "- Base-APK ZPK filenames are attached to dossiers as static evidence without committing APK contents.",
        "",
        "## Module map",
        "",
        "| Module | Status | Structure snapshot | Live samples | Live endpoints | Completion | Highest-priority next action |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for spec in specs:
        summary = summaries[spec["id"]]
        snapshot = f"{summary['schema_message_count']} messages / {summary['schema_endpoint_count']} endpoints"
        live_count = summary["live_sample_count"]
        if summary["crosscutting_live_sample_count"]:
            live_count = f"{live_count} + {summary['crosscutting_live_sample_count']} cross-cut"
        lines.append(
            f"| [{spec['title']}]({spec['id']}.md) | {summary['status']} | {snapshot} | {live_count} | "
            f"{summary['live_endpoint_count']} | {summary['completion_score']}/100 | {spec['next_actions'][0]} |"
        )

    lines.extend(["", "## Most structurally complete now", ""])
    for summary in sorted(summaries.values(), key=lambda item: (-item["completion_score"], item["title"]))[:10]:
        lines.append(
            f"- [{summary['title']}]({summary['module_id']}.md) — {summary['completion_score']}/100, "
            f"{summary['live_sample_count']} primary live samples, {summary['live_endpoint_count']} live endpoints."
        )

    lines.extend(["", "## Live sample pending", ""])
    for summary in sorted(schema_only + inferred, key=lambda item: item["title"]):
        action = next(spec["next_actions"][0] for spec in specs if spec["id"] == summary["module_id"])
        lines.append(f"- [{summary['title']}]({summary['module_id']}.md) — {action}")

    lines.extend([
        "",
        "## Machine-readable tables",
        "",
        "- `modules.csv` — one row per module with status, coverage, proto/service scope and next action.",
        "- `endpoints.csv` — every recovered service method with request/response types, flow role and live counts.",
        "- `fields.csv` — schema field definitions plus sanitized live populated paths, counts and variability (never values).",
        "- `module_specs.json` — maintained module boundaries, flow notes, static evidence and future actions.",
        "",
        "## Rebuild",
        "",
        "Descriptor + committed sanitized inventories only:",
        "",
        "Run `scripts\\sync_local_runtime.ps1` first if the ignored local descriptor binary is not present at its expected path.",
        "",
        "```powershell",
        "py scripts\\build_module_catalog.py",
        "```",
        "",
        "To add local non-empty/distinct/variability counts and APK ZPK filenames without exporting values:",
        "",
        "```powershell",
        "py scripts\\build_module_catalog.py --capture-session <local-session-dir> --apk <local-base.apk>",
        "```",
        "",
        "## Evidence limitations",
        "",
        "- Current live data is unmarked, so endpoint-to-click correlation remains incomplete.",
        "- `live-confirmed` means structural presence in this one session, not complete coverage or business interpretation.",
        "- Field distinctness is calculated locally from decoded values and exported only as counts/labels; the values themselves remain uncommitted.",
        "- Cross-cutting sample counts use exact unique sequences when the local capture is supplied; otherwise the builder uses a conservative per-payload estimate from sanitized field counts.",
        "- Modules may share messages/fields. `endpoints.csv` assigns one primary module, while cross-cutting economy/reward field evidence may appear in multiple dossiers.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the sanitized Huuuge module structure catalog")
    parser.add_argument("--descriptors", type=Path, default=DEFAULT_DESCRIPTORS)
    parser.add_argument("--specs", type=Path, default=DEFAULT_SPECS)
    parser.add_argument("--live-inventory", type=Path, default=DEFAULT_LIVE_INVENTORY)
    parser.add_argument("--live-fields", type=Path, default=DEFAULT_LIVE_FIELDS)
    parser.add_argument("--capture-session", type=Path, help="Optional local value-bearing session; only counts/fingerprints are emitted")
    parser.add_argument("--apk", type=Path, help="Optional local base APK used only to inventory ZPK filenames")
    parser.add_argument("--session-id", default="20260825_182300")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build_catalog(args)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
