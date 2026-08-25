# Collection / Collection Event / Club Set

Collection-event milestones, collectible themes/items/sets, duplicate state, boxes/raffles and club-set variants.

## Catalog status

- Evidence status: **live-confirmed (cross-cutting/config only)**
- Structural completeness: **65/100 — partial live structure**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **44**
- Live endpoints / schema endpoints: **0 / 7**
- Live populated field paths: **79**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **39**

- `Casino.AddDciEventRequest.ClubSetEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.CollectionEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.CollectionEvent.Milestone` (AppClient.proto)
- `Casino.AddPromotionRequest.CollectionEvent` (AppClient.proto)
- `Casino.AddPromotionRequest.CollectionEvent.Milestone` (AppClient.proto)
- `Casino.ClubSetBox` (Common.proto)
- `Casino.ClubSetCollectItemsRequest` (AppServer.proto)
- `Casino.ClubSetCollectItemsResponse` (AppServer.proto)
- `Casino.ClubSetConfigData` (AppClient.proto)
- `Casino.ClubSetDuplicatesReward` (Common.proto)
- `Casino.ClubSetGrandReward` (Common.proto)
- `Casino.ClubSetItem` (Common.proto)
- `Casino.ClubSetMilestoneReward` (Common.proto)
- `Casino.ClubSetProgressData` (AppClient.proto)
- `Casino.ClubSetTutorialProgressRequest` (AppServer.proto)
- `Casino.ClubSetTutorialProgressResponse` (AppServer.proto)
- `Casino.CollectiblesBox` (Common.proto)
- `Casino.CollectiblesBoxData` (Common.proto)
- `Casino.CollectiblesBoxData.CharmsBoxData` (Common.proto)
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData` (Common.proto)
- `Casino.CollectiblesBoxData.RaffleCost` (Common.proto)
- `Casino.CollectiblesBoxInfo` (Common.proto)
- `Casino.CollectiblesBoxOpenRequest` (AppServer.proto)
- `Casino.CollectiblesBoxOpenResponse` (AppServer.proto)
- `Casino.CollectiblesBoxReraffleRequest` (AppServer.proto)
- `Casino.CollectiblesBoxReraffleResponse` (AppServer.proto)
- `Casino.CollectiblesDuplicatesState` (Common.proto)
- `Casino.CollectiblesItem` (Common.proto)
- `Casino.CollectiblesSet` (Common.proto)
- `Casino.CollectiblesSetReward` (Common.proto)
- `Casino.CollectionEventState` (Common.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.GetClubSetThemeStatusRequest` (AppServer.proto)
- `Casino.GetClubSetThemeStatusResponse` (AppServer.proto)
- `Casino.GetCollectiblesThemeStatusRequest` (AppServer.proto)
- `Casino.GetCollectiblesThemeStatusResponse` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.CollectiblesMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo` (AppServer.proto)
- `Casino.UpdateClubSetProgressRequest` (AppClient.proto)

## RPC and flow structure

Inferred flow: event/theme definition -> theme/status fetch -> box open/reraffle or item collection -> duplicate/set progress update -> milestone/grand reward claim. Club Set reuses related collectible structures.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.GetCollectiblesThemeStatus` | `Casino.GetCollectiblesThemeStatusRequest` | `Casino.GetCollectiblesThemeStatusResponse` | 0 | 0 | schema-only |
| `AppServer.CollectiblesBoxOpen` | `Casino.CollectiblesBoxOpenRequest` | `Casino.CollectiblesBoxOpenResponse` | 0 | 0 | schema-only |
| `AppServer.CollectiblesBoxReraffle` | `Casino.CollectiblesBoxReraffleRequest` | `Casino.CollectiblesBoxReraffleResponse` | 0 | 0 | schema-only |
| `AppServer.GetClubSetThemeStatus` | `Casino.GetClubSetThemeStatusRequest` | `Casino.GetClubSetThemeStatusResponse` | 0 | 0 | schema-only |
| `AppServer.ClubSetTutorialProgress` | `Casino.ClubSetTutorialProgressRequest` | `Casino.ClubSetTutorialProgressResponse` | 0 | 0 | schema-only |
| `AppServer.ClubSetCollectItems` | `Casino.ClubSetCollectItemsRequest` | `Casino.ClubSetCollectItemsResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateClubSetProgress` | `Casino.UpdateClubSetProgressRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.CollectionEvent.gfx_set_id (int32, required)`
- `Casino.AddPromotionRequest.CollectionEvent.gfx_set_id (int32, required)`
- `Casino.ClubSetCollectItemsRequest.theme_id (int32, required)`
- `Casino.ClubSetConfigData.theme_id (int32, optional)`
- `Casino.ClubSetGrandReward.bundle_id (string, optional)`
- `Casino.ClubSetItem.id (int32, required)`
- `Casino.ClubSetMilestoneReward.bundle_id (string, optional)`
- `Casino.ClubSetTutorialProgressRequest.theme_id (int32, required)`
- `Casino.CollectiblesBox.box_id (int32, required)`
- `Casino.CollectiblesBox.campaign_id (string, optional)`
- `Casino.CollectiblesBox.giver_user_id (int64, optional)`
- `Casino.CollectiblesBox.lost_charm_id (int64, optional)`
- `Casino.CollectiblesBox.raffle_id (int64, required)`
- `Casino.CollectiblesBox.theme_id (int32, required)`
- `Casino.CollectiblesBoxData.CharmsBoxData.box_id (int32, required)`
- `Casino.CollectiblesBoxData.raffle_id (int64, required)`
- `Casino.CollectiblesBoxInfo.box_id (int32, required)`
- `Casino.CollectiblesBoxOpenRequest.raffle_id (int64, required)`
- `Casino.CollectiblesBoxReraffleRequest.raffle_id (int64, required)`
- `Casino.CollectiblesItem.id (int32, required)`
- `Casino.CollectiblesItem.set_id (int32, required)`
- `Casino.CollectiblesSet.id (int32, required)`
- `Casino.CollectiblesSetReward.id (int32, required)`
- `Casino.CollectionEventState.event_id (int64, required)`
- `Casino.GetClubSetThemeStatusRequest.theme_id (int32, required)`
- `Casino.GetCollectiblesThemeStatusRequest.theme_id (int32, required)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.milestone_id (int32, optional)`

### Progression / state

- `Casino.AddDciEventRequest.ClubSetEvent.progress_data (Casino.ClubSetProgressData, optional)`
- `Casino.AddDciEventRequest.CollectionEvent.state (Casino.CollectionEventState, optional)`
- `Casino.AddPromotionRequest.CollectionEvent.end_level (int32, required)`
- `Casino.AddPromotionRequest.CollectionEvent.start_level (int32, required)`
- `Casino.ClubSetBox.highest_guaranteed_rarity_items_count (int32, optional)`
- `Casino.ClubSetCollectItemsResponse.status (Casino.ClubSetCollectItemsResponse.Status, required)`
- `Casino.ClubSetProgressData.completed_in_other_club (bool, optional)`
- `Casino.ClubSetProgressData.tutorial_step (int32, optional)`
- `Casino.ClubSetTutorialProgressResponse.status (Casino.ClubSetTutorialProgressResponse.Status, required)`
- `Casino.CollectiblesBoxData.CharmsBoxData.duplicates_state_after (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.CollectiblesBoxData.CharmsBoxData.duplicates_state_before (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.CollectiblesBoxData.CharmsBoxData.new_theme_level (int32, optional)`
- `Casino.CollectiblesBoxInfo.highest_guaranteed_rarity_items_count (int32, required)`
- `Casino.CollectiblesBoxInfo.items_count (int32, required)`
- `Casino.CollectiblesBoxOpenResponse.status (Casino.CollectiblesBoxOpenResponse.Status, required)`
- `Casino.CollectiblesBoxReraffleResponse.status (Casino.CollectiblesBoxReraffleResponse.Status, required)`
- `Casino.CollectiblesItem.level (int32, optional)`
- `Casino.CollectiblesSet.level (int32, optional)`
- `Casino.CollectiblesSetReward.level (int32, optional)`
- `Casino.CollectionEventState.event_completed (bool, optional)`
- `Casino.CollectionEventState.item_bar_progression (int64, optional)`
- `Casino.CollectionEventState.milestone_completed (bool, optional)`
- `Casino.GetClubSetThemeStatusResponse.status (Casino.GetClubSetThemeStatusResponse.Status, required)`
- `Casino.GetCollectiblesThemeStatusResponse.iteration (Casino.CharmsThemeIteration, repeated)`
- `Casino.GetCollectiblesThemeStatusResponse.status (Casino.GetCollectiblesThemeStatusResponse.Status, required)`
- `Casino.LoginResponse.MissedInfo.CollectiblesMissedInfo.new_theme_level (int32, optional)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.eventCompleted (bool, optional)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.milestones_count (int32, optional)`
- `Casino.UpdateClubSetProgressRequest.progress_data (Casino.ClubSetProgressData, required)`

### Cost / input

- `Casino.ClubSetItem.amount (int32, optional)`
- `Casino.CollectiblesBoxData.RaffleCost.amount (int64, optional)`
- `Casino.CollectiblesBoxData.RaffleCost.cost_type (int32, required)`
- `Casino.CollectiblesBoxData.next_raffle_cost (Casino.CollectiblesBoxData.RaffleCost, required)`
- `Casino.CollectiblesDuplicatesState.amount (int32, required)`
- `Casino.CollectiblesDuplicatesState.requirement (int32, required)`
- `Casino.CollectiblesItem.amount (int32, optional)`

### Currency / balance

- `Casino.CollectiblesBoxData.RaffleCost.currency_type (int32, optional)`

### Reward / output

- `Casino.AddDciEventRequest.CollectionEvent.Milestone.reward (Casino.Reward, repeated)`
- `Casino.AddPromotionRequest.CollectionEvent.Milestone.reward (Casino.Reward, required)`
- `Casino.ClubSetConfigData.grand_reward (Casino.ClubSetGrandReward, optional)`
- `Casino.ClubSetConfigData.milestone_reward (Casino.ClubSetMilestoneReward, repeated)`
- `Casino.ClubSetDuplicatesReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetGrandReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetGrandReward.user_reward (Casino.Reward, repeated)`
- `Casino.ClubSetMilestoneReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetMilestoneReward.user_reward (Casino.Reward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData.main_reward (Casino.Reward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData.milestone_reward (Casino.TimeBasedCharmsMilestoneReward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.duplicates_reward (Casino.Reward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.milestone_reward (Casino.CharmsMilestone, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.set_reward (Casino.CollectiblesSetReward, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.theme_reward (Casino.CharmsThemeReward, optional)`
- `Casino.CollectiblesDuplicatesState.reward (Casino.Reward, repeated)`
- `Casino.CollectiblesSetReward.reward (Casino.Reward, repeated)`
- `Casino.GetClubSetThemeStatusResponse.duplicates_reward (Casino.ClubSetDuplicatesReward, optional)`
- `Casino.GetClubSetThemeStatusResponse.grand_reward (Casino.ClubSetGrandReward, optional)`
- `Casino.GetClubSetThemeStatusResponse.milestone_reward (Casino.ClubSetMilestoneReward, repeated)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.reward (Casino.Reward, repeated)`

### Timing / reset / expiry

- `Casino.CollectiblesBoxData.CharmsBoxData.time_based_charms_box_data (Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData, optional)`
- `Casino.CollectiblesItem.first_time (bool, optional)`

### Segment / eligibility / limit

- `Casino.CollectionEventState.item_bar_progression_cap (int64, optional)`

### Other structural fields

- `Casino.AddDciEventRequest.ClubSetEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.ClubSetEvent.config_data (Casino.ClubSetConfigData, optional)`
- `Casino.AddDciEventRequest.ClubSetEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.CollectionEvent.Milestone.items_to_collect (int64, required)`
- `Casino.AddDciEventRequest.CollectionEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.CollectionEvent.balloons (Casino.AddDciEventRequest.BalloonsEvent, optional)`
- `Casino.AddDciEventRequest.CollectionEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.CollectionEvent.milestone (Casino.AddDciEventRequest.CollectionEvent.Milestone, repeated)`
- `Casino.AddPromotionRequest.CollectionEvent.Milestone.items_to_collect (int32, required)`
- `Casino.AddPromotionRequest.CollectionEvent.milestone (Casino.AddPromotionRequest.CollectionEvent.Milestone, repeated)`
- `Casino.ClubSetBox.highest_guaranteed_rarity (int32, optional)`
- `Casino.ClubSetBox.number_of_boxes (int32, optional)`
- `Casino.ClubSetCollectItemsResponse.error_code (int32, optional)`
- `Casino.ClubSetCollectItemsResponse.number_of_boxes (int32, optional)`
- `Casino.ClubSetItem.rarity (int32, required)`
- `Casino.ClubSetMilestoneReward.step (int32, optional)`
- `Casino.ClubSetProgressData.collected_items (int32, optional)`
- `Casino.ClubSetProgressData.number_of_boxes (int32, optional)`
- `Casino.ClubSetProgressData.total_items (int32, optional)`
- `Casino.ClubSetTutorialProgressRequest.is_last_step (bool, required)`
- `Casino.ClubSetTutorialProgressRequest.step (int32, required)`
- `Casino.ClubSetTutorialProgressResponse.error_code (int32, optional)`
- `Casino.CollectiblesBox.box_type (int32, optional)`
- `Casino.CollectiblesBox.source (int32, required)`
- `Casino.CollectiblesBox.type (int32, required)`
- `Casino.CollectiblesBoxData.CharmsBoxData.TimeBasedCharmsBoxData.item (Casino.TimeBasedCharmItem, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.item (Casino.CollectiblesItem, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.reraffled_item (Casino.CollectiblesItem, repeated)`
- `Casino.CollectiblesBoxData.CharmsBoxData.source (int32, required)`
- `Casino.CollectiblesBoxData.RaffleCost.reraffles_left (int32, optional)`
- `Casino.CollectiblesBoxData.RaffleCost.reraffles_permitted (int32, optional)`
- `Casino.CollectiblesBoxData.box_type (int32, required)`
- `Casino.CollectiblesBoxData.charms_data (Casino.CollectiblesBoxData.CharmsBoxData, optional)`
- `Casino.CollectiblesBoxInfo.box_type (int32, required)`
- `Casino.CollectiblesBoxInfo.event_type (int32, required)`
- `Casino.CollectiblesBoxInfo.highest_guaranteed_rarity (int32, required)`
- `Casino.CollectiblesBoxOpenRequest.type (int32, required)`
- `Casino.CollectiblesBoxOpenResponse.box_data (Casino.CollectiblesBoxData, optional)`
- `Casino.CollectiblesBoxOpenResponse.error_code (int32, optional)`
- `Casino.CollectiblesBoxReraffleResponse.box_data (Casino.CollectiblesBoxData, optional)`
- … 18 more rows in `fields.csv`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateProgressRequest.collection_event_state.collected_items` | 29 | 29 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.collection_event_state.event_completed` | 29 | 29 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.collection_event_state.event_id` | 29 | 29 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.collection_event_state.item_bar_progression` | 29 | 29 | 29 | varying-in-session |
| `Casino.UpdateProgressRequest.collection_event_state.item_bar_progression_cap` | 29 | 29 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.collection_event_state.milestone_completed` | 29 | 29 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.collection_event_state.milestone_idx` | 29 | 29 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.box_id` | 8 | 88 | 10 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.box_type` | 8 | 88 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.raffle_id` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.source` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.theme_id` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.type` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.box_id` | 8 | 88 | 10 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.box_type` | 8 | 88 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.event_type` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.highest_guaranteed_rarity` | 8 | 88 | 5 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.highest_guaranteed_rarity_items_count` | 8 | 88 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.items_count` | 8 | 88 | 6 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box.box_id` | 8 | 88 | 10 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box.box_type` | 8 | 88 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box.raffle_id` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box.source` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box.theme_id` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box.type` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box_info.box_id` | 8 | 88 | 10 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box_info.box_type` | 8 | 88 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box_info.event_type` | 8 | 88 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box_info.highest_guaranteed_rarity` | 8 | 88 | 5 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box_info.highest_guaranteed_rarity_items_count` | 8 | 88 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].promo_reward[].reward.collectibles_box_info.items_count` | 8 | 88 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.box_id` | 5 | 45 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.box_type` | 5 | 45 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.raffle_id` | 5 | 45 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.source` | 5 | 45 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.theme_id` | 5 | 45 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.type` | 5 | 45 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.box_id` | 5 | 45 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.box_type` | 5 | 45 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.event_type` | 5 | 45 | 1 | constant-in-session |
| … | | | | 39 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260825_182300`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Inferred flow: event/theme definition -> theme/status fetch -> box open/reraffle or item collection -> duplicate/set progress update -> milestone/grand reward claim. Club Set reuses related collectible structures.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_collection_event_2_etc2.zpk`
- ZPK asset: `assets/sound_club_set.zpk`
- ZPK asset: `assets/sound_collection_event.zpk`
- `atlas_collection_event_2_etc2.zpk`, `sound_collection_event.zpk` and Club Set assets provide module-specific static evidence.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Collection Event, collection album/theme and any Club Set screen with markers.
- Inspect one set, item/duplicate detail, box odds/cost and milestone track.
- Open or claim one naturally available box/item/milestone and revisit progress.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
