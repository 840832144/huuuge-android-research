# Conquest

Conquest event configuration, tile/arena/slot state, challenges, progress, leaderboards, missed info and summary rewards.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **35/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 6**
- Live populated field paths: **0**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **29**

- `Casino.AddDciEventRequest.ConquestEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef` (AppClient.proto)
- `Casino.ConquestArenaUpdateResponse` (AppServer.proto)
- `Casino.ConquestChallengeLeaderboard` (Common.proto)
- `Casino.ConquestChallengeLeaderboard.SlotItem` (Common.proto)
- `Casino.ConquestChallengeProgress` (Common.proto)
- `Casino.ConquestEventProgress` (Common.proto)
- `Casino.ConquestLeaderboard` (Common.proto)
- `Casino.ConquestLeaderboard.Item` (Common.proto)
- `Casino.ConquestReward` (Common.proto)
- `Casino.ConquestSlotUpdateResponse` (AppServer.proto)
- `Casino.ConquestSummaryDetailsRequest` (AppServer.proto)
- `Casino.ConquestSummaryDetailsResponse` (AppServer.proto)
- `Casino.ConquestSummaryDetailsResponse.SummaryDetailItem` (AppServer.proto)
- `Casino.ConquestSummaryRequest` (AppServer.proto)
- `Casino.ConquestSummaryResponse` (AppServer.proto)
- `Casino.ConquestSummaryResponse.SummaryItem` (AppServer.proto)
- `Casino.ConquestTileUpdateResponse` (AppServer.proto)
- `Casino.ConquestTournamentLeaderboard` (Common.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward` (AppServer.proto)
- `Casino.UpdateProgressRequest.ConquestProgress` (AppClient.proto)

## RPC and flow structure

Schema flow: DCI event definition and missed info -> tile/arena/slot update requests -> challenge/event progress -> summary/summary-details fetch -> reward and leaderboard state.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.UpdateConquestTile` | `Casino.EmptyRequest` | `Casino.ConquestTileUpdateResponse` | 0 | 0 | schema-only |
| `AppServer.UpdateConquestArena` | `Casino.EmptyRequest` | `Casino.ConquestArenaUpdateResponse` | 0 | 0 | schema-only |
| `AppServer.UpdateConquestSlot` | `Casino.EmptyRequest` | `Casino.ConquestSlotUpdateResponse` | 0 | 0 | schema-only |
| `AppServer.FetchConquestSummary` | `Casino.ConquestSummaryRequest` | `Casino.ConquestSummaryResponse` | 0 | 0 | schema-only |
| `AppServer.FetchConquestSummaryDetails` | `Casino.ConquestSummaryDetailsRequest` | `Casino.ConquestSummaryDetailsResponse` | 0 | 0 | schema-only |
| `AppClient.AddConquestMissedInfo` | `Casino.LoginResponse.MissedInfo.ConquestMissedInfo` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress.challenge_id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.conquest_cluster_id (int64, optional)`
- `Casino.AddDciEventRequest.ConquestEvent.distributed_event_id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.division_id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.instance_id (int64, required)`
- `Casino.ConquestArenaUpdateResponse.distributed_event_id (int64, optional)`
- `Casino.ConquestChallengeLeaderboard.SlotItem.challenge_id (int64, required)`
- `Casino.ConquestChallengeProgress.challenge_id (int64, required)`
- `Casino.ConquestSlotUpdateResponse.distributed_event_id (int64, optional)`
- `Casino.ConquestSummaryDetailsRequest.challenge_id (int64, required)`
- `Casino.ConquestSummaryDetailsResponse.distributed_event_id (int64, optional)`
- `Casino.ConquestSummaryResponse.SummaryItem.challenge_id (int64, required)`
- `Casino.ConquestSummaryResponse.distributed_event_id (int64, optional)`
- `Casino.ConquestTileUpdateResponse.distributed_event_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.challenge_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.conquest_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.challenge_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.conquest_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.conquest_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.distributed_event_id (int64, required)`
- `Casino.UpdateProgressRequest.ConquestProgress.distributed_event_id (int64, required)`

### Progression / state

- `Casino.AddDciEventRequest.ConquestEvent.player_progress (Casino.AddDciEventRequest.ConquestEvent.PlayerProgress, repeated)`
- `Casino.ConquestArenaUpdateResponse.conquest_event_progress (Casino.ConquestEventProgress, optional)`
- `Casino.ConquestArenaUpdateResponse.status (Casino.ConquestArenaUpdateResponse.Status, required)`
- `Casino.ConquestSlotUpdateResponse.conquest_event_progress (Casino.ConquestEventProgress, optional)`
- `Casino.ConquestSlotUpdateResponse.status (Casino.ConquestSlotUpdateResponse.Status, required)`
- `Casino.ConquestSummaryDetailsResponse.status (Casino.ConquestSummaryDetailsResponse.Status, required)`
- `Casino.ConquestSummaryResponse.conquest_challenge_progress (Casino.ConquestChallengeProgress, repeated)`
- `Casino.ConquestSummaryResponse.conquest_event_progress (Casino.ConquestEventProgress, optional)`
- `Casino.ConquestSummaryResponse.status (Casino.ConquestSummaryResponse.Status, required)`
- `Casino.ConquestTileUpdateResponse.conquest_event_progress (Casino.ConquestEventProgress, optional)`
- `Casino.ConquestTileUpdateResponse.status (Casino.ConquestTileUpdateResponse.Status, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.challenge_progress (Casino.ConquestChallengeProgress, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.event_progress (Casino.ConquestEventProgress, optional)`
- `Casino.UpdateProgressRequest.ConquestProgress.progress (Casino.ConquestChallengeProgress, required)`

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.chips_to_flag (int64, required)`

### Reward / output

- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.challenge_reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.tournament_reward (Casino.ConquestReward, repeated)`
- `Casino.ConquestReward.reward (Casino.Reward, repeated)`
- `Casino.ConquestTileUpdateResponse.tournament_reward (Casino.ConquestReward, repeated)`
- `Casino.ConquestTournamentLeaderboard.jackpot_reward (Casino.ConquestReward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.challenge_reward (Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.event_reward (Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward, optional)`

### Timing / reset / expiry

- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.end_time (int32, required)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.start_time (int32, required)`

### Segment / eligibility / limit

- `Casino.ConquestSummaryDetailsRequest.limit (uint32, optional)`
- `Casino.ConquestSummaryRequest.limit (uint32, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.is_eligible (bool, optional)`

### Other structural fields

- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress.player_challenge_flags (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.definition (Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.family_name (string, required)`
- `Casino.AddDciEventRequest.ConquestEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.ConquestEvent.challenge_definition (Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.chat_history (Casino.ClubsProto.ClubNotificationRequest, repeated)`
- `Casino.ConquestArenaUpdateResponse.challenge_leaderboard (Casino.ConquestChallengeLeaderboard, optional)`
- `Casino.ConquestArenaUpdateResponse.error_code (int32, optional)`
- `Casino.ConquestArenaUpdateResponse.tournament_leaderboard (Casino.ConquestTournamentLeaderboard, optional)`
- `Casino.ConquestChallengeLeaderboard.SlotItem.leaderboard (Casino.ConquestLeaderboard, required)`
- `Casino.ConquestChallengeLeaderboard.slot_item (Casino.ConquestChallengeLeaderboard.SlotItem, repeated)`
- `Casino.ConquestChallengeProgress.club_challenge_flags (int64, optional)`
- `Casino.ConquestChallengeProgress.club_challenge_place (int32, optional)`
- `Casino.ConquestChallengeProgress.player_challenge_flags (int64, optional)`
- `Casino.ConquestChallengeProgress.player_challenge_place (int32, optional)`
- `Casino.ConquestEventProgress.club_event_flags (int64, optional)`
- `Casino.ConquestEventProgress.club_event_place (int32, optional)`
- `Casino.ConquestEventProgress.player_event_flags (int64, optional)`
- `Casino.ConquestEventProgress.player_event_place (int32, optional)`
- `Casino.ConquestEventProgress.total_clubs_in_instance (int32, required)`
- `Casino.ConquestEventProgress.total_members_in_club (int32, required)`
- `Casino.ConquestLeaderboard.Item.club_info (Casino.ClubInfo, required)`
- `Casino.ConquestLeaderboard.Item.flags (uint64, required)`
- `Casino.ConquestLeaderboard.item (Casino.ConquestLeaderboard.Item, repeated)`
- `Casino.ConquestSlotUpdateResponse.challenge_leaderboard (Casino.ConquestChallengeLeaderboard, optional)`
- `Casino.ConquestSlotUpdateResponse.error_code (int32, optional)`
- `Casino.ConquestSummaryDetailsRequest.offset (uint32, optional)`
- `Casino.ConquestSummaryDetailsResponse.SummaryDetailItem.avatar (Casino.Avatar, required)`
- `Casino.ConquestSummaryDetailsResponse.SummaryDetailItem.club (Casino.ClubInfo, required)`
- `Casino.ConquestSummaryDetailsResponse.SummaryDetailItem.flags (uint64, required)`
- `Casino.ConquestSummaryDetailsResponse.detail_item (Casino.ConquestSummaryDetailsResponse.SummaryDetailItem, repeated)`
- `Casino.ConquestSummaryDetailsResponse.error_code (int32, optional)`
- `Casino.ConquestSummaryDetailsResponse.own_club (Casino.ClubInfo, optional)`
- `Casino.ConquestSummaryDetailsResponse.own_flags (uint64, optional)`
- `Casino.ConquestSummaryDetailsResponse.own_position (uint32, optional)`
- `Casino.ConquestSummaryRequest.offset (uint32, optional)`
- `Casino.ConquestSummaryResponse.SummaryItem.club_info (Casino.ClubInfo, optional)`
- `Casino.ConquestSummaryResponse.SummaryItem.type (Casino.ConquestSummaryResponse.SummaryItem.Type, required)`
- `Casino.ConquestSummaryResponse.error_code (int32, optional)`
- `Casino.ConquestSummaryResponse.item (Casino.ConquestSummaryResponse.SummaryItem, repeated)`
- … 8 more rows in `fields.csv`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: DCI event definition and missed info -> tile/arena/slot update requests -> challenge/event progress -> summary/summary-details fetch -> reward and leaderboard state.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/sound_conquest.zpk`
- `sound_conquest.zpk` confirms packaged Conquest client content despite no dedicated live endpoint in this session.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open the Conquest map, arena, slot/challenge and summary/leaderboard screens with markers.
- Start or progress one challenge through normal play, then revisit its tile.
- Open any completed-event or missed-info popup to capture reward reconciliation.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
