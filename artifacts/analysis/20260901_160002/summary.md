# Sanitized RPC discovery summary — 20260901_160002

This report contains aggregate metadata and protobuf field names only. Raw wrappers, decoded values, account identifiers, signatures, and local file paths are intentionally excluded from version control.

## Session facts

- First indexed message: `2026-09-01T16:00:12.879`
- Last indexed message: `2026-09-01T16:43:37.000`
- Messages: **8398**
- Decoded: **8372/8398**
- Unique service/method endpoints: **62**
- Inventory rows (direction/type-specific): **92**
- Sanitized protobuf field-path/type observations: **1313**
- Rows without decoded JSON (undecoded payloads): **26**
- Game: `12.08.27100` (`versionCode=1786533240`)
- Instrumentation: Frida/Gadget `17.17.0`, `Pie64_1 / HuuugeResearch`
- Descriptor SHA-256: `8e91f6f3b05e4ad01950d74650bdf8b00adda07ee5de6cb8c9c6d835b5aedf92`
- Capture manifest: status `stopped`; lifecycle markers: `collector-ready`, `collector-start`, `collector-stop`, `hooks-installed`

## Heuristic domain coverage

Domain labels are deterministic discovery heuristics based on service/method names; they are not claims about server-side business ownership.

| Domain | Messages | Unique endpoints |
|---|---:|---:|
| clubs/VIP/progression | 860 | 5 |
| offers/economy | 285 | 13 |
| other/unknown | 3440 | 29 |
| passes/events | 653 | 4 |
| slots | 3160 | 11 |

## Observed endpoints by domain

### clubs/VIP/progression

- `AppClient.UpdateProgress` — 651
- `AppClient.UpdateFame` — 109
- `AppClient.UpdateLoyaltyProgram` — 63
- `AppClient.UpdateCharmsProgress` — 31
- `AppServer.GetAssignmentProgress` — 6

### offers/economy

- `AppClient.UpdateShop` — 138
- `AppServer.CollectMysteryReward` — 126
- `AppClient.UpdateGift` — 5
- `AppClient.UpdateNextMysteryReward` — 3
- `AppClient.ConfirmFreeGiftRound` — 2
- `AppClient.UpdateDirectPurchaseOffer` — 2
- `AppServer.StartPersonalOffer` — 2
- `AppServer.TriggerDirectPurchaseOffer` — 2
- `AppClient.AddPersonalOffer` — 1
- `AppClient.NotifyRewardBundles` — 1
- `AppClient.OfferTrailUpdate` — 1
- `AppClient.UpdatePersonalOfferGlobals` — 1
- `AppServer.DiscardPersonalOffer` — 1

### other/unknown

- `AppServer.ResetUserInactivity` — 2974
- `AppClient.SendAdditionalData` — 295
- `AppClient.AddDciEvent` — 78
- `AppServer.` — 26
- `AppClient.LikeNotify` — 9
- `AppServer.TriggerAnnouncement` — 8
- `AppServer.GetGamePlayerCount` — 6
- `AppServer.QueryPlayer` — 6
- `AppServer.GetExtraItems` — 4
- `AppServer.GetFriends` — 4
- `AppClient.UpdateAssignmentEvents` — 3
- `AdventureServer.AdventureGetActivePhase` — 2
- `AppClient.Handshake` — 2
- `AppServer.Connect` — 2
- `AppServer.LikePlayer` — 2
- `AppServer.Login` — 2
- `AppServer.QueryGameFamily` — 2
- `AppServer.RegisterDevice` — 2
- `AppServer.SimpleRateUsTriggered` — 2
- `AppServer.UpdateFacebookToken` — 2
- `AdventureClient.AdventureUpdate` — 1
- `AppClient.LogMessage` — 1
- `AppClient.NotAcceptedUserCentricsTag` — 1
- `AppClient.SimpleRateUsInit` — 1
- `AppClient.UpdateAnnouncements` — 1
- `AppClient.UpdateBets` — 1
- `AppClient.UpdateExternalAuthMapping` — 1
- `AppServer.FocusChange` — 1
- `ContactPointClient.ContactPointUpdate` — 1

### passes/events

- `AppClient.VaultProgressUpdate` — 602
- `AppClient.BattlePassMissionProgressUpdate` — 45
- `AppClient.VaultUpdate` — 5
- `AppClient.BattlePassUpdate` — 1

### slots

- `SlotsGameClient.RoomUsers` — 1493
- `SlotsGameServer.Spin` — 1290
- `SlotsGameServer.FreeSpin` — 214
- `AppServer.GetJackpotValues` — 54
- `AppServer.GetPlayerList` — 50
- `AppServer.QueryGamePlayer` — 38
- `AppServer.QueryGame` — 8
- `SlotsGameClient.UpdateJackpot` — 5
- `AppServer.JoinGame` — 4
- `AppServer.LeaveGame` — 2
- `AppServer.ListGames` — 2

## Sanitized schema coverage

The companion `field_paths.csv` inventories observed decoded `data` paths and scalar types without retaining values. It is discovery evidence only; no business meaning or single-system numerical model is asserted in this session summary.

## Limitations / next capture improvements

- Manual module/action markers are intentionally absent from the planner workflow, so RPC bursts cannot be mapped to precise clicks beyond method semantics, timestamps and separately recorded observation baselines.
- No dedicated endpoint was observed for: Lottery, Collection Event, Conquest.
- Raw and decoded value-bearing captures remain local and are required for later numerical extraction.
