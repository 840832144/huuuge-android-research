# MiniPass

MiniPass event phases, missions, milestones, subscription state, tutorial and completion updates.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **85/100 — substantial live structure**
- Primary live samples: **10** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **4 / 10**
- Live populated field paths: **37**

## Schema scope

- Proto files: `AppServer.proto`, `Common.proto`, `MiniPass.proto`, `Services.proto`
- Services: `MiniPassClient`, `MiniPassServer`
- Related message types: **24**

- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.MakeInAppPurchaseRequest.MiniPassData` (AppServer.proto)
- `Casino.MiniPassEvent` (MiniPass.proto)
- `Casino.MiniPassGetMilestonesRequest` (MiniPass.proto)
- `Casino.MiniPassGetMilestonesResponse` (MiniPass.proto)
- `Casino.MiniPassGetMissionsRequest` (MiniPass.proto)
- `Casino.MiniPassGetMissionsResponse` (MiniPass.proto)
- `Casino.MiniPassMilestone` (MiniPass.proto)
- `Casino.MiniPassMilestoneCompletedRequest` (MiniPass.proto)
- `Casino.MiniPassMission` (MiniPass.proto)
- `Casino.MiniPassMission.Limitation` (MiniPass.proto)
- `Casino.MiniPassMission.Limitation.Value` (MiniPass.proto)
- `Casino.MiniPassMissionCompletedRequest` (MiniPass.proto)
- `Casino.MiniPassMissionsUpdateRequest` (MiniPass.proto)
- `Casino.MiniPassNextPhaseRequest` (MiniPass.proto)
- `Casino.MiniPassNextPhaseResponse` (MiniPass.proto)
- `Casino.MiniPassRemoveRequest` (MiniPass.proto)
- `Casino.MiniPassReward` (MiniPass.proto)
- `Casino.MiniPassSubscriptionUpdateRequest` (MiniPass.proto)
- `Casino.MiniPassTutorialCompletedResponse` (MiniPass.proto)
- `Casino.MiniPassUpdateRequest` (MiniPass.proto)
- `Casino.Reward.MiniPassPoints` (Common.proto)
- `Casino.Reward.MiniPassSubscription` (Common.proto)

## RPC and flow structure

Observed/schema flow: update establishes event/phase -> mission and milestone fetches return definitions -> mission/milestone completion updates report progress -> next-phase/subscription/tutorial messages alter pass state.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `MiniPassServer.MiniPassGetMissions` | `Casino.MiniPassGetMissionsRequest` | `Casino.MiniPassGetMissionsResponse` | 1 | 1 | observed-live |
| `MiniPassServer.MiniPassGetMilestones` | `Casino.MiniPassGetMilestonesRequest` | `Casino.MiniPassGetMilestonesResponse` | 0 | 0 | schema-only |
| `MiniPassServer.MiniPassNextPhase` | `Casino.MiniPassNextPhaseRequest` | `Casino.MiniPassNextPhaseResponse` | 0 | 0 | schema-only |
| `MiniPassServer.MiniPassTutorialCompleted` | `Casino.EmptyRequest` | `Casino.MiniPassTutorialCompletedResponse` | 1 | 1 | observed-live |
| `MiniPassClient.MiniPassUpdate` | `Casino.MiniPassUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `MiniPassClient.MiniPassRemove` | `Casino.MiniPassRemoveRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `MiniPassClient.MiniPassMissionsUpdate` | `Casino.MiniPassMissionsUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `MiniPassClient.MiniPassMissionCompleted` | `Casino.MiniPassMissionCompletedRequest` | `Casino.EmptyResponse` | 5 | 0 | observed-live |
| `MiniPassClient.MiniPassMilestoneCompleted` | `Casino.MiniPassMilestoneCompletedRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `MiniPassClient.MiniPassSubscriptionUpdate` | `Casino.MiniPassSubscriptionUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.MakeInAppPurchaseRequest.MiniPassData.event_id (string, required)`
- `Casino.MakeInAppPurchaseRequest.MiniPassData.phase_id (string, optional)`
- `Casino.MiniPassEvent.event_id (string, required)`
- `Casino.MiniPassEvent.phase_id (string, required)`
- `Casino.MiniPassEvent.product_id (string, optional)`
- `Casino.MiniPassGetMilestonesRequest.event_id (string, required)`
- `Casino.MiniPassGetMilestonesRequest.phase_id (string, required)`
- `Casino.MiniPassGetMissionsRequest.event_id (string, required)`
- `Casino.MiniPassGetMissionsRequest.phase_id (string, required)`
- `Casino.MiniPassMilestoneCompletedRequest.event_id (string, required)`
- `Casino.MiniPassMilestoneCompletedRequest.phase_id (string, required)`
- `Casino.MiniPassMission.id (string, required)`
- `Casino.MiniPassMissionCompletedRequest.event_id (string, required)`
- `Casino.MiniPassMissionCompletedRequest.mission (Casino.MiniPassMission, required)`
- `Casino.MiniPassMissionCompletedRequest.phase_id (string, required)`
- `Casino.MiniPassMissionsUpdateRequest.event_id (string, required)`
- `Casino.MiniPassMissionsUpdateRequest.phase_id (string, required)`
- `Casino.MiniPassNextPhaseRequest.event_id (string, required)`
- `Casino.MiniPassRemoveRequest.event_id (string, required)`
- `Casino.MiniPassReward.reward_bundle_id (string, optional)`
- `Casino.MiniPassSubscriptionUpdateRequest.event_id (string, required)`
- `Casino.MiniPassSubscriptionUpdateRequest.phase_id (string, required)`
- `Casino.Reward.MiniPassPoints.event_id (string, required)`
- `Casino.Reward.MiniPassPoints.phase_id (string, optional)`
- `Casino.Reward.MiniPassSubscription.event_id (string, required)`
- `Casino.Reward.MiniPassSubscription.phase_id (string, optional)`

### Progression / state

- `Casino.MiniPassEvent.pass_status (Casino.MiniPassStatus, required)`
- `Casino.MiniPassGetMilestonesResponse.status (Casino.MiniPassGetMilestonesResponse.Status, required)`
- `Casino.MiniPassGetMissionsResponse.status (Casino.MiniPassGetMissionsResponse.Status, required)`
- `Casino.MiniPassMilestoneCompletedRequest.pass_status (Casino.MiniPassStatus, required)`
- `Casino.MiniPassMission.iteration (int64, optional)`
- `Casino.MiniPassMission.progress (Casino.BigNumber, optional)`
- `Casino.MiniPassNextPhaseResponse.status (Casino.MiniPassNextPhaseResponse.Status, required)`
- `Casino.MiniPassTutorialCompletedResponse.status (Casino.MiniPassTutorialCompletedResponse.Status, required)`
- `Casino.MiniPassUpdateRequest.tutorial_completed (bool, optional)`

### Cost / input

- `Casino.MiniPassMilestone.requirement (int64, required)`
- `Casino.MiniPassMission.requirement (Casino.BigNumber, required)`
- `Casino.Reward.MiniPassPoints.amount (int64, required)`

### Currency / balance

- `Casino.MiniPassEvent.pass_points_balance (int64, optional)`

### Reward / output

- `Casino.MiniPassEvent.grand_reward (Casino.MiniPassReward, optional)`
- `Casino.MiniPassEvent.subscription_rewards (Casino.Item, repeated)`
- `Casino.MiniPassGetMilestonesResponse.grand_reward (Casino.MiniPassReward, optional)`
- `Casino.MiniPassMilestone.free_reward (Casino.MiniPassReward, optional)`
- `Casino.MiniPassMilestone.premium_reward (Casino.MiniPassReward, optional)`
- `Casino.MiniPassMilestoneCompletedRequest.grand_reward (Casino.MiniPassReward, optional)`
- `Casino.MiniPassSubscriptionUpdateRequest.grand_reward (Casino.MiniPassReward, optional)`
- `Casino.MiniPassSubscriptionUpdateRequest.subscription_rewards (Casino.Item, repeated)`

### Timing / reset / expiry

- `Casino.MiniPassEvent.expire (int64, optional)`

### Segment / eligibility / limit

- `Casino.MiniPassMission.limitations (Casino.MiniPassMission.Limitation, repeated)`

### Other structural fields

- `Casino.MiniPassEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.MiniPassEvent.ghost_mode (bool, optional)`
- `Casino.MiniPassEvent.milestones (Casino.MiniPassMilestone, repeated)`
- `Casino.MiniPassEvent.missions (Casino.MiniPassMission, repeated)`
- `Casino.MiniPassEvent.pass_variant (string, optional)`
- `Casino.MiniPassEvent.subscription_type (string, optional)`
- `Casino.MiniPassGetMilestonesResponse.error_code (int32, optional)`
- `Casino.MiniPassGetMilestonesResponse.milestones (Casino.MiniPassMilestone, repeated)`
- `Casino.MiniPassGetMissionsResponse.error_code (int32, optional)`
- `Casino.MiniPassGetMissionsResponse.missions (Casino.MiniPassMission, repeated)`
- `Casino.MiniPassMilestoneCompletedRequest.milestones (Casino.MiniPassMilestone, repeated)`
- `Casino.MiniPassMission.Limitation.Value.value_big_int (Casino.BigNumber, optional)`
- `Casino.MiniPassMission.Limitation.Value.value_bool (bool, optional)`
- `Casino.MiniPassMission.Limitation.Value.value_double (double, optional)`
- `Casino.MiniPassMission.Limitation.Value.value_string (string, optional)`
- `Casino.MiniPassMission.Limitation.Value.value_strings (string, repeated)`
- `Casino.MiniPassMission.Limitation.type (string, required)`
- `Casino.MiniPassMission.Limitation.value (Casino.MiniPassMission.Limitation.Value, required)`
- `Casino.MiniPassMission.action_type (string, required)`
- `Casino.MiniPassMission.hbi_name (string, optional)`
- `Casino.MiniPassMission.items (Casino.Item, repeated)`
- `Casino.MiniPassMissionsUpdateRequest.missions (Casino.MiniPassMission, repeated)`
- `Casino.MiniPassNextPhaseResponse.error_code (int32, optional)`
- `Casino.MiniPassNextPhaseResponse.mini_pass_event (Casino.MiniPassEvent, optional)`
- `Casino.MiniPassReward.collected (bool, optional)`
- `Casino.MiniPassReward.items (Casino.Item, repeated)`
- `Casino.MiniPassSubscriptionUpdateRequest.milestones (Casino.MiniPassMilestone, repeated)`
- `Casino.MiniPassSubscriptionUpdateRequest.subscription_type (string, required)`
- `Casino.MiniPassTutorialCompletedResponse.error_code (int32, optional)`
- `Casino.MiniPassUpdateRequest.art_config (Casino.Art, optional)`
- `Casino.MiniPassUpdateRequest.mini_pass_events (Casino.MiniPassEvent, repeated)`
- `Casino.Reward.MiniPassPoints.variant (string, optional)`
- `Casino.Reward.MiniPassSubscription.subscription_type (string, required)`

## Live-session coverage

Observed endpoint samples in `20260825_182300`:

- `MiniPassClient.MiniPassMissionCompleted` — 5 (5 request, 0 response)
- `MiniPassServer.MiniPassGetMissions` — 2 (1 request, 1 response)
- `MiniPassServer.MiniPassTutorialCompleted` — 2 (1 request, 1 response)
- `MiniPassClient.MiniPassMilestoneCompleted` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.MiniPassMissionCompletedRequest.event_id` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.action_type` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.hbi_name` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.id` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.items[].metadata[].key` | 5 | 15 | 3 | varying-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.items[].metadata[].value` | 5 | 15 | 3 | varying-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.items[].source` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.items[].type` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.items[].value` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.iteration` | 5 | 5 | 5 | varying-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.progress.value` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.mission.requirement.value` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassMissionCompletedRequest.phase_id` | 5 | 5 | 1 | constant-in-session |
| `Casino.MiniPassGetMissionsRequest.event_id` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsRequest.phase_id` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].action_type` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].hbi_name` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].id` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].items[].metadata[].key` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].items[].metadata[].value` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].items[].source` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].items[].type` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].items[].value` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].iteration` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].progress.value` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.missions[].requirement.value` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassGetMissionsResponse.status` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.event_id` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.milestones[].free_reward.collected` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.milestones[].free_reward.items[].source` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.milestones[].free_reward.items[].type` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.milestones[].free_reward.items[].value` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.milestones[].free_reward.reward_bundle_id` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.milestones[].requirement` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.pass_status` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassMilestoneCompletedRequest.phase_id` | 1 | 1 | 1 | single-observation |
| `Casino.MiniPassTutorialCompletedResponse.status` | 1 | 1 | 1 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260825_182300`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: update establishes event/phase -> mission and milestone fetches return definitions -> mission/milestone completion updates report progress -> next-phase/subscription/tutorial messages alter pass state.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open MiniPass main, missions and milestone/reward-track screens with separate markers.
- Progress and claim one mission/milestone naturally, then revisit the track.
- Open subscription/premium details to capture entitlement and expiry fields without purchasing.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
