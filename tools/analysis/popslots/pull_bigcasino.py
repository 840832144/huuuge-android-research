#!/usr/bin/env python3
"""Pull libBigCasino.so from Pop! Slots APK (arm path in base.apk) for static
analysis. Also locate it on the running process."""
import subprocess
import pathlib

ADB = "C:/platform-tools/adb.exe"
def sh(c):
    r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell"] + c,
                       capture_output=True, text=True, timeout=60)
    return (r.stdout + r.stderr).strip()

print("== find libBigCasino.so in apk ==")
print(sh(["su", "-c", "unzip -l /data/app/com.playstudios.popslots-0rQKzkNbsJ4Xkb3m5Azlfg==/base.apk 2>/dev/null | grep -i 'libBigCasino'"]))
print("== extract to /data/local/tmp ==")
print(sh(["su", "-c", "cd /data/local/tmp && unzip -o /data/app/com.playstudios.popslots-0rQKzkNbsJ4Xkb3m5Azlfg==/base.apk 'lib/x86_64/libBigCasino.so' >/dev/null 2>&1 && ls -la /data/local/tmp/lib/x86_64/libBigCasino.so 2>&1"]))
print("== pull to host ==")
r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "pull",
                    "/data/local/tmp/lib/x86_64/libBigCasino.so",
                    r"C:\bigfish_research\toptycoon\libBigCasino.so"],
                   capture_output=True, text=True, timeout=120)
print(r.stdout.strip(), r.stderr.strip()[-200:])
p = pathlib.Path(r"C:\bigfish_research\toptycoon\libBigCasino.so")
if p.exists():
    print("pulled size:", p.stat().st_size)
