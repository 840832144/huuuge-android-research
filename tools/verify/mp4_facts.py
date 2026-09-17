#!/usr/bin/env python3
"""Verify the framing facts of an MP4 (duration, resolution, frame rate) with no
external tool: dependency-free ISOBMFF box parsing. Useful when ffprobe is not
installed and a delivered video's declared duration / size / fps must be checked.

Per-track reporting: each track's frame rate is computed with **that track's own**
`mdhd` timescale (using the first `mdhd` for every `stts` mislabels an audio
track as a video frame rate).

Usage:
  python mp4_facts.py <file.mp4> [more.mp4 ...]

Cross-checked against ffprobe (duration/resolution/fps agree).
"""
from __future__ import annotations

import argparse
import struct
import sys

CONTAINER = {"moov", "trak", "mdia", "minf", "stbl", "udta", "edts"}
TARGET = {"mvhd", "tkhd", "stts", "mdhd", "hdlr", "stsd"}


def walk(buf, start, end, path=()):
    """Yield (box_type, payload_offset, payload_size, ancestor_path)."""
    off = start
    while off + 8 <= end:
        size = struct.unpack(">I", buf[off:off + 4])[0]
        btype = buf[off + 4:off + 8].decode("latin-1", "replace")
        hdr = 8
        if size == 1:
            if off + 16 > end:
                break
            size = struct.unpack(">Q", buf[off + 8:off + 16])[0]
            hdr = 16
        elif size == 0:
            size = end - off
        if size < hdr:
            break
        payload = off + hdr
        if btype in TARGET:
            yield btype, payload, size - hdr, path
        if btype in CONTAINER:
            # A `trak` must carry a unique identity in the path: with a plain
            # "trak" token every track yields the same path prefix, so all tracks
            # collapse into one slot and later ones (typically audio) overwrite
            # earlier ones (typically video).
            token = ("trak@%d" % off) if btype == "trak" else btype
            yield from walk(buf, payload, off + size, path + (token,))
        off += size


def _u32(b, o):
    return struct.unpack(">I", b[o:o + 4])[0]


def top_level(buf):
    """List top-level boxes, tolerating 32/64-bit sizes and size==0 (to EOF)."""
    out = []
    off = 0
    while off + 8 <= len(buf):
        size = struct.unpack(">I", buf[off:off + 4])[0]
        btype = buf[off + 4:off + 8].decode("latin-1", "replace")
        hdr = 8
        if size == 1:
            if off + 16 > len(buf):
                break
            size = struct.unpack(">Q", buf[off + 8:off + 16])[0]
            hdr = 16
        elif size == 0:
            size = len(buf) - off
        if size < hdr:
            break
        printable = all(32 <= c < 127 for c in buf[off + 4:off + 8])
        out.append((btype if printable else repr(buf[off + 4:off + 8]), size, off))
        off += size
    return out


def inspect(path):
    data = open(path, "rb").read()
    boxes = list(walk(data, 0, len(data)))

    summary = {"file": path}
    tracks = {}
    order = {}

    def slot(bpath, trak_pos):
        """Map a trak to a stable 0-based display index, in order of appearance."""
        key = bpath[:trak_pos + 1]
        if key not in order:
            order[key] = len(order)
        return order[key]

    for btype, p, _size, bpath in boxes:
        trak_index = None
        for i, part in enumerate(bpath):
            if part.startswith("trak@"):
                trak_index = i
        idx = slot(bpath, trak_index) if trak_index is not None else None
        if btype == "mvhd":
            version = data[p]
            if version == 1:
                ts, dur = _u32(data, p + 20), struct.unpack(">Q", data[p + 24:p + 32])[0]
            else:
                ts, dur = _u32(data, p + 12), _u32(data, p + 16)
            summary["timescale"] = ts
            summary["duration_sec"] = round(dur / ts, 3) if ts else None
        elif btype == "tkhd" and idx is not None:
            t = tracks.setdefault(idx, {})
            version = data[p]
            off = 88 if version == 1 else 76
            t["width"] = _u32(data, p + off) / 65536.0
            t["height"] = _u32(data, p + off + 4) / 65536.0
        elif btype == "hdlr" and idx is not None:
            tracks.setdefault(idx, {})["handler"] = data[p + 8:p + 12].decode("latin-1", "replace")
        elif btype == "mdhd" and idx is not None:
            t = tracks.setdefault(idx, {})
            version = data[p]
            off = 20 if version == 1 else 12
            t["media_timescale"] = _u32(data, p + off)
            t["media_duration_sec"] = round(_u32(data, p + off + 4) / (t["media_timescale"] or 1), 3)
        elif btype == "stts" and idx is not None:
            t = tracks.setdefault(idx, {})
            n = _u32(data, p + 4)
            samples = ticks = 0
            q = p + 8
            for _ in range(n):
                cnt, delta = struct.unpack(">II", data[q:q + 8])
                samples += cnt
                ticks += cnt * delta
                q += 8
            ts = t.get("media_timescale") or summary.get("timescale") or 0
            t["samples"] = samples
            t["fps"] = round(samples / (ticks / ts), 3) if (ts and ticks) else None

    print("== {} ==".format(path))
    if summary.get("duration_sec") is None:
        boxes = top_level(data)
        kinds = {t for t, _s, _o in boxes}
        print("  no mvhd/moov could be parsed — this is not a plain MP4 container")
        if "moof" in kinds:
            print("  (fragmented MP4: duration lives in sidx/moof fragments)")
        print("  top-level boxes: {}".format(
            ", ".join("{}@{}".format(t, o) for t, _s, o in boxes[:8]) or "(none recognised)"))
        return summary
    print("  container duration: {} s (timescale {})".format(
        summary.get("duration_sec"), summary.get("timescale")))
    media_kinds = {"vide": "video", "soun": "audio", "text": "text", "meta": "meta", "hint": "hint"}
    for idx in sorted(tracks):
        t = tracks[idx]
        kind = media_kinds.get(t.get("handler", ""), t.get("handler") or "?")
        line = "  track[{}] {}: ".format(idx, kind)
        if kind == "video" and t.get("width"):
            line += "{}x{} ".format(int(t["width"]), int(t["height"]))
        if t.get("media_duration_sec") is not None:
            line += "{}(s) ".format(t["media_duration_sec"])
        if t.get("fps") is not None:
            line += "fps={}{}".format(t["fps"], "  <- frame rate" if kind == "video" else "  (not a video frame rate)")
        print(line.rstrip())
    return summary


def main():
    try:                                   # Windows consoles are often cp936/cp1252
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+", help="MP4 file(s) to inspect")
    args = ap.parse_args()
    for path in args.files:
        try:
            inspect(path)
        except Exception as exc:
            print("== {} ==".format(path))
            print("  error:", exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
