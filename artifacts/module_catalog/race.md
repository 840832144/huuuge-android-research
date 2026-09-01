# Race

Race status updates, leaderboard/detail queries, rank changes and place rewards.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 3**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Race.proto`, `Services.proto`
- Services: `RaceClient`, `RaceServer`
- Related message types: **14**

- `Casino.EmptyResponse` (Services.proto)
- `Casino.RaceProto` (Race.proto)
- `Casino.RaceProto.GetLeaderboardsRequest` (Race.proto)
- `Casino.RaceProto.GetLeaderboardsResponse` (Race.proto)
- `Casino.RaceProto.LeaderboardPosition` (Race.proto)
- `Casino.RaceProto.PlaceReward` (Race.proto)
- `Casino.RaceProto.RaceGetDetailedLeaderboardRequest` (Race.proto)
- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse` (Race.proto)
- `Casino.RaceProto.RaceUpdateStatusRequest` (Race.proto)
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification` (Race.proto)
- `Casino.RaceProto.ShortLeaderboard` (Race.proto)
- `Casino.RaceProto.ShortLeaderboard.Bundle` (Race.proto)
- `Casino.RaceProto.ShortLeaderboard.Limitation` (Race.proto)
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value` (Race.proto)

## RPC and flow structure

Schema flow: server status update -> leaderboard/detail fetch -> qualifying play changes score/rank -> rank-change notification -> place reward.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `RaceServer.RaceGetLeaderboards` | `Casino.RaceProto.GetLeaderboardsRequest` | `Casino.RaceProto.GetLeaderboardsResponse` | 0 | 0 | schema-only |
| `RaceServer.RaceGetDetailedLeaderboard` | `Casino.RaceProto.RaceGetDetailedLeaderboardRequest` | `Casino.RaceProto.RaceGetDetailedLeaderboardResponse` | 0 | 0 | schema-only |
| `RaceClient.RaceUpdateStatus` | `Casino.RaceProto.RaceUpdateStatusRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.RaceProto.LeaderboardPosition.player_id (uint64, required)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardRequest.race_id (string, required)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse.race_id (string, optional)`
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.race_id (string, optional)`
- `Casino.RaceProto.RaceUpdateStatusRequest.available_rewards_bundle_id (string, repeated)`
- `Casino.RaceProto.ShortLeaderboard.Bundle.id (string, optional)`
- `Casino.RaceProto.ShortLeaderboard.race_id (string, required)`
- `Casino.RaceProto.ShortLeaderboard.segment_id (int64, optional)`
- `Casino.RaceProto.ShortLeaderboard.slot_id (string, optional)`

### Progression / state

- `Casino.RaceProto.GetLeaderboardsResponse.status (Casino.RaceProto.GetLeaderboardsResponse.Status, required)`
- `Casino.RaceProto.LeaderboardPosition.points (Casino.BigNumber, optional)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse.status (Casino.RaceProto.RaceGetDetailedLeaderboardResponse.Status, required)`
- `Casino.RaceProto.RaceUpdateStatusRequest.rank_change_notification (Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification, repeated)`
- `Casino.RaceProto.ShortLeaderboard.Bundle.status (Casino.RaceProto.ShortLeaderboard.Bundle.Status, optional)`
- `Casino.RaceProto.ShortLeaderboard.status (Casino.RaceProto.ShortLeaderboard.Status, optional)`

### Cost / input

- `Casino.RaceProto.ShortLeaderboard.Bundle.min_bet (Casino.Chips, optional)`
- `Casino.RaceProto.ShortLeaderboard.min_bet (Casino.Chips, optional)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.RaceProto.GetLeaderboardsRequest.get_place_rewards (bool, optional)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardRequest.get_place_rewards (bool, optional)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse.reward (Casino.RaceProto.PlaceReward, repeated)`
- `Casino.RaceProto.ShortLeaderboard.reward (Casino.RaceProto.PlaceReward, repeated)`

### Timing / reset / expiry

- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse.updated_leaderboard_time (uint64, optional)`
- `Casino.RaceProto.ShortLeaderboard.Bundle.expire_time (uint64, optional)`
- `Casino.RaceProto.ShortLeaderboard.end_time (uint64, optional)`

### Segment / eligibility / limit

- `Casino.RaceProto.ShortLeaderboard.limitation (Casino.RaceProto.ShortLeaderboard.Limitation, repeated)`

### Other structural fields

- `Casino.RaceProto.GetLeaderboardsRequest.scope (Casino.RaceProto.GetLeaderboardsRequest.Scope, optional)`
- `Casino.RaceProto.GetLeaderboardsResponse.error_code (int32, optional)`
- `Casino.RaceProto.GetLeaderboardsResponse.leaderboard (Casino.RaceProto.ShortLeaderboard, repeated)`
- `Casino.RaceProto.GetLeaderboardsResponse.metadata (string, optional)`
- `Casino.RaceProto.LeaderboardPosition.place (uint64, required)`
- `Casino.RaceProto.PlaceReward.item (Casino.Item, repeated)`
- `Casino.RaceProto.PlaceReward.place (uint64, required)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardRequest.range_end (uint64, optional)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardRequest.range_start (uint64, optional)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse.error_code (int32, optional)`
- `Casino.RaceProto.RaceGetDetailedLeaderboardResponse.leaderboard (Casino.RaceProto.LeaderboardPosition, repeated)`
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.name (string, optional)`
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.place (uint64, optional)`
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.race_type (string, optional)`
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.type (Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.Type, optional)`
- `Casino.RaceProto.RaceUpdateStatusRequest.bundle_claimed (string, repeated)`
- `Casino.RaceProto.RaceUpdateStatusRequest.finished_leaderboard (string, repeated)`
- `Casino.RaceProto.RaceUpdateStatusRequest.new_unseen_leaderboard (string, repeated)`
- `Casino.RaceProto.ShortLeaderboard.Bundle.display_priority (int32, optional)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value.value_big_int (Casino.BigNumber, optional)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value.value_bool (bool, optional)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value.value_double (double, optional)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value.value_int (int64, optional)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value.value_string (string, optional)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.Value.value_strings (string, repeated)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.type (string, required)`
- `Casino.RaceProto.ShortLeaderboard.Limitation.value (Casino.RaceProto.ShortLeaderboard.Limitation.Value, required)`
- `Casino.RaceProto.ShortLeaderboard.bundle (Casino.RaceProto.ShortLeaderboard.Bundle, optional)`
- `Casino.RaceProto.ShortLeaderboard.display_priority (int32, optional)`
- `Casino.RaceProto.ShortLeaderboard.leaderboard (Casino.RaceProto.LeaderboardPosition, repeated)`
- `Casino.RaceProto.ShortLeaderboard.name (string, optional)`
- `Casino.RaceProto.ShortLeaderboard.race_type (string, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: server status update -> leaderboard/detail fetch -> qualifying play changes score/rank -> rank-change notification -> place reward.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open race overview, reward tiers and both leaderboard/detail views with markers.
- Perform one qualifying action and refresh rank.
- Open final result/reward popup when naturally available.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
