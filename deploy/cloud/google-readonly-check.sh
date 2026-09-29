#!/system/bin/sh
# TASK-0031: fixed read-only inventory; no install, enable, clear, restart or credentials.
printf 'TASK0031_GOOGLE_READONLY_BEGIN\n'
for key in ro.build.version.release ro.build.version.sdk ro.product.cpu.abi; do
    printf '%s=%s\n' "$key" "$(getprop "$key")"
done
printf 'utc=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

for pkg in com.android.vending com.google.android.gms com.google.android.gsf com.google.android.gsf.login; do
    for mode in present enabled disabled; do
        case "$mode" in
            present) out=$(pm list packages --user 0 "$pkg" 2>&1); rc=$? ;;
            enabled) out=$(pm list packages -e --user 0 "$pkg" 2>&1); rc=$? ;;
            disabled) out=$(pm list packages -d --user 0 "$pkg" 2>&1); rc=$? ;;
        esac
        case "$out" in
            *Error*|*Exception*|*Permission*|*Unknown*) rc=1 ;;
        esac
        if [ "$rc" -ne 0 ]; then
            value=unknown
        elif printf '%s\n' "$out" | grep -Fx "package:$pkg" >/dev/null; then
            value=yes
        elif [ -z "$out" ]; then
            value=no
        else
            value=unknown
        fi
        printf '%s.%s=%s\n' "$pkg" "$mode" "$value"
    done
done

if command -v curl >/dev/null 2>&1; then
    for host in play.google.com accounts.google.com; do
        code=$(curl --head --silent --connect-timeout 5 --max-time 8 \
            --output /dev/null --write-out '%{http_code}' "https://$host/" 2>/dev/null)
        rc=$?
        printf 'https.%s.http=%s exit=%s\n' "$host" "$code" "$rc"
    done
else
    printf 'https_probe=unavailable_no_curl\n'
fi
printf 'TASK0031_GOOGLE_READONLY_END\n'
