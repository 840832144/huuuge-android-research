#!/usr/bin/env python3
"""Check Pop! Slots process state: is MainActivity resumed? engine loaded?
threads? window? """
import subprocess

ADB = "C:/platform-tools/adb.exe"
def sh(c):
    r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell"] + c,
                       capture_output=True, text=True, timeout=40)
    return (r.stdout + r.stderr).strip()

print("== top resumed activity ==")
print(sh(["dumpsys", "activity", "activities", "|", "grep", "-iE", "ResumedActivity|popslots|mResumed"]))
print("== popslots pid alive? ==")
print(sh(["ps", "-A", "|", "grep", "popslots"]))
print("== process threads of 15177 (engine loading?) ==")
print(sh(["su", "-c", "ls /proc/15177/task 2>/dev/null | wc -l"]))
print("== any window tokens for popslots ==")
print(sh(["dumpsys", "window", "windows", "|", "grep", "-iE", "popslot|Window #"]))
print("== logcat popslots proc (pid filter) ==")
print(sh(["logcat", "-d", "--pid=15177", "|", "tail", "-15"]))
