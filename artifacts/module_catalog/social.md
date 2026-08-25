# Social Recommendations / Invites

Experimental invite tokens and cross-player recommendation/invite flows outside clubs and ordinary friends.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 2**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Common.proto`, `Services.proto`
- Services: `ExperimentalSocialRecommendationsServer`
- Related message types: **5**

- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.Experimental.SocialRecommendations` (Common.proto)
- `Casino.Experimental.SocialRecommendations.GetInviteTokenResponse` (Common.proto)
- `Casino.Experimental.SocialRecommendations.InviteTokenUsedRequest` (Common.proto)

## RPC and flow structure

Schema flow: request invite token -> share/use token externally -> server records token usage and returns acknowledgement.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `ExperimentalSocialRecommendationsServer.GetInviteToken` | `Casino.EmptyRequest` | `Casino.Experimental.SocialRecommendations.GetInviteTokenResponse` | 0 | 0 | schema-only |
| `ExperimentalSocialRecommendationsServer.InviteTokenUsed` | `Casino.Experimental.SocialRecommendations.InviteTokenUsedRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Progression / state

- `Casino.Experimental.SocialRecommendations.GetInviteTokenResponse.status (Casino.Experimental.SocialRecommendations.GetInviteTokenResponse.Status, required)`

### Cost / input

- `Casino.Experimental.SocialRecommendations.GetInviteTokenResponse.token (string, optional)`
- `Casino.Experimental.SocialRecommendations.InviteTokenUsedRequest.token (string, required)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.Experimental.SocialRecommendations.GetInviteTokenResponse.error_code (int32, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: request invite token -> share/use token externally -> server records token usage and returns acknowledgement.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open any invite/recommendation/referral screen with a marker.
- Do not publish tokens; only inspect local structure and normal UI state.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
