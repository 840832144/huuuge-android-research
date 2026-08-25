# Content Tournaments

Content-item tournament state, leaderboards, ranks and tournament rewards.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 2**
- Live populated field paths: **0**

## Schema scope

- Proto files: `ContentTournament.proto`, `Services.proto`
- Services: `AppServer`
- Related message types: **6**

- `Casino.ContentTournamentProto` (ContentTournament.proto)
- `Casino.ContentTournamentProto.ContentItem` (ContentTournament.proto)
- `Casino.ContentTournamentProto.GetLeaderboardsRequest` (ContentTournament.proto)
- `Casino.ContentTournamentProto.GetLeaderboardsResponse` (ContentTournament.proto)
- `Casino.ContentTournamentProto.GetStateResponse` (ContentTournament.proto)
- `Casino.EmptyRequest` (Services.proto)

## RPC and flow structure

Schema flow: state fetch identifies active content/item and timing -> leaderboard fetch returns ranks/progress/rewards -> gameplay elsewhere changes score.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.ContentTournamentGetState` | `Casino.EmptyRequest` | `Casino.ContentTournamentProto.GetStateResponse` | 0 | 0 | schema-only |
| `AppServer.ContentTournamentGetLeaderboards` | `Casino.ContentTournamentProto.GetLeaderboardsRequest` | `Casino.ContentTournamentProto.GetLeaderboardsResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.ContentTournamentProto.ContentItem.player_id (uint64, required)`
- `Casino.ContentTournamentProto.GetLeaderboardsRequest.tournament_id (uint64, required)`
- `Casino.ContentTournamentProto.GetStateResponse.tournament_id (uint64, required)`

### Progression / state

- `Casino.ContentTournamentProto.GetLeaderboardsResponse.status (Casino.ContentTournamentProto.GetLeaderboardsResponse.Status, required)`
- `Casino.ContentTournamentProto.GetStateResponse.is_active (bool, required)`
- `Casino.ContentTournamentProto.GetStateResponse.status (Casino.ContentTournamentProto.GetStateResponse.Status, required)`

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Timing / reset / expiry

- `Casino.ContentTournamentProto.GetStateResponse.end_time (uint32, optional)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.ContentTournamentProto.ContentItem.metadata (string, required)`
- `Casino.ContentTournamentProto.ContentItem.place (uint64, required)`
- `Casino.ContentTournamentProto.ContentItem.value (uint64, required)`
- `Casino.ContentTournamentProto.GetLeaderboardsResponse.content_items (Casino.ContentTournamentProto.ContentItem, repeated)`
- `Casino.ContentTournamentProto.GetLeaderboardsResponse.error_code (int32, optional)`
- `Casino.ContentTournamentProto.GetStateResponse.error_code (int32, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: state fetch identifies active content/item and timing -> leaderboard fetch returns ranks/progress/rewards -> gameplay elsewhere changes score.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open every tournament screen, content item, rules/rewards and leaderboard with markers.
- Play one qualifying action, then refresh the leaderboard.
- Open completed/result state when available.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
