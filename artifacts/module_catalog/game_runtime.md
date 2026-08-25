# Game Runtime / Host / Room State

Generic game host/server connections, player joins/leaves, room state, profiles, challenges, config, statistics and metrics shared across games.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **35/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 21**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Common.proto`, `CommonGameClient.proto`, `GameHost.proto`, `GameServer.proto`, `Services.proto`
- Services: `GameHost`, `GameServer`
- Related message types: **66**

- `Casino.AddChallengeRequest` (GameServer.proto)
- `Casino.AddChallengeResponse` (GameServer.proto)
- `Casino.BetMetadata` (GameServer.proto)
- `Casino.BetsList` (GameServer.proto)
- `Casino.CancelChallengeRequest` (GameServer.proto)
- `Casino.CancelChallengeResponse` (GameServer.proto)
- `Casino.CloseGameRequest` (GameServer.proto)
- `Casino.CloseGameResponse` (GameServer.proto)
- `Casino.DisconnectPlayerRequest` (GameHost.proto)
- `Casino.DuplicateGameRequest` (GameServer.proto)
- `Casino.DuplicateGameResponse` (GameServer.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.Event` (GameHost.proto)
- `Casino.Event.Param` (GameHost.proto)
- `Casino.ExecuteCommandRequest` (Common.proto)
- `Casino.ExecuteCommandResponse` (Common.proto)
- `Casino.GameData` (GameHost.proto)
- `Casino.GameData.JackpotDefData` (GameHost.proto)
- `Casino.GameData.MachineDefData` (GameHost.proto)
- `Casino.GameHostConnectRequest` (GameHost.proto)
- `Casino.GameHostConnectResponse` (GameHost.proto)
- `Casino.GameHostDisconnectRequest` (GameHost.proto)
- `Casino.GameHostDisconnectResponse` (GameHost.proto)
- `Casino.GameServerConnectRequest` (GameHost.proto)
- `Casino.GameServerConnectResponse` (GameHost.proto)
- `Casino.GiveFreeGiftRoundRequest` (GameHost.proto)
- `Casino.JackpotGetRequest` (GameHost.proto)
- `Casino.JackpotGetResponse` (GameHost.proto)
- `Casino.JackpotHitRequest` (GameHost.proto)
- `Casino.JackpotHitRequest.Jackpot` (GameHost.proto)
- `Casino.JackpotHitResponse` (GameHost.proto)
- `Casino.JackpotHitResponse.Jackpot` (GameHost.proto)
- `Casino.JackpotIncrRequest` (GameHost.proto)
- `Casino.JackpotIncrRequest.Jackpot` (GameHost.proto)
- `Casino.JackpotInitRequest` (GameHost.proto)
- `Casino.JackpotInitRequest.Jackpot` (GameHost.proto)
- `Casino.LeaguePointBonus` (CommonGameClient.proto)
- `Casino.LogEventParam` (GameHost.proto)
- `Casino.LogEventRequest` (GameHost.proto)
- `Casino.PlayerGetChipsRequest` (GameServer.proto)
- `Casino.PlayerGetChipsResponse` (GameServer.proto)
- `Casino.PlayerJoinRequest` (GameServer.proto)
- `Casino.PlayerJoinResponse` (GameServer.proto)
- `Casino.PlayerLeftRequest` (GameServer.proto)
- `Casino.PlayerLeftResponse` (GameServer.proto)
- `Casino.PlayerUpdateBetsRequest` (GameServer.proto)
- `Casino.PlayerUpdateProfileRequest` (GameServer.proto)
- `Casino.PlayerUpdateProfileRequest.UpdateClub` (GameServer.proto)
- `Casino.ReserveSeatRequest` (GameServer.proto)
- `Casino.ReserveSeatResponse` (GameServer.proto)
- `Casino.ResetUserInactivityRequest` (Common.proto)
- `Casino.StartLeaguePointsRequest` (GameServer.proto)
- `Casino.UpdateChipsRequest` (GameServer.proto)
- `Casino.UpdateChipsResponse` (GameServer.proto)
- `Casino.UpdateConfigRequest` (GameServer.proto)
- `Casino.UpdateConfigResponse` (GameServer.proto)
- `Casino.UpdateLeaderboardRequest` (GameHost.proto)
- `Casino.UpdateMetricsRequest` (GameHost.proto)
- `Casino.UpdateMetricsRequest.GameMetrics` (GameHost.proto)
- `Casino.UpdatePlayerGameEventRequest` (GameServer.proto)
- `Casino.UpdatePlayerGameEventResponse` (GameServer.proto)
- `Casino.UpdateRoomInfoRequest` (GameHost.proto)
- `Casino.UpdateStatisticRequest` (GameHost.proto)
- `Casino.UpdateStatisticRequest.Entry` (GameHost.proto)
- `Casino.UpdateUserRequest` (GameHost.proto)
- `Casino.UpdateUserRequest.ChallengeProgress` (GameHost.proto)

## RPC and flow structure

Schema flow: app joins a game -> game host/server connect and player join -> room/config/profile/challenge/statistic updates -> game-specific services run -> player leaves/disconnects and metrics flush.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `GameHost.Connect` | `Casino.GameServerConnectRequest` | `Casino.GameServerConnectResponse` | 0 | 0 | schema-only |
| `GameHost.GameConnect` | `Casino.GameHostConnectRequest` | `Casino.GameHostConnectResponse` | 0 | 0 | schema-only |
| `GameHost.UpdateUser` | `Casino.UpdateUserRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.UpdateLeaderboard` | `Casino.UpdateLeaderboardRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.UpdateStatistic` | `Casino.UpdateStatisticRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.LogEvent` | `Casino.LogEventRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.Disconnect` | `Casino.GameHostDisconnectRequest` | `Casino.GameHostDisconnectResponse` | 0 | 0 | schema-only |
| `GameHost.DisconnectPlayer` | `Casino.DisconnectPlayerRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.UpdateMetrics` | `Casino.UpdateMetricsRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.UpdateRoomInfo` | `Casino.UpdateRoomInfoRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameServer.PlayerJoin` | `Casino.PlayerJoinRequest` | `Casino.PlayerJoinResponse` | 0 | 0 | schema-only |
| `GameServer.PlayerLeft` | `Casino.PlayerLeftRequest` | `Casino.PlayerLeftResponse` | 0 | 0 | schema-only |
| `GameServer.DuplicateGame` | `Casino.DuplicateGameRequest` | `Casino.DuplicateGameResponse` | 0 | 0 | schema-only |
| `GameServer.CloseGame` | `Casino.CloseGameRequest` | `Casino.CloseGameResponse` | 0 | 0 | schema-only |
| `GameServer.ReserveSeat` | `Casino.ReserveSeatRequest` | `Casino.ReserveSeatResponse` | 0 | 0 | schema-only |
| `GameServer.ResetUserInactivity` | `Casino.ResetUserInactivityRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameServer.ExecuteCommand` | `Casino.ExecuteCommandRequest` | `Casino.ExecuteCommandResponse` | 0 | 0 | schema-only |
| `GameServer.AddChallenge` | `Casino.AddChallengeRequest` | `Casino.AddChallengeResponse` | 0 | 0 | schema-only |
| `GameServer.RemoveChallenge` | `Casino.CancelChallengeRequest` | `Casino.CancelChallengeResponse` | 0 | 0 | schema-only |
| `GameServer.UpdateConfig` | `Casino.UpdateConfigRequest` | `Casino.UpdateConfigResponse` | 0 | 0 | schema-only |
| `GameServer.UpdatePlayerGameEvent` | `Casino.UpdatePlayerGameEventRequest` | `Casino.UpdatePlayerGameEventResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddChallengeRequest.challenge_id (int32, required)`
- `Casino.CancelChallengeRequest.challenge_id (int32, required)`
- `Casino.DisconnectPlayerRequest.disconnect_request_id (int32, required)`
- `Casino.DisconnectPlayerRequest.room_id (uint64, optional)`
- `Casino.Event.event (string, required)`
- `Casino.GameData.JackpotDefData.jackpot_id (uint32, repeated)`
- `Casino.GameData.MachineDefData.math_id (string, required)`
- `Casino.GameData.MachineDefData.persistent_slot_id (string, optional)`
- `Casino.GameServerConnectRequest.server_id (int64, required)`
- `Casino.JackpotGetRequest.jackpot_id (uint32, repeated)`
- `Casino.JackpotHitRequest.Jackpot.id (uint32, required)`
- `Casino.JackpotIncrRequest.Jackpot.id (uint32, required)`
- `Casino.JackpotInitRequest.Jackpot.id (uint32, required)`
- `Casino.PlayerGetChipsRequest.user_id (int64, required)`
- `Casino.PlayerJoinRequest.math_id (string, optional)`
- `Casino.PlayerJoinRequest.other_user_id (int64, optional)`
- `Casino.PlayerJoinRequest.room_id (uint64, optional)`
- `Casino.PlayerJoinRequest.user_id (int64, required)`
- `Casino.PlayerJoinResponse.on_join_stat_key (int32, optional)`
- `Casino.PlayerJoinResponse.room_id (uint64, optional)`
- `Casino.PlayerJoinResponse.test_group_id (uint32, optional)`
- `Casino.ReserveSeatRequest.user_id (int64, required)`
- `Casino.UpdatePlayerGameEventRequest.event (Casino.GameEvent, repeated)`
- `Casino.UpdateStatisticRequest.Entry.key (int32, required)`
- `Casino.UpdateUserRequest.ChallengeProgress.challenge_id (int32, required)`

### Progression / state

- `Casino.AddChallengeResponse.status (Casino.AddChallengeResponse.Status, required)`
- `Casino.CancelChallengeResponse.status (Casino.CancelChallengeResponse.Status, required)`
- `Casino.CloseGameResponse.status (Casino.CloseGameResponse.Status, required)`
- `Casino.DuplicateGameRequest.level (int64, optional)`
- `Casino.DuplicateGameResponse.status (Casino.DuplicateGameResponse.Status, required)`
- `Casino.ExecuteCommandResponse.status (Casino.ExecuteCommandResponse.Status, required)`
- `Casino.GameHostConnectResponse.status (Casino.GameHostConnectResponse.Status, required)`
- `Casino.GameHostDisconnectResponse.status (Casino.GameHostDisconnectResponse.Status, required)`
- `Casino.GameServerConnectResponse.status (Casino.GameServerConnectResponse.Status, required)`
- `Casino.PlayerGetChipsResponse.status (Casino.PlayerGetChipsResponse.Status, required)`
- `Casino.PlayerJoinResponse.status (Casino.PlayerJoinResponse.Status, required)`
- `Casino.ReserveSeatResponse.status (Casino.ReserveSeatResponse.Status, required)`
- `Casino.StartLeaguePointsRequest.level1 (uint32, optional)`
- `Casino.StartLeaguePointsRequest.level2 (uint32, optional)`
- `Casino.StartLeaguePointsRequest.level3 (uint32, optional)`
- `Casino.StartLeaguePointsRequest.level_max (uint32, optional)`
- `Casino.UpdateConfigResponse.status (Casino.UpdateConfigResponse.Status, required)`
- `Casino.UpdateMetricsRequest.GameMetrics.user_count (uint64, optional)`
- `Casino.UpdateMetricsRequest.user_count (uint64, required)`
- `Casino.UpdatePlayerGameEventResponse.status (Casino.UpdatePlayerGameEventResponse.Status, required)`
- `Casino.UpdateUserRequest.challenge_progress (Casino.UpdateUserRequest.ChallengeProgress, optional)`

### Cost / input

- `Casino.BetMetadata.target_bet (int64, required)`
- `Casino.BetsList.bets (uint64, repeated)`
- `Casino.DuplicateGameRequest.bets (int64, repeated)`
- `Casino.JackpotHitRequest.Jackpot.bet (uint64, required)`
- `Casino.JackpotHitRequest.Jackpot.max_bet (uint64, required)`
- `Casino.JackpotInitRequest.Jackpot.max_bet (uint64, required)`
- `Casino.PlayerJoinRequest.sorted_bets (Casino.BetsList, optional)`
- `Casino.PlayerJoinRequest.tutorial_initial_bet (int64, optional)`
- `Casino.PlayerUpdateBetsRequest.sorted_bets (Casino.BetsList, required)`
- `Casino.UpdateUserRequest.bet (int64, optional)`
- `Casino.UpdateUserRequest.real_bet (int64, optional)`

### Currency / balance

- `Casino.PlayerGetChipsResponse.chips (Casino.Chips, optional)`
- `Casino.PlayerGetChipsResponse.legacy_chips (int64, optional)`
- `Casino.UpdateChipsRequest.chips_delta (Casino.Chips, optional)`
- `Casino.UpdateChipsRequest.legacy_chips_delta (int64, required)`
- `Casino.UpdateUserRequest.ChallengeProgress.chips (int64, required)`

### Reward / output

- `Casino.GiveFreeGiftRoundRequest.win_multiplier (double, optional)`
- `Casino.JackpotHitResponse.Jackpot.legacy_win (uint64, required)`
- `Casino.JackpotHitResponse.Jackpot.win (Casino.Chips, optional)`
- `Casino.LeaguePointBonus.bonus_percent (uint32, optional)`
- `Casino.UpdateUserRequest.legacy_payout (int64, optional)`
- `Casino.UpdateUserRequest.legacy_win (int64, optional)`
- `Casino.UpdateUserRequest.legacy_win_for_fame (int64, optional)`
- `Casino.UpdateUserRequest.legacy_win_for_lp (int64, optional)`
- `Casino.UpdateUserRequest.payout (Casino.Chips, optional)`
- `Casino.UpdateUserRequest.win (Casino.Chips, optional)`
- `Casino.UpdateUserRequest.win_for_fame (Casino.Chips, optional)`
- `Casino.UpdateUserRequest.win_for_lp (Casino.Chips, optional)`

### Timing / reset / expiry

- `Casino.PlayerJoinRequest.time_ms (int64, optional)`
- `Casino.ReserveSeatRequest.duration (int32, required)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.AddChallengeRequest.parameters (Casino.KeyValueMap, optional)`
- `Casino.AddChallengeRequest.slot_family (string, required)`
- `Casino.AddChallengeRequest.type (Casino.HuuugePassChallenge, required)`
- `Casino.BetMetadata.user_events (string, repeated)`
- `Casino.BetsList.metadata (Casino.BetMetadata, repeated)`
- `Casino.CloseGameRequest.game_name (string, required)`
- `Casino.DisconnectPlayerRequest.force_disconnect (bool, optional)`
- `Casino.DuplicateGameRequest.dst_game_name (string, required)`
- `Casino.DuplicateGameRequest.src_game_name (string, required)`
- `Casino.Event.Param.int_value (int64, optional)`
- `Casino.Event.Param.string_value (string, optional)`
- `Casino.Event.params (Casino.Event.Param, repeated)`
- `Casino.ExecuteCommandRequest.command (string, required)`
- `Casino.ExecuteCommandResponse.error_code (int32, optional)`
- `Casino.ExecuteCommandResponse.message (string, optional)`
- `Casino.GameData.MachineDefData.game_conf_path (string, optional)`
- `Casino.GameData.MachineDefData.jackpot_def_data (Casino.GameData.JackpotDefData, optional)`
- `Casino.GameData.MachineDefData.math_path (string, optional)`
- `Casino.GameData.machine_def_data (Casino.GameData.MachineDefData, repeated)`
- `Casino.GameHostConnectRequest.client_service_index (int32, repeated)`
- `Casino.GameHostConnectRequest.config_version (uint64, required)`
- `Casino.GameHostConnectRequest.game_data (Casino.GameData, optional)`
- `Casino.GameHostConnectRequest.game_def (Casino.GameDef, required)`
- `Casino.GameHostConnectRequest.required_server_version (int32, optional)`
- `Casino.GameHostConnectRequest.server_service_index (int32, repeated)`
- `Casino.GameHostConnectResponse.error_code (int32, optional)`
- `Casino.GameHostDisconnectRequest.game_name (string, required)`
- `Casino.GameHostDisconnectResponse.error_code (int32, optional)`
- `Casino.GameServerConnectRequest.metrics (Casino.UpdateMetricsRequest, required)`
- `Casino.GameServerConnectRequest.protocol_version (int32, required)`
- `Casino.GameServerConnectResponse.error_code (int32, optional)`
- `Casino.GiveFreeGiftRoundRequest.receivers (int64, repeated)`
- `Casino.JackpotGetResponse.legacy_value (uint64, repeated)`
- `Casino.JackpotGetResponse.value (Casino.Chips, repeated)`
- `Casino.JackpotHitRequest.Jackpot.legacy_min_value (uint64, required)`
- `Casino.JackpotHitRequest.Jackpot.min_value (Casino.Chips, optional)`
- `Casino.JackpotHitRequest.jackpot (Casino.JackpotHitRequest.Jackpot, repeated)`
- `Casino.JackpotHitResponse.Jackpot.club_share (double, optional)`
- `Casino.JackpotHitResponse.Jackpot.legacy_value (uint64, required)`
- `Casino.JackpotHitResponse.Jackpot.value (Casino.Chips, optional)`
- … 55 more rows in `fields.csv`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: app joins a game -> game host/server connect and player join -> room/config/profile/challenge/statistic updates -> game-specific services run -> player leaves/disconnects and metrics flush.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_ingame_cards_1_etc2.zpk`
- ZPK asset: `assets/atlas_ingame_cards_2_etc2.zpk`
- ZPK asset: `assets/atlas_ingame_common_1_etc2.zpk`
- ZPK asset: `assets/atlas_ingame_common_2_etc2.zpk`
- ZPK asset: `assets/data-games.zpk`
- ZPK asset: `assets/sound_ingame.zpk`
- ZPK asset: `assets/sound_ingame_vo_male.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Use markers for lobby entry, game join, room loaded, game leave and reconnect.
- Visit one non-slot game to distinguish generic room traffic from game-specific RPCs.
- Capture a natural reconnect or room transition if it occurs.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
