# Huuuge Casino — BattlePass recovered schema

Recovered directly from the serialized `FileDescriptorProto` embedded in `libClawApp.so`.

The authoritative machine-readable schema is in `huuuge_descriptors.pb`.

## BattlePassMilestone

| # | label | type | field |
|---:|---|---|---|
| 1 | required | `int32` | `level` |
| 2 | required | `int64` | `requirement` |
| 3 | optional | `Casino.BattlePassReward` | `free_reward` |
| 4 | optional | `Casino.BattlePassReward` | `premium_reward` |
| 5 | optional | `Casino.BattlePassReward` | `deluxe_reward` |

## BattlePassMission

| # | label | type | field |
|---:|---|---|---|
| 1 | required | `string` | `id` |
| 2 | required | `string` | `set_id` |
| 3 | required | `Casino.BattlePassMission.Type` | `type` |
| 4 | required | `Casino.BattlePassMission.Status` | `status` |
| 5 | required | `Casino.BigNumber` | `progress` |
| 6 | required | `Casino.BigNumber` | `requirement` |
| 7 | required | `string` | `action_type` |
| 8 | repeated | `Casino.BattlePassMission.Limitation` | `limitation` |
| 9 | repeated | `Casino.Reward` | `reward` |
| 10 | optional | `string` | `reward_bundle_id` |
| 11 | optional | `string` | `hbi_name` |
| 12 | optional | `int64` | `segment_id` |
| 13 | optional | `bool` | `skippable` |

## BattlePassUpdateRequest

| # | label | type | field |
|---:|---|---|---|
| 1 | required | `Casino.BattlePassUpdateRequest.Status` | `status` |
| 2 | optional | `string` | `event_id` |
| 3 | optional | `string` | `battle_pass_id` |
| 4 | optional | `int64` | `daily_expire` |
| 5 | optional | `int64` | `pass_expire` |
| 6 | optional | `Casino.BattlePassType` | `pass_type` |
| 7 | optional | `int32` | `pass_level` |
| 8 | optional | `int64` | `pass_points_balance` |
| 9 | optional | `bool` | `tutorial_completed` |
| 10 | optional | `Casino.BattlePassUpdateRequest.Product` | `premium_product` |
| 11 | optional | `Casino.BattlePassUpdateRequest.Product` | `deluxe_product` |
| 12 | optional | `int32` | `unlock_level` |
| 13 | repeated | `Casino.BattlePassMission` | `daily_mission` |
| 14 | repeated | `Casino.BattlePassMissionSet` | `weekly_mission` |
| 15 | repeated | `Casino.BattlePassMilestone` | `milestone` |
| 16 | repeated | `Casino.BattlePassFinalBundle` | `final_bundle` |
| 17 | repeated | `Casino.ConfigHbiData` | `config_hbi_data` |
| 18 | optional | `Casino.Art` | `art_config` |
| 19 | optional | `Casino.BattlePassPrestige` | `prestige` |
| 20 | optional | `int32` | `mission_skip_balance` |
| 21 | repeated | `Casino.BattlePassItem` | `event_items` |

## BattlePassGetMilestonesResponse

| # | label | type | field |
|---:|---|---|---|
| 1 | required | `Casino.BattlePassGetMilestonesResponse.Status` | `status` |
| 2 | optional | `int32` | `error_code` |
| 3 | repeated | `Casino.BattlePassMilestone` | `milestone` |
| 4 | repeated | `Casino.BattlePassFinalBundle` | `final_bundle` |
