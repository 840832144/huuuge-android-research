# Elites / Play Together

Elites eligibility, active/calculating states, missions/milestones, leaderboard and play-together information.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 8**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Elites.proto`, `Services.proto`
- Services: `ElitesClient`, `ElitesServer`
- Related message types: **25**

- `Casino.ElitesBundle` (Elites.proto)
- `Casino.ElitesBundle.Metadata` (Elites.proto)
- `Casino.ElitesEventData` (Elites.proto)
- `Casino.ElitesGetDataRequest` (Elites.proto)
- `Casino.ElitesGetDataResponse` (Elites.proto)
- `Casino.ElitesGetDataResponse.Action` (Elites.proto)
- `Casino.ElitesGetDataResponse.LeagueItems` (Elites.proto)
- `Casino.ElitesGetDataResponse.Limitation` (Elites.proto)
- `Casino.ElitesGetDataResponse.Limitation.Value` (Elites.proto)
- `Casino.ElitesGetDataResponse.Mission` (Elites.proto)
- `Casino.ElitesGetDataResponse.Multiplier` (Elites.proto)
- `Casino.ElitesGetDataResponse.PointsPerAmount` (Elites.proto)
- `Casino.ElitesGetLeaderboardRequest` (Elites.proto)
- `Casino.ElitesGetLeaderboardResponse` (Elites.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.LeaderboardEntry` (Elites.proto)
- `Casino.LeaderboardEntry.Player` (Elites.proto)
- `Casino.LeaderboardRank` (Elites.proto)
- `Casino.NotifyElitesActiveRequest` (Elites.proto)
- `Casino.NotifyElitesActiveRequest.MilestonesProgress` (Elites.proto)
- `Casino.NotifyElitesMilestoneCompletedRequest` (Elites.proto)
- `Casino.NotifyElitesTooLowLevelRequest` (Elites.proto)
- `Casino.PlayTogetherInfoRequest` (Elites.proto)
- `Casino.RankOutcome` (Elites.proto)

## RPC and flow structure

Schema flow: eligibility/active notification -> data fetch returns event/missions -> progress/milestone completion -> calculating/final leaderboard -> play-together info.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `ElitesServer.ElitesGetData` | `Casino.ElitesGetDataRequest` | `Casino.ElitesGetDataResponse` | 0 | 0 | schema-only |
| `ElitesServer.ElitesGetLeaderboard` | `Casino.ElitesGetLeaderboardRequest` | `Casino.ElitesGetLeaderboardResponse` | 0 | 0 | schema-only |
| `ElitesClient.NotifyElitesTooLowLevel` | `Casino.NotifyElitesTooLowLevelRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ElitesClient.NotifyElitesActive` | `Casino.NotifyElitesActiveRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ElitesClient.NotifyElitesSoon` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ElitesClient.NotifyElitesMilestoneCompleted` | `Casino.NotifyElitesMilestoneCompletedRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ElitesClient.NotifyElitesCalculating` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ElitesClient.PlayTogetherInfo` | `Casino.PlayTogetherInfoRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.ElitesBundle.Metadata.key (string, optional)`
- `Casino.ElitesBundle.bundle_id (string, optional)`
- `Casino.ElitesEventData.event_id (string, optional)`
- `Casino.ElitesEventData.league_id (int32, optional)`
- `Casino.ElitesEventData.season_id (int32, optional)`
- `Casino.ElitesGetDataRequest.season_id (int32, optional)`
- `Casino.ElitesGetDataResponse.LeagueItems.league_id (int32, optional)`
- `Casino.ElitesGetDataResponse.leaderboard_id (string, optional)`
- `Casino.ElitesGetLeaderboardRequest.leaderboard_id (string, optional)`
- `Casino.LeaderboardEntry.Player.avatar_frame_id (int32, optional)`
- `Casino.LeaderboardEntry.Player.avatar_id (int64, optional)`
- `Casino.LeaderboardEntry.Player.id (int64, optional)`
- `Casino.LeaderboardEntry.player (Casino.LeaderboardEntry.Player, optional)`

### Progression / state

- `Casino.ElitesGetDataResponse.Mission.points (int64, optional)`
- `Casino.ElitesGetDataResponse.PointsPerAmount.points (int32, optional)`
- `Casino.ElitesGetDataResponse.player_rank (Casino.LeaderboardRank, optional)`
- `Casino.ElitesGetDataResponse.points_total (int64, optional)`
- `Casino.ElitesGetDataResponse.status (Casino.ElitesGetDataResponse.Status, optional)`
- `Casino.ElitesGetDataResponse.weekly_benefits_active (bool, optional)`
- `Casino.ElitesGetLeaderboardResponse.player_rank (Casino.LeaderboardRank, optional)`
- `Casino.ElitesGetLeaderboardResponse.points_total (int64, optional)`
- `Casino.ElitesGetLeaderboardResponse.status (Casino.ElitesGetLeaderboardResponse.Status, optional)`
- `Casino.LeaderboardEntry.points (int64, optional)`
- `Casino.NotifyElitesActiveRequest.MilestonesProgress.completed_milestones (int32, optional)`
- `Casino.NotifyElitesActiveRequest.leaderboard_rank (Casino.LeaderboardRank, optional)`
- `Casino.NotifyElitesActiveRequest.milestones_progress (Casino.NotifyElitesActiveRequest.MilestonesProgress, optional)`
- `Casino.NotifyElitesMilestoneCompletedRequest.completed_milestones (int32, optional)`
- `Casino.RankOutcome.levels (int32, optional)`

### Cost / input

- `Casino.ElitesGetDataResponse.Action.points_per_amount (Casino.ElitesGetDataResponse.PointsPerAmount, optional)`
- `Casino.ElitesGetDataResponse.Mission.milestone_requirements (int64, repeated)`
- `Casino.ElitesGetDataResponse.PointsPerAmount.amount (int32, optional)`
- `Casino.ElitesGetLeaderboardResponse.top_league_points_threshold (int64, optional)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.ElitesGetDataResponse.season_rewards (Casino.ElitesGetDataResponse.LeagueItems, repeated)`
- `Casino.NotifyElitesActiveRequest.bonuses (Casino.Item, repeated)`

### Timing / reset / expiry

- `Casino.ElitesEventData.season_expire_timestamp_in_sec (uint64, optional)`
- `Casino.ElitesGetDataResponse.Mission.mystery_end_timestamp_in_sec (uint64, optional)`
- `Casino.ElitesGetDataResponse.Mission.mystery_start_timestamp_in_sec (uint64, optional)`
- `Casino.ElitesGetDataResponse.Multiplier.end_timestamp_in_sec (uint64, optional)`
- `Casino.ElitesGetDataResponse.Multiplier.start_timestamp_in_sec (uint64, optional)`
- `Casino.ElitesGetDataResponse.week_expire_timestamp_in_sec (uint64, optional)`

### Segment / eligibility / limit

- `Casino.ElitesGetDataResponse.Action.limitation (Casino.ElitesGetDataResponse.Limitation, repeated)`
- `Casino.ElitesGetDataResponse.Multiplier.limited_to_slot (string, repeated)`
- `Casino.NotifyElitesTooLowLevelRequest.unlock_level (int32, optional)`

### Other structural fields

- `Casino.ElitesBundle.Metadata.value (string, optional)`
- `Casino.ElitesBundle.items (Casino.Item, repeated)`
- `Casino.ElitesBundle.metadata (Casino.ElitesBundle.Metadata, repeated)`
- `Casino.ElitesEventData.art_config (Casino.Art, optional)`
- `Casino.ElitesEventData.week (int32, optional)`
- `Casino.ElitesGetDataRequest.week (int32, optional)`
- `Casino.ElitesGetDataResponse.Action.name (string, optional)`
- `Casino.ElitesGetDataResponse.LeagueItems.items (Casino.Item, repeated)`
- `Casino.ElitesGetDataResponse.Limitation.Value.value_big_int (Casino.BigNumber, optional)`
- `Casino.ElitesGetDataResponse.Limitation.Value.value_bool (bool, optional)`
- `Casino.ElitesGetDataResponse.Limitation.Value.value_double (double, optional)`
- `Casino.ElitesGetDataResponse.Limitation.Value.value_int (int64, optional)`
- `Casino.ElitesGetDataResponse.Limitation.Value.value_string (string, optional)`
- `Casino.ElitesGetDataResponse.Limitation.Value.value_strings (string, repeated)`
- `Casino.ElitesGetDataResponse.Limitation.type (string, optional)`
- `Casino.ElitesGetDataResponse.Limitation.value (Casino.ElitesGetDataResponse.Limitation.Value, optional)`
- `Casino.ElitesGetDataResponse.Mission.actions (Casino.ElitesGetDataResponse.Action, repeated)`
- `Casino.ElitesGetDataResponse.Mission.multipliers (Casino.ElitesGetDataResponse.Multiplier, repeated)`
- `Casino.ElitesGetDataResponse.Mission.order (int32, optional)`
- `Casino.ElitesGetDataResponse.Multiplier.value (double, optional)`
- `Casino.ElitesGetDataResponse.error_code (int32, optional)`
- `Casino.ElitesGetDataResponse.missions (Casino.ElitesGetDataResponse.Mission, repeated)`
- `Casino.ElitesGetDataResponse.weekly_benefits (Casino.ElitesGetDataResponse.LeagueItems, repeated)`
- `Casino.ElitesGetLeaderboardResponse.error_code (int32, optional)`
- `Casino.ElitesGetLeaderboardResponse.leaderboard_entries (Casino.LeaderboardEntry, repeated)`
- `Casino.LeaderboardEntry.Player.name (string, optional)`
- `Casino.LeaderboardEntry.outcome (Casino.RankOutcome, optional)`
- `Casino.LeaderboardEntry.position (int32, optional)`
- `Casino.LeaderboardRank.outcome (Casino.RankOutcome, optional)`
- `Casino.LeaderboardRank.position (int32, optional)`
- `Casino.NotifyElitesActiveRequest.MilestonesProgress.pending_milestones_bundles (Casino.ElitesBundle, repeated)`
- `Casino.NotifyElitesActiveRequest.MilestonesProgress.total_milestones (int32, optional)`
- `Casino.NotifyElitesActiveRequest.event_data (Casino.ElitesEventData, optional)`
- `Casino.NotifyElitesActiveRequest.pending_weekly_bundle (Casino.ElitesBundle, optional)`
- `Casino.NotifyElitesMilestoneCompletedRequest.pending_milestone_bundle (Casino.ElitesBundle, optional)`
- `Casino.NotifyElitesMilestoneCompletedRequest.total_milestones (int32, optional)`
- `Casino.NotifyElitesTooLowLevelRequest.event_data (Casino.ElitesEventData, optional)`
- `Casino.PlayTogetherInfoRequest.club_members (uint32, optional)`
- `Casino.RankOutcome.type (Casino.RankOutcome.Type, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: eligibility/active notification -> data fetch returns event/missions -> progress/milestone completion -> calculating/final leaderboard -> play-together info.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Elites event, missions/milestones, leaderboard and Play Together screens with markers.
- Perform one qualifying action and refresh event data.
- Capture calculating/final state if the event naturally transitions.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
