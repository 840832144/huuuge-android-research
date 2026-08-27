# Contact Point / Engagement Surface

Contact-point event updates and first-time interaction acknowledgement for engagement surfaces.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **60/100 — partial live structure**
- Primary live samples: **1** from `LOT-20260827-A`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **1 / 2**
- Live populated field paths: **2**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `ContactPoint.proto`, `Services.proto`
- Services: `AppServer`, `ContactPointClient`
- Related message types: **4**

- `Casino.AddDciEventRequest.ContactPointEvent` (AppClient.proto)
- `Casino.ContactPointFtueInteractionRequest` (AppServer.proto)
- `Casino.ContactPointUpdateRequest` (ContactPoint.proto)
- `Casino.EmptyResponse` (Services.proto)

## RPC and flow structure

Schema flow: DCI contact-point event/config -> client update renders the surface -> FTUE interaction acknowledgement records first use.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.ContactPointFtueInteraction` | `Casino.ContactPointFtueInteractionRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ContactPointClient.ContactPointUpdate` | `Casino.ContactPointUpdateRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |

## Structural fields

### Entity identifiers

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Progression / state

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.AddDciEventRequest.ContactPointEvent.hmac (string, required)`
- `Casino.AddDciEventRequest.ContactPointEvent.is_vip (bool, required)`
- `Casino.AddDciEventRequest.ContactPointEvent.show_ftue (bool, optional)`
- `Casino.ContactPointFtueInteractionRequest.message_read (bool, required)`
- `Casino.ContactPointUpdateRequest.hmac (string, optional)`
- `Casino.ContactPointUpdateRequest.is_vip (bool, optional)`

## Live-session coverage

Observed endpoint samples in `LOT-20260827-A`:

- `ContactPointClient.ContactPointUpdate` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.ContactPointUpdateRequest.hmac` | 1 | 1 | 1 | single-observation |
| `Casino.ContactPointUpdateRequest.is_vip` | 1 | 1 | 1 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: DCI contact-point event/config -> client update renders the surface -> FTUE interaction acknowledgement records first use.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open any inbox/contact/help/engagement surface that resembles a contact point and mark it.
- Complete only a normal first-use tutorial interaction if naturally presented.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
