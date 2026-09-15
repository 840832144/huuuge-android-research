#!/usr/bin/env python3
"""Determine whether Pop! Slots lobby/characters are rendered by WebView (JS/
HTML5) or the native Shaker engine. Check WebView urls, loaded web assets, and
which process space renders."""
import subprocess

ADB = "C:/platform-tools/adb.exe"
def sh(c):
    r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell"] + c,
                       capture_output=True, text=True, timeout=40)
    return (r.stdout + r.stderr).strip()

print("== webview files (html/js/assets) in app data ==")
print(sh(["su", "-c", "find /data/data/com.playstudios.popslots -type f 2>/dev/null | grep -iE 'webview|htt|cache|http' | head -20"]))
print("== webview data dir contents ==")
print(sh(["su", "-c", "ls -R /data/data/com.playstudios.popslots/app_webview 2>/dev/null | head -30"]))
print("== app assets (js/html/unity in apk) ==")
print(sh(["su", "-c", "unzip -l /data/app/com.playstudios.popslots-0rQKzkNbsJ4Xkb3m5Azlfg==/base.apk 2>/dev/null | grep -iE '\\.js$|\\.html$|assets/' | head -30"]))
print("== crwebview / chrome process for popslots ==")
print(sh(["ps", "-A", "|", "grep", "-iE", "popslot|webview|chrome|sandbox"]))
print("== netstat: any non-80/443 (websocket) ==")
print(sh(["su", "-c", "cat /proc/15177/net/tcp 2>/dev/null | awk 'NR>1{print $2,$3,$4}' | head -20"]))
