#!/system/bin/sh
# Long-lived task transport only. No gameplay, Frida, API token or vendor session.
set -eu
umask 077
d=/data/local/tmp/task0037/ssh
cd "$d"
# Exclusive launch reservation: never overwrite a stale or unknown PID.
mkdir running
printf '%s ' "$$" > running/owner
awk '{print $22}' /proc/$$/stat >> running/owner
child=
finish() {
    if [ -n "$child" ]; then kill -TERM "$child" 2>/dev/null || true; wait "$child" 2>/dev/null || true; fi
    rm -f running/owner
    rmdir running
    exit 0
}
trap finish TERM INT
export LD_LIBRARY_PATH=/data/local/tmp/task0037/ssh/lib
while [ ! -f stop ]; do
    ./bin/ssh -F config -N -T task0037-linux &
    child=$!
    wait "$child" || true
    child=
    sleep 5
done
finish
