# Non-Spin Bonus Games

Bonus-game discovery, buy/info/data flows, bonus decisions/results and integration with Slots.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **35/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 7**
- Live populated field paths: **0**

## Schema scope

- Proto files: `NonSpinBonusGame.proto`, `Services.proto`, `Slots.proto`
- Services: `AppServer`, `GameHost`, `SlotsGameClient`, `SlotsGameServer`
- Related message types: **13**

- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.NonSpinBonusGameProto` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BonusResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BuyBonusRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BuyBonusResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.Data` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetDataRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetDataResponse` (NonSpinBonusGame.proto)
- `Casino.SlotsProto.PlayBonusDecision` (Slots.proto)
- `Casino.SlotsProto.SpinResponse.Bonus` (Slots.proto)

## RPC and flow structure

Schema flow: fetch bonus info/data -> optional buy bonus -> trigger from Slots -> play decision(s) -> bonus response -> finish and return to slot state.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.BuyNonSpinBonus` | `Casino.NonSpinBonusGameProto.BuyBonusRequest` | `Casino.NonSpinBonusGameProto.BuyBonusResponse` | 0 | 0 | schema-only |
| `AppServer.GetNonSpinBonusInfo` | `Casino.NonSpinBonusGameProto.GetBonusInfoRequest` | `Casino.NonSpinBonusGameProto.GetBonusInfoResponse` | 0 | 0 | schema-only |
| `GameHost.GetNonSpinBonusGameData` | `Casino.NonSpinBonusGameProto.GetDataRequest` | `Casino.NonSpinBonusGameProto.GetDataResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.TriggerNonSpinBonusGame` | `Casino.NonSpinBonusGameProto.GetDataRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.FinishNonSpinBonusGame` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.PlayNonSpinBonusGame` | `Casino.SlotsProto.PlayBonusDecision` | `Casino.SlotsProto.SpinResponse.Bonus` | 0 | 0 | schema-only |
| `SlotsGameClient.OnTriggerNonSpinBonusGameResponse` | `Casino.NonSpinBonusGameProto.BonusResponse` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Progression / state

- `Casino.NonSpinBonusGameProto.BuyBonusResponse.status (Casino.NonSpinBonusGameProto.BuyBonusResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.Data.count (uint32, required)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.status (Casino.NonSpinBonusGameProto.GetBonusInfoResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.GetDataResponse.status (Casino.NonSpinBonusGameProto.GetDataResponse.Status, required)`

### Cost / input

- `Casino.NonSpinBonusGameProto.BonusResponse.bet (uint64, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.price (Casino.Chips, optional)`
- `Casino.NonSpinBonusGameProto.Data.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.price (Casino.Chips, optional)`
- `Casino.NonSpinBonusGameProto.GetDataResponse.bet (uint64, optional)`

### Currency / balance

- `Casino.SlotsProto.SpinResponse.Bonus.cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.Bonus.legacy_cash (uint64, required)`

### Reward / output

- `Casino.NonSpinBonusGameProto.BonusResponse.bonus (Casino.SlotsProto.SpinResponse.Bonus, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.bonus_name (string, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusResponse.non_spin_bonus_game (Casino.NonSpinBonusGameProto.Data, optional)`
- `Casino.NonSpinBonusGameProto.Data.bonus_name (string, required)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.bonus_name (string, required)`
- `Casino.NonSpinBonusGameProto.GetDataRequest.bonus_name (string, required)`

### Timing / reset / expiry

- `Casino.NonSpinBonusGameProto.Data.end_time (uint32, required)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.NonSpinBonusGameProto.BonusResponse.free_spins (Casino.SlotsProto.SpinResponse.FreeSpins, optional)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.family_name (string, optional)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.slot_name (string, optional)`
- `Casino.NonSpinBonusGameProto.BuyBonusResponse.error_code (int32, optional)`
- `Casino.NonSpinBonusGameProto.Data.family_name (string, optional)`
- `Casino.NonSpinBonusGameProto.Data.type (uint32, required)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.family_name (string, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.slot_name (string, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.error_code (int32, optional)`
- `Casino.NonSpinBonusGameProto.GetDataRequest.family_name (string, optional)`
- `Casino.SlotsProto.PlayBonusDecision.decision (uint32, repeated)`
- `Casino.SlotsProto.SpinResponse.Bonus.result (uint32, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: fetch bonus info/data -> optional buy bonus -> trigger from Slots -> play decision(s) -> bonus response -> finish and return to slot state.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_dailybonus_2_etc2.zpk`
- ZPK asset: `assets/atlas_dailybonus_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/sound_minigames.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Enter a slot with a visible non-spin bonus and mark trigger/start/end.
- Inspect bonus-info and buy-bonus screens without purchasing unless already intended.
- Play one naturally triggered bonus decision path.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
