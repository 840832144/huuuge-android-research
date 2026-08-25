# Vault

Vault event availability, segment/minimum-level gating, progress, multipliers, benefits/promotions and balance updates.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **65/100 — partial live structure**
- Primary live samples: **5** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **1 / 4**
- Live populated field paths: **8**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`, `Vault.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **18**

- `Casino.AddDciEventRequest.VaultEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.VaultPromoEvent` (AppClient.proto)
- `Casino.BalanceUpdate` (Vault.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.GetVaultResponse` (Vault.proto)
- `Casino.LoginResponse.MissedInfo.VaultMissedInfo` (AppServer.proto)
- `Casino.TierUpdate` (Vault.proto)
- `Casino.Vault` (Common.proto)
- `Casino.Vault.VaultStatus` (Common.proto)
- `Casino.VaultBenefitPromo` (Common.proto)
- `Casino.VaultEvent` (Vault.proto)
- `Casino.VaultEvent.VaultBenefitPromoConfig` (Vault.proto)
- `Casino.VaultEvent.VaultPromoConfig` (Vault.proto)
- `Casino.VaultMultipliers` (Common.proto)
- `Casino.VaultProgressUpdateRequest` (Vault.proto)
- `Casino.VaultPromo` (Common.proto)
- `Casino.VaultUpdateRequest` (Vault.proto)

## RPC and flow structure

Observed/schema flow: DCI/static event definition -> `VaultUpdate` sets availability/config -> `VaultProgressUpdate` and balance updates change progress -> `GetVault` returns current state -> config-read acknowledges the new configuration.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.GetVault` | `Casino.EmptyRequest` | `Casino.GetVaultResponse` | 0 | 0 | schema-only |
| `AppServer.NewVaultConfigRead` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.VaultUpdate` | `Casino.VaultUpdateRequest` | `Casino.EmptyResponse` | 5 | 0 | observed-live |
| `AppClient.VaultProgressUpdate` | `Casino.VaultProgressUpdateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.LoginResponse.MissedInfo.VaultMissedInfo.vault_id (int64, required)`
- `Casino.Vault.product_id (string, optional)`
- `Casino.Vault.segment_id (int64, optional)`
- `Casino.Vault.vault_id (int64, optional)`
- `Casino.VaultEvent.event_id (int64, required)`
- `Casino.VaultPromo.product_id (string, optional)`

### Progression / state

- `Casino.GetVaultResponse.status (Casino.GetVaultResponse.Status, required)`
- `Casino.TierUpdate.steps_count (int32, required)`
- `Casino.TierUpdate.tier_start_level (int64, required)`
- `Casino.Vault.VaultStatus.steps_count (int32, required)`
- `Casino.Vault.VaultStatus.tier_start_level (int32, required)`
- `Casino.Vault.state (Casino.Vault.State, required)`
- `Casino.Vault.vault_status (Casino.Vault.VaultStatus, optional)`
- `Casino.VaultProgressUpdateRequest.tier_update (Casino.TierUpdate, optional)`

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- `Casino.BalanceUpdate.chips (Casino.Chips, required)`
- `Casino.Vault.VaultStatus.chips (Casino.Chips, required)`
- `Casino.VaultMultipliers.chips_multiplier (double, optional)`
- `Casino.VaultProgressUpdateRequest.balance_update (Casino.BalanceUpdate, required)`

### Reward / output

- `Casino.LoginResponse.MissedInfo.VaultMissedInfo.reward (Casino.Reward, repeated)`

### Timing / reset / expiry

- `Casino.VaultEvent.VaultBenefitPromoConfig.expire (int64, required)`
- `Casino.VaultEvent.VaultPromoConfig.expire (int64, required)`

### Segment / eligibility / limit

- `Casino.TierUpdate.cap (Casino.Chips, required)`
- `Casino.Vault.VaultStatus.cap (Casino.Chips, required)`
- `Casino.Vault.minimum_level (int32, optional)`

### Other structural fields

- `Casino.AddDciEventRequest.VaultEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.VaultEvent.vault (Casino.Vault, required)`
- `Casino.AddDciEventRequest.VaultPromoEvent.benefit_promo (Casino.VaultBenefitPromo, optional)`
- `Casino.AddDciEventRequest.VaultPromoEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.VaultPromoEvent.vault_promo (Casino.VaultPromo, optional)`
- `Casino.BalanceUpdate.cap_reached (bool, required)`
- `Casino.BalanceUpdate.contribution_ratio (double, optional)`
- `Casino.BalanceUpdate.current_step (int32, required)`
- `Casino.GetVaultResponse.error_code (int32, optional)`
- `Casino.GetVaultResponse.vault (Casino.Vault, optional)`
- `Casino.GetVaultResponse.vault_benefit_promo (Casino.VaultBenefitPromo, optional)`
- `Casino.GetVaultResponse.vault_promo (Casino.VaultPromo, optional)`
- `Casino.TierUpdate.seed (Casino.Chips, required)`
- `Casino.Vault.VaultStatus.additional_benefit (Casino.Reward, repeated)`
- `Casino.Vault.VaultStatus.contribution_ratio (double, optional)`
- `Casino.Vault.VaultStatus.current_step (int32, required)`
- `Casino.Vault.VaultStatus.is_new_config (bool, optional)`
- `Casino.Vault.multipliers (Casino.VaultMultipliers, optional)`
- `Casino.Vault.seed (Casino.Chips, optional)`
- `Casino.VaultBenefitPromo.additional_benefit (Casino.Reward, repeated)`
- `Casino.VaultBenefitPromo.label (string, optional)`
- `Casino.VaultBenefitPromo.type (int32, required)`
- `Casino.VaultEvent.VaultBenefitPromoConfig.benefit_promo (Casino.VaultBenefitPromo, required)`
- `Casino.VaultEvent.VaultBenefitPromoConfig.config_hbi_data (Casino.ConfigHbiData, required)`
- `Casino.VaultEvent.VaultPromoConfig.config_hbi_data (Casino.ConfigHbiData, required)`
- `Casino.VaultEvent.VaultPromoConfig.vault_promo (Casino.VaultPromo, required)`
- `Casino.VaultEvent.art_config (Casino.Art, optional)`
- `Casino.VaultEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.VaultEvent.vault (Casino.Vault, required)`
- `Casino.VaultEvent.vault_benefit_promo_config (Casino.VaultEvent.VaultBenefitPromoConfig, optional)`
- `Casino.VaultEvent.vault_promo_config (Casino.VaultEvent.VaultPromoConfig, optional)`
- `Casino.VaultMultipliers.contribution_multiplier (double, optional)`
- `Casino.VaultMultipliers.seed_multiplier (double, optional)`
- `Casino.VaultPromo.multipliers (Casino.VaultMultipliers, optional)`
- `Casino.VaultPromo.type (int32, required)`
- `Casino.VaultUpdateRequest.is_restricted_mode (bool, optional)`
- `Casino.VaultUpdateRequest.vault_event (Casino.VaultEvent, optional)`

## Live-session coverage

Observed endpoint samples in `20260825_182300`:

- `AppClient.VaultUpdate` — 5 (5 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.VaultUpdateRequest.is_restricted_mode` | 5 | 5 | 1 | constant-in-session |
| `Casino.VaultUpdateRequest.vault_event.config_hbi_data[].config_identifier_str` | 5 | 10 | 2 | varying-in-session |
| `Casino.VaultUpdateRequest.vault_event.config_hbi_data[].config_type` | 5 | 10 | 2 | varying-in-session |
| `Casino.VaultUpdateRequest.vault_event.config_hbi_data[].hbi_data.id` | 5 | 10 | 2 | varying-in-session |
| `Casino.VaultUpdateRequest.vault_event.event_id` | 5 | 5 | 1 | constant-in-session |
| `Casino.VaultUpdateRequest.vault_event.vault.minimum_level` | 5 | 5 | 1 | constant-in-session |
| `Casino.VaultUpdateRequest.vault_event.vault.segment_id` | 5 | 5 | 1 | constant-in-session |
| `Casino.VaultUpdateRequest.vault_event.vault.state` | 5 | 5 | 1 | constant-in-session |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260825_182300`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: DCI/static event definition -> `VaultUpdate` sets availability/config -> `VaultProgressUpdate` and balance updates change progress -> `GetVault` returns current state -> config-read acknowledges the new configuration.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_vault2_anim_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_vault2_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/sound_vault.zpk`
- Vault-specific atlas, animation and sound ZPKs confirm a dedicated client module.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Vault main/detail/help screens and mark each view.
- Perform ordinary actions that add Vault progress, then reopen Vault.
- If a claim/open action is naturally available, mark before/after without changing purchase state.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
