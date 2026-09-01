# Battle Pass

Battle Pass event state, daily/weekly missions, free/premium/deluxe milestones, prestige, skip balance and entitlement updates.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **75/100 — substantial live structure**
- Primary live samples: **46** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **2 / 9**
- Live populated field paths: **208**

## Schema scope

- Proto files: `BattlePass.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **27**

- `Casino.BattlePassFinalBundle` (BattlePass.proto)
- `Casino.BattlePassGetDailyMissionsResponse` (BattlePass.proto)
- `Casino.BattlePassGetMilestonesResponse` (BattlePass.proto)
- `Casino.BattlePassGetWeeklyMissionsResponse` (BattlePass.proto)
- `Casino.BattlePassItem` (BattlePass.proto)
- `Casino.BattlePassLevelCompletedRequest` (BattlePass.proto)
- `Casino.BattlePassMilestone` (BattlePass.proto)
- `Casino.BattlePassMission` (BattlePass.proto)
- `Casino.BattlePassMission.Limitation` (BattlePass.proto)
- `Casino.BattlePassMission.Limitation.Value` (BattlePass.proto)
- `Casino.BattlePassMissionProgressUpdateRequest` (BattlePass.proto)
- `Casino.BattlePassMissionSet` (BattlePass.proto)
- `Casino.BattlePassPremiumUpdateRequest` (BattlePass.proto)
- `Casino.BattlePassPrestige` (BattlePass.proto)
- `Casino.BattlePassPrestigeBenefit` (BattlePass.proto)
- `Casino.BattlePassPrestigeTier` (BattlePass.proto)
- `Casino.BattlePassReward` (BattlePass.proto)
- `Casino.BattlePassSkipMissionRequest` (BattlePass.proto)
- `Casino.BattlePassSkipMissionResponse` (BattlePass.proto)
- `Casino.BattlePassTutorialCompletedResponse` (BattlePass.proto)
- `Casino.BattlePassType` (Common.proto)
- `Casino.BattlePassUpdateRequest` (BattlePass.proto)
- `Casino.BattlePassUpdateRequest.Product` (BattlePass.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.Reward.BattlePassPoints` (Common.proto)
- `Casino.Reward.BattlePassPremium` (Common.proto)

## RPC and flow structure

Schema flow: `BattlePassUpdate` establishes event/pass/products/missions/milestones -> daily/weekly/milestone fetches refresh tracks -> progress and level-completed updates advance state -> premium update changes entitlement -> tutorial/skip operations acknowledge user actions.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.BattlePassGetDailyMissions` | `Casino.EmptyRequest` | `Casino.BattlePassGetDailyMissionsResponse` | 0 | 0 | schema-only |
| `AppServer.BattlePassGetWeeklyMissions` | `Casino.EmptyRequest` | `Casino.BattlePassGetWeeklyMissionsResponse` | 0 | 0 | schema-only |
| `AppServer.BattlePassGetMilestones` | `Casino.EmptyRequest` | `Casino.BattlePassGetMilestonesResponse` | 0 | 0 | schema-only |
| `AppServer.BattlePassTutorialCompleted` | `Casino.EmptyRequest` | `Casino.BattlePassTutorialCompletedResponse` | 0 | 0 | schema-only |
| `AppServer.BattlePassSkipMission` | `Casino.BattlePassSkipMissionRequest` | `Casino.BattlePassSkipMissionResponse` | 0 | 0 | schema-only |
| `AppClient.BattlePassUpdate` | `Casino.BattlePassUpdateRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.BattlePassMissionProgressUpdate` | `Casino.BattlePassMissionProgressUpdateRequest` | `Casino.EmptyResponse` | 45 | 0 | observed-live |
| `AppClient.BattlePassLevelCompleted` | `Casino.BattlePassLevelCompletedRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.BattlePassPremiumUpdate` | `Casino.BattlePassPremiumUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.BattlePassItem.reward_bundle_id (string, optional)`
- `Casino.BattlePassMission.id (string, required)`
- `Casino.BattlePassMission.reward_bundle_id (string, optional)`
- `Casino.BattlePassMission.segment_id (int64, optional)`
- `Casino.BattlePassMission.set_id (string, required)`
- `Casino.BattlePassMissionProgressUpdateRequest.mission (Casino.BattlePassMission, required)`
- `Casino.BattlePassMissionSet.mission (Casino.BattlePassMission, repeated)`
- `Casino.BattlePassMissionSet.set_id (string, required)`
- `Casino.BattlePassReward.reward_bundle_id (string, optional)`
- `Casino.BattlePassSkipMissionRequest.id (string, required)`
- `Casino.BattlePassSkipMissionRequest.set_id (string, required)`
- `Casino.BattlePassUpdateRequest.Product.product_id (string, required)`
- `Casino.BattlePassUpdateRequest.battle_pass_id (string, optional)`
- `Casino.BattlePassUpdateRequest.event_id (string, optional)`
- `Casino.Reward.BattlePassPremium.battle_pass_id (string, required)`

### Progression / state

- `Casino.BattlePassFinalBundle.level (int32, required)`
- `Casino.BattlePassGetDailyMissionsResponse.status (Casino.BattlePassGetDailyMissionsResponse.Status, required)`
- `Casino.BattlePassGetMilestonesResponse.status (Casino.BattlePassGetMilestonesResponse.Status, required)`
- `Casino.BattlePassGetWeeklyMissionsResponse.status (Casino.BattlePassGetWeeklyMissionsResponse.Status, required)`
- `Casino.BattlePassLevelCompletedRequest.pass_level (int32, required)`
- `Casino.BattlePassMilestone.level (int32, required)`
- `Casino.BattlePassMission.progress (Casino.BigNumber, required)`
- `Casino.BattlePassMission.status (Casino.BattlePassMission.Status, required)`
- `Casino.BattlePassPrestige.current_tier (int32, required)`
- `Casino.BattlePassPrestige.state (Casino.BattlePassPrestige.State, required)`
- `Casino.BattlePassPrestige.tiers (Casino.BattlePassPrestigeTier, repeated)`
- `Casino.BattlePassPrestigeTier.tier (int32, required)`
- `Casino.BattlePassSkipMissionResponse.status (Casino.BattlePassSkipMissionResponse.Status, required)`
- `Casino.BattlePassTutorialCompletedResponse.status (Casino.BattlePassTutorialCompletedResponse.Status, required)`
- `Casino.BattlePassUpdateRequest.pass_level (int32, optional)`
- `Casino.BattlePassUpdateRequest.status (Casino.BattlePassUpdateRequest.Status, required)`
- `Casino.BattlePassUpdateRequest.tutorial_completed (bool, optional)`

### Cost / input

- `Casino.BattlePassFinalBundle.requirement (int64, required)`
- `Casino.BattlePassMilestone.requirement (int64, required)`
- `Casino.BattlePassMission.requirement (Casino.BigNumber, required)`
- `Casino.Reward.BattlePassPoints.amount (int64, required)`

### Currency / balance

- `Casino.BattlePassSkipMissionResponse.mission_skip_balance (int32, optional)`
- `Casino.BattlePassUpdateRequest.mission_skip_balance (int32, optional)`
- `Casino.BattlePassUpdateRequest.pass_points_balance (int64, optional)`

### Reward / output

- `Casino.BattlePassFinalBundle.deluxe_reward (Casino.BattlePassReward, optional)`
- `Casino.BattlePassFinalBundle.premium_reward (Casino.BattlePassReward, optional)`
- `Casino.BattlePassMilestone.deluxe_reward (Casino.BattlePassReward, optional)`
- `Casino.BattlePassMilestone.free_reward (Casino.BattlePassReward, optional)`
- `Casino.BattlePassMilestone.premium_reward (Casino.BattlePassReward, optional)`
- `Casino.BattlePassMission.reward (Casino.Reward, repeated)`
- `Casino.BattlePassReward.reward (Casino.Reward, repeated)`

### Timing / reset / expiry

- `Casino.BattlePassUpdateRequest.daily_expire (int64, optional)`
- `Casino.BattlePassUpdateRequest.pass_expire (int64, optional)`

### Segment / eligibility / limit

- `Casino.BattlePassMission.limitation (Casino.BattlePassMission.Limitation, repeated)`
- `Casino.BattlePassUpdateRequest.unlock_level (int32, optional)`

### Other structural fields

- `Casino.BattlePassFinalBundle.type (Casino.BattlePassFinalBundle.FinalBundleType, optional)`
- `Casino.BattlePassGetDailyMissionsResponse.daily_mission (Casino.BattlePassMission, repeated)`
- `Casino.BattlePassGetDailyMissionsResponse.error_code (int32, optional)`
- `Casino.BattlePassGetMilestonesResponse.error_code (int32, optional)`
- `Casino.BattlePassGetMilestonesResponse.final_bundle (Casino.BattlePassFinalBundle, repeated)`
- `Casino.BattlePassGetMilestonesResponse.milestone (Casino.BattlePassMilestone, repeated)`
- `Casino.BattlePassGetWeeklyMissionsResponse.error_code (int32, optional)`
- `Casino.BattlePassGetWeeklyMissionsResponse.weekly_mission (Casino.BattlePassMissionSet, repeated)`
- `Casino.BattlePassItem.collected (bool, optional)`
- `Casino.BattlePassItem.items (Casino.Item, repeated)`
- `Casino.BattlePassLevelCompletedRequest.final_bundle (Casino.BattlePassFinalBundle, repeated)`
- `Casino.BattlePassLevelCompletedRequest.milestone (Casino.BattlePassMilestone, repeated)`
- `Casino.BattlePassMission.Limitation.Value.value_big_int (Casino.BigNumber, optional)`
- `Casino.BattlePassMission.Limitation.Value.value_bool (bool, optional)`
- `Casino.BattlePassMission.Limitation.Value.value_double (double, optional)`
- `Casino.BattlePassMission.Limitation.Value.value_int (int64, optional)`
- `Casino.BattlePassMission.Limitation.Value.value_string (string, optional)`
- `Casino.BattlePassMission.Limitation.Value.value_strings (string, repeated)`
- `Casino.BattlePassMission.Limitation.type (string, required)`
- `Casino.BattlePassMission.Limitation.value (Casino.BattlePassMission.Limitation.Value, required)`
- `Casino.BattlePassMission.action_type (string, required)`
- `Casino.BattlePassMission.hbi_name (string, optional)`
- `Casino.BattlePassMission.skippable (bool, optional)`
- `Casino.BattlePassMission.type (Casino.BattlePassMission.Type, required)`
- `Casino.BattlePassMissionSet.end_date (int64, optional)`
- `Casino.BattlePassMissionSet.set_type (Casino.BattlePassMissionSet.MissionSetType, optional)`
- `Casino.BattlePassMissionSet.start_date (int64, required)`
- `Casino.BattlePassPremiumUpdateRequest.final_bundle (Casino.BattlePassFinalBundle, repeated)`
- `Casino.BattlePassPremiumUpdateRequest.milestone (Casino.BattlePassMilestone, repeated)`
- `Casino.BattlePassPremiumUpdateRequest.pass_type (Casino.BattlePassType, required)`
- `Casino.BattlePassPremiumUpdateRequest.prestige (Casino.BattlePassPrestige, optional)`
- `Casino.BattlePassPrestige.decay_warning_start_date (int64, optional)`
- `Casino.BattlePassPrestigeBenefit.benefit_type (string, required)`
- `Casino.BattlePassPrestigeBenefit.value (string, optional)`
- `Casino.BattlePassPrestigeTier.benefits (Casino.BattlePassPrestigeBenefit, repeated)`
- `Casino.BattlePassReward.collected (bool, optional)`
- `Casino.BattlePassSkipMissionResponse.error_code (int32, optional)`
- `Casino.BattlePassTutorialCompletedResponse.error_code (int32, optional)`
- `Casino.BattlePassType.type (Casino.BattlePassType.PassType, required)`
- `Casino.BattlePassUpdateRequest.Product.worth (int64, required)`
- … 12 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260901_160002`:

- `AppClient.BattlePassMissionProgressUpdate` — 45 (45 request, 0 response)
- `AppClient.BattlePassUpdate` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.BattlePassMissionProgressUpdateRequest.mission.action_type` | 45 | 45 | 6 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.hbi_name` | 45 | 45 | 6 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.id` | 45 | 45 | 8 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.progress.value` | 45 | 45 | 33 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.requirement.value` | 45 | 45 | 7 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward[].battle_pass_points.amount` | 45 | 45 | 5 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward[].id` | 45 | 71 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.segment_id` | 45 | 45 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.set_id` | 45 | 45 | 5 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.skippable` | 45 | 45 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.status` | 45 | 45 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.type` | 45 | 45 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward[].big_chips_delta.value` | 26 | 26 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward[].chips_delta` | 26 | 26 | 2 | varying-in-session |
| `Casino.BattlePassMissionProgressUpdateRequest.mission.reward_bundle_id` | 5 | 5 | 5 | varying-in-session |
| `Casino.BattlePassUpdateRequest.art_config.expiration_date` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.art_config.package[].path` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.art_config.package[].reskin_name` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.art_config.package[].type` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.art_config.package[].version` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.battle_pass_id` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.config_hbi_data[].config_identifier` | 1 | 11 | 11 | single-observation |
| `Casino.BattlePassUpdateRequest.config_hbi_data[].config_type` | 1 | 11 | 11 | single-observation |
| `Casino.BattlePassUpdateRequest.config_hbi_data[].hbi_data.id` | 1 | 11 | 4 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_expire` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].action_type` | 1 | 8 | 8 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].hbi_name` | 1 | 8 | 8 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].id` | 1 | 8 | 8 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].limitation[].type` | 1 | 2 | 2 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].limitation[].value.value_string` | 1 | 2 | 2 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].progress.value` | 1 | 8 | 2 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].requirement.value` | 1 | 8 | 7 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].reward[].battle_pass_points.amount` | 1 | 7 | 3 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].reward[].big_chips_delta.value` | 1 | 7 | 6 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].reward[].charms_trade_token_delta` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].reward[].chips_delta` | 1 | 7 | 6 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].reward[].id` | 1 | 15 | 3 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].reward_bundle_id` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].segment_id` | 1 | 8 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.daily_mission[].set_id` | 1 | 8 | 1 | single-observation |
| … | | | | 168 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: `BattlePassUpdate` establishes event/pass/products/missions/milestones -> daily/weekly/milestone fetches refresh tracks -> progress and level-completed updates advance state -> premium update changes entitlement -> tutorial/skip operations acknowledge user actions.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_battle_pass_common_2_etc2.zpk`
- `atlas_battle_pass_common_2_etc2.zpk` and recovered BattlePass descriptors provide a strong schema/static skeleton.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- When an eligible account is available, open the Battle Pass main screen, reward track and daily/weekly mission tabs with markers.
- Capture one progress change and one naturally available milestone/reward claim.
- Open premium/deluxe details without purchasing to capture product/eligibility structure.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
