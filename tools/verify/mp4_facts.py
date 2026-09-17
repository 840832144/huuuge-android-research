#!/usr/bin/env python3
"""Verify the framing facts of an MP4 (duration, resolution, frame rate) with no
external tool: dependency-free ISOBMFF box parsing. Useful when ffprobe is not
installed and a delivered video's declared duration / size / fps must be checked.

Usage:
  python mp4_facts.py <file.mp4> [more.mp4 ...]
"""
import argparse
import struct
import sys


def walk(buf, start, end, want, out, depth=0):
    """Recursively find box types in `want`; record (type, payload_offset, size)."""
    off = start
    while off + 8 <= end:
        size = struct.unpack(">I", buf[off:off + 4])[0]
        btype = buf[off + 4:off + 8].decode("latin-1")
        hdr = 8
        if size == 1:                      # 64-bit size
            size = struct.unpack(">Q", buf[off + 8:off + 16])[0]
            hdr = 16
        elif size == 0:
            size = end - off
        if size < hdr:
            break
        payload = off + hdr
        if btype in want:
            out.setdefault(btype, []).append((payload, size - hdr))
        if btype in ("moov", "trak", "mdia", "minf", "stbl", "udta"):
            walk(buf, payload, off + size, want, out, depth + 1)
        off += size


def inspect(path):
    data = open(path, "rb").read()
    found = {}
    walk(data, 0, len(data), {"mvhd", "tkhd", "stts", "stsd", "mdhd"}, found)

    result = {}
    if "mvhd" in found:
        p, _ = found["mvhd"][0]
        version = data[p]
        if version == 1:
            timescale = struct.unpack(">I", data[p + 20:p + 24])[0]
            duration = struct.unpack(">Q", data[p + 24:p + 32])[0]
        else:
            timescale = struct.unpack(">I", data[p + 12:p + 16])[0]
            duration = struct.unpack(">I", data[p + 16:p + 20])[0]
        result["timescale"] = timescale
        result["duration_units"] = duration
        result["duration_sec"] = round(duration / timescale, 2) if timescale else None

    if "mdhd" in found:
        p, _ = found["mdhd"][0]
        version = data[p]
        off = 20 if version == 1 else 12
        mt = struct.unpack(">I", data[p + off:p + off + 4])[0]
        md = struct.unpack(">I", data[p + off + 4:p + off + 8])[0]
        result["media_timescale"] = mt
        result["media_duration_sec"] = round(md / mt, 2) if mt else None

    if "tkhd" in found:
        p, _ = found["tkhd"][0]
        version = data[p]
        off = 88 if version == 1 else 76
        w = struct.unpack(">I", data[p + off:p + off + 4])[0] / 65536.0
        h = struct.unpack(">I", data[p + off + 4:p + off + 8])[0] / 65536.0
        result["track_count"] = len(found["tkhd"])
        result.setdefault("tracks", []).append({"width": w, "height": h})

    if "stts" in found:
        for idx, (p, _) in enumerate(found["stts"]):
            n = struct.unpack(">I", data[p + 4:p + 8])[0]
            samples = 0
            ticks = 0
            q = p + 8
            for _ in range(n):
                cnt, delta = struct.unpack(">II", data[q:q + 8])
                samples += cnt
                ticks += cnt * delta
                q += 8
            mt = result.get("media_timescale") or result.get("timescale") or 0
            fps = round(samples / (ticks / mt), 3) if (mt and ticks) else None
            result.setdefault("stts", []).append({"samples": samples, "ticks": ticks, "fps": fps})

    for k, v in result.items():
        print("  {}: {}".format(k, v))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+", help="MP4 file(s) to inspect")
    args = ap.parse_args()
    for path in args.files:
        print("== {} ==".format(path))
        try:
            inspect(path)
        except Exception as exc:
            print("  error:", exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
