# Sanitized RPC discovery summary — 20260825_182300

This report contains aggregate metadata and protobuf field names only. Raw wrappers, decoded values, account identifiers, signatures, and local file paths are intentionally excluded from version control.

## Session facts

- Capture start: `2026-08-25T18:23:06.234`
- Capture end: `2026-08-25T18:29:29.701`
- Messages: **741**
- Decoded: **741/741**
- Unique service/method endpoints: **42**
- Inventory rows (direction/type-specific): **66**
- Sanitized protobuf field-path/type observations: **511**
- Missing decoded JSON files during summary: **0**
- Game: `12.07.27012` (`versionCode=1784198526`)
- Instrumentation: Frida/Gadget `17.17.0`, `Pie64_1 / HuuugeResearch / 127.0.0.1:5565 / Houdini ARM64 Gadget`
- Descriptor SHA-256: `8e91f6f3b05e4ad01950d74650bdf8b00adda07ee5de6cb8c9c6d835b5aedf92`

## Heuristic domain coverage

Domain labels are deterministic discovery heuristics based on service/method names; they are not claims about server-side business ownership.

| Domain | Messages | Unique endpoints |
|---|---:|---:|
| clubs/VIP/progression | 70 | 4 |
| offers/economy | 55 | 12 |
| other/unknown | 217 | 11 |
| passes/events | 15 | 5 |
| slots | 384 | 10 |

## Observed endpoints by domain

### clubs/VIP/progression

- `AppClient.UpdateProgress` — 59
- `AppClient.UpdateLoyaltyProgram` — 5
- `AppClient.UpdateFame` — 4
- `AppClient.UpdateCharmsProgress` — 2

### offers/economy

- `AppClient.UpdateShop` — 24
- `AppServer.CollectMysteryReward` — 10
- `AppServer.MakeInAppPurchase` — 4
- `AppServer.TriggerDirectPurchaseOffer` — 4
- `AppClient.ConfirmFreeGiftRound` — 2
- `AppServer.ClaimRewardBundleBulk` — 2
- `AppServer.CollectFreeDiamonds` — 2
- `AppServer.CollectShopBonus` — 2
- `AppServer.StartPersonalOffer` — 2
- `AppClient.OfferTrailUpdate` — 1
- `AppClient.UpdateGift` — 1
- `AppServer.DiscardPersonalOffer` — 1

### other/unknown

- `AppServer.ResetUserInactivity` — 140
- `AppClient.SendAdditionalData` — 46
- `AppServer.TriggerAnnouncement` — 8
- `AppClient.UpdateAnnouncements` — 7
- `AppClient.AddDciEvent` — 5
- `AppServer.CollectHourlyBonus` — 2
- `AppServer.FocusChange` — 2
- `AppServer.LikePlayer` — 2
- `AppServer.QueryPlayer` — 2
- `AppServer.SyncTime` — 2
- `AppClient.LikeNotify` — 1

### passes/events

- `AppClient.VaultUpdate` — 5
- `MiniPassClient.MiniPassMissionCompleted` — 5
- `MiniPassServer.MiniPassGetMissions` — 2
- `MiniPassServer.MiniPassTutorialCompleted` — 2
- `MiniPassClient.MiniPassMilestoneCompleted` — 1

### slots

- `SlotsGameClient.RoomUsers` — 116
- `AppServer.GetPlayerList` — 96
- `AppServer.GetJackpotValues` — 60
- `SlotsGameServer.Spin` — 58
- `SlotsGameClient.UpdateJackpot` — 26
- `AppServer.QueryGame` — 12
- `AppServer.JoinGame` — 4
- `AppServer.LeaveGame` — 4
- `AppServer.ListGames` — 4
- `AppServer.QueryGamePlayer` — 4

## Sanitized schema coverage

The companion `field_paths.csv` inventories observed decoded `data` paths and scalar types without retaining values. It is discovery evidence only; no business meaning or single-system numerical model is asserted in this session summary.

## Limitations / next capture improvements

- This session predates first-class `manifest.json` generation; version and hash facts here were supplied during post-capture summarization.
- No action markers were recorded, so RPC bursts cannot be mapped to precise clicks beyond method semantics and timestamps.
- No Lottery, Battle Pass, Collection Event, or Conquest endpoint was observed in this session.
- Raw and decoded value-bearing captures remain local and are required for later numerical extraction.
