# Missions / Quests / Daily-Weekly Tasks

Generic assignment events and progress/claim structure, distinct from Battle Pass, MiniPass, Adventure and Elites-specific missions.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **85/100 — substantial live structure**
- Primary live samples: **83** from `LOT-20260827-A`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **3 / 3**
- Live populated field paths: **49**

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
| `AppServer.GetAssignmentProgress` | `Casino.GetAssignmentProgressRequest` | `Casino.GetAssignmentProgressResponse` | 4 | 4 | observed-live |
| `AppClient.UpdateAssignmentEvents` | `Casino.UpdateAssignmentEventsRequest` | `Casino.EmptyResponse` | 65 | 0 | observed-live |
| `AppClient.UpdateAssignmentProgress` | `Casino.UpdateAssignmentProgressRequest` | `Casino.EmptyResponse` | 10 | 0 | observed-live |

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

Observed endpoint samples in `LOT-20260827-A`:

- `AppClient.UpdateAssignmentEvents` — 65 (65 request, 0 response)
- `AppClient.UpdateAssignmentProgress` — 10 (10 request, 0 response)
- `AppServer.GetAssignmentProgress` — 8 (4 request, 4 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateAssignmentEventsRequest.added[].action_type` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.cooldown` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.cta_text` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.fullscreen_url[]` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.lobby_tile` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.newsfeed_url[]` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.scenario[].display_priority` | 65 | 303 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.scenario[].type` | 65 | 303 | 3 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.template_id` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].banner.type` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].config_hbi_data[].config_identifier` | 65 | 202 | 5 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].config_hbi_data[].config_type` | 65 | 202 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].config_hbi_data[].hbi_data.id` | 65 | 202 | 3 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].display_name` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].event_id` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].expire` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].hbi_data.id` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].requirement.value` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].id` | 65 | 101 | 2 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].status` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].progress.value` | 65 | 101 | 49 | varying-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].type` | 65 | 101 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box.box_id` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box.box_type` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box.raffle_id` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box.source` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box.theme_id` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box.type` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box_info.box_id` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box_info.box_type` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box_info.event_type` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box_info.highest_guaranteed_rarity` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box_info.highest_guaranteed_rarity_items_count` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].collectibles_box_info.items_count` | 52 | 52 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].limitation[].type` | 49 | 49 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].limitation[].value.value_strings[]` | 49 | 49 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].inventory_delta.amount` | 49 | 49 | 1 | constant-in-session |
| `Casino.UpdateAssignmentEventsRequest.added[].milestone[].reward[].inventory_delta.id` | 49 | 49 | 1 | constant-in-session |
| `Casino.UpdateAssignmentProgressRequest.progress.event_id` | 10 | 10 | 1 | constant-in-session |
| `Casino.UpdateAssignmentProgressRequest.progress.milestone[].requirement.value` | 10 | 10 | 1 | constant-in-session |
| … | | | | 9 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

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
