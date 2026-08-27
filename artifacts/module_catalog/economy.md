# Currency / Balance / Economy Statistics

Cross-cutting cash/chips/currency balances, bets/costs, prices, quantities and reward outputs observed across gameplay and meta systems.

## Catalog status

- Evidence status: **live-confirmed (cross-cutting/config only)**
- Structural completeness: **65/100 — partial live structure**
- Primary live samples: **0** from `LOT-20260827-A`
- Cross-cutting live samples: **4950**
- Live endpoints / schema endpoints: **0 / 2**
- Live populated field paths: **692**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Definition.proto`, `GameServer.proto`, `Services.proto`, `Vault.proto`
- Services: `GameServer`
- Related message types: **17**

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts` (AppClient.proto)
- `Casino.BalanceUpdate` (Vault.proto)
- `Casino.BankBonus` (AppServer.proto)
- `Casino.BigNumber` (Definition.proto)
- `Casino.Chips` (Definition.proto)
- `Casino.CollectBankBonusResponse` (AppServer.proto)
- `Casino.CollectBankBonusResponse.BankBonus` (AppServer.proto)
- `Casino.IapProduct` (Common.proto)
- `Casino.IapProduct.RewardData` (Common.proto)
- `Casino.LiteModeCollectFreeChipsResponse` (AppServer.proto)
- `Casino.PlayerGetChipsRequest` (GameServer.proto)
- `Casino.PlayerGetChipsResponse` (GameServer.proto)
- `Casino.Reward.CashPrize` (Common.proto)
- `Casino.ShopProduct` (Common.proto)
- `Casino.UpdateBankBonusRequest` (AppServer.proto)
- `Casino.UpdateChipsRequest` (GameServer.proto)
- `Casino.UpdateChipsResponse` (GameServer.proto)

## RPC and flow structure

Cross-cutting inferred flow: login/profile establishes balances -> gameplay/purchase/reward operations consume or produce resources -> response/update messages carry new balances/statistics. This dossier references other modules rather than owning one feature lifecycle.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `GameServer.PlayerUpdateChips` | `Casino.UpdateChipsRequest` | `Casino.UpdateChipsResponse` | 0 | 0 | schema-only |
| `GameServer.PlayerGetChips` | `Casino.PlayerGetChipsRequest` | `Casino.PlayerGetChipsResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.product (Casino.IapProduct, repeated)`
- `Casino.IapProduct.product_id (string, required)`
- `Casino.PlayerGetChipsRequest.user_id (int64, required)`
- `Casino.ShopProduct.id (string, required)`

### Progression / state

- `Casino.CollectBankBonusResponse.status (Casino.CollectBankBonusResponse.Status, required)`
- `Casino.LiteModeCollectFreeChipsResponse.status (Casino.LiteModeCollectFreeChipsResponse.Status, required)`
- `Casino.PlayerGetChipsResponse.status (Casino.PlayerGetChipsResponse.Status, required)`

### Cost / input

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.ticket_color (Casino.LotteryColor, required)`

### Currency / balance

- `Casino.BalanceUpdate.chips (Casino.Chips, required)`
- `Casino.LiteModeCollectFreeChipsResponse.chips (Casino.Chips, optional)`
- `Casino.PlayerGetChipsResponse.chips (Casino.Chips, optional)`
- `Casino.PlayerGetChipsResponse.legacy_chips (int64, optional)`
- `Casino.UpdateChipsRequest.chips_delta (Casino.Chips, optional)`
- `Casino.UpdateChipsRequest.legacy_chips_delta (int64, required)`

### Reward / output

- `Casino.BankBonus.reward (Casino.Reward, repeated)`
- `Casino.CollectBankBonusResponse.BankBonus.reward (Casino.Reward, repeated)`
- `Casino.CollectBankBonusResponse.bank_bonus (Casino.CollectBankBonusResponse.BankBonus, repeated)`
- `Casino.CollectBankBonusResponse.rewards_state_info (Casino.RewardsStateInfo, optional)`
- `Casino.IapProduct.RewardData.reward (Casino.Reward, required)`
- `Casino.IapProduct.bank_bonus_days (int32, optional)`
- `Casino.IapProduct.bank_bonus_type (int32, optional)`
- `Casino.IapProduct.reward_data (Casino.IapProduct.RewardData, repeated)`
- `Casino.UpdateBankBonusRequest.bank_bonus (Casino.BankBonus, repeated)`

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- `Casino.BankBonus.available (bool, optional)`

### Other structural fields

- `Casino.BalanceUpdate.cap_reached (bool, required)`
- `Casino.BalanceUpdate.contribution_ratio (double, optional)`
- `Casino.BalanceUpdate.current_step (int32, required)`
- `Casino.BankBonus.day (uint32, optional)`
- `Casino.BankBonus.days (uint32, optional)`
- `Casino.BankBonus.free_activated (bool, optional)`
- `Casino.BankBonus.type (int32, required)`
- `Casino.BigNumber.value (bytes, required)`
- `Casino.Chips.value (bytes, required)`
- `Casino.CollectBankBonusResponse.BankBonus.day_collected (int32, required)`
- `Casino.CollectBankBonusResponse.BankBonus.type (int32, required)`
- `Casino.CollectBankBonusResponse.error_code (int32, optional)`
- `Casino.IapProduct.RewardData.big_value_for_money (Casino.BigNumber, optional)`
- `Casino.IapProduct.RewardData.share (double, optional)`
- `Casino.IapProduct.RewardData.value_for_money (int64, optional)`
- `Casino.IapProduct.crossout (bool, optional)`
- `Casino.IapProduct.custom_fields (Casino.CustomFields, optional)`
- `Casino.IapProduct.sale (double, optional)`
- `Casino.IapProduct.tag (int32, repeated)`
- `Casino.LiteModeCollectFreeChipsResponse.error_code (int32, optional)`
- `Casino.Reward.CashPrize.value (int64, required)`
- `Casino.ShopProduct.tag (int32, repeated)`
- `Casino.UpdateBankBonusRequest.update_source (string, optional)`
- `Casino.UpdateChipsResponse.valid (bool, required)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.SlotsProto.UserList.user[].cash.value` | 1315 | 1317 | 1064 | varying-in-session |
| `Casino.SlotsProto.UserList.user[].legacy_cash` | 1315 | 1317 | 1064 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.cash.value` | 633 | 633 | 585 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.cash.value` | 633 | 633 | 585 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.legacy_cash` | 633 | 633 | 585 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.legacy_cash` | 633 | 633 | 585 | varying-in-session |
| `Casino.SlotsProto.SpinRequest.bet` | 588 | 588 | 4 | varying-in-session |
| `Casino.SlotsProto.SpinRequest.max_bet_btn` | 588 | 588 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].type` | 587 | 1174 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.levels_amount` | 587 | 587 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.target_level` | 587 | 587 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.value` | 587 | 587 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].type` | 587 | 1129 | 2 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.cap_reached` | 410 | 410 | 2 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.chips.value` | 410 | 410 | 410 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.current_step` | 410 | 410 | 11 | varying-in-session |
| `Casino.VaultProgressUpdateRequest.balance_update.contribution_ratio` | 409 | 409 | 6 | varying-in-session |
| `Casino.LotteryTossRequest.data.ticket_color` | 346 | 346 | 4 | varying-in-session |
| `Casino.LotteryTossRequest.data.ticket_number` | 346 | 346 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.data.ticket_color` | 346 | 346 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.data.ticket_number` | 346 | 346 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.state.free_ticket_state.progress` | 346 | 346 | 7 | varying-in-session |
| `Casino.LotteryTossResponse.state.free_ticket_state.threshold` | 346 | 346 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.state.free_ticket_state.ticket_color` | 346 | 346 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.state.puzzle_board[].reward.big_chips_delta.value` | 346 | 1384 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.state.puzzle_board[].reward.chips_delta` | 346 | 1384 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.state.ticket_balance[].amount` | 346 | 1384 | 125 | varying-in-session |
| `Casino.LotteryTossResponse.state.ticket_balance[].id` | 346 | 1384 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].type` | 333 | 666 | 2 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].level.levels_amount` | 333 | 333 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].level.target_level` | 333 | 333 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].level.value` | 333 | 333 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].type` | 333 | 777 | 2 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.reward[].big_chips_delta.value` | 318 | 318 | 42 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.reward[].chips_delta` | 318 | 318 | 42 | varying-in-session |
| `Casino.UpdateShopRequest.product[].bank_bonus_days` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].bank_bonus_type` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].big_value_for_money.value` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.big_chips_delta.value` | 153 | 918 | 6 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.charms_trade_token_delta` | 153 | 1224 | 7 | varying-in-session |
| … | | | | 662 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Cross-cutting inferred flow: login/profile establishes balances -> gameplay/purchase/reward operations consume or produce resources -> response/update messages carry new balances/statistics. This dossier references other modules rather than owning one feature lifecycle.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_dailybonus_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_liveops_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tile_shop_v2_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tile_shop_v3_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles_reskinned_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc2_1_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc2_2_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc_1_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_vault2_anim_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_vault2_sku_hc_2_etc2.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Mark visible balances before and after a spin, reward claim and shop preview in one marked session.
- Open all currency/balance detail popups and note which screen each balance belongs to.
- Avoid deliberate spending solely for research; use naturally intended actions.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
