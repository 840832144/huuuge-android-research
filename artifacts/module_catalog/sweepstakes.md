# Sweepstakes / Scheduled Draws

Open/completed sweepstakes draws, ticket updates, entry, winner publishing consent and tutorial state.

## Catalog status

- Evidence status: **live-confirmed (cross-cutting/config only)**
- Structural completeness: **50/100 — schema skeleton**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **1**
- Live endpoints / schema endpoints: **0 / 6**
- Live populated field paths: **2**

## Schema scope

- Proto files: `Common.proto`, `Services.proto`, `Sweepstakes.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **14**

- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.Reward.SweepstakesTickets` (Common.proto)
- `Casino.SweepstakesCompletedDraw` (Sweepstakes.proto)
- `Casino.SweepstakesGetCompletedDrawsResponse` (Sweepstakes.proto)
- `Casino.SweepstakesJoinDrawRequest` (Sweepstakes.proto)
- `Casino.SweepstakesJoinDrawResponse` (Sweepstakes.proto)
- `Casino.SweepstakesOpenDraw` (Sweepstakes.proto)
- `Casino.SweepstakesOpenDraw.DrawReward` (Sweepstakes.proto)
- `Casino.SweepstakesTicketsUpdateRequest` (Sweepstakes.proto)
- `Casino.SweepstakesTutorialCompletedResponse` (Sweepstakes.proto)
- `Casino.SweepstakesUpdatePublishWinnerDataConsentRequest` (Sweepstakes.proto)
- `Casino.SweepstakesUpdatePublishWinnerDataConsentResponse` (Sweepstakes.proto)
- `Casino.SweepstakesUpdateRequest` (Sweepstakes.proto)

## RPC and flow structure

Schema flow: update publishes open draw and tickets -> join draw consumes entry -> completed-draw fetch returns outcome/reward -> consent/tutorial endpoints update presentation state.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.SweepstakesGetCompletedDraws` | `Casino.EmptyRequest` | `Casino.SweepstakesGetCompletedDrawsResponse` | 0 | 0 | schema-only |
| `AppServer.SweepstakesJoinDraw` | `Casino.SweepstakesJoinDrawRequest` | `Casino.SweepstakesJoinDrawResponse` | 0 | 0 | schema-only |
| `AppServer.SweepstakesUpdatePublishWinnerDataConsent` | `Casino.SweepstakesUpdatePublishWinnerDataConsentRequest` | `Casino.SweepstakesUpdatePublishWinnerDataConsentResponse` | 0 | 0 | schema-only |
| `AppServer.SweepstakesTutorialCompleted` | `Casino.EmptyRequest` | `Casino.SweepstakesTutorialCompletedResponse` | 0 | 0 | schema-only |
| `AppClient.SweepstakesUpdate` | `Casino.SweepstakesUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.SweepstakesTicketsUpdate` | `Casino.SweepstakesTicketsUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.SweepstakesCompletedDraw.id (string, required)`
- `Casino.SweepstakesJoinDrawRequest.draw_id (string, required)`
- `Casino.SweepstakesOpenDraw.id (string, required)`
- `Casino.SweepstakesUpdatePublishWinnerDataConsentRequest.draw_id (string, required)`

### Progression / state

- `Casino.SweepstakesCompletedDraw.status (Casino.SweepstakesCompletedDraw.Status, required)`
- `Casino.SweepstakesGetCompletedDrawsResponse.status (Casino.SweepstakesGetCompletedDrawsResponse.Status, required)`
- `Casino.SweepstakesJoinDrawResponse.status (Casino.SweepstakesJoinDrawResponse.Status, required)`
- `Casino.SweepstakesTutorialCompletedResponse.status (Casino.SweepstakesTutorialCompletedResponse.Status, required)`
- `Casino.SweepstakesUpdatePublishWinnerDataConsentResponse.status (Casino.SweepstakesUpdatePublishWinnerDataConsentResponse.Status, required)`
- `Casino.SweepstakesUpdateRequest.tutorial_completed (bool, optional)`

### Cost / input

- `Casino.Reward.SweepstakesTickets.amount (int64, required)`
- `Casino.SweepstakesOpenDraw.ticket_balance (int32, required)`
- `Casino.SweepstakesTicketsUpdateRequest.tickets_gained (int32, required)`
- `Casino.SweepstakesTutorialCompletedResponse.tickets_gained (int32, optional)`

### Currency / balance

- `Casino.SweepstakesTicketsUpdateRequest.balance (int64, required)`

### Reward / output

- `Casino.SweepstakesCompletedDraw.claimed_reward (Casino.Reward, repeated)`
- `Casino.SweepstakesCompletedDraw.prize_pool (Casino.Reward, repeated)`
- `Casino.SweepstakesCompletedDraw.winner (Casino.Avatar, repeated)`
- `Casino.SweepstakesOpenDraw.DrawReward.cash_reward (Casino.Reward, required)`
- `Casino.SweepstakesOpenDraw.DrawReward.ingame_reward (Casino.Reward, repeated)`
- `Casino.SweepstakesOpenDraw.draw_reward (Casino.SweepstakesOpenDraw.DrawReward, repeated)`
- `Casino.SweepstakesOpenDraw.publish_winner_data_consent (bool, optional)`

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- `Casino.SweepstakesOpenDraw.ticket_limit (int32, required)`
- `Casino.SweepstakesUpdateRequest.available (bool, required)`

### Other structural fields

- `Casino.SweepstakesCompletedDraw.draw_date (int64, required)`
- `Casino.SweepstakesGetCompletedDrawsResponse.draws (Casino.SweepstakesCompletedDraw, repeated)`
- `Casino.SweepstakesGetCompletedDrawsResponse.error_code (int32, optional)`
- `Casino.SweepstakesJoinDrawResponse.error_code (int32, optional)`
- `Casino.SweepstakesOpenDraw.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.SweepstakesOpenDraw.draw_date (int64, required)`
- `Casino.SweepstakesOpenDraw.hbi_data (Casino.HbiData, optional)`
- `Casino.SweepstakesOpenDraw.joined (bool, required)`
- `Casino.SweepstakesOpenDraw.start_date (int64, required)`
- `Casino.SweepstakesTicketsUpdateRequest.source (Casino.SweepstakesTicketsUpdateRequest.TicketsSource, required)`
- `Casino.SweepstakesTutorialCompletedResponse.error_code (int32, optional)`
- `Casino.SweepstakesUpdatePublishWinnerDataConsentRequest.consent (bool, required)`
- `Casino.SweepstakesUpdatePublishWinnerDataConsentResponse.error_code (int32, optional)`
- `Casino.SweepstakesUpdateRequest.open_draw (Casino.SweepstakesOpenDraw, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.LoginResponse.sweepstakes_update.available` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.sweepstakes_update.tutorial_completed` | 1 | 1 | 1 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: update publishes open draw and tickets -> join draw consumes entry -> completed-draw fetch returns outcome/reward -> consent/tutorial endpoints update presentation state.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open sweepstakes/current draw, ticket balance and completed-draw/history screens with markers.
- Inspect entry requirement and reward tiers.
- Join one naturally available draw and revisit history after completion when possible.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
