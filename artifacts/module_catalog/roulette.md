# Roulette

Roulette room state, readiness, betting windows, bet updates and payout.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 6**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Roulette.proto`, `Services.proto`
- Services: `RouletteGameClient`, `RouletteGameServer`
- Related message types: **14**

- `Casino.EmptyResponse` (Services.proto)
- `Casino.RouletteProto` (Roulette.proto)
- `Casino.RouletteProto.AddBetReq` (Roulette.proto)
- `Casino.RouletteProto.ConfirmRes` (Roulette.proto)
- `Casino.RouletteProto.PayoutReq` (Roulette.proto)
- `Casino.RouletteProto.ReadyReq` (Roulette.proto)
- `Casino.RouletteProto.RouletteBet` (Roulette.proto)
- `Casino.RouletteProto.StartBettingReq` (Roulette.proto)
- `Casino.RouletteProto.UpdateBetsReq` (Roulette.proto)
- `Casino.RouletteProto.UserBets` (Roulette.proto)
- `Casino.RouletteProto.UserPayouts` (Roulette.proto)
- `Casino.RouletteProto.UserSeat` (Roulette.proto)
- `Casino.RouletteProto.UsersListReq` (Roulette.proto)
- `Casino.RouletteProto.WinHistory` (Roulette.proto)

## RPC and flow structure

Schema flow: join/ready/room users -> start betting -> add/update bets -> wheel result -> payout.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `RouletteGameServer.AddBet` | `Casino.RouletteProto.AddBetReq` | `Casino.RouletteProto.ConfirmRes` | 0 | 0 | schema-only |
| `RouletteGameServer.Ready` | `Casino.RouletteProto.ReadyReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `RouletteGameClient.RoomUsers` | `Casino.RouletteProto.UsersListReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `RouletteGameClient.StartPlacingBets` | `Casino.RouletteProto.StartBettingReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `RouletteGameClient.UpdateBets` | `Casino.RouletteProto.UpdateBetsReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `RouletteGameClient.Payout` | `Casino.RouletteProto.PayoutReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Progression / state

- `Casino.RouletteProto.ConfirmRes.status (Casino.RouletteProto.ConfirmRes.Status, required)`

### Cost / input

- `Casino.RouletteProto.AddBetReq.bets (Casino.RouletteProto.RouletteBet, repeated)`
- `Casino.RouletteProto.RouletteBet.bet (uint64, required)`
- `Casino.RouletteProto.UserBets.bets (Casino.RouletteProto.RouletteBet, repeated)`

### Currency / balance

- `Casino.RouletteProto.UserBets.cash (Casino.Chips, optional)`
- `Casino.RouletteProto.UserBets.legacy_cash (int64, required)`
- `Casino.RouletteProto.UserPayouts.cash (Casino.Chips, optional)`
- `Casino.RouletteProto.UserPayouts.legacy_cash (int64, required)`
- `Casino.RouletteProto.UserSeat.cash (Casino.Chips, optional)`
- `Casino.RouletteProto.UserSeat.legacy_cash (int64, required)`

### Reward / output

- `Casino.RouletteProto.PayoutReq.winField (int32, required)`
- `Casino.RouletteProto.UserPayouts.payout (uint64, required)`
- `Casino.RouletteProto.WinHistory.winFields (int32, repeated)`

### Timing / reset / expiry

- `Casino.RouletteProto.PayoutReq.timestamp (int64, optional)`
- `Casino.RouletteProto.StartBettingReq.resetReady (bool, required)`
- `Casino.RouletteProto.StartBettingReq.timeToBet (uint32, required)`
- `Casino.RouletteProto.StartBettingReq.timestamp (int64, optional)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.RouletteProto.AddBetReq.gameId (uint32, required)`
- `Casino.RouletteProto.PayoutReq.gameId (uint32, required)`
- `Casino.RouletteProto.PayoutReq.users (Casino.RouletteProto.UserPayouts, repeated)`
- `Casino.RouletteProto.ReadyReq.gameId (uint32, required)`
- `Casino.RouletteProto.RouletteBet.posX (int32, required)`
- `Casino.RouletteProto.RouletteBet.posY (int32, required)`
- `Casino.RouletteProto.StartBettingReq.gameId (uint32, required)`
- `Casino.RouletteProto.UpdateBetsReq.gameId (uint32, required)`
- `Casino.RouletteProto.UpdateBetsReq.users (Casino.RouletteProto.UserBets, repeated)`
- `Casino.RouletteProto.UserBets.userId (uint64, required)`
- `Casino.RouletteProto.UserPayouts.event_flags (uint64, optional)`
- `Casino.RouletteProto.UserPayouts.userId (uint64, required)`
- `Casino.RouletteProto.UserSeat.ready (bool, optional)`
- `Casino.RouletteProto.UserSeat.seat (int32, required)`
- `Casino.RouletteProto.UserSeat.userId (uint64, required)`
- `Casino.RouletteProto.UsersListReq.history (Casino.RouletteProto.WinHistory, optional)`
- `Casino.RouletteProto.UsersListReq.users (Casino.RouletteProto.UserSeat, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: join/ready/room users -> start betting -> add/update bets -> wheel result -> payout.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open a Roulette room and mark ready/betting/result.
- Play only one ordinary intended minimum-bet round and inspect bet types.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
