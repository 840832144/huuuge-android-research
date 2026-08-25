# Charms / Trading

Charms collections, packs/boxes, milestones, time-based state, duplicate/trade tokens, requests/exchanges and tutorials.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **65/100 — partial live structure**
- Primary live samples: **2** from `20260825_182300`
- Cross-cutting live samples: **15**
- Live endpoints / schema endpoints: **1 / 12**
- Live populated field paths: **7**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **43**

- `Casino.AddDciEventRequest.CharmsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.RewardPromo` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.StarsPerRarity` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.Trading` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.Tutorial` (AppClient.proto)
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial` (AppClient.proto)
- `Casino.CharmsBoxOpenAllRequest` (AppServer.proto)
- `Casino.CharmsBoxOpenAllResponse` (AppServer.proto)
- `Casino.CharmsMilestone` (Common.proto)
- `Casino.CharmsPacksInfo` (Common.proto)
- `Casino.CharmsPacksInfo.BoxTypeInfo` (Common.proto)
- `Casino.CharmsPastCollection` (Common.proto)
- `Casino.CharmsPastCollectionsResponse` (AppServer.proto)
- `Casino.CharmsProgressData` (AppClient.proto)
- `Casino.CharmsProgressData.CharmsTradingInfo` (AppClient.proto)
- `Casino.CharmsResetNewBadgeRequest` (AppServer.proto)
- `Casino.CharmsResetRequest` (AppServer.proto)
- `Casino.CharmsResetResponse` (AppServer.proto)
- `Casino.CharmsStatistics` (Common.proto)
- `Casino.CharmsThemeIteration` (Common.proto)
- `Casino.CharmsThemeReward` (Common.proto)
- `Casino.CharmsTradeActionRequest` (AppServer.proto)
- `Casino.CharmsTradeActionResponse` (AppServer.proto)
- `Casino.CharmsTradeAvatarRequestRecord` (AppServer.proto)
- `Casino.CharmsTradeExchangeExecuteRequest` (AppServer.proto)
- `Casino.CharmsTradeExchangeExecuteResponse` (AppServer.proto)
- `Casino.CharmsTradeRequestListFetchRequest` (AppServer.proto)
- `Casino.CharmsTradeRequestListFetchResponse` (AppServer.proto)
- `Casino.CharmsTutorialProgressRequest` (AppServer.proto)
- `Casino.CharmsTutorialProgressResponse` (AppServer.proto)
- `Casino.CollectiblesBoxData.CharmsBoxData` (Common.proto)
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData` (Common.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.TimeBasedCharmItem` (Common.proto)
- `Casino.TimeBasedCharmsMainReward` (Common.proto)
- `Casino.TimeBasedCharmsMilestoneReward` (Common.proto)
- `Casino.TimeBasedCharmsStateRequest` (AppServer.proto)
- `Casino.TimeBasedCharmsStateResponse` (AppServer.proto)
- `Casino.UpdateCharmsProgressRequest` (AppClient.proto)

## RPC and flow structure

Observed/schema flow: event/config update -> state/progress update -> box/packs collection -> duplicate/token accumulation -> trade request/list/exchange -> reset/tutorial/past-collection flows.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.CharmsReset` | `Casino.CharmsResetRequest` | `Casino.CharmsResetResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsBoxOpenAll` | `Casino.CharmsBoxOpenAllRequest` | `Casino.CharmsBoxOpenAllResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsTradeAction` | `Casino.CharmsTradeActionRequest` | `Casino.CharmsTradeActionResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsTradeRequestListFetch` | `Casino.CharmsTradeRequestListFetchRequest` | `Casino.CharmsTradeRequestListFetchResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsTradeExchangeExecute` | `Casino.CharmsTradeExchangeExecuteRequest` | `Casino.CharmsTradeExchangeExecuteResponse` | 0 | 0 | schema-only |
| `AppServer.TimeBasedCharmsState` | `Casino.TimeBasedCharmsStateRequest` | `Casino.TimeBasedCharmsStateResponse` | 0 | 0 | schema-only |
| `AppServer.TimeBasedCharmsTutorialProgress` | `Casino.CharmsTutorialProgressRequest` | `Casino.CharmsTutorialProgressResponse` | 0 | 0 | schema-only |
| `AppServer.TimeBasedCharmsReset` | `Casino.EmptyRequest` | `Casino.CharmsResetResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsTutorialProgress` | `Casino.CharmsTutorialProgressRequest` | `Casino.CharmsTutorialProgressResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsResetNewBadge` | `Casino.CharmsResetNewBadgeRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.CharmsPastCollections` | `Casino.EmptyRequest` | `Casino.CharmsPastCollectionsResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateCharmsProgress` | `Casino.UpdateCharmsProgressRequest` | `Casino.EmptyResponse` | 2 | 0 | observed-live |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData.theme_id (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId.charm_id (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_charm_id (Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.event_id (int64, required)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.theme_id (int64, required)`
- `Casino.CharmsMilestone.id (int32, required)`
- `Casino.CharmsPastCollection.theme_id (int32, required)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trading_group_id (int64, optional)`
- `Casino.CharmsResetNewBadgeRequest.set_id (int32, required)`
- `Casino.CharmsResetRequest.theme_id (int32, required)`
- `Casino.CharmsThemeIteration.id (int32, required)`
- `Casino.CharmsTradeActionRequest.charm_id (int32, required)`
- `Casino.CharmsTradeAvatarRequestRecord.charm_id (int32, required)`
- `Casino.CharmsTradeAvatarRequestRecord.exchange_charm_id (int32, optional)`
- `Casino.CharmsTradeExchangeExecuteRequest.charm_id (int32, required)`
- `Casino.CharmsTradeExchangeExecuteRequest.desired_charm_id (int32, optional)`
- `Casino.CharmsTradeExchangeExecuteRequest.user_id (int64, required)`
- `Casino.CollectiblesBoxData.CharmsBoxData.box_id (int32, required)`
- `Casino.TimeBasedCharmItem.id (int32, required)`
- `Casino.TimeBasedCharmsStateRequest.event_id (int64, required)`

### Progression / state

- `Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData.theme_level (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.duplicates_state (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.progress_data (Casino.CharmsProgressData, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.tutorial (Casino.AddDciEventRequest.CharmsEvent.Tutorial, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.tutorial (Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial, optional)`
- `Casino.CharmsBoxOpenAllResponse.status (Casino.CharmsBoxOpenAllResponse.Status, required)`
- `Casino.CharmsPastCollectionsResponse.status (Casino.CharmsPastCollectionsResponse.Status, required)`
- `Casino.CharmsResetResponse.duplicates_state (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.CharmsResetResponse.status (Casino.CharmsResetResponse.Status, required)`
- `Casino.CharmsStatistics.completed_sets (int32, required)`
- `Casino.CharmsThemeIteration.level (int32, optional)`
- `Casino.CharmsThemeReward.level (int32, optional)`
- `Casino.CharmsTradeActionResponse.status (Casino.CharmsTradeActionResponse.Status, required)`
- `Casino.CharmsTradeExchangeExecuteResponse.status (Casino.CharmsTradeExchangeExecuteResponse.Status, required)`
- `Casino.CharmsTradeRequestListFetchResponse.status (Casino.CharmsTradeRequestListFetchResponse.Status, required)`
- `Casino.CharmsTutorialProgressResponse.status (Casino.CharmsTutorialProgressResponse.Status, required)`
- `Casino.CollectiblesBoxData.CharmsBoxData.duplicates_state_after (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.CollectiblesBoxData.CharmsBoxData.duplicates_state_before (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.CollectiblesBoxData.CharmsBoxData.new_theme_level (int32, optional)`
- `Casino.TimeBasedCharmsStateResponse.status (Casino.TimeBasedCharmsStateResponse.Status, required)`
- `Casino.UpdateCharmsProgressRequest.progress_data (Casino.CharmsProgressData, required)`

### Cost / input

- `Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId.token_delta (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_duplicate_charm (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_missing_charm (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_new_charm (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_request_creation (int32, repeated)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trade_token_quantity (int32, optional)`
- `Casino.CharmsResetResponse.token_quantity (int32, optional)`
- `Casino.CharmsTradeExchangeExecuteResponse.token_quantity (int32, optional)`
- `Casino.TimeBasedCharmItem.amount (int32, optional)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.AddDciEventRequest.CharmsEvent.Tutorial.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.reward_promo_main (Casino.AddDciEventRequest.CharmsEvent.RewardPromo, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.reward_promo_milestone (Casino.AddDciEventRequest.CharmsEvent.RewardPromo, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.reward_promo_set (Casino.AddDciEventRequest.CharmsEvent.RewardPromo, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.set_reward (Casino.CollectiblesSetReward, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.theme_reward (Casino.CharmsThemeReward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.main_reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.main_reward_for_all_rounds (Casino.TimeBasedCharmsMainReward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.milestone_reward (Casino.TimeBasedCharmsMilestoneReward, repeated)`
- `Casino.CharmsMilestone.reward (Casino.Reward, repeated)`
- `Casino.CharmsResetResponse.duplicates_reward (Casino.Reward, repeated)`
- `Casino.CharmsThemeReward.reward (Casino.Reward, repeated)`
- `Casino.CharmsTutorialProgressRequest.rewards_data (Casino.RewardsData, optional)`
- `Casino.CharmsTutorialProgressResponse.rewards_data (Casino.RewardsData, optional)`
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData.main_reward (Casino.Reward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData.milestone_reward (Casino.TimeBasedCharmsMilestoneReward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.duplicates_reward (Casino.Reward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.milestone_reward (Casino.CharmsMilestone, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.set_reward (Casino.CollectiblesSetReward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.theme_reward (Casino.CharmsThemeReward, optional)`
- `Casino.TimeBasedCharmsMainReward.reward (Casino.Reward, repeated)`
- `Casino.TimeBasedCharmsMilestoneReward.reward (Casino.Reward, repeated)`
- `Casino.TimeBasedCharmsStateResponse.remaining_main_reward (Casino.Reward, repeated)`
- `Casino.TimeBasedCharmsStateResponse.remaining_milestone_reward (Casino.TimeBasedCharmsMilestoneReward, repeated)`

### Timing / reset / expiry

- `Casino.AddDciEventRequest.CharmsEvent.RewardPromo.expire (int64, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.request_duration (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.number_of_resets (int32, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.number_of_resets (int32, optional)`
- `Casino.CharmsMilestone.expire (int64, optional)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trades_reset_timer (int64, optional)`
- `Casino.CharmsResetResponse.repeat_round_after_reset (bool, optional)`
- `Casino.CharmsResetResponse.reset_rewards_data (Casino.RewardsData, optional)`
- `Casino.CharmsTradeActionResponse.expire_timestamp (int64, optional)`
- `Casino.CharmsTradeAvatarRequestRecord.expire_timestamp (int64, required)`
- `Casino.CharmsTradeExchangeExecuteResponse.trades_reset_timer (int64, optional)`
- `Casino.CollectiblesBoxData.CharmsBoxData.time_based_charms_box_data (Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData, optional)`
- `Casino.TimeBasedCharmItem.first_time (bool, optional)`
- `Casino.TimeBasedCharmsStateResponse.number_of_resets (int32, optional)`

### Segment / eligibility / limit

- `Casino.AddDciEventRequest.CharmsEvent.Trading.daily_limit (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.temporary_unlocked_charms (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.unlock_level (int32, optional)`

### Other structural fields

- `Casino.AddDciEventRequest.CharmsEvent.StarsPerRarity.rarity (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.StarsPerRarity.stars_value (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.blocked_charms (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.blocked_rarities (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Tutorial.step (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.box_for_spin_config (Casino.AddDciEventRequest.BoxForSpinConfig, required)`
- `Casino.AddDciEventRequest.CharmsEvent.collectibles_statistics (Casino.CharmsStatistics, required)`
- `Casino.AddDciEventRequest.CharmsEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.difficulty (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.item (Casino.CollectiblesItem, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.primary_data (Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData, required)`
- `Casino.AddDciEventRequest.CharmsEvent.set (Casino.CollectiblesSet, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.stars_per_rarity (Casino.AddDciEventRequest.CharmsEvent.StarsPerRarity, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.trading (Casino.AddDciEventRequest.CharmsEvent.Trading, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial.step (int32, required)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.box_for_spin_config (Casino.AddDciEventRequest.BoxForSpinConfig, required)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.item (Casino.TimeBasedCharmItem, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.show_xl_ui (bool, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.theme_name (string, required)`
- `Casino.CharmsBoxOpenAllRequest.box_type (int32, repeated)`
- `Casino.CharmsBoxOpenAllResponse.box_data (Casino.CollectiblesBoxData, repeated)`
- `Casino.CharmsBoxOpenAllResponse.error_code (int32, optional)`
- `Casino.CharmsMilestone.promo (bool, optional)`
- `Casino.CharmsPacksInfo.BoxTypeInfo.box_type (int32, required)`
- `Casino.CharmsPacksInfo.BoxTypeInfo.first_box (Casino.CollectiblesBox, optional)`
- `Casino.CharmsPacksInfo.BoxTypeInfo.number_of_boxes (int32, required)`
- `Casino.CharmsPacksInfo.info (Casino.CharmsPacksInfo.BoxTypeInfo, repeated)`
- `Casino.CharmsPastCollection.collected_items (int32, required)`
- `Casino.CharmsPastCollection.total_items (int32, required)`
- `Casino.CharmsPastCollectionsResponse.error_code (int32, optional)`
- `Casino.CharmsPastCollectionsResponse.past_collection_data (Casino.CharmsPastCollection, repeated)`
- `Casino.CharmsProgressData.CharmsTradingInfo.is_trade_request_answered (bool, optional)`
- `Casino.CharmsProgressData.CharmsTradingInfo.trades_left (int32, optional)`
- `Casino.CharmsProgressData.milestone (Casino.CharmsMilestone, optional)`
- `Casino.CharmsProgressData.packs_info (Casino.CharmsPacksInfo, optional)`
- `Casino.CharmsProgressData.trading_info (Casino.CharmsProgressData.CharmsTradingInfo, optional)`
- `Casino.CharmsResetResponse.error_code (int32, optional)`
- … 35 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260825_182300`:

- `AppClient.UpdateCharmsProgress` — 2 (2 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateShopRequest.product[].reward_data[].reward.charms_trade_token_delta` | 8 | 64 | 7 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.charms_trade_token_delta` | 8 | 64 | 8 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].charms_trade_token_delta` | 5 | 15 | 3 | varying-in-session |
| `Casino.UpdateCharmsProgressRequest.progress_data.trading_info.trade_token_quantity` | 2 | 2 | 2 | varying-in-session |
| `Casino.CollectMysteryRewardResponse.next_mystery_reward.rewards[].charms_trade_token_delta` | 1 | 1 | 1 | single-observation |
| `Casino.CollectMysteryRewardResponse.rewards_data.reward[].charms_trade_token_delta` | 1 | 1 | 1 | single-observation |
| `Casino.UpdateProgressRequest.rewards_data.reward[].charms_trade_token_delta` | 1 | 1 | 1 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260825_182300`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: event/config update -> state/progress update -> box/packs collection -> duplicate/token accumulation -> trade request/list/exchange -> reset/tutorial/past-collection flows.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/sound_charms.zpk`
- ZPK asset: `assets/sound_charms_tbc.zpk`
- `sound_charms.zpk` and `sound_charms_tbc.zpk` confirm dedicated Charms variants.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Charms collection, milestones, pack/box and trading screens with markers.
- Inspect duplicate/token balances and one trade request/detail.
- Open a naturally available box or execute a harmless normal trade only if already intended, then revisit progress.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
