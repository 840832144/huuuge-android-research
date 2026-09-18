#!/usr/bin/env python3
"""Self-check for mp4_facts.py that needs **no binary fixture**: it synthesises
minimal ISOBMFF files at runtime and asserts the parser's output.

Why: the multi-track regression (a plain `trak` path token made every track share
one slot, so an audio track silently overwrote the video track) only showed up on
files that have both tracks. The delivered sample had no audio track, so the bug
survived a manual check. This guard covers the multi-track case without committing
any media file.

Run:  python test_mp4_facts.py      (exit code 0 = pass)
"""
from __future__ import annotations

import contextlib
import io
import pathlib
import struct
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mp4_facts  # noqa: E402


def box(btype: str, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload) + 8) + btype.encode("latin-1") + payload


def full_box(version: int, flags: int, body: bytes) -> bytes:
    return struct.pack(">B", version) + struct.pack(">I", flags)[1:] + body


def mvhd(timescale: int, length_units: int) -> bytes:
    body = (struct.pack(">I", 0) + struct.pack(">I", 0) +      # created / modified
            struct.pack(">I", timescale) + struct.pack(">I", length_units) +
            bytes(80))                                          # rest is unused by the parser
    return box("mvhd", full_box(0, 0, body))


def tkhd(width: int, height: int) -> bytes:
    body = (struct.pack(">I", 0) + struct.pack(">I", 0) +      # created / modified
            struct.pack(">I", 1) + struct.pack(">I", 0) +      # track id / reserved
            struct.pack(">I", 0) + bytes(8) +                  # duration / reserved
            struct.pack(">h", 0) + struct.pack(">h", 0) +      # layer / alternate group
            struct.pack(">h", 0) + struct.pack(">h", 0) +      # volume / reserved
            bytes(36) +                                        # matrix
            struct.pack(">I", width << 16) + struct.pack(">I", height << 16))
    return box("tkhd", full_box(0, 0, body))


def mdhd(timescale: int, length_units: int) -> bytes:
    body = (struct.pack(">I", 0) + struct.pack(">I", 0) +
            struct.pack(">I", timescale) + struct.pack(">I", length_units) +
            struct.pack(">hh", 0, 0))
    return box("mdhd", full_box(0, 0, body))


def hdlr(handler: str) -> bytes:
    return box("hdlr", full_box(0, 0, struct.pack(">I", 0) + handler.encode("latin-1") + bytes(12)))


def stts(samples: int, delta: int) -> bytes:
    return box("stts", full_box(0, 0, struct.pack(">I", 1) + struct.pack(">II", samples, delta)))


def track(handler: str, timescale: int, samples: int, delta: int,
          width: int = 0, height: int = 0) -> bytes:
    length = samples * delta
    stbl = box("stbl", stts(samples, delta))
    mdia = box("mdia", mdhd(timescale, length) + hdlr(handler) + box("minf", stbl))
    return box("trak", tkhd(width, height) + mdia)


def build(path: pathlib.Path, tracks: list[bytes], timescale: int, total_units: int) -> None:
    moov = box("moov", mvhd(timescale, total_units) + b"".join(tracks))
    path.write_bytes(box("ftyp", b"isom" + struct.pack(">I", 512) + b"isomiso2") + moov)


def capture(path: pathlib.Path) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mp4_facts.inspect(str(path))
    return buf.getvalue()


def main() -> int:
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)

        # 1) multi-track: 1 s of 30 fps video (timescale 1000, delta 33) + audio
        multi = tmp_path / "multi.mp4"
        build(multi,
              [track("vide", 1000, 30, 33, width=640, height=360),
               track("soun", 48000, 40, 1200)],
              timescale=1000, total_units=1000)
        out = capture(multi)
        if "track[0] video: 640x360" not in out:
            failures.append("multi-track: video track missing or wrong size\n" + out)
        if "track[1] audio" not in out:
            failures.append("multi-track: audio track missing (tracks collapsed?)\n" + out)
        if "fps=30.303" not in out:
            failures.append("multi-track: unexpected video fps\n" + out)

        # 2) audio listed first: the regression specifically hit this ordering
        reversed_file = tmp_path / "audiofirst.mp4"
        build(reversed_file,
              [track("soun", 48000, 40, 1200),
               track("vide", 1000, 30, 33, width=640, height=360)],
              timescale=1000, total_units=1000)
        out = capture(reversed_file)
        if "video" not in out:
            failures.append("audio-first: video track swallowed\n" + out)

        # 3) single track must still report exactly one track
        single = tmp_path / "single.mp4"
        build(single, [track("vide", 1000, 30, 33, width=640, height=360)],
              timescale=1000, total_units=990)
        out = capture(single)
        if out.count("track[") != 1:
            failures.append("single-track: expected exactly one track\n" + out)

        # 4) a file that is not a plain MP4 container must say so, not print None
        junk = tmp_path / "junk.mp4"
        junk.write_bytes(b"ftypisom" + bytes(64))
        out = capture(junk)
        if "not a plain MP4 container" not in out:
            failures.append("unparsable: missing diagnostic\n" + out)
        if "None" in out:
            failures.append("unparsable: printed None instead of a diagnostic\n" + out)

    if failures:
        print("FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: multi-track, audio-first, single-track and unparsable cases all behave")
    return 0


if __name__ == "__main__":
    sys.exit(main())
