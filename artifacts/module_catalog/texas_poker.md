# Texas Poker

Texas game snapshots, player actions, buy-in/rebuy, blinds, auto-actions, tips and tournament completion.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 10**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Services.proto`, `Texas.proto`
- Services: `TexasGameClient`, `TexasGameServer`
- Related message types: **19**

- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.TexasProto` (Texas.proto)
- `Casino.TexasProto.AutoAction` (Texas.proto)
- `Casino.TexasProto.CollectBuyinReq` (Texas.proto)
- `Casino.TexasProto.Config` (Texas.proto)
- `Casino.TexasProto.FinishTournamentReq` (Texas.proto)
- `Casino.TexasProto.FinishTournamentReq.PlaceInfo` (Texas.proto)
- `Casino.TexasProto.Game` (Texas.proto)
- `Casino.TexasProto.NextBlindsReq` (Texas.proto)
- `Casino.TexasProto.PerformAction` (Texas.proto)
- `Casino.TexasProto.Player` (Texas.proto)
- `Casino.TexasProto.ReBuyReq` (Texas.proto)
- `Casino.TexasProto.ReBuyRes` (Texas.proto)
- `Casino.TexasProto.Seat` (Texas.proto)
- `Casino.TexasProto.TipDealer` (Texas.proto)
- `Casino.TexasProto.TipDealerNotify` (Texas.proto)
- `Casino.TexasProto.UpdateGame` (Texas.proto)
- `Casino.TexasProto.Winner` (Texas.proto)

## RPC and flow structure

Schema flow: join/set ready -> game snapshots -> perform/auto actions -> blinds/buy-in/rebuy/tip events -> tournament finish/place info.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `TexasGameServer.PerformAction` | `Casino.TexasProto.PerformAction` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameServer.TipDealer` | `Casino.TexasProto.TipDealer` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameServer.ReBuy` | `Casino.TexasProto.ReBuyReq` | `Casino.TexasProto.ReBuyRes` | 0 | 0 | schema-only |
| `TexasGameServer.UpdateAutoAction` | `Casino.TexasProto.AutoAction` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameServer.SetReady` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameClient.UpdateGame` | `Casino.TexasProto.UpdateGame` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameClient.NotifyTipDealer` | `Casino.TexasProto.TipDealerNotify` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameClient.CollectBuyin` | `Casino.TexasProto.CollectBuyinReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameClient.FinishTournament` | `Casino.TexasProto.FinishTournamentReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `TexasGameClient.NextBlinds` | `Casino.TexasProto.NextBlindsReq` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.TexasProto.Config.game_id (string, required)`
- `Casino.TexasProto.FinishTournamentReq.PlaceInfo.user_id (int64, required)`
- `Casino.TexasProto.Player.user_id (int64, optional)`
- `Casino.TexasProto.Seat.player (Casino.TexasProto.Player, optional)`
- `Casino.TexasProto.TipDealerNotify.user_id (int64, required)`
- `Casino.TexasProto.UpdateGame.game (Casino.TexasProto.Game, optional)`
- `Casino.TexasProto.Winner.user_id (int64, required)`

### Progression / state

- `Casino.TexasProto.Game.active_player (int32, optional)`
- `Casino.TexasProto.Game.state (Casino.TexasProto.State, optional)`
- `Casino.TexasProto.PerformAction.state (Casino.TexasProto.State, optional)`
- `Casino.TexasProto.ReBuyRes.status (Casino.TexasProto.ReBuyRes.Status, required)`
- `Casino.TexasProto.Seat.state (Casino.TexasProto.Seat.State, required)`

### Cost / input

- `Casino.TexasProto.Game.stake (uint64, optional)`
- `Casino.TexasProto.Player.stake (uint64, optional)`

### Currency / balance

- `Casino.TexasProto.CollectBuyinReq.chips_delta (int64, required)`
- `Casino.TexasProto.FinishTournamentReq.chips (uint64, optional)`
- `Casino.TexasProto.PerformAction.chips (int64, optional)`
- `Casino.TexasProto.Player.chips (uint64, optional)`
- `Casino.TexasProto.ReBuyReq.chips (uint64, required)`
- `Casino.TexasProto.TipDealer.chips (uint64, required)`
- `Casino.TexasProto.TipDealerNotify.chips (uint64, required)`
- `Casino.TexasProto.UpdateGame.chips_delta (int64, optional)`

### Reward / output

- `Casino.TexasProto.Game.win_hand (Casino.TexasProto.Hand, optional)`
- `Casino.TexasProto.Game.winners (Casino.TexasProto.Winner, repeated)`
- `Casino.TexasProto.Player.win_chips (uint64, optional)`

### Timing / reset / expiry

- `Casino.TexasProto.Config.move_time (int64, optional)`
- `Casino.TexasProto.Config.showdown_time (int64, optional)`
- `Casino.TexasProto.Game.timer (int64, optional)`
- `Casino.TexasProto.NextBlindsReq.timestamp (int64, optional)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.TexasProto.AutoAction.enabled (bool, required)`
- `Casino.TexasProto.AutoAction.mode (Casino.TexasProto.AutoAction.Mode, optional)`
- `Casino.TexasProto.Config.start_delay (int64, optional)`
- `Casino.TexasProto.FinishTournamentReq.PlaceInfo.place (uint32, required)`
- `Casino.TexasProto.FinishTournamentReq.places (Casino.TexasProto.FinishTournamentReq.PlaceInfo, repeated)`
- `Casino.TexasProto.Game.big_blind (uint64, optional)`
- `Casino.TexasProto.Game.community_cards (Casino.Card, repeated)`
- `Casino.TexasProto.Game.dealer (int32, optional)`
- `Casino.TexasProto.Game.my_hand (Casino.TexasProto.Hand, optional)`
- `Casino.TexasProto.Game.pot (uint64, optional)`
- `Casino.TexasProto.Game.rake (uint64, optional)`
- `Casino.TexasProto.Game.seats (Casino.TexasProto.Seat, repeated)`
- `Casino.TexasProto.Game.small_blind (uint64, optional)`
- `Casino.TexasProto.NextBlindsReq.big_blind (uint64, required)`
- `Casino.TexasProto.NextBlindsReq.small_blind (uint64, required)`
- `Casino.TexasProto.PerformAction.action (Casino.TexasProto.Action, optional)`
- `Casino.TexasProto.PerformAction.game_seq (uint32, required)`
- `Casino.TexasProto.Player.blind (Casino.TexasProto.Blind, optional)`
- `Casino.TexasProto.Player.last_action (Casino.TexasProto.Action, optional)`
- `Casino.TexasProto.Player.pocket_cards (Casino.Card, repeated)`
- `Casino.TexasProto.UpdateGame.config (Casino.TexasProto.Config, optional)`
- `Casino.TexasProto.UpdateGame.game_seq (uint32, required)`
- `Casino.TexasProto.Winner.cards (Casino.Card, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: join/set ready -> game snapshots -> perform/auto actions -> blinds/buy-in/rebuy/tip events -> tournament finish/place info.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open a Texas table/tournament and mark lobby, buy-in, hand and result.
- Play only an ordinary intended low-stakes hand and inspect blinds/rebuy UI.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
