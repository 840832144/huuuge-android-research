# Toy Tycoon Generic Protocol Capture — Architecture & Verified Hooks

> Goal: a **module-agnostic** capture tool so the planner can extract numeric
> values for ANY module (slots, building, card packs, teams, mail, …) — not a
> slots-only viewer.
>
> Key verified finding: **`UploadHandler.Finalize` (client→server request body)
> and `DownloadHandler.Finalize` (server→client response) are the generic,
> module-agnostic capture points** — every module's traffic flows through them.
> Combined with the static 422-message protobuf schema, this yields per-module
> request/response field values.

## Verified capture architecture (2026-09-07)

```
ARM64 Frida Gadget (Houdini)  [127.0.0.1:27045]
  └─ Interceptor.attach(il2cpp_runtime_invoke)   ← runs on game thread (TLS-safe)
       ├─ capture game-thread C# calls (any class)
       └─ on runtime_invoke, watch network classes:
            UploadHandler.Finalize   → client request protobuf body
            DownloadHandler.Finalize → server response protobuf body
  + static 422-message / 1264-field protocol dict (toytycoon_protocol_dict.json)
  → decode each module's CG/GC fields
```

## Why generic (module-agnostic) works

- `UploadHandler`/`DownloadHandler`/`UnityWebRequest` are Unity's HTTP layer,
  shared by **all** server requests regardless of gameplay module. Hooking them
  is not limited to slots.
- Verified live: when the user tapped the **Building** module, both
  `UploadHandler.Finalize` (up) and `DownloadHandler.Finalize` (down) fired and
  captured request/response bytes containing readable strings (e.g. `hico`,
  `uklar`), confirming cross-module coverage.

## What we confirmed read/attachable

- `il2cpp_runtime_invoke` (game thread) — capture method names/classes.
- `BaseSlotsGame.SlotsGame/SlotColumn` (slots business), plus generic
  `Protos.House.*` messages (CGRewardList, GC*CollectReward, CGUploadEnergy,
  CGUploadCoin, etc.) and player-currency/energy fields.
- Actual balance numeric value read from game objects (e.g. ~174167 coins).

## Capture scripts (local, `C:\bigfish_research\toptycoon\`)

- `capture_net.py` — generic network hook (UploadHandler/DownloadHandler/
  UnityWebRequest), logs obj bytes during any module play.
- `capture_proto_bytes.py` / `capture_finalize_body.py` — attempt to read the
  protobuf body bytes precisely (needs a stable Gadget session; environment is
  fragile under Houdini).
- `capture_biz_invoke.py` — game-thread business-class method capture.
- `bootstrap_gadget_tt.py` — ARM64 Gadget injection (adapted Huuuge).

## Environment fragility (important)

This BlueStacks instance is **ARM64 via Houdini**; the Frida Gadget session is
**unstable** (frequent disconnects, restart needed). il2cpp/network object access
is fragile — this is an environment property, not a wrong approach. Stable
capture requires a freshly injected Gadget session used immediately, ideally
with the capture script ALREADY loaded before heavy gameplay.

## Decoding plan (next)

1. Read `UploadHandler.Finalize` return value (byte[]) — the concrete protobuf
   request body. (il2cpp byte[] layout: [0]=klass, [8]=len, [16]=data.)
2. Read `DownloadHandler` response the same way.
3. Decode with the static protobuf dict → per-module field values.

## Reusable assets

- Static protocol dict: `toytycoon_protocol_dict.json` (422 messages, 48 services).
- Root + frida-server + ARM64 Gadget injection pipeline (documented in
  ENVIRONMENT_LOCK.md / RUNTIME_CAPTURE_MINIMAL.md).
