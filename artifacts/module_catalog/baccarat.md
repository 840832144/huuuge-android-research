# Baccarat

Baccarat room users, betting window, bet updates, configuration and payout.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 6**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Baccarat.proto`, `Services.proto`
- Services: `BaccaratGameClient`, `BaccaratGameServer`
- Related message types: **15**

- `Casino.BaccaratProto` (Baccarat.proto)
- `Casino.BaccaratProto.AddBetReq` (Baccarat.proto)
- `Casino.BaccaratProto.BaccaratBet` (Baccarat.proto)
- `Casino.BaccaratProto.Card` (Baccarat.proto)
- `Casino.BaccaratProto.Configuration` (Baccarat.proto)
- `Casino.BaccaratProto.ConfirmRes` (Baccarat.proto)
- `Casino.BaccaratProto.PayoutReq` (Baccarat.proto)
- `Casino.BaccaratProto.StartBettingReq` (Baccarat.proto)
- `Casino.BaccaratProto.UpdateBetsReq` (Baccarat.proto)
- `Casino.BaccaratProto.UserBets` (Baccarat.proto)
- `Casino.BaccaratProto.UserPayouts` (Baccarat.proto)
- `Casino.BaccaratProto.UserSeat` (Baccarat.proto)
- `Casino.BaccaratProto.UsersListReq` (Baccarat.proto)
- `Casino.BaccaratProto.WinHistory` (Baccarat.proto)
- `Casino.EmptyResponse` (Services.proto)

## RPC and flow structure

Schema flow: join/config/room users -> start betting -> add/update bets -> close/result -> payout update.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `BaccaratGameServer.AddBet` | `Casino.BaccaratProto.AddBetReq` | `Casino.BaccaratProto.ConfirmRes` | 0 | 0 | schema-only |
| `BaccaratGameClient.RoomUsers` | `Casino.BaccaratProto.UsersListReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BaccaratGameClient.StartPlacingBets` | `Casino.BaccaratProto.StartBettingReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BaccaratGameClient.UpdateBets` | `Casino.BaccaratProto.UpdateBetsReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BaccaratGameClient.Payout` | `Casino.BaccaratProto.PayoutReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BaccaratGameClient.SetConfiguration` | `Casino.BaccaratProto.Configuration` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.BaccaratProto.BaccaratBet.player (uint64, optional)`
- `Casino.BaccaratProto.PayoutReq.player (Casino.BaccaratProto.Card, repeated)`

### Progression / state

- `Casino.BaccaratProto.Card.rank (Casino.BaccaratProto.Card.CardRank, required)`
- `Casino.BaccaratProto.ConfirmRes.status (Casino.BaccaratProto.ConfirmRes.Status, required)`

### Cost / input

- `Casino.BaccaratProto.AddBetReq.bet (Casino.BaccaratProto.BaccaratBet, required)`
- `Casino.BaccaratProto.UserBets.bet (Casino.BaccaratProto.BaccaratBet, required)`

### Currency / balance

- `Casino.BaccaratProto.UserBets.cash (Casino.Chips, optional)`
- `Casino.BaccaratProto.UserBets.legacy_cash (int64, required)`
- `Casino.BaccaratProto.UserPayouts.cash (Casino.Chips, optional)`
- `Casino.BaccaratProto.UserPayouts.legacy_cash (int64, required)`
- `Casino.BaccaratProto.UserSeat.cash (Casino.Chips, optional)`
- `Casino.BaccaratProto.UserSeat.legacy_cash (int64, required)`

### Reward / output

- `Casino.BaccaratProto.PayoutReq.winType (uint64, required)`
- `Casino.BaccaratProto.UserPayouts.payout (uint64, required)`
- `Casino.BaccaratProto.WinHistory.wins (uint64, repeated)`

### Timing / reset / expiry

- `Casino.BaccaratProto.Configuration.payoutTime (float, required)`
- `Casino.BaccaratProto.Configuration.refillTime (float, required)`
- `Casino.BaccaratProto.PayoutReq.timestamp (int64, optional)`
- `Casino.BaccaratProto.StartBettingReq.timestamp (int64, optional)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.BaccaratProto.AddBetReq.gameId (uint32, required)`
- `Casino.BaccaratProto.BaccaratBet.dealer (uint64, optional)`
- `Casino.BaccaratProto.BaccaratBet.dealerPair (uint64, optional)`
- `Casino.BaccaratProto.BaccaratBet.playerPair (uint64, optional)`
- `Casino.BaccaratProto.BaccaratBet.tie (uint64, optional)`
- `Casino.BaccaratProto.Card.suit (Casino.BaccaratProto.Card.CardSuit, required)`
- `Casino.BaccaratProto.PayoutReq.dealer (Casino.BaccaratProto.Card, repeated)`
- `Casino.BaccaratProto.PayoutReq.gameId (uint32, required)`
- `Casino.BaccaratProto.PayoutReq.refill (bool, optional)`
- `Casino.BaccaratProto.PayoutReq.users (Casino.BaccaratProto.UserPayouts, repeated)`
- `Casino.BaccaratProto.StartBettingReq.gameId (uint32, required)`
- `Casino.BaccaratProto.UpdateBetsReq.gameId (uint32, required)`
- `Casino.BaccaratProto.UpdateBetsReq.users (Casino.BaccaratProto.UserBets, repeated)`
- `Casino.BaccaratProto.UserBets.userId (uint64, required)`
- `Casino.BaccaratProto.UserPayouts.event_flags (uint64, optional)`
- `Casino.BaccaratProto.UserPayouts.userId (uint64, required)`
- `Casino.BaccaratProto.UserSeat.seat (int32, required)`
- `Casino.BaccaratProto.UserSeat.userId (uint64, required)`
- `Casino.BaccaratProto.UsersListReq.history (Casino.BaccaratProto.WinHistory, optional)`
- `Casino.BaccaratProto.UsersListReq.users (Casino.BaccaratProto.UserSeat, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: join/config/room users -> start betting -> add/update bets -> close/result -> payout update.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open a Baccarat room and mark join/config/betting/result.
- Place only an ordinary intended minimum bet and observe one completed round.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
