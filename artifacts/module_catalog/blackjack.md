# Blackjack

Blackjack room state, bets, actions, insurance and payout.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 6**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Blackjack.proto`, `Services.proto`
- Services: `BlackjackGameClient`, `BlackjackGameServer`
- Related message types: **15**

- `Casino.BlackjackActionRequest` (Blackjack.proto)
- `Casino.BlackjackActionResponse` (Blackjack.proto)
- `Casino.BlackjackBetRequest` (Blackjack.proto)
- `Casino.BlackjackCard` (Blackjack.proto)
- `Casino.BlackjackHand` (Blackjack.proto)
- `Casino.BlackjackInsuranceResponse` (Blackjack.proto)
- `Casino.BlackjackPayoutRequest` (Blackjack.proto)
- `Casino.BlackjackPod` (Blackjack.proto)
- `Casino.BlackjackProto` (Blackjack.proto)
- `Casino.BlackjackStartBetsRequest` (Blackjack.proto)
- `Casino.BlackjackState` (Blackjack.proto)
- `Casino.BlackjackUserSeat` (Blackjack.proto)
- `Casino.BlackjackUsersList` (Blackjack.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)

## RPC and flow structure

Schema flow: join/room users -> start bets/set bet -> action/progress sequence -> optional insurance -> payout.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `BlackjackGameServer.SetBet` | `Casino.BlackjackBetRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BlackjackGameClient.StartPlacingBets` | `Casino.BlackjackStartBetsRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BlackjackGameClient.RoomUsers` | `Casino.BlackjackUsersList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BlackjackGameClient.Progress` | `Casino.BlackjackActionRequest` | `Casino.BlackjackActionResponse` | 0 | 0 | schema-only |
| `BlackjackGameClient.Payout` | `Casino.BlackjackPayoutRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `BlackjackGameClient.Insurance` | `Casino.EmptyRequest` | `Casino.BlackjackInsuranceResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Progression / state

- `Casino.BlackjackActionRequest.state (Casino.BlackjackState, required)`
- `Casino.BlackjackCard.rank (Casino.BlackjackCard.CardRank, required)`
- `Casino.BlackjackHand.points (uint32, required)`
- `Casino.BlackjackPayoutRequest.state (Casino.BlackjackState, required)`

### Cost / input

- `Casino.BlackjackBetRequest.bet (uint64, required)`
- `Casino.BlackjackHand.bet (uint64, optional)`

### Currency / balance

- `Casino.BlackjackPod.cash (Casino.Chips, optional)`
- `Casino.BlackjackPod.legacy_cash (int64, optional)`
- `Casino.BlackjackUserSeat.cash (Casino.Chips, optional)`
- `Casino.BlackjackUserSeat.legacy_cash (int64, required)`

### Reward / output

- `Casino.BlackjackHand.payout (uint64, optional)`

### Timing / reset / expiry

- `Casino.BlackjackStartBetsRequest.timeToBet (uint32, required)`

### Segment / eligibility / limit

- `Casino.BlackjackActionRequest.actionAllowed (uint32, optional)`

### Other structural fields

- `Casino.BlackjackActionRequest.action (Casino.BlackjackActionRequest.ActionRequest, required)`
- `Casino.BlackjackActionResponse.action (uint32, optional)`
- `Casino.BlackjackCard.suit (Casino.BlackjackCard.CardSuit, required)`
- `Casino.BlackjackHand.cards (Casino.BlackjackCard, repeated)`
- `Casino.BlackjackInsuranceResponse.insurance (Casino.BlackjackInsuranceResponse.InsuranceResponse, required)`
- `Casino.BlackjackPod.current (bool, optional)`
- `Casino.BlackjackPod.event_flags (uint64, optional)`
- `Casino.BlackjackPod.hands (Casino.BlackjackHand, repeated)`
- `Casino.BlackjackPod.userId (uint64, required)`
- `Casino.BlackjackState.gameSeq (uint32, required)`
- `Casino.BlackjackState.pods (Casino.BlackjackPod, repeated)`
- `Casino.BlackjackUserSeat.seat (int32, required)`
- `Casino.BlackjackUserSeat.userId (uint64, required)`
- `Casino.BlackjackUsersList.users (Casino.BlackjackUserSeat, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: join/room users -> start bets/set bet -> action/progress sequence -> optional insurance -> payout.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open a Blackjack room and mark betting/action/result states.
- Play only one ordinary intended minimum-bet round and mark insurance if offered.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
