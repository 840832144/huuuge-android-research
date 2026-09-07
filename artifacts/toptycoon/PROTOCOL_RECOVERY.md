# Toy Tycoon F4 — Protocol Layer Recovered (static, via Game.Hotfix.dll)

> Static route result. The business protocol is a custom binary CG/GC message
> protocol (Google-Protobuf style), NOT HTTP JSON. This doc records the
> recovered protocol structure from the `Game.Hotfix.dll` assembly extracted
> from the YooAsset hot-update bundle.

## What was done (static route, no hooking, no root)

Extracted the hot-update logic assembly and configs from the YooAsset bundles
(`assets/yoo/Logic/*`) using UnityPy:

- `assets/bin/Data` code bundles are **UnityFS 5.x** AssetBundles (YooAsset raw
  resource bundles).
- UnityPy recovered `TextAsset` **`Game.Hotfix.dll`** (14.4MB) and
  **`Game.Hotfix.pdb`** (6.2MB) plus `main` (459KB) from the `logic_*` bundles.
- The DLL is an **Assembly Store** blob; slicing at the first `MZ...PE` yielded a
  real .NET assembly (`BSJB` metadata present).
- Parsed `TypeDef`/`MethodDef`/`Field` via `dnfile` to recover the protocol
  layer at field granularity.

## Recovered protocol structure

This is a **Google-Protobuf style** system. Each service has a `*Reflection`
registry (service descriptor), and messages come in **CG (Client->Game) / GC
(Game->Client)** pairs, plus **CL/LC** for the login service.

- **48 `*Reflection` / service descriptors** across `Protos.*`.
- **422 protocol messages** (368 with field definitions):
  - `Protos.House` (main game: Slots, Card, Reward, Charge, House, Teamduel,
    Squadrace, Steal, etc.): 274 messages.
  - `Protos.Xxxteam`: 52; `Protos` (login CL/LC): 32; `Protos.Xxxgame`: 28;
    `Protos.Xxxfriend`: 26; `Protos.Xxxmail`: 10.
- **1264 field slots** total.
- Protobuf message classes use the canonical shape: `_parser`, `_unknownFields`,
  `XxxFieldNumber` (proto tag const), `xxx_` (backing field), `*_codec`.

## Full protocol dictionary (reusable schema)

The complete schema is exported to a JSON dictionary:

```
tools/analysis/toytycoon/export_toytycoon_protocol.py <Game_Hotfix_pe.dll> <out.json>
```

Example service/message fields recovered:

- `Protos.House.GCGiveCard`: `error_`, `errmsg_`, `cards_`, `targetGuid_`,
  `giveCount_`, `giveTime_`
- `Protos.House.CGAddCard` / `GCAddCard` / `CGCardExchangeRewards` /
  `CGApplyChristmasCardMark` / `CGMyChristmasCardInfo`, ...
- `Protos.Xxxmail.MailCell` (25 fields): `oid_`, `senderGuid_`, `senderName_`,
  `createTime_`, `expireTime_`, `title_`, `content_`, `conttype_`, `isread_`...

## Config layer (client-side)

`Config.*` namespaces hold client config tables. Business fields recovered
from the string heap include `funcHost`, `token`, `freeToken`, `maxToken`,
`TokenPerEnergy`, `NoLoginTime`, `energyLoginBuffItemSource`, `fBLoginReward`,
`AdsLogindays`, `server ask`, `sendMessage`, and various `tokenId*`.

## Network transport evidence

- Runtime TCP shows business traffic to **`47.88.24.84:443`** (TLS, non-Google
  node) — the game server.
- Transport is the custom **CG/GC binary protocol over TLS**, serialized via
  protobuf `WriteTo`/`Deserialize*`. The concrete socket wrapper class is
  obfuscated (no `Client`/`Socket`/`Net`-named class); the protocol messages and
  their fields are fully recoverable statically without needing it.

## Modules beyond slots (user note)

Full idle economy sim with bottom nav modules: build (House), friends, card
packs, team, mail, and the slot/machine game. These map to the
`Protos.House` / `Protos.Xxxfriend` / `Protos.Xxxteam` / `Protos.Xxxmail` /
`Protos.Xxxgame` protocol groups.

## Reusability / safety status (most-safe method)

This static route needs **no root, no Frida, no APK repack, no injection**, and
does not touch the packer (`libpglarmor`, `libOni`). It produces the full
protocol schema (fields + tags + services) which another person can regenerate
with the standalone exporter. The exporter is under
`tools/analysis/toytycoon/`.

## Optional runtime capture of values (not yet done)

To capture runtime **field values** (not just schema), a future step could hook
the protobuf `WriteTo`/`Deserialize*` via `xlua.hotfix` (xLua runtime patch) —
reversible, no packer interference, no root. That is a separate, optional step;
the schema itself is already fully available statically.
