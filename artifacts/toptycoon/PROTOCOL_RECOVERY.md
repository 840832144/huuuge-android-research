# Toy Tycoon F4 — Protocol Layer Recovered (static, via Game.Hotfix.dll)

> Static route result. The business protocol is a custom binary CG/GC message
> protocol (protobuf-style), NOT HTTP JSON. This doc records the recovered
> protocol structure from the `Game.Hotfix.dll` assembly extracted from the
> YooAsset hot-update bundle.

## What was done (static route, no hooking)

Extracted the hot-update logic assembly and configs from the YooAsset bundles
(`assets/yoo/Logic/*`) using UnityPy:

- `assets/bin/Data` code bundles are **UnityFS 5.x** AssetBundles (YooAsset raw
  resource bundles).
- UnityPy recovered `TextAsset` **`Game.Hotfix.dll`** (14.4MB) and
  **`Game.Hotfix.pdb`** (6.2MB) plus `main` (459KB) from the `logic_*` bundles.
- The DLL is an **Assembly Store** blob; slicing at the first `MZ...PE` yielded a
  real .NET assembly (`BSJB` metadata present, references
  `UnityEngine`/`System`/`Http`/`WebRequest`).
- Parsed `TypeDef`/`MethodDef` via `dnfile` to recover the protocol layer.

## Recovered protocol structure

**This is a custom binary message protocol.** All business traffic uses
`Protos.*` namespaces with **pairs of CG (Client->Game request) and GC
(Game->Client response) classes**:

| namespace | module | CG/GC message pairs |
|---|---|---|
| `Protos.House` | building / house / facility | 137 |
| `Protos.Xxxteam` | team / cooperation | 26 |
| `Protos.Xxxgame` | core game | 14 |
| `Protos.Xxxfriend` | friends | 13 |
| `Protos.Xxxmail` | mail | 5 |
| **TOTAL** | | **195 pairs** |

Example protocol classes: `CGClientVersion`/`GCClientVersion`,
`CGChristmasCard*`, `CGMexicanFoodRequestMaterial*`, `CGSquadRaceInvite*`,
`CGSendChat`/`GCSendChat`, `CGSendRequest`/`GCSendRequest`.

Serialization entry points found: `WriteTo` (write) and `Deserialize*`
(`DeserializeserverActivityRow`, etc.) on the message/row classes.

## Config layer (client-side)

`Config.*` namespaces hold client config tables (e.g.
`Config.ActivityServer.serverActivity`, `Config.ThreePickOneThanksgiving`,
`Config.FivePlusOneThanksgivingDay`, `Config.ChristmasDecals`). Many business
config fields were recovered from the string heap, including `funcHost`,
`token`, `freeToken`, `maxToken`, `TokenPerEnergy`, `NoLoginTime`,
`energyLoginBuffItemSource`, `fBLoginReward`, `AdsLogindays`, `server ask`,
`sendMessage`, and various `tokenId*`.

## Network transport evidence

- Runtime TCP shows business traffic to **`47.88.24.84:443`** (TLS, non-Google
  node) — the game server.
- The transport is the custom **CG/GC binary protocol over TLS**; protocol
  frames are serialized via `WriteTo`/`Deserialize*` and carried on a socket
  (the concrete socket/session wrapper class is obfuscated — not a
  `Client`/`Socket`/`Net`-named class).
- No HTTP JSON business API seen in logs/assets.

## Modules beyond slots (user note)

The game is a full idle economy sim with bottom nav modules: build (House),
friends, card packs, team, and the slot/machine game. These map to the
`Protos.House` / `Protos.Xxxfriend` / `Protos.Xxxteam` / `Protos.Xxxgame`
protocol groups.

## Next step (awaiting direction)

Static route has bounded the protocol to 195 CG/GC message pairs, but the
concrete transport framing + host binding is in a small obfuscated socket
wrapper. To fully capture field-level protocol, a **runtime hook** is needed:
hook the `WriteTo`/`Deserialize*` chain (or the socket send/recv) via a Frida
Gadget. Note: instance is **not rooted** and has a packer (`libpglarmor`,
`libOni`), so APK-repack injection is the no-root route (contend with the
packer). Alternative: decompile the socket wrapper from the PE to read the
frame/host code statically.
