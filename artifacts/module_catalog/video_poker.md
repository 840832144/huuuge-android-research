# Video Poker

Video Poker hand draws, held-card second draw, double mode and jackpots.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 7**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Services.proto`, `VideoPoker.proto`
- Services: `VideoPokerGameClient`, `VideoPokerGameServer`
- Related message types: **14**

- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.VideoPokerProto` (VideoPoker.proto)
- `Casino.VideoPokerProto.DrawNewHandRequest` (VideoPoker.proto)
- `Casino.VideoPokerProto.DrawNewHandResponse` (VideoPoker.proto)
- `Casino.VideoPokerProto.DrawSecondHandRequest` (VideoPoker.proto)
- `Casino.VideoPokerProto.DrawSecondHandResponse` (VideoPoker.proto)
- `Casino.VideoPokerProto.JackpotList` (VideoPoker.proto)
- `Casino.VideoPokerProto.JackpotList.Jackpot` (VideoPoker.proto)
- `Casino.VideoPokerProto.SelectDoubleModeCardRequest` (VideoPoker.proto)
- `Casino.VideoPokerProto.SelectDoubleModeCardResponse` (VideoPoker.proto)
- `Casino.VideoPokerProto.StartDoubleModeResponse` (VideoPoker.proto)
- `Casino.VideoPokerProto.User` (VideoPoker.proto)
- `Casino.VideoPokerProto.UserList` (VideoPoker.proto)

## RPC and flow structure

Schema flow: draw new hand -> select held cards/draw second hand -> payout state -> optional double mode/card choice -> jackpot update/hit.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `VideoPokerGameClient.RoomUsers` | `Casino.VideoPokerProto.UserList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `VideoPokerGameClient.UpdateJackpot` | `Casino.VideoPokerProto.JackpotList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `VideoPokerGameClient.HitJackpot` | `Casino.VideoPokerProto.JackpotList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `VideoPokerGameServer.DrawNewHand` | `Casino.VideoPokerProto.DrawNewHandRequest` | `Casino.VideoPokerProto.DrawNewHandResponse` | 0 | 0 | schema-only |
| `VideoPokerGameServer.DrawSecondHand` | `Casino.VideoPokerProto.DrawSecondHandRequest` | `Casino.VideoPokerProto.DrawSecondHandResponse` | 0 | 0 | schema-only |
| `VideoPokerGameServer.StartDoubleMode` | `Casino.EmptyRequest` | `Casino.VideoPokerProto.StartDoubleModeResponse` | 0 | 0 | schema-only |
| `VideoPokerGameServer.SelectDoubleModeCard` | `Casino.VideoPokerProto.SelectDoubleModeCardRequest` | `Casino.VideoPokerProto.SelectDoubleModeCardResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.VideoPokerProto.JackpotList.Jackpot.id (uint32, required)`
- `Casino.VideoPokerProto.User.user_id (int64, required)`

### Progression / state

- `Casino.VideoPokerProto.DrawSecondHandResponse.rank (Casino.Card.CardRank, optional)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.rank2 (Casino.Card.CardRank, optional)`

### Cost / input

- `Casino.VideoPokerProto.DrawNewHandRequest.bet (int64, required)`

### Currency / balance

- `Casino.VideoPokerProto.User.cash (Casino.Chips, optional)`
- `Casino.VideoPokerProto.User.event_cash (Casino.Chips, optional)`
- `Casino.VideoPokerProto.User.legacy_cash (int64, optional)`
- `Casino.VideoPokerProto.User.legacy_event_cash (int64, optional)`

### Reward / output

- `Casino.VideoPokerProto.DrawNewHandResponse.card_win (int32, repeated)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.card_win (int32, repeated)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.legacy_payout (int64, optional)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.payout (Casino.Chips, optional)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.legacy_win (uint64, optional)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.win (Casino.Chips, optional)`
- `Casino.VideoPokerProto.SelectDoubleModeCardResponse.legacy_payout (int64, optional)`
- `Casino.VideoPokerProto.SelectDoubleModeCardResponse.payout (Casino.Chips, optional)`

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.VideoPokerProto.DrawNewHandResponse.card (Casino.Card, repeated)`
- `Casino.VideoPokerProto.DrawSecondHandRequest.card (int32, repeated)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.card (Casino.Card, repeated)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.jackpot (bool, required)`
- `Casino.VideoPokerProto.DrawSecondHandResponse.poker_hand (Casino.PokerHand, optional)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.legacy_value (uint64, required)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.value (Casino.Chips, optional)`
- `Casino.VideoPokerProto.JackpotList.club_share (double, optional)`
- `Casino.VideoPokerProto.JackpotList.jackpot (Casino.VideoPokerProto.JackpotList.Jackpot, repeated)`
- `Casino.VideoPokerProto.SelectDoubleModeCardRequest.card (int32, required)`
- `Casino.VideoPokerProto.SelectDoubleModeCardResponse.card (Casino.Card, required)`
- `Casino.VideoPokerProto.SelectDoubleModeCardResponse.double_mode (bool, optional)`
- `Casino.VideoPokerProto.StartDoubleModeResponse.card (Casino.Card, required)`
- `Casino.VideoPokerProto.User.event_flags (uint64, optional)`
- `Casino.VideoPokerProto.UserList.user (Casino.VideoPokerProto.User, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: draw new hand -> select held cards/draw second hand -> payout state -> optional double mode/card choice -> jackpot update/hit.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Video Poker and mark first draw, hold selection, second draw and result.
- Play only an ordinary intended minimum-bet hand; mark double mode if naturally offered.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
