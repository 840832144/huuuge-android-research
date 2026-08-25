# Missions / Quests / Daily-Weekly Tasks

Generic assignment events and progress/claim structure, distinct from Battle Pass, MiniPass, Adventure and Elites-specific missions.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 3**
- Live populated field paths: **0**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **16**

- `Casino.AssignmentMilestone` (Common.proto)
- `Casino.AssignmentProgress` (Common.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.GetAssignmentProgressRequest` (AppServer.proto)
- `Casino.GetAssignmentProgressResponse` (AppServer.proto)
- `Casino.Reward.MissionsData` (Common.proto)
- `Casino.UpdateAssignmentEventsRequest` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.BannerText` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.Scenario` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams` (AppClient.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.StepRewards` (AppClient.proto)
- `Casino.UpdateAssignmentProgressRequest` (AppClient.proto)

## RPC and flow structure

Inferred flow: server pushes assignment definitions/limits/streak steps -> client progress updates -> explicit progress fetch -> reward bundle claim through the shared rewards module.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.GetAssignmentProgress` | `Casino.GetAssignmentProgressRequest` | `Casino.GetAssignmentProgressResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateAssignmentEvents` | `Casino.UpdateAssignmentEventsRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateAssignmentProgress` | `Casino.UpdateAssignmentProgressRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AssignmentMilestone.reward_bundle_id (string, optional)`
- `Casino.AssignmentProgress.event_id (int64, required)`
- `Casino.GetAssignmentProgressRequest.event_id (int64, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.BannerText.key (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.template_id (int32, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.event_id (int64, required)`

### Progression / state

- `Casino.AssignmentMilestone.status (Casino.AssignmentMilestone.Status, required)`
- `Casino.AssignmentProgress.progress (Casino.BigNumber, required)`
- `Casino.GetAssignmentProgressResponse.assignment_progress (Casino.AssignmentProgress, repeated)`
- `Casino.GetAssignmentProgressResponse.status (Casino.GetAssignmentProgressResponse.Status, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.progress (Casino.BigNumber, optional)`
- `Casino.UpdateAssignmentProgressRequest.progress (Casino.AssignmentProgress, required)`

### Cost / input

- `Casino.AssignmentMilestone.requirement (Casino.BigNumber, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.newsfeed_url (string, repeated)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.AssignmentMilestone.reward (Casino.Reward, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.StepRewards.rewards (Casino.Reward, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.steps_rewards (Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.StepRewards, repeated)`

### Timing / reset / expiry

- `Casino.Reward.MissionsData.club_missions_end_time (int32, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.cooldown (int32, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.step_expire (int64, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.streak_expire (int64, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.expire (int64, optional)`

### Segment / eligibility / limit

- `Casino.UpdateAssignmentEventsRequest.Assignment.limitation (Casino.UpdateAssignmentEventsRequest.Assignment.Limitation, repeated)`

### Other structural fields

- `Casino.AssignmentProgress.milestone (Casino.AssignmentMilestone, repeated)`
- `Casino.GetAssignmentProgressResponse.error_code (int32, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.BannerText.value (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.Scenario.display_priority (int32, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.Scenario.type (string, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.banner_text (Casino.UpdateAssignmentEventsRequest.Assignment.Banner.BannerText, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.cta_text (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.fullscreen_url (string, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.lobby_tile (bool, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.scenario (Casino.UpdateAssignmentEventsRequest.Assignment.Banner.Scenario, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Banner.type (Casino.UpdateAssignmentEventsRequest.Assignment.Banner.Type, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value.value_big_int (Casino.BigNumber, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value.value_bool (bool, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value.value_double (double, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value.value_int (int64, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value.value_string (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value.value_strings (string, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.type (string, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.value (Casino.UpdateAssignmentEventsRequest.Assignment.Limitation.Value, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.current_step (int32, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.metadata (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.num_steps (int32, required)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.action_type (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.banner (Casino.UpdateAssignmentEventsRequest.Assignment.Banner, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.display_name (string, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.hbi_data (Casino.HbiData, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.milestone (Casino.AssignmentMilestone, repeated)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.streak_params (Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams, optional)`
- `Casino.UpdateAssignmentEventsRequest.Assignment.type (Casino.UpdateAssignmentEventsRequest.Assignment.Type, optional)`
- `Casino.UpdateAssignmentEventsRequest.added (Casino.UpdateAssignmentEventsRequest.Assignment, repeated)`
- `Casino.UpdateAssignmentEventsRequest.removed (Casino.UpdateAssignmentEventsRequest.Assignment, repeated)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Inferred flow: server pushes assignment definitions/limits/streak steps -> client progress updates -> explicit progress fetch -> reward bundle claim through the shared rewards module.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open daily, weekly and general mission/quest panels separately and mark each tab.
- Progress one visible task through ordinary play, then reopen the task panel.
- Claim one completed task reward if available and mark before/after.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
