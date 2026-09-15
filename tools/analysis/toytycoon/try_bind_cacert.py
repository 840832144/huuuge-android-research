#!/usr/bin/env python3
"""Attempt bind-mount a writable cacerts dir over /system/etc/security/cacerts,
and drop the mitmproxy CA into it. Root-only."""
import subprocess

ADB = "C:\\platform-tools\\adb.exe"
def sh(cmd):
    r = subprocess.run([ADB,"-s","127.0.0.1:5605","shell"] + cmd, capture_output=True, text=True, timeout=40)
    return (r.stdout + r.stderr).strip()

# cert hash filename for system CACerts
FN = "b69ec367.0"
CERT_SRC = "/data/local/tmp/mitm-ca.pem"

# 1) push cert to a writable spot
subprocess.run([ADB,"-s","127.0.0.1:5605","push",
    r"C:\bigfish_research\toptycoon\mitm\mitmproxy-ca-cert.cer", CERT_SRC], capture_output=True)

# 2) make a writable cert dir on /data (rw) and copy cert in
print("== mkdir /data/local/cacerts ==")
print(sh(["su","-c","mkdir -p /data/local/cacerts && cp {s} /data/local/cacerts/{f} && chmod 644 /data/local/cacerts/{f} && ls -la /data/local/cacerts/".format(s=CERT_SRC, f=FN)]))
print("== try bind mount /data/local/cacerts over /system/etc/security/cacerts ==")
print(sh(["su","-c","mount -o bind /data/local/cacerts /system/etc/security/cacerts 2>&1 || echo FAIL"]))
print("== verify ==")
print(sh(["su","-c","ls -la /system/etc/security/cacerts/ 2>&1 | grep {f}".format(f=FN)]))
print("== try remount /system now (post-bind) ==")
print(sh(["su","-c","mount -o rw,remount /system 2>&1 || echo FAIL"]))
