# Personal Awards

Game-host-managed personal award progress and progress retrieval.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 2**
- Live populated field paths: **0**

## Schema scope

- Proto files: `PersonalAwards.proto`, `Services.proto`
- Services: `GameHost`
- Related message types: **18**

- `Casino.PersonalAwardsProto` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.GetProgressRequest` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.GetProgressResponse` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalAward` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalAwardList` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalAwardList.PersonalAwardData` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalBucket` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalBucketAward` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalCounter` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalCounterList` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalCounterList.PersonalCounterData` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalFlag` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalFlagList` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalState` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalStateList` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.PersonalStateList.PersonalStateData` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.UpdateProgressRequest` (PersonalAwards.proto)
- `Casino.PersonalAwardsProto.UpdateProgressResponse` (PersonalAwards.proto)

## RPC and flow structure

Schema flow: game host retrieves current personal-award progress -> qualifying game actions update progress -> response returns normalized award state.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `GameHost.UpdatePersonalAwardsProgress` | `Casino.PersonalAwardsProto.UpdateProgressRequest` | `Casino.PersonalAwardsProto.UpdateProgressResponse` | 0 | 0 | schema-only |
| `GameHost.GetPersonalAwardsProgress` | `Casino.PersonalAwardsProto.GetProgressRequest` | `Casino.PersonalAwardsProto.GetProgressResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.PersonalAwardsProto.GetProgressRequest.slot_id (string, required)`
- `Casino.PersonalAwardsProto.PersonalAward.id (int32, required)`
- `Casino.PersonalAwardsProto.PersonalAwardList.PersonalAwardData.key (uint64, required)`
- `Casino.PersonalAwardsProto.PersonalAwardList.id (int32, required)`
- `Casino.PersonalAwardsProto.PersonalBucketAward.id (int32, required)`
- `Casino.PersonalAwardsProto.PersonalCounter.id (int32, required)`
- `Casino.PersonalAwardsProto.PersonalCounterList.PersonalCounterData.key (uint64, required)`
- `Casino.PersonalAwardsProto.PersonalCounterList.id (uint32, required)`
- `Casino.PersonalAwardsProto.PersonalFlag.id (uint32, required)`
- `Casino.PersonalAwardsProto.PersonalFlagList.id (uint32, required)`
- `Casino.PersonalAwardsProto.PersonalState.id (int32, required)`
- `Casino.PersonalAwardsProto.PersonalStateList.PersonalStateData.key (uint64, required)`
- `Casino.PersonalAwardsProto.PersonalStateList.id (int32, required)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.slot_id (string, required)`

### Progression / state

- `Casino.PersonalAwardsProto.GetProgressResponse.counters (Casino.PersonalAwardsProto.PersonalCounter, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.counters_list (Casino.PersonalAwardsProto.PersonalCounterList, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.states (Casino.PersonalAwardsProto.PersonalState, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.states_list (Casino.PersonalAwardsProto.PersonalStateList, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.status (Casino.PersonalAwardsProto.GetProgressResponse.Status, required)`
- `Casino.PersonalAwardsProto.PersonalAward.progress (int32, required)`
- `Casino.PersonalAwardsProto.PersonalAwardList.PersonalAwardData.progress (int32, required)`
- `Casino.PersonalAwardsProto.PersonalBucket.progress (uint32, required)`
- `Casino.PersonalAwardsProto.PersonalCounter.max_progress (int32, optional)`
- `Casino.PersonalAwardsProto.PersonalCounter.progress (int32, required)`
- `Casino.PersonalAwardsProto.PersonalCounterList.PersonalCounterData.max_progress (uint32, optional)`
- `Casino.PersonalAwardsProto.PersonalCounterList.PersonalCounterData.progress (uint32, required)`
- `Casino.PersonalAwardsProto.PersonalCounterList.counters (Casino.PersonalAwardsProto.PersonalCounterList.PersonalCounterData, repeated)`
- `Casino.PersonalAwardsProto.PersonalStateList.states (Casino.PersonalAwardsProto.PersonalStateList.PersonalStateData, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.counters (Casino.PersonalAwardsProto.PersonalCounter, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.counters_list (Casino.PersonalAwardsProto.PersonalCounterList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.states (Casino.PersonalAwardsProto.PersonalState, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.states_list (Casino.PersonalAwardsProto.PersonalStateList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressResponse.status (Casino.PersonalAwardsProto.UpdateProgressResponse.Status, required)`

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.PersonalAwardsProto.GetProgressResponse.awards (Casino.PersonalAwardsProto.PersonalAward, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.awards_list (Casino.PersonalAwardsProto.PersonalAwardList, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.bucket_awards (Casino.PersonalAwardsProto.PersonalBucketAward, repeated)`
- `Casino.PersonalAwardsProto.PersonalAwardList.awards (Casino.PersonalAwardsProto.PersonalAwardList.PersonalAwardData, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.awards (Casino.PersonalAwardsProto.PersonalAward, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.awards_list (Casino.PersonalAwardsProto.PersonalAwardList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.bucket_awards (Casino.PersonalAwardsProto.PersonalBucketAward, repeated)`

### Timing / reset / expiry

- `Casino.PersonalAwardsProto.UpdateProgressRequest.expire_time_seconds (uint32, optional)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.PersonalAwardsProto.GetProgressResponse.error_code (int32, optional)`
- `Casino.PersonalAwardsProto.GetProgressResponse.flags (Casino.PersonalAwardsProto.PersonalFlag, repeated)`
- `Casino.PersonalAwardsProto.GetProgressResponse.flags_list (Casino.PersonalAwardsProto.PersonalFlagList, repeated)`
- `Casino.PersonalAwardsProto.PersonalAward.contribution (Casino.Chips, optional)`
- `Casino.PersonalAwardsProto.PersonalAward.legacy_contribution (int64, required)`
- `Casino.PersonalAwardsProto.PersonalAwardList.PersonalAwardData.contribution (Casino.Chips, optional)`
- `Casino.PersonalAwardsProto.PersonalAwardList.PersonalAwardData.legacy_contribution (int64, required)`
- `Casino.PersonalAwardsProto.PersonalBucket.contribution (Casino.Chips, optional)`
- `Casino.PersonalAwardsProto.PersonalBucket.legacy_contribution (uint64, required)`
- `Casino.PersonalAwardsProto.PersonalBucketAward.buckets (Casino.PersonalAwardsProto.PersonalBucket, repeated)`
- `Casino.PersonalAwardsProto.PersonalCounter.enabled (bool, required)`
- `Casino.PersonalAwardsProto.PersonalCounterList.PersonalCounterData.enabled (bool, required)`
- `Casino.PersonalAwardsProto.PersonalFlagList.keys (uint64, repeated)`
- `Casino.PersonalAwardsProto.PersonalState.value (int64, optional)`
- `Casino.PersonalAwardsProto.PersonalStateList.PersonalStateData.value (int64, required)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.flags (Casino.PersonalAwardsProto.PersonalFlag, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressRequest.flags_list (Casino.PersonalAwardsProto.PersonalFlagList, repeated)`
- `Casino.PersonalAwardsProto.UpdateProgressResponse.error_code (int32, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: game host retrieves current personal-award progress -> qualifying game actions update progress -> response returns normalized award state.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Locate and open personal-award/achievement progress screens with markers.
- Play one qualifying game action and revisit progress.
- Open any award claim/detail popup that appears naturally.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
