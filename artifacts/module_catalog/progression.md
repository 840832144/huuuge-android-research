# Fame / Level / General Progression

Player fame, level/rank, general progress payloads, game-event progress and bet/progression configuration outside dedicated event modules.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **85/100 — substantial live structure**
- Primary live samples: **761** from `20260901_160002`
- Cross-cutting live samples: **814**
- Live endpoints / schema endpoints: **3 / 8**
- Live populated field paths: **163**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `BattlePass.proto`, `Clubs.proto`, `Common.proto`, `CommonGameClient.proto`, `Elites.proto`, `GameHost.proto`, `GameServer.proto`, `PersonalAwards.proto`, `Race.proto`, `Services.proto`, `Vault.proto`
- Services: `AppClient`, `GameServer`
- Related message types: **54**

- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent.LotteryMachine` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState` (AppClient.proto)
- `Casino.AssignmentProgress` (Common.proto)
- `Casino.BattlePassMissionProgressUpdateRequest` (BattlePass.proto)
- `Casino.CharmsProgressData` (AppClient.proto)
- `Casino.CharmsProgressData.CharmsTradingInfo` (AppClient.proto)
- `Casino.CharmsTutorialProgressRequest` (AppServer.proto)
- `Casino.CharmsTutorialProgressResponse` (AppServer.proto)
- `Casino.ClubSetProgressData` (AppClient.proto)
- `Casino.ClubSetTutorialProgressRequest` (AppServer.proto)
- `Casino.ClubSetTutorialProgressResponse` (AppServer.proto)
- `Casino.ClubsProto.ClubListEntry.RankDelta` (Clubs.proto)
- `Casino.ConquestChallengeProgress` (Common.proto)
- `Casino.ConquestEventProgress` (Common.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.GameEvent` (Common.proto)
- `Casino.GetAssignmentProgressRequest` (AppServer.proto)
- `Casino.GetAssignmentProgressResponse` (AppServer.proto)
- `Casino.LeaderboardRank` (Elites.proto)
- `Casino.LeaguePointBonus` (CommonGameClient.proto)
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo` (AppServer.proto)
- `Casino.MinigameEventTrail` (Common.proto)
- `Casino.MinigameEventTrail.Step` (Common.proto)
- `Casino.NotifyElitesActiveRequest.MilestonesProgress` (Elites.proto)
- `Casino.PersonalAwardsProto.GetProgressRequest` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.GetProgressResponse` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.UpdateProgressRequest` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.UpdateProgressResponse` (PersonalAwards.proto)
- `Casino.PlayerProfile.FameInfo` (AppServer.proto)
- `Casino.PlayerProfile.Rank` (AppServer.proto)
- `Casino.PlayerUpdateBetsRequest` (GameServer.proto)
- `Casino.PlayerUpdateProfileRequest` (GameServer.proto)
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification` (Race.proto)
- `Casino.RankOutcome` (Elites.proto)
- `Casino.Reward.LeaguePointsBonus` (Common.proto)
- `Casino.StartLeaguePointsRequest` (GameServer.proto)
- `Casino.TowerRunProgress` (Common.proto)
- `Casino.UpdateAssignmentProgressRequest` (AppClient.proto)
- `Casino.UpdateBetsRequest` (AppClient.proto)
- `Casino.UpdateCharmsProgressRequest` (AppClient.proto)
- `Casino.UpdateClubSetProgressRequest` (AppClient.proto)
- `Casino.UpdateFameRequest` (AppClient.proto)
- `Casino.UpdateGameEventRequest` (AppClient.proto)
- `Casino.UpdatePlayerGameEventRequest` (GameServer.proto)
- `Casino.UpdatePlayerGameEventResponse` (GameServer.proto)
- `Casino.UpdateProgressRequest` (AppClient.proto)
- `Casino.UpdateProgressRequest.ConquestProgress` (AppClient.proto)
- `Casino.UpdateProgressRequest.MiniGameEventProgress` (AppClient.proto)
- `Casino.UpdateProgressRequest.TowerKeyProgress` (AppClient.proto)
- `Casino.UpdateUserRequest.ChallengeProgress` (GameHost.proto)
- `Casino.VaultProgressUpdateRequest` (Vault.proto)

## RPC and flow structure

Observed/schema flow: login/profile establishes current rank/fame -> server progress/fame updates follow gameplay/rewards -> client acknowledges -> level/rank-dependent unlocks and event progress alter other modules.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppClient.UpdateProgress` | `Casino.UpdateProgressRequest` | `Casino.EmptyResponse` | 651 | 0 | observed-live |
| `AppClient.UpdateFame` | `Casino.UpdateFameRequest` | `Casino.EmptyResponse` | 109 | 0 | observed-live |
| `AppClient.UpdateGameEvent` | `Casino.UpdateGameEventRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateBets` | `Casino.UpdateBetsRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `GameServer.PlayerUpdateProfile` | `Casino.PlayerUpdateProfileRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameServer.PlayerUpdateBets` | `Casino.PlayerUpdateBetsRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameServer.StartLeaguePoints` | `Casino.StartLeaguePointsRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameServer.EndLeaguePoints` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress.challenge_id (int64, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.game_id (int64, required)`
- `Casino.AssignmentProgress.event_id (int64, required)`
- `Casino.BattlePassMissionProgressUpdateRequest.mission (Casino.BattlePassMission, required)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trading_group_id (int64, optional)`
- `Casino.ClubSetTutorialProgressRequest.theme_id (int32, required)`
- `Casino.ConquestChallengeProgress.challenge_id (int64, required)`
- `Casino.GameEvent.id (int32, optional)`
- `Casino.GetAssignmentProgressRequest.event_id (int64, repeated)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.game_id (int64, required)`
- `Casino.PersonalAwardsProto.GetProgressRequest.slot_id (string, required)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.slot_id (string, required)`
- `Casino.PlayerProfile.FameInfo.fame_req_id (int32, required)`
- `Casino.RaceProto.RaceUpdateStatusRequest.RankChangeNotification.race_id (string, optional)`
- `Casino.UpdateGameEventRequest.event (Casino.GameEvent, repeated)`
- `Casino.UpdatePlayerGameEventRequest.event (Casino.GameEvent, repeated)`
- `Casino.UpdateProgressRequest.ConquestProgress.distributed_event_id (int64, required)`
- `Casino.UpdateProgressRequest.MiniGameEventProgress.event_id (int64, required)`
- `Casino.UpdateProgressRequest.TowerKeyProgress.event_id (int64, required)`
- `Casino.UpdateProgressRequest.unlocked_feature_id (uint32, repeated)`
- `Casino.UpdateProgressRequest.user_id (int64, required)`
- `Casino.UpdateUserRequest.ChallengeProgress.challenge_id (int32, required)`

### Progression / state

- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.show_tutorial (bool, optional)`
- `Casino.AddDciEventRequest.MiniGameEvent.mini_game_progress_state (Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState, required)`
- `Casino.AssignmentProgress.progress (Casino.BigNumber, required)`
- `Casino.CharmsTutorialProgressResponse.status (Casino.CharmsTutorialProgressResponse.Status, required)`
- `Casino.ClubSetProgressData.completed_in_other_club (bool, optional)`
- `Casino.ClubSetProgressData.tutorial_step (int32, optional)`
- `Casino.ClubSetTutorialProgressResponse.status (Casino.ClubSetTutorialProgressResponse.Status, required)`
- `Casino.GetAssignmentProgressResponse.assignment_progress (Casino.AssignmentProgress, repeated)`
- `Casino.GetAssignmentProgressResponse.status (Casino.GetAssignmentProgressResponse.Status, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.event_completed (bool, optional)`
- `Casino.NotifyElitesActiveRequest.MilestonesProgress.completed_milestones (int32, optional)`
- `Casino.PersonalAwardsProto.GetProgressResponse.counters (Casino.PersonalAwardsProto.PersonalCounter, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.counters_list (Casino.PersonalAwardsProto.PersonalCounterList, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.states (Casino.PersonalAwardsProto.PersonalState, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.states_list (Casino.PersonalAwardsProto.PersonalStateList, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.status (Casino.PersonalAwardsProto.GetProgressResponse.Status, required)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.counters (Casino.PersonalAwardsProto.PersonalCounter, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.counters_list (Casino.PersonalAwardsProto.PersonalCounterList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.states (Casino.PersonalAwardsProto.PersonalState, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.states_list (Casino.PersonalAwardsProto.PersonalStateList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressResponse.status (Casino.PersonalAwardsProto.UpdateProgressResponse.Status, required)`
- `Casino.PlayerProfile.Rank.rank (int32, required)`
- `Casino.PlayerProfile.Rank.rank_req_value (int64, repeated)`
- `Casino.RankOutcome.levels (int32, optional)`
- `Casino.StartLeaguePointsRequest.level1 (uint32, optional)`
- `Casino.StartLeaguePointsRequest.level2 (uint32, optional)`
- `Casino.StartLeaguePointsRequest.level3 (uint32, optional)`
- `Casino.StartLeaguePointsRequest.level_max (uint32, optional)`
- `Casino.TowerRunProgress.current_difficulty_level (int32, required)`
- `Casino.TowerRunProgress.state (int32, required)`
- `Casino.TowerRunProgress.zonk_health_points (int32, optional)`
- `Casino.UpdateAssignmentProgressRequest.progress (Casino.AssignmentProgress, required)`
- `Casino.UpdateCharmsProgressRequest.progress_data (Casino.CharmsProgressData, required)`
- `Casino.UpdateClubSetProgressRequest.progress_data (Casino.ClubSetProgressData, required)`
- `Casino.UpdatePlayerGameEventResponse.status (Casino.UpdatePlayerGameEventResponse.Status, required)`
- `Casino.UpdateProgressRequest.ConquestProgress.progress (Casino.ConquestChallengeProgress, required)`
- `Casino.UpdateProgressRequest.TowerKeyProgress.key_progress (double, required)`
- `Casino.UpdateProgressRequest.collection_event_state (Casino.CollectionEventState, optional)`
- `Casino.UpdateProgressRequest.level (int64, optional)`
- `Casino.UpdateProgressRequest.mini_game_event_progress (Casino.UpdateProgressRequest.MiniGameEventProgress, optional)`
- … 5 more rows in `fields.csv`

### Cost / input

- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.current_sum_of_bets (Casino.Chips, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.required_sum_of_bets (Casino.Chips, required)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trade_token_quantity (int32, optional)`
- `Casino.PlayerUpdateBetsRequest.sorted_bets (Casino.BetsList, required)`
- `Casino.UpdateBetsRequest.bets_on_fire_config (Casino.UpdateBetsRequest.BetsOnFireConfig, optional)`
- `Casino.UpdateProgressRequest.MiniGameEventProgress.current_sum_of_bets (Casino.Chips, required)`
- `Casino.UpdateProgressRequest.MiniGameEventProgress.required_sum_of_bets (Casino.Chips, required)`

### Currency / balance

- `Casino.UpdateProgressRequest.video_ad_chips_delta (int64, optional)`
- `Casino.UpdateProgressRequest.video_ad_piggy_bank_chips_delta (int64, optional)`
- `Casino.UpdateUserRequest.ChallengeProgress.chips (int64, required)`
- `Casino.VaultProgressUpdateRequest.balance_update (Casino.BalanceUpdate, required)`

### Reward / output

- `Casino.CharmsTutorialProgressRequest.rewards_data (Casino.RewardsData, optional)`
- `Casino.CharmsTutorialProgressResponse.rewards_data (Casino.RewardsData, optional)`
- `Casino.LeaguePointBonus.bonus_percent (uint32, optional)`
- `Casino.MinigameEventTrail.Step.reward (Casino.Reward, repeated)`
- `Casino.MinigameEventTrail.rewards_multiplier (double, required)`
- `Casino.PersonalAwardsProto.GetProgressResponse.awards (Casino.PersonalAwardsProto.PersonalAward, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.awards_list (Casino.PersonalAwardsProto.PersonalAwardList, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.bucket_awards (Casino.PersonalAwardsProto.PersonalBucketAward, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.awards (Casino.PersonalAwardsProto.PersonalAward, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.awards_list (Casino.PersonalAwardsProto.PersonalAwardList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.bucket_awards (Casino.PersonalAwardsProto.PersonalBucketAward, repeated)`
- `Casino.Reward.LeaguePointsBonus.bonus_percentage (int64, required)`
- `Casino.UpdateProgressRequest.rewards_data (Casino.RewardsData, optional)`

### Timing / reset / expiry

- `Casino.CharmsProgressData.CharmsTradingInfo.trades_reset_timer (int64, optional)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.expire_time_seconds (uint32, optional)`
- `Casino.Reward.LeaguePointsBonus.expiration_time_in_millis (int64, required)`

### Segment / eligibility / limit

- `Casino.AddDciEventRequest.MiniGameEvent.bulk_play_cap (int32, optional)`
- `Casino.UpdateProgressRequest.unlocked_game (Casino.GameDef, repeated)`

### Other structural fields

- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress.player_challenge_flags (int64, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.LotteryMachine.result (int32, repeated)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.moves (int32, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.spin_idx (int32, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.step_idx (int32, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.MiniGameEvent.lottery_machine (Casino.AddDciEventRequest.MiniGameEvent.LotteryMachine, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.trail (Casino.MinigameEventTrail, required)`
- `Casino.AssignmentProgress.milestone (Casino.AssignmentMilestone, repeated)`
- `Casino.CharmsProgressData.CharmsTradingInfo.is_trade_request_answered (bool, optional)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trades_left (int32, optional)`
- `Casino.CharmsProgressData.milestone (Casino.CharmsMilestone, optional)`
- `Casino.CharmsProgressData.packs_info (Casino.CharmsPacksInfo, optional)`
- `Casino.CharmsProgressData.trading_info (Casino.CharmsProgressData.CharmsTradingInfo, optional)`
- `Casino.CharmsTutorialProgressRequest.is_last_step (bool, required)`
- `Casino.CharmsTutorialProgressRequest.step (int32, required)`
- `Casino.CharmsTutorialProgressResponse.error_code (int32, optional)`
- `Casino.ClubSetProgressData.collected_items (int32, optional)`
- `Casino.ClubSetProgressData.number_of_boxes (int32, optional)`
- `Casino.ClubSetProgressData.total_items (int32, optional)`
- `Casino.ClubSetTutorialProgressRequest.is_last_step (bool, required)`
- `Casino.ClubSetTutorialProgressRequest.step (int32, required)`
- `Casino.ClubSetTutorialProgressResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubListEntry.RankDelta.delta (int32, optional)`
- `Casino.ClubsProto.ClubListEntry.RankDelta.new_flag (bool, optional)`
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
- `Casino.GetAssignmentProgressResponse.error_code (int32, optional)`
- `Casino.LeaderboardRank.outcome (Casino.RankOutcome, optional)`
- `Casino.LeaderboardRank.position (int32, optional)`
- `Casino.LeaguePointBonus.club_players (uint32, optional)`
- `Casino.LeaguePointBonus.enabled (bool, required)`
- … 40 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260901_160002`:

- `AppClient.UpdateProgress` — 651 (651 request, 0 response)
- `AppClient.UpdateFame` — 109 (109 request, 0 response)
- `AppClient.UpdateBets` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateProgressRequest.user_id` | 651 | 651 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.econ_stats.stat[].key` | 645 | 23220 | 36 | varying-in-session |
| `Casino.UpdateProgressRequest.econ_stats.stat[].value_double` | 645 | 7740 | 12 | varying-in-session |
| `Casino.UpdateProgressRequest.econ_stats.stat[].value_int` | 645 | 15480 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.mini_game_event_progress.current_sum_of_bets.value` | 645 | 645 | 36 | varying-in-session |
| `Casino.UpdateProgressRequest.mini_game_event_progress.event_id` | 645 | 645 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.mini_game_event_progress.moves` | 645 | 645 | 42 | varying-in-session |
| `Casino.UpdateProgressRequest.mini_game_event_progress.required_sum_of_bets.value` | 645 | 645 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].type` | 645 | 1290 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].type` | 645 | 1156 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.xp` | 645 | 645 | 623 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.cap_reached` | 602 | 602 | 1 | constant-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.chips.value` | 602 | 602 | 602 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.contribution_ratio` | 602 | 602 | 6 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.current_step` | 602 | 602 | 6 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].time.duration` | 516 | 1013 | 23 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].time.value` | 516 | 1013 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].time.expire_time` | 502 | 502 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.levels_amount` | 143 | 143 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.target_level` | 143 | 143 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.value` | 143 | 143 | 1 | constant-in-session |
| `Casino.UpdateFameRequest.fame_delta.value` | 109 | 109 | 45 | varying-in-session |
| `Casino.UpdateFameRequest.legacy_fame_delta` | 109 | 109 | 45 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.free_ticket.progress` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.lottery_multiplier.level` | 68 | 68 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.level` | 66 | 66 | 66 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.reward[].id` | 66 | 216 | 5 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.reward[].big_chips_delta.value` | 63 | 63 | 63 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.reward[].chips_delta` | 63 | 63 | 63 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.reward[].loyalty_points` | 63 | 63 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.video_ad_chips_delta` | 63 | 63 | 63 | varying-in-session |
| `Casino.UpdateProgressRequest.xp_level` | 63 | 63 | 63 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.action_type` | 45 | 45 | 6 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.hbi_name` | 45 | 45 | 6 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.id` | 45 | 45 | 8 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.progress.value` | 45 | 45 | 33 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.requirement.value` | 45 | 45 | 7 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward[].battle_pass_points.amount` | 45 | 45 | 5 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward[].id` | 45 | 71 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.segment_id` | 45 | 45 | 2 | varying-in-session |
| … | | | | 123 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: login/profile establishes current rank/fame -> server progress/fame updates follow gameplay/rewards -> client acknowledges -> level/rank-dependent unlocks and event progress alter other modules.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_topbar_sku_hc2_1_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc2_2_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc_1_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc_2_etc2.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open profile, fame/level progress, rank benefits and any progression history screen with markers.
- Perform a short normal play burst that changes fame/progress, then reopen profile.
- Mark any level-up or unlock popup that occurs naturally.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
