# Huuuge Live Probe

Target: `com.huuuge.casino.slots`

This is a passive research collector for the user's own Android emulator session. It does not modify currency, rewards, requests, or server state. It copies the game's already-serialized/decrypted `Casino::RpcMessage` objects and decodes them with descriptors recovered from the uploaded APK.

## What the static analysis confirmed

Main native module:

```text
lib/arm64-v8a/libClawApp.so
```

Useful symbols preserved in the current APK:

```text
Casino::Connection::WriteMessage(google::protobuf::Message const&)
Casino::Connection::HandleRequest(Casino::RpcMessage const&)
Casino::Connection::HandleResponse(Casino::RpcMessage const&)
Casino::RpcMessage::ByteSize() const
Casino::RpcMessage::SerializeWithCachedSizesToArray(unsigned char*) const
```

`Connection::WriteMessage` serializes protobuf before the game's ChaCha20/socket layer. `Connection::Interpret` parses the wrapper and uses LZ4 when `uncompressed_payload_size` is present before dispatching requests/responses.

## Step 1 — discover BlueStacks and check the isolated instance

From the repository root, run the read-only host discovery first:

```powershell
.\scripts\discover_bluestacks.ps1
```

Never infer the instance from whichever ADB device happens to be first. Pass the
research instance serial explicitly:

PowerShell:

```powershell
cd <this folder>
.\check_device.ps1 -Serial 127.0.0.1:5565
```

`check_device.ps1` is intentionally read-only and no longer calls `adb root`.
Keep the output. Most important lines are the OS ABI, native bridge, package ABI,
and whether a root command actually returns `uid=0(root)`.

On BlueStacks 5 China 5.22.170.6509, merely seeing `/system/xbin/su`,
`bst.enable_root_access=1`, or `bst.config.bindmount=1` is not proof of general
root. The bundled `su` is whitelist-gated. Verify the returned UID.

## Step 2 — install host tools

```powershell
py -m pip install -U -r requirements.txt
frida --version
```

Download the **Android frida-server matching exactly the `frida --version` shown above** and matching the emulator ABI. Extract the `.xz` first. If the user-level Python Scripts directory is not on `PATH`, the repository scripts still obtain the host version through `import frida`.

Typical mapping:

- `arm64-v8a` / `aarch64` -> Android arm64 server
- `x86_64` -> Android x86_64 server

The app APK itself contains ARM64 native code, but use the **emulator OS ABI** reported by `getprop`, not the APK split name, when choosing frida-server.

## Step 3 — start frida-server

If a root command returned `uid=0(root)`:

```powershell
.\start_frida_server.ps1 `
  -Serial 127.0.0.1:5565 `
  -ServerPath "C:\path\to\frida-server"
```

Success means `frida-ps -U` lists Android processes.

For a permission diagnostic only, `-DiagnosticShellMode` starts the server as
the ADB shell user. It may enumerate processes, but it is not a working attach
path: `PermissionDeniedError` against Huuuge means root is still required.

If neither `adb root` nor `su` gives root, stop here. Do not patch the game yet; use a rooted emulator instance or a test Android emulator for the next attempt.

## Step 4 — build descriptors

From the repository root:

```powershell
py scripts\build_descriptors.py
```

This creates `artifacts\live_probe\huuuge_descriptors.pb` from the recovered `.proto` files.

## Step 5 — open Huuuge

Open Huuuge Casino normally in BlueStacks and wait until the lobby is loaded.

## Step 6 — start collector

Everything:

```powershell
py live_decode.py
```

Recommended first run, only print likely live-ops systems to console while still saving every RPC to disk:

```powershell
py live_decode.py --device-id 127.0.0.1:5565 --filter BattlePass,MiniPass,Vault,Offer,Collection,Conquest,Charm,Loyalty
```

To also print full JSON for matched messages:

```powershell
py live_decode.py --device-id 127.0.0.1:5565 --filter BattlePass --all-json
```

When an ARM64 Frida Gadget is loaded into an ARM-translated app, connect to its
forwarded listen endpoint and select the Gadget process explicitly:

```powershell
py live_decode.py --remote-endpoint 127.0.0.1:27043 --process Gadget --filter BattlePass --all-json
```

This is distinct from the x86_64 root server endpoint: the server controls the
outer BlueStacks/Houdini process, while the ARM64 Gadget exposes the translated
ARM module view needed for `libClawApp.so` symbols and interceptors.

For BlueStacks/Houdini, `bootstrap_houdini_gadget.py` can cold-spawn the app,
observe the real native-bridge namespace used for `libClawApp.so`, and load an
already-staged ARM64 Gadget through that same namespace. With Gadget configured
as `on_load: wait`, leave the bootstrap helper running, connect
`live_decode.py` to the Gadget endpoint, and the app resumes with hooks installed
before its startup RPC traffic.

Then browse the corresponding event pages in the game.

## Output

Each run creates:

```text
captures/YYYYMMDD_HHMMSS/
  index.csv
  messages.jsonl
  raw/*.rpc.bin
  json/*.json
```

`index.csv` is the fastest file to send back for triage. For detailed numerical analysis, send the session folder or `messages.jsonl` + `json/`.

## Expected Battle Pass messages

Recovered service/method examples include:

```text
AppServer.BattlePassGetDailyMissions
AppServer.BattlePassGetWeeklyMissions
AppServer.BattlePassGetMilestones
AppServer.BattlePassSkipMission
AppClient.BattlePassUpdate
AppClient.BattlePassMissionProgressUpdate
AppClient.BattlePassLevelCompleted
AppClient.BattlePassPremiumUpdate
```

The recovered Battle Pass schemas expose fields including:

```text
level
requirement
free_reward
premium_reward
deluxe_reward
progress
action_type
limitation
reward
pass_level
pass_points_balance
premium_product
deluxe_product
unlock_level
```

So one captured event update can often be converted directly into a structured reward/requirement table without OCR.
