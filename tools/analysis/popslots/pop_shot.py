#!/usr/bin/env python3
"""Screenshot Pop! Slots + check engine (lua/js?) + confirm it's in the lobby."""
import subprocess, base64, pathlib

ADB = "C:/platform-tools/adb.exe"
def sh(c):
    r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell"] + c,
                       capture_output=True, text=True, timeout=40)
    return (r.stdout + r.stderr).strip()

print("== foreground ==")
print(sh(["dumpsys", "window", "|", "grep", "mCurrentFocus"]))
print("== maps: lua/js/script ==")
print(sh(["su", "-c", "cat /proc/15177/maps 2>/dev/null | grep -iE 'lua|\.lua|\.js|jsc|v8|quick' | head -10"]))
print("== libBigCasino exports sample (symbol richness) ==")
print(sh(["su", "-c", "cat /proc/15177/maps 2>/dev/null | grep BigCasino | head -3"]))

# screenshot
base64img = sh(["screencap", "-p", "|", "base64", "-w0"])
try:
    data = base64.b64decode(base64img)
    p = pathlib.Path(r"C:\bigfish_research\toptycoon\pop_shot.png")
    p.write_bytes(data)
    print("screenshot bytes:", len(data), "->", p)
except Exception as e:
    print("screenshot failed:", e)
