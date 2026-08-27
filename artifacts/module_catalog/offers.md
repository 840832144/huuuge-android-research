# Offers / Shop / Bundles

Shop promotions, personal/direct-purchase offers, Offer Trail, Tile Shop, product/reward composition, display placement and offer timing.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **90/100 — substantial live structure**
- Primary live samples: **340** from `LOT-20260827-A`
- Cross-cutting live samples: **15**
- Live endpoints / schema endpoints: **8 / 15**
- Live populated field paths: **270**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Offers.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`, `OfferServer`
- Related message types: **62**

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoFrame` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoRibbon` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.OfferSaleBadge` (AppClient.proto)
- `Casino.AddPersonalOfferRequest` (AppClient.proto)
- `Casino.AddPersonalOfferRequest.ActivePersonalOffer` (AppClient.proto)
- `Casino.AddPersonalOfferRequest.PersonalOffer` (AppClient.proto)
- `Casino.AddPromotionRequest` (AppClient.proto)
- `Casino.AddPromotionRequest.CollectionEvent` (AppClient.proto)
- `Casino.AddPromotionRequest.CollectionEvent.Milestone` (AppClient.proto)
- `Casino.AddPromotionRequest.DisplayPlace` (AppClient.proto)
- `Casino.AddPromotionRequest.FullBanner` (AppClient.proto)
- `Casino.AddPromotionRequest.InAppPromotion` (AppClient.proto)
- `Casino.AddPromotionRequest.NativeBanner` (AppClient.proto)
- `Casino.AddPromotionRequest.NativeBanner.Title` (AppClient.proto)
- `Casino.AddPromotionRequest.Product` (AppClient.proto)
- `Casino.AddPromotionRequest.PromoLeaderboard` (AppClient.proto)
- `Casino.AddPromotionRequest.PromoLottery` (AppClient.proto)
- `Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier` (AppClient.proto)
- `Casino.AddPromotionResponse` (AppClient.proto)
- `Casino.CancelPersonalOfferRequest` (AppClient.proto)
- `Casino.CancelPersonalOfferRequest.PersonalOffer` (AppClient.proto)
- `Casino.CancelPromotionRequest` (AppClient.proto)
- `Casino.CollectShopBonusResponse` (AppServer.proto)
- `Casino.DailyWheelOffer` (AppServer.proto)
- `Casino.DailyWheelOffer.Promotion` (AppServer.proto)
- `Casino.DailyWheelOffer.Wedge` (AppServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.FreeOffer` (Offers.proto)
- `Casino.MakeInAppPurchaseRequest.OfferData` (AppServer.proto)
- `Casino.OfferBase` (AppClient.proto)
- `Casino.OfferId` (Common.proto)
- `Casino.OfferTimer` (AppClient.proto)
- `Casino.OfferTrail` (Offers.proto)
- `Casino.OfferTrail.CancelRequest` (Offers.proto)
- `Casino.OfferTrail.UpdateRequest` (Offers.proto)
- `Casino.OfferTrail.UpdateRequest.Tile` (Offers.proto)
- `Casino.PaidOffer` (Offers.proto)
- `Casino.PaidOffer.Metadata` (Offers.proto)
- `Casino.ReloadOfferRequest` (AppClient.proto)
- `Casino.ShopProduct` (Common.proto)
- `Casino.StartPersonalOfferRequest` (AppServer.proto)
- `Casino.StartPersonalOfferResponse` (AppServer.proto)
- `Casino.TileShop` (Offers.proto)
- `Casino.TileShop.Config` (Offers.proto)
- `Casino.TileShop.Metadata` (Offers.proto)
- `Casino.TileShop.Tile` (Offers.proto)
- `Casino.TileShopResponse` (Offers.proto)
- `Casino.TriggerDirectPurchaseOfferRequest` (AppServer.proto)
- `Casino.TriggerDirectPurchaseOfferResponse` (AppServer.proto)
- `Casino.UpdateDirectPurchaseOfferRequest` (AppClient.proto)
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer` (AppClient.proto)
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance` (AppClient.proto)
- `Casino.UpdatePersonalOfferGlobalsRequest` (AppClient.proto)
- `Casino.UpdatePersonalOfferGlobalsRequest.PersonalOfferGlobals` (AppClient.proto)
- `Casino.UpdateShopRequest` (Common.proto)
- `Casino.UpdateShopRequest.ShopPromotion` (Common.proto)
- `Casino.UpdateShopRequest.ShopPromotion.PromoIap` (Common.proto)
- `Casino.UpdateShopRequest.ShopPromotion.PromoIap.PromoReward` (Common.proto)
- `Casino.UpdateShopResponse` (Common.proto)

## RPC and flow structure

Observed/schema flow: server pushes shop/promotions/personal/direct offers -> client opens/triggers an offer -> Offer Trail/Tile Shop provides staged tiles -> purchase handoff moves to the Purchases module -> cancel/reload/expiry removes or refreshes offers.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.CollectShopBonus` | `Casino.EmptyRequest` | `Casino.CollectShopBonusResponse` | 1 | 1 | observed-live |
| `AppServer.StartPersonalOffer` | `Casino.StartPersonalOfferRequest` | `Casino.StartPersonalOfferResponse` | 0 | 0 | schema-only |
| `AppServer.DiscardPersonalOffer` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 3 | 0 | observed-live |
| `AppServer.TriggerDirectPurchaseOffer` | `Casino.TriggerDirectPurchaseOfferRequest` | `Casino.TriggerDirectPurchaseOfferResponse` | 12 | 12 | observed-live |
| `AppClient.AddPromotion` | `Casino.AddPromotionRequest` | `Casino.AddPromotionResponse` | 0 | 0 | schema-only |
| `AppClient.CancelPromotion` | `Casino.CancelPromotionRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateShop` | `Casino.UpdateShopRequest` | `Casino.UpdateShopResponse` | 153 | 153 | observed-live |
| `AppClient.UpdatePersonalOfferGlobals` | `Casino.UpdatePersonalOfferGlobalsRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.AddPersonalOffer` | `Casino.AddPersonalOfferRequest` | `Casino.EmptyResponse` | 2 | 0 | observed-live |
| `AppClient.CancelPersonalOffer` | `Casino.CancelPersonalOfferRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateDirectPurchaseOffer` | `Casino.UpdateDirectPurchaseOfferRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.OfferTrailUpdate` | `Casino.OfferTrail.UpdateRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.OfferTrailCancel` | `Casino.OfferTrail.CancelRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ReloadOffers` | `Casino.ReloadOfferRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `OfferServer.GetTileShop` | `Casino.EmptyRequest` | `Casino.TileShopResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.product (Casino.IapProduct, repeated)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.product (Casino.IapProduct, required)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.template_id (int32, required)`
- `Casino.AddPromotionRequest.CollectionEvent.gfx_set_id (int32, required)`
- `Casino.AddPromotionRequest.FullBanner.id (int32, required)`
- `Casino.AddPromotionRequest.InAppPromotion.product (Casino.AddPromotionRequest.Product, repeated)`
- `Casino.AddPromotionRequest.Product.product_id (string, required)`
- `Casino.AddPromotionRequest.Product.ref_product_id (string, optional)`
- `Casino.AddPromotionRequest.event_id (int64, optional)`
- `Casino.AddPromotionRequest.group_id (int64, optional)`
- `Casino.AddPromotionRequest.segment_id (int64, optional)`
- `Casino.CancelPersonalOfferRequest.PersonalOffer.id (Casino.OfferId, required)`
- `Casino.CancelPromotionRequest.event_id (int64, repeated)`
- `Casino.DailyWheelOffer.Promotion.iap_id (string, optional)`
- `Casino.DailyWheelOffer.Promotion.segment_id (int64, required)`
- `Casino.DailyWheelOffer.event_id (int64, required)`
- `Casino.DailyWheelOffer.iap_id (string, required)`
- `Casino.DailyWheelOffer.segment_id (int64, required)`
- `Casino.FreeOffer.bundle_id (string, optional)`
- `Casino.FreeOffer.config_id (string, optional)`
- `Casino.MakeInAppPurchaseRequest.OfferData.id (int64, required)`
- `Casino.OfferBase.id (Casino.OfferId, required)`
- `Casino.OfferBase.segment_id (int64, required)`
- `Casino.OfferId.config_id (int64, required)`
- `Casino.OfferTrail.CancelRequest.event_id (string, optional)`
- `Casino.OfferTrail.UpdateRequest.Tile.id (int32, optional)`
- `Casino.OfferTrail.UpdateRequest.event_id (string, optional)`
- `Casino.OfferTrail.UpdateRequest.tile (Casino.OfferTrail.UpdateRequest.Tile, repeated)`
- `Casino.PaidOffer.Metadata.key (string, optional)`
- `Casino.PaidOffer.config_id (string, optional)`
- `Casino.PaidOffer.product_id (string, optional)`
- `Casino.ShopProduct.id (string, required)`
- `Casino.StartPersonalOfferRequest.id (Casino.OfferId, required)`
- `Casino.TileShop.Config.config_id (string, optional)`
- `Casino.TileShop.Config.promo_config_id (string, optional)`
- `Casino.TileShop.Metadata.key (string, optional)`
- `Casino.TileShop.Tile.offer (Casino.PaidOffer, optional)`
- `Casino.TileShop.tile (Casino.TileShop.Tile, repeated)`
- `Casino.TriggerDirectPurchaseOfferRequest.id (Casino.OfferId, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.product (Casino.IapProduct, required)`
- … 3 more rows in `fields.csv`

### Progression / state

- `Casino.AddPersonalOfferRequest.active_personal_offer (Casino.AddPersonalOfferRequest.ActivePersonalOffer, optional)`
- `Casino.AddPromotionRequest.CollectionEvent.end_level (int32, required)`
- `Casino.AddPromotionRequest.CollectionEvent.start_level (int32, required)`
- `Casino.AddPromotionRequest.FullBanner.count (int32, optional)`
- `Casino.CollectShopBonusResponse.status (Casino.CollectShopBonusResponse.Status, required)`
- `Casino.DailyWheelOffer.Promotion.active_promotion (Casino.DailyWheelOffer.Promotion.Type, required)`
- `Casino.ReloadOfferRequest.active_personal_offer (Casino.AddPersonalOfferRequest.ActivePersonalOffer, optional)`
- `Casino.StartPersonalOfferResponse.status (Casino.StartPersonalOfferResponse.Status, required)`
- `Casino.TileShopResponse.status (Casino.TileShopResponse.Status, optional)`
- `Casino.TriggerDirectPurchaseOfferResponse.status (Casino.TriggerDirectPurchaseOfferResponse.Status, required)`
- `Casino.UpdateShopResponse.status (Casino.UpdateShopResponse.Status, required)`

### Cost / input

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.ticket_color (Casino.LotteryColor, required)`
- `Casino.AddPromotionRequest.FullBanner.deep_link_token (string, optional)`
- `Casino.AddPromotionRequest.NativeBanner.deep_link_token (string, optional)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.news_feed (Casino.NewsFeedBanner, optional)`

### Currency / balance

- `Casino.AddPromotionRequest.Product.diamonds_multiplier (int32, optional)`
- `Casino.CollectShopBonusResponse.chips_delta (Casino.Chips, optional)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance.chipsback (double, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance.show_chipsback_badge (bool, required)`

### Reward / output

- `Casino.AddPromotionRequest.CollectionEvent.Milestone.reward (Casino.Reward, required)`
- `Casino.DailyWheelOffer.Wedge.reward (Casino.Reward, repeated)`
- `Casino.DailyWheelOffer.additional_reward (Casino.Reward, optional)`
- `Casino.UpdateShopRequest.ShopPromotion.PromoIap.PromoReward.reward (Casino.Reward, required)`
- `Casino.UpdateShopRequest.ShopPromotion.PromoIap.promo_reward (Casino.UpdateShopRequest.ShopPromotion.PromoIap.PromoReward, repeated)`

### Timing / reset / expiry

- `Casino.AddPersonalOfferRequest.ActivePersonalOffer.reappear_timer (int64, required)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.one_time (bool, optional)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.timer (int64, optional)`
- `Casino.AddPromotionRequest.InAppPromotion.one_time (bool, optional)`
- `Casino.AddPromotionRequest.InAppPromotion.show_timer (bool, optional)`
- `Casino.AddPromotionRequest.duration (int32, optional)`
- `Casino.AddPromotionRequest.expire (int32, required)`
- `Casino.CollectShopBonusResponse.shop_bonus_timer (int32, optional)`
- `Casino.OfferBase.expire (int64, required)`
- `Casino.OfferTrail.UpdateRequest.end_time (int32, optional)`
- `Casino.PaidOffer.created_at (int32, optional)`
- `Casino.UpdatePersonalOfferGlobalsRequest.PersonalOfferGlobals.min_time_to_start (int32, optional)`
- `Casino.UpdatePersonalOfferGlobalsRequest.PersonalOfferGlobals.reappear_timer (int32, optional)`
- `Casino.UpdatePersonalOfferGlobalsRequest.PersonalOfferGlobals.time_on_screen (int32, optional)`
- `Casino.UpdateShopRequest.ShopPromotion.expire (int64, required)`
- `Casino.UpdateShopRequest.sale_expire (int32, optional)`

### Segment / eligibility / limit

- `Casino.AddPersonalOfferRequest.PersonalOffer.occurrence_limit (int32, optional)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.total_limit (int32, required)`
- `Casino.AddPromotionRequest.FullBanner.limit (int32, optional)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance.cap (int64, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.total_limit (int32, required)`

### Other structural fields

- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoFrame.show_promo_frame (bool, required)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoRibbon.show_promo_ribbon (string, required)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.OfferSaleBadge.showSaleDPO (bool, required)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.OfferSaleBadge.showSalePO (bool, required)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.lottery_promo_frame (Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoFrame, optional)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.lottery_promo_ribbon (Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoRibbon, optional)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.offer_sale_badge (Casino.AddDciEventRequest.OtherPromotionsEvent.OfferSaleBadge, optional)`
- `Casino.AddPersonalOfferRequest.ActivePersonalOffer.occurrence_used (int32, required)`
- `Casino.AddPersonalOfferRequest.ActivePersonalOffer.personal_offer (Casino.AddPersonalOfferRequest.PersonalOffer, required)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.offer_base (Casino.OfferBase, required)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.paid_offer (Casino.PaidOffer, optional)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.scenario (int32, repeated)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.total_used (int32, required)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.url (string, repeated)`
- `Casino.AddPersonalOfferRequest.PersonalOffer.version (int64, optional)`
- `Casino.AddPersonalOfferRequest.personal_offer (Casino.AddPersonalOfferRequest.PersonalOffer, repeated)`
- `Casino.AddPromotionRequest.CollectionEvent.Milestone.items_to_collect (int32, required)`
- `Casino.AddPromotionRequest.CollectionEvent.milestone (Casino.AddPromotionRequest.CollectionEvent.Milestone, repeated)`
- `Casino.AddPromotionRequest.DisplayPlace.name (string, required)`
- `Casino.AddPromotionRequest.DisplayPlace.priority (int32, required)`
- `Casino.AddPromotionRequest.FullBanner.deep_link (string, optional)`
- `Casino.AddPromotionRequest.FullBanner.display_place (Casino.AddPromotionRequest.DisplayPlace, repeated)`
- `Casino.AddPromotionRequest.FullBanner.freq (int32, optional)`
- `Casino.AddPromotionRequest.FullBanner.session_freq (int32, optional)`
- `Casino.AddPromotionRequest.FullBanner.url (string, repeated)`
- `Casino.AddPromotionRequest.FullBanner.url_link (string, optional)`
- `Casino.AddPromotionRequest.InAppPromotion.priority (int32, required)`
- `Casino.AddPromotionRequest.InAppPromotion.type (int32, required)`
- `Casino.AddPromotionRequest.NativeBanner.Title.language (string, required)`
- `Casino.AddPromotionRequest.NativeBanner.Title.text (string, required)`
- `Casino.AddPromotionRequest.NativeBanner.deep_link (string, optional)`
- `Casino.AddPromotionRequest.NativeBanner.header (Casino.AddPromotionRequest.NativeBanner.Title, repeated)`
- `Casino.AddPromotionRequest.NativeBanner.name (string, required)`
- `Casino.AddPromotionRequest.NativeBanner.show_video_ad (bool, optional)`
- `Casino.AddPromotionRequest.NativeBanner.title (Casino.AddPromotionRequest.NativeBanner.Title, repeated)`
- `Casino.AddPromotionRequest.Product.multiplier (int32, optional)`
- `Casino.AddPromotionRequest.Product.tag (int32, optional)`
- `Casino.AddPromotionRequest.PromoLeaderboard.category (int32, optional)`
- `Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier.color (int32, required)`
- `Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier.multiplier (double, required)`
- … 69 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `LOT-20260827-A`:

- `AppClient.UpdateShop` — 306 (153 request, 153 response)
- `AppServer.TriggerDirectPurchaseOffer` — 24 (12 request, 12 response)
- `AppServer.DiscardPersonalOffer` — 3 (3 request, 0 response)
- `AppServer.CollectShopBonus` — 2 (1 request, 1 response)
- `AppClient.AddPersonalOffer` — 2 (2 request, 0 response)
- `AppClient.UpdatePersonalOfferGlobals` — 1 (1 request, 0 response)
- `AppClient.UpdateDirectPurchaseOffer` — 1 (1 request, 0 response)
- `AppClient.OfferTrailUpdate` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateShopRequest.dci_config_info.identifier.config_id` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.dci_config_info.identifier.flags` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.dci_config_info.segment_id` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].bank_bonus_days` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].bank_bonus_type` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].custom_fields` | 153 | n/a | n/a | not-assessed |
| `Casino.UpdateShopRequest.product[].custom_fields.custom_field_1` | 153 | 1224 | 5 | varying-in-session |
| `Casino.UpdateShopRequest.product[].custom_fields.custom_field_3` | 153 | 1224 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].product_id` | 153 | 1530 | 10 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].big_value_for_money.value` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.big_chips_delta.value` | 153 | 918 | 6 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.charms_trade_token_delta` | 153 | 1224 | 7 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.chips_delta` | 153 | 918 | 6 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.box_id` | 153 | 1683 | 11 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.box_type` | 153 | 1683 | 3 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.raffle_id` | 153 | 1683 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.source` | 153 | 1683 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.theme_id` | 153 | 1683 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box.type` | 153 | 1683 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.box_id` | 153 | 1683 | 11 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.box_type` | 153 | 1683 | 3 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.event_type` | 153 | 1683 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.highest_guaranteed_rarity` | 153 | 1683 | 5 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.highest_guaranteed_rarity_items_count` | 153 | 1683 | 3 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.collectibles_box_info.items_count` | 153 | 1683 | 6 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.diamonds_delta` | 153 | 306 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.extra_item_boost.time.duration` | 153 | 1530 | 5 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.extra_item_boost.time.expire_time` | 153 | 1530 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.extra_item_boost.time.value` | 153 | 1530 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.extra_item_boost.type` | 153 | 1530 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.id` | 153 | 7038 | 8 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].reward.loyalty_points` | 153 | 1377 | 7 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].share` | 153 | 459 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].reward_data[].value_for_money` | 153 | 306 | 2 | varying-in-session |
| `Casino.UpdateShopRequest.product[].tag[]` | 153 | 1683 | 6 | varying-in-session |
| `Casino.UpdateShopRequest.shop_promotion.dci_config_info.identifier.config_id` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.dci_config_info.identifier.flags` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.dci_config_info.segment_id` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.expire` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.shop_promotion.promo_iap[].product_id` | 153 | 1224 | 8 | varying-in-session |
| … | | | | 230 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: server pushes shop/promotions/personal/direct offers -> client opens/triggers an offer -> Offer Trail/Tile Shop provides staged tiles -> purchase handoff moves to the Purchases module -> cancel/reload/expiry removes or refreshes offers.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_custom_tiles_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_dailybonus_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_liveops_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_promo_2_etc2.zpk`
- ZPK asset: `assets/atlas_promo_tiles_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_single_tile_hc_placeholder_square_med_2_etc2.zpk`
- ZPK asset: `assets/atlas_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tile_shop_v2_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tile_shop_v3_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles2_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles3_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles4_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles_reskinned_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc2_1_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc2_2_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc_1_etc2.zpk`
- ZPK asset: `assets/atlas_topbar_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_vault2_anim_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_vault2_sku_hc_2_etc2.zpk`
- Promo, SKU, Tile Shop, tiles and live-ops atlas ZPKs confirm multiple presentation channels.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open main shop, each offer family, bundle detail, personal offer, Offer Trail and Tile Shop with markers.
- Inspect price/reward/limit/expiry screens without purchasing.
- Close/reopen an offer and revisit after a natural refresh to capture lifecycle changes.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
