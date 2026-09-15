#!/usr/bin/env python3
"""Pop! Slots: identify the business protocol. Check the :80 (plaintext HTTP)
host, the main :443 host, and whether it uses WebSocket / custom socket or
standard HTTP by dumping a bit of traffic (it's root+already proven for TT)."""
import subprocess
import socket

ADB = "C:/platform-tools/adb.exe"
def sh(c):
    r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell"] + c,
                       capture_output=True, text=True, timeout=40)
    return (r.stdout + r.stderr).strip()

# hex IPs from tcp -> decimal
def ip_of(h):
    # little-endian hex, e.g. 680E4112 -> 18.14.65.18
    b = bytes.fromhex(h)
    return "{}.{}.{}.{}".format(b[3], b[2], b[1], b[0])

print("== active TCP (state) to :80 (0050) and :443 (01BB) ==")
tcp = sh(["su", "-c", "cat /proc/15177/net/tcp 2>/dev/null"])
for line in tcp.splitlines()[1:]:
    parts = line.split()
    if len(parts) < 4: continue
    local, rem, state = parts[1], parts[2], parts[3]
    l_ip, l_p = local.split(":")
    r_ip, r_p = rem.split(":")
    if r_p in ("01BB", "0050", "01BB"):
        try:
            print("  local {}:{} -> {}:{} state={}".format(ip_of(l_ip), int(l_p,16), ip_of(r_ip), int(r_p,16), state))
        except Exception as e:
            pass

print("== try reverse lookup on key IPs ==")
for ip in ["18.14.65.18", "3.214.175.18", "150.6.171.104"]:
    try:
        hn = socket.gethostbyaddr(ip)
        print("  {} -> {}".format(ip, hn[0]))
    except Exception as e:
        print("  {} -> (no PTR)".format(ip))

print("== Cocos network libs (curl/socket) in maps ==")
print(sh(["su", "-c", "cat /proc/15177/maps 2>/dev/null | grep -oE '/[^ ]+\\.so' | grep -iE 'curl|socket|ssl|http' | sort -u | head -20"]))
