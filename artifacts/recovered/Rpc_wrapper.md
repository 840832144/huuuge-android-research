# Casino.RpcMessage wrapper

This is the top-level Protobuf RPC envelope recovered from `Services.proto`.

| # | label | type | field |
|---:|---|---|---|
| 1 | required | `Casino.RpcMessage.Type` | `type` |
| 2 | required | `int32` | `service_index` |
| 3 | required | `int32` | `method_index` |
| 4 | repeated | `bytes` | `payload` |
| 5 | optional | `int64` | `user_id` |
| 6 | optional | `uint32` | `seq_number` |
| 7 | optional | `uint32` | `uncompressed_payload_size` |
| 8 | optional | `Casino.RpcMessage.ProxyError` | `proxy_error` |
| 9 | optional | `uint32` | `method_hash` |

## Relevant service indexes

- `0` = `AppServer`
- `1` = `AppClient`

Method indexes are zero-based positions in `Services.proto`; see `service_method_map.csv`.

### Battle Pass

- AppServer / 139: BattlePassGetDailyMissions
- AppServer / 140: BattlePassGetWeeklyMissions
- AppServer / 141: BattlePassGetMilestones
- AppServer / 142: BattlePassTutorialCompleted
- AppServer / 143: BattlePassSkipMission
- AppClient / 53: BattlePassUpdate
- AppClient / 54: BattlePassMissionProgressUpdate
- AppClient / 55: BattlePassLevelCompleted
- AppClient / 56: BattlePassPremiumUpdate
