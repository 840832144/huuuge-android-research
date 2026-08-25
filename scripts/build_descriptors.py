from __future__ import annotations

import argparse
from pathlib import Path

from grpc_tools import protoc
import pkg_resources

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTO_DIR = ROOT / "artifacts" / "recovered" / "recovered_protos"
DEFAULT_OUT = ROOT / "artifacts" / "live_probe" / "huuuge_descriptors.pb"


def main() -> None:
    ap = argparse.ArgumentParser(description="Rebuild Huuuge protobuf descriptor set from recovered .proto files")
    ap.add_argument("--proto-dir", type=Path, default=DEFAULT_PROTO_DIR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    proto_dir = args.proto_dir.resolve()
    out = args.out.resolve()
    protos = sorted(proto_dir.glob("*.proto"))
    if not protos:
        raise SystemExit(f"No .proto files found in {proto_dir}")

    google_proto = Path(pkg_resources.resource_filename("grpc_tools", "_proto"))
    out.parent.mkdir(parents=True, exist_ok=True)

    argv = [
        "protoc",
        f"-I{proto_dir}",
        f"-I{google_proto}",
        f"--descriptor_set_out={out}",
        "--include_imports",
        *[str(p) for p in protos],
    ]
    rc = protoc.main(argv)
    if rc != 0:
        raise SystemExit(rc)
    print(f"Wrote {out} ({out.stat().st_size} bytes) from {len(protos)} proto files")


if __name__ == "__main__":
    main()
