# Adventure

Adventure phases, difficulty, missions/limitations, milestones, skip tokens and rewards.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 5**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Adventure.proto`, `Common.proto`, `Services.proto`
- Services: `AdventureClient`, `AdventureServer`
- Related message types: **21**

- `Casino.ActiveMissions` (Adventure.proto)
- `Casino.AdventureActivePhaseRequest` (Adventure.proto)
- `Casino.AdventureActivePhaseResponse` (Adventure.proto)
- `Casino.AdventureBackground` (Adventure.proto)
- `Casino.AdventureDifficultyRequest` (Adventure.proto)
- `Casino.AdventureMissionUpdateRequest` (Adventure.proto)
- `Casino.AdventurePhaseState` (Adventure.proto)
- `Casino.AdventureSkipMissionRequest` (Adventure.proto)
- `Casino.AdventureSkipMissionResponse` (Adventure.proto)
- `Casino.AdventureUpdateRequest` (Adventure.proto)
- `Casino.ClubSetMilestoneReward` (Common.proto)
- `Casino.Difficulty` (Adventure.proto)
- `Casino.DifficultyList` (Adventure.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.Milestone` (Adventure.proto)
- `Casino.MilestoneReward` (Adventure.proto)
- `Casino.Mission` (Adventure.proto)
- `Casino.Mission.Limitation` (Adventure.proto)
- `Casino.PhaseLocked` (Adventure.proto)
- `Casino.Reward.AdventureSkipToken` (Common.proto)
- `Casino.TimeBasedCharmsMilestoneReward` (Common.proto)

## RPC and flow structure

Schema flow: active-phase fetch -> set difficulty -> server update with phase/missions -> mission progress updates -> skip mission using configured input -> milestone rewards.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AdventureServer.AdventureGetActivePhase` | `Casino.AdventureActivePhaseRequest` | `Casino.AdventureActivePhaseResponse` | 0 | 0 | schema-only |
| `AdventureServer.AdventureSetDifficulty` | `Casino.AdventureDifficultyRequest` | `Casino.AdventureActivePhaseResponse` | 0 | 0 | schema-only |
| `AdventureServer.AdventureSkipMission` | `Casino.AdventureSkipMissionRequest` | `Casino.AdventureSkipMissionResponse` | 0 | 0 | schema-only |
| `AdventureClient.AdventureUpdate` | `Casino.AdventureUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AdventureClient.AdventureMissionUpdate` | `Casino.AdventureMissionUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.ActiveMissions.mission (Casino.Mission, repeated)`
- `Casino.AdventureActivePhaseRequest.theme_id (int32, required)`
- `Casino.AdventureActivePhaseResponse.phase_id (int32, optional)`
- `Casino.AdventureBackground.background_id (int32, required)`
- `Casino.AdventureBackground.phase_id (int32, required)`
- `Casino.AdventureDifficultyRequest.difficulty_id (int32, required)`
- `Casino.AdventureDifficultyRequest.theme_id (int32, required)`
- `Casino.AdventureMissionUpdateRequest.mission (Casino.Mission, optional)`
- `Casino.AdventureMissionUpdateRequest.theme_id (int32, optional)`
- `Casino.AdventurePhaseState.difficulty_id (int32, optional)`
- `Casino.AdventureSkipMissionRequest.theme_id (int32, required)`
- `Casino.AdventureUpdateRequest.event_id (string, optional)`
- `Casino.AdventureUpdateRequest.phase_id (int32, optional)`
- `Casino.AdventureUpdateRequest.theme_id (int32, optional)`
- `Casino.ClubSetMilestoneReward.bundle_id (string, optional)`
- `Casino.Difficulty.id (int32, required)`
- `Casino.Milestone.id (int32, required)`
- `Casino.MilestoneReward.bundle_id (string, optional)`
- `Casino.MilestoneReward.milestone_id (int32, optional)`
- `Casino.PhaseLocked.phase_id (int32, required)`

### Progression / state

- `Casino.AdventureActivePhaseResponse.adventure_phase_state (Casino.AdventurePhaseState, optional)`
- `Casino.AdventureActivePhaseResponse.phase_locked (Casino.PhaseLocked, optional)`
- `Casino.AdventureActivePhaseResponse.status (Casino.AdventureActivePhaseResponse.Status, required)`
- `Casino.AdventureSkipMissionResponse.status (Casino.AdventureSkipMissionResponse.Status, required)`
- `Casino.AdventureUpdateRequest.active_missions (Casino.ActiveMissions, optional)`
- `Casino.AdventureUpdateRequest.phase_locked (Casino.PhaseLocked, optional)`
- `Casino.AdventureUpdateRequest.status (Casino.AdventureUpdateRequest.Status, required)`
- `Casino.Milestone.state (Casino.Milestone.State, required)`
- `Casino.Mission.progress (Casino.BigNumber, required)`

### Cost / input

- `Casino.Difficulty.min_bet (Casino.Chips, optional)`
- `Casino.Mission.requirement (Casino.BigNumber, required)`
- `Casino.Mission.skip_cost (int64, optional)`
- `Casino.Reward.AdventureSkipToken.amount (int64, required)`

### Currency / balance

- `Casino.AdventurePhaseState.skip_balance (int64, optional)`
- `Casino.AdventureSkipMissionResponse.skip_balance (int64, optional)`
- `Casino.AdventureUpdateRequest.skip_balance (int64, optional)`

### Reward / output

- `Casino.AdventurePhaseState.pending_reward (Casino.MilestoneReward, optional)`
- `Casino.AdventureSkipMissionResponse.pending_milestone_rewards (int32, optional)`
- `Casino.AdventureUpdateRequest.pending_milestone_rewards (int32, optional)`
- `Casino.ClubSetMilestoneReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetMilestoneReward.user_reward (Casino.Reward, repeated)`
- `Casino.TimeBasedCharmsMilestoneReward.reward (Casino.Reward, repeated)`

### Timing / reset / expiry

- `Casino.AdventureUpdateRequest.expire_timestamp_in_seconds (uint64, optional)`
- `Casino.PhaseLocked.unlock_timestamp_in_seconds (uint64, optional)`

### Segment / eligibility / limit

- `Casino.AdventureUpdateRequest.unlock_level (int32, optional)`
- `Casino.Mission.limitation (Casino.Mission.Limitation, repeated)`

### Other structural fields

- `Casino.ActiveMissions.slot_name (string, optional)`
- `Casino.AdventureActivePhaseResponse.difficulties (Casino.DifficultyList, optional)`
- `Casino.AdventureActivePhaseResponse.error_code (int32, optional)`
- `Casino.AdventureActivePhaseResponse.show_intro (bool, optional)`
- `Casino.AdventureMissionUpdateRequest.slot_name (string, optional)`
- `Casino.AdventurePhaseState.milestone (Casino.Milestone, repeated)`
- `Casino.AdventureSkipMissionRequest.mission_order_idx (int32, required)`
- `Casino.AdventureSkipMissionResponse.error_code (int32, optional)`
- `Casino.AdventureUpdateRequest.art_config (Casino.Art, optional)`
- `Casino.AdventureUpdateRequest.background (Casino.AdventureBackground, repeated)`
- `Casino.AdventureUpdateRequest.item (Casino.Item, repeated)`
- `Casino.ClubSetMilestoneReward.step (int32, optional)`
- `Casino.Difficulty.item (Casino.Item, repeated)`
- `Casino.DifficultyList.difficulty (Casino.Difficulty, repeated)`
- `Casino.Milestone.item (Casino.Item, repeated)`
- `Casino.Milestone.slot_name (string, required)`
- `Casino.MilestoneReward.item (Casino.Item, repeated)`
- `Casino.Mission.Limitation.type (string, required)`
- `Casino.Mission.Limitation.value_big_int (Casino.BigNumber, optional)`
- `Casino.Mission.Limitation.value_bool (bool, optional)`
- `Casino.Mission.mission_name (string, required)`
- `Casino.Mission.mission_order_idx (int32, required)`
- `Casino.TimeBasedCharmsMilestoneReward.step (int32, required)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: active-phase fetch -> set difficulty -> server update with phase/missions -> mission progress updates -> skip mission using configured input -> milestone rewards.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Adventure map/phase, difficulty, missions and milestone screens with markers.
- Inspect skip cost/token balance without using it unless already intended.
- Progress one mission normally and revisit its phase.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
