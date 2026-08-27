# Loyalty / VIP

Loyalty event tiers, feature multipliers/flags, tutorial/reset acknowledgement and tier/progress state.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **75/100 — substantial live structure**
- Primary live samples: **73** from `LOT-20260827-A`
- Cross-cutting live samples: **385**
- Live endpoints / schema endpoints: **1 / 3**
- Live populated field paths: **38**

## Schema scope

- Proto files: `AppClient.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **7**

- `Casino.AddDciEventRequest.LoyaltyEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureFlags` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureMultipliers` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier` (AppClient.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.UpdateLoyaltyRequest` (AppClient.proto)

## RPC and flow structure

Observed/schema flow: DCI loyalty definition supplies tiers/multipliers/flags -> `UpdateLoyaltyProgram` changes current state -> tutorial/reset acknowledgements update UI state.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.LoyaltyTutorialShown` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.LoyaltyResetShown` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateLoyaltyProgram` | `Casino.UpdateLoyaltyRequest` | `Casino.EmptyResponse` | 73 | 0 | observed-live |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureFlags.feature_id (int32, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureMultipliers.feature_id (int32, optional)`

### Progression / state

- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.points_to_keep_status (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.required_points (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.can_collect_points (bool, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.current_tier_label (string, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.points (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.tiers (Casino.AddDciEventRequest.LoyaltyEvent.Tier, repeated)`
- `Casino.UpdateLoyaltyRequest.can_collect_points (bool, optional)`
- `Casino.UpdateLoyaltyRequest.is_keep_status_reached (bool, optional)`
- `Casino.UpdateLoyaltyRequest.tier (string, optional)`

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- `Casino.UpdateLoyaltyRequest.loyalty_points_balance (int64, optional)`

### Reward / output

- `Casino.AddDciEventRequest.LoyaltyEvent.tutorial_reward (Casino.Reward, optional)`

### Timing / reset / expiry

- `Casino.AddDciEventRequest.LoyaltyEvent.reset_timestamp (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.tier_before_reset (string, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.year_reset (bool, optional)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureFlags.flag (bool, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureMultipliers.multiplier (float, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.feature_flags (Casino.AddDciEventRequest.LoyaltyEvent.FeatureFlags, repeated)`
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.feature_multipliers (Casino.AddDciEventRequest.LoyaltyEvent.FeatureMultipliers, repeated)`
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.label (string, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`

## Live-session coverage

Observed endpoint samples in `LOT-20260827-A`:

- `AppClient.UpdateLoyaltyProgram` — 73 (73 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateShopRequest.product[].reward_data[].reward.loyalty_points` | 153 | 1377 | 7 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.loyalty_points` | 153 | 1224 | 7 | varying-in-session |
| `Casino.VaultUpdateRequest.vault_event.vault.vault_status.additional_benefit[].loyalty_points` | 74 | 74 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.tickets_products[].product[].reward_data[].reward.loyalty_points` | 73 | 803 | 7 | varying-in-session |
| `Casino.UpdateLoyaltyRequest.can_collect_points` | 73 | 73 | 1 | constant-in-session |
| `Casino.UpdateLoyaltyRequest.is_keep_status_reached` | 73 | 73 | 1 | constant-in-session |
| `Casino.UpdateLoyaltyRequest.loyalty_points_balance` | 73 | 73 | 73 | varying-in-session |
| `Casino.UpdateLoyaltyRequest.tier` | 73 | 73 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.reward[].loyalty_points` | 69 | 69 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.rewards_data.reward[].loyalty_points` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.reward[].loyalty_points` | 4 | 4 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.can_collect_points` | 2 | 2 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.loyalty.config_hbi_data[].config_identifier` | 2 | 12 | 7 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.config_hbi_data[].config_type` | 2 | 12 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.config_hbi_data[].config_uuid` | 2 | 10 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.config_hbi_data[].hbi_data.id` | 2 | 12 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.current_tier_label` | 2 | 2 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.loyalty.points` | 2 | 2 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.reset_timestamp` | 2 | 2 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.loyalty.tier_before_reset` | 2 | 2 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].feature_flags[].feature_id` | 2 | 56 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].feature_flags[].flag` | 2 | 56 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].feature_multipliers[].feature_id` | 2 | 350 | 25 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].feature_multipliers[].multiplier` | 2 | 350 | 22 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].label` | 2 | 14 | 7 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].points_to_keep_status` | 2 | 14 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tiers[].required_points` | 2 | 14 | 7 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.tutorial_reward.id` | 2 | 2 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.loyalty.tutorial_reward.loyalty_points` | 2 | 2 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.loyalty.year_reset` | 2 | 2 | 1 | constant-in-session |
| `Casino.BattlePassGetMilestonesResponse.milestone[].deluxe_reward.reward[].loyalty_points` | 2 | 2 | 1 | constant-in-session |
| `Casino.BattlePassGetMilestonesResponse.milestone[].premium_reward.reward[].loyalty_points` | 2 | 2 | 1 | constant-in-session |
| `Casino.BattlePassUpdateRequest.milestone[].deluxe_reward.reward[].loyalty_points` | 1 | 1 | 1 | single-observation |
| `Casino.BattlePassUpdateRequest.milestone[].premium_reward.reward[].loyalty_points` | 1 | 1 | 1 | single-observation |
| `Casino.ContactPointUpdateRequest.is_vip` | 1 | 1 | 1 | single-observation |
| `Casino.GetVaultResponse.vault.vault_status.additional_benefit[].loyalty_points` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.update_shop_request.product[].reward_data[].reward.loyalty_points` | 1 | 9 | 7 | single-observation |
| `Casino.LoginResponse.update_shop_request.shop_promotion.promo_iap[].promo_reward[].reward.loyalty_points` | 1 | 8 | 7 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: DCI loyalty definition supplies tiers/multipliers/flags -> `UpdateLoyaltyProgram` changes current state -> tutorial/reset acknowledgements update UI state.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/sound_loyalty.zpk`
- `sound_loyalty.zpk` provides module-specific static evidence.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open the Loyalty/VIP overview, tier benefits and progress/history screens with markers.
- Trigger one ordinary progress update, then reopen the tier screen.
- Inspect reset/season timing and locked next-tier requirements.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
