# Purchase / Checkout / Price Localization

In-app purchase requests, checkout/localization, pending/paid notifications, Huuuge Pay bundles and localized price points.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **80/100 — substantial live structure**
- Primary live samples: **16** from `LOT-20260827-A`
- Cross-cutting live samples: **114**
- Live endpoints / schema endpoints: **1 / 9**
- Live populated field paths: **77**

## Schema scope

- Proto files: `AppCharge.proto`, `AppClient.proto`, `AppServer.proto`, `Purchases.proto`, `Services.proto`, `Vouchers.proto`
- Services: `AppClient`, `AppServer`, `AppchargeClient`, `PurchaseClient`, `PurchaseServer`
- Related message types: **32**

- `Casino.EmptyResponse` (Services.proto)
- `Casino.HuuugePayPendingPurchaseRequest` (AppCharge.proto)
- `Casino.HuuugePayPendingPurchaseRequest.Metadata` (AppCharge.proto)
- `Casino.LocalizePricesRequest` (AppServer.proto)
- `Casino.LocalizePricesResponse` (AppServer.proto)
- `Casino.LocalizedPrice` (AppServer.proto)
- `Casino.LocalizedPricePoint` (Purchases.proto)
- `Casino.LocalizedPricePointsRequest` (Purchases.proto)
- `Casino.LocalizedPricePointsResponse` (Purchases.proto)
- `Casino.LoginResponse.PurchaseSupportedCountry` (AppServer.proto)
- `Casino.MakeInAppPurchaseRequest` (AppServer.proto)
- `Casino.MakeInAppPurchaseRequest.CheckoutLocalizationData` (AppServer.proto)
- `Casino.MakeInAppPurchaseRequest.MiniPassData` (AppServer.proto)
- `Casino.MakeInAppPurchaseRequest.OfferData` (AppServer.proto)
- `Casino.MakeInAppPurchaseResponse` (AppServer.proto)
- `Casino.MakeInAppPurchaseResponse.Checkout` (AppServer.proto)
- `Casino.NotifyPendingBundlesRequest` (AppCharge.proto)
- `Casino.NotifyPendingBundlesRequest.Bundle` (AppCharge.proto)
- `Casino.NotifyPendingBundlesRequest.Bundle.Metadata` (AppCharge.proto)
- `Casino.NotifyPurchasePaidRequest` (Purchases.proto)
- `Casino.NotifyPurchasePaidRequest.Metadata` (Purchases.proto)
- `Casino.PendingExternalSdkPurchaseRequest` (AppClient.proto)
- `Casino.PendingExternalSdkPurchaseRequest.PendingExternalSdkPurchase` (AppClient.proto)
- `Casino.TriggerDirectPurchaseOfferRequest` (AppServer.proto)
- `Casino.TriggerDirectPurchaseOfferResponse` (AppServer.proto)
- `Casino.UpdateDirectPurchaseOfferRequest` (AppClient.proto)
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer` (AppClient.proto)
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance` (AppClient.proto)
- `Casino.ValidatePostalCodeRequest` (AppServer.proto)
- `Casino.ValidatePostalCodeResponse` (AppServer.proto)
- `Casino.VouchersMakePurchaseRequest` (Vouchers.proto)
- `Casino.VouchersMakePurchaseResponse` (Vouchers.proto)

## RPC and flow structure

Observed/schema flow: localize price/offer -> initiate `MakeInAppPurchase`/voucher purchase -> checkout response or external SDK handoff -> pending/paid notification -> reward delivery handled by shared reward messages.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.MakeInAppPurchase` | `Casino.MakeInAppPurchaseRequest` | `Casino.MakeInAppPurchaseResponse` | 8 | 8 | observed-live |
| `AppServer.LocalizePrices` | `Casino.LocalizePricesRequest` | `Casino.LocalizePricesResponse` | 0 | 0 | schema-only |
| `AppServer.ValidatePostalCode` | `Casino.ValidatePostalCodeRequest` | `Casino.ValidatePostalCodeResponse` | 0 | 0 | schema-only |
| `AppServer.VouchersMakePurchase` | `Casino.VouchersMakePurchaseRequest` | `Casino.VouchersMakePurchaseResponse` | 0 | 0 | schema-only |
| `AppClient.PendingExternalSdkPurchase` | `Casino.PendingExternalSdkPurchaseRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppchargeClient.HuuugePayPendingPurchase` | `Casino.HuuugePayPendingPurchaseRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppchargeClient.NotifyPendingBundles` | `Casino.NotifyPendingBundlesRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `PurchaseServer.GetLocalizedPricePoints` | `Casino.LocalizedPricePointsRequest` | `Casino.LocalizedPricePointsResponse` | 0 | 0 | schema-only |
| `PurchaseClient.NotifyPurchasePaid` | `Casino.NotifyPurchasePaidRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.HuuugePayPendingPurchaseRequest.Metadata.key (string, optional)`
- `Casino.HuuugePayPendingPurchaseRequest.payment_id (string, optional)`
- `Casino.HuuugePayPendingPurchaseRequest.product_id (string, optional)`
- `Casino.HuuugePayPendingPurchaseRequest.request_id (string, optional)`
- `Casino.MakeInAppPurchaseRequest.MiniPassData.event_id (string, required)`
- `Casino.MakeInAppPurchaseRequest.MiniPassData.phase_id (string, optional)`
- `Casino.MakeInAppPurchaseRequest.OfferData.id (int64, required)`
- `Casino.MakeInAppPurchaseRequest.battle_pass_id (string, optional)`
- `Casino.MakeInAppPurchaseRequest.product_id (string, required)`
- `Casino.MakeInAppPurchaseRequest.purchase_id (string, optional)`
- `Casino.MakeInAppPurchaseRequest.request_id (string, optional)`
- `Casino.MakeInAppPurchaseRequest.store_iap_id (string, optional)`
- `Casino.MakeInAppPurchaseResponse.provider_purchase_id (string, optional)`
- `Casino.MakeInAppPurchaseResponse.request_id (string, optional)`
- `Casino.NotifyPendingBundlesRequest.Bundle.Metadata.key (string, optional)`
- `Casino.NotifyPendingBundlesRequest.Bundle.id (string, optional)`
- `Casino.NotifyPurchasePaidRequest.Metadata.key (string, optional)`
- `Casino.NotifyPurchasePaidRequest.product_id (string, optional)`
- `Casino.NotifyPurchasePaidRequest.provider_purchase_id (string, optional)`
- `Casino.NotifyPurchasePaidRequest.purchase_id (string, optional)`
- `Casino.NotifyPurchasePaidRequest.request_id (string, optional)`
- `Casino.PendingExternalSdkPurchaseRequest.PendingExternalSdkPurchase.payment_id (string, required)`
- `Casino.PendingExternalSdkPurchaseRequest.PendingExternalSdkPurchase.product_id (string, required)`
- `Casino.PendingExternalSdkPurchaseRequest.PendingExternalSdkPurchase.request_id (string, required)`
- `Casino.TriggerDirectPurchaseOfferRequest.id (Casino.OfferId, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.product (Casino.IapProduct, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.template_id (int32, required)`
- `Casino.VouchersMakePurchaseRequest.item_id (int32, required)`

### Progression / state

- `Casino.LocalizePricesResponse.status (Casino.LocalizePricesResponse.Status, required)`
- `Casino.LocalizedPricePointsResponse.status (Casino.LocalizedPricePointsResponse.Status, optional)`
- `Casino.MakeInAppPurchaseResponse.status (Casino.MakeInAppPurchaseResponse.Status, required)`
- `Casino.TriggerDirectPurchaseOfferResponse.status (Casino.TriggerDirectPurchaseOfferResponse.Status, required)`
- `Casino.ValidatePostalCodeResponse.status (Casino.ValidatePostalCodeResponse.Status, required)`
- `Casino.VouchersMakePurchaseResponse.status (Casino.VouchersMakePurchaseResponse.Status, required)`

### Cost / input

- `Casino.HuuugePayPendingPurchaseRequest.price_point (uint64, optional)`
- `Casino.LocalizePricesResponse.localized_prices (Casino.LocalizedPrice, repeated)`
- `Casino.LocalizedPrice.display_price (int32, required)`
- `Casino.LocalizedPrice.price_point (int64, required)`
- `Casino.LocalizedPricePoint.display_price (string, optional)`
- `Casino.LocalizedPricePoint.localized_price_point (int64, optional)`
- `Casino.LocalizedPricePoint.price_point (int64, optional)`
- `Casino.LocalizedPricePointsRequest.price_points (int64, repeated)`
- `Casino.LocalizedPricePointsResponse.localized_price_points (Casino.LocalizedPricePoint, repeated)`
- `Casino.MakeInAppPurchaseRequest.local_price (double, optional)`
- `Casino.MakeInAppPurchaseRequest.localized_price_point (int64, optional)`
- `Casino.MakeInAppPurchaseRequest.lottery_ticket_color (Casino.LotteryColor, optional)`
- `Casino.PendingExternalSdkPurchaseRequest.PendingExternalSdkPurchase.price_point (uint64, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.news_feed (Casino.NewsFeedBanner, optional)`
- `Casino.VouchersMakePurchaseRequest.expected_price (int64, required)`

### Currency / balance

- `Casino.LocalizedPrice.currency_code (string, required)`
- `Casino.LocalizedPricePoint.currency_code (string, optional)`
- `Casino.MakeInAppPurchaseRequest.big_chips_value (Casino.Chips, optional)`
- `Casino.MakeInAppPurchaseRequest.chips_value (int64, optional)`
- `Casino.MakeInAppPurchaseRequest.diamonds_value (int64, optional)`
- `Casino.MakeInAppPurchaseRequest.local_currency_code (string, optional)`
- `Casino.MakeInAppPurchaseRequest.vault_balance (Casino.Chips, optional)`
- `Casino.MakeInAppPurchaseResponse.big_chips_value (Casino.Chips, optional)`
- `Casino.MakeInAppPurchaseResponse.chips_value (int64, optional)`
- `Casino.MakeInAppPurchaseResponse.diamonds_value (int64, optional)`
- `Casino.MakeInAppPurchaseResponse.piggy_bank_chips_delta (int64, optional)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance.chipsback (double, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance.show_chipsback_badge (bool, required)`

### Reward / output

- `Casino.MakeInAppPurchaseRequest.rewards_data (Casino.RewardsData, optional)`
- `Casino.MakeInAppPurchaseResponse.bank_bonus_days (uint32, optional)`
- `Casino.MakeInAppPurchaseResponse.rewards_data (Casino.RewardsData, optional)`
- `Casino.VouchersMakePurchaseRequest.expected_reward (Casino.Reward, repeated)`
- `Casino.VouchersMakePurchaseResponse.rewards_data (Casino.RewardsData, optional)`

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- `Casino.LocalizePricesRequest.chosen_country_code (string, required)`
- `Casino.LocalizedPricePoint.country_code (string, optional)`
- `Casino.LocalizedPricePointsRequest.country_code (string, optional)`
- `Casino.LoginResponse.PurchaseSupportedCountry.country_code (string, optional)`
- `Casino.LoginResponse.PurchaseSupportedCountry.country_name (string, optional)`
- `Casino.MakeInAppPurchaseRequest.CheckoutLocalizationData.country_code (string, optional)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.Insurance.cap (int64, required)`
- `Casino.UpdateDirectPurchaseOfferRequest.DirectPurchaseOffer.total_limit (int32, required)`
- `Casino.ValidatePostalCodeRequest.country (string, required)`

### Other structural fields

- `Casino.HuuugePayPendingPurchaseRequest.Metadata.value (string, optional)`
- `Casino.HuuugePayPendingPurchaseRequest.metadata (Casino.HuuugePayPendingPurchaseRequest.Metadata, repeated)`
- `Casino.LocalizePricesRequest.chosen_zip_code (string, optional)`
- `Casino.LocalizePricesResponse.error_code (int32, optional)`
- `Casino.LocalizePricesResponse.validation_error (Casino.ValidationError, optional)`
- `Casino.LocalizedPricePoint.fraction_digits (int32, optional)`
- `Casino.LocalizedPricePointsResponse.error_code (int32, optional)`
- `Casino.MakeInAppPurchaseRequest.OfferData.type (int32, required)`
- `Casino.MakeInAppPurchaseRequest.OfferData.version (int64, optional)`
- `Casino.MakeInAppPurchaseRequest.checkout_localization_data (Casino.MakeInAppPurchaseRequest.CheckoutLocalizationData, optional)`
- `Casino.MakeInAppPurchaseRequest.data (bytes, optional)`
- `Casino.MakeInAppPurchaseRequest.iap_type (Casino.MakeInAppPurchaseRequest.IapType, optional)`
- `Casino.MakeInAppPurchaseRequest.is_purchase_from_appcharge_sdk (bool, optional)`
- `Casino.MakeInAppPurchaseRequest.is_purchase_from_huuuge_pay (bool, optional)`
- `Casino.MakeInAppPurchaseRequest.is_purchase_from_samsung (bool, optional)`
- `Casino.MakeInAppPurchaseRequest.is_purchase_from_web (bool, optional)`
- `Casino.MakeInAppPurchaseRequest.mini_pass_data (Casino.MakeInAppPurchaseRequest.MiniPassData, optional)`
- `Casino.MakeInAppPurchaseRequest.mode (Casino.MakeInAppPurchaseRequest.Mode, required)`
- `Casino.MakeInAppPurchaseRequest.offer_data (Casino.MakeInAppPurchaseRequest.OfferData, optional)`
- `Casino.MakeInAppPurchaseRequest.paid_offer (Casino.PaidOffer, optional)`
- `Casino.MakeInAppPurchaseRequest.payment_flow (string, optional)`
- `Casino.MakeInAppPurchaseRequest.stripe_customer_data (Casino.StripeCustomerData, optional)`
- `Casino.MakeInAppPurchaseResponse.Checkout.payment_provider (string, optional)`
- `Casino.MakeInAppPurchaseResponse.Checkout.url (string, optional)`
- `Casino.MakeInAppPurchaseResponse.checkout (Casino.MakeInAppPurchaseResponse.Checkout, optional)`
- `Casino.MakeInAppPurchaseResponse.end_of_day (int32, optional)`
- `Casino.MakeInAppPurchaseResponse.error_code (int32, optional)`
- `Casino.MakeInAppPurchaseResponse.extra_params (Casino.KeyValue, repeated)`
- `Casino.MakeInAppPurchaseResponse.promo_code (bool, optional)`
- `Casino.MakeInAppPurchaseResponse.stripe_data (Casino.StripeData, optional)`
- `Casino.MakeInAppPurchaseResponse.update_shop_request (Casino.UpdateShopRequest, optional)`
- `Casino.MakeInAppPurchaseResponse.validation_errors (Casino.ValidationError, optional)`
- `Casino.NotifyPendingBundlesRequest.Bundle.Metadata.value (string, optional)`
- `Casino.NotifyPendingBundlesRequest.Bundle.item (Casino.Item, repeated)`
- `Casino.NotifyPendingBundlesRequest.Bundle.metadata (Casino.NotifyPendingBundlesRequest.Bundle.Metadata, repeated)`
- `Casino.NotifyPendingBundlesRequest.Bundle.source (string, optional)`
- `Casino.NotifyPendingBundlesRequest.bundle (Casino.NotifyPendingBundlesRequest.Bundle, repeated)`
- `Casino.NotifyPurchasePaidRequest.Metadata.value (string, optional)`
- `Casino.NotifyPurchasePaidRequest.metadata (Casino.NotifyPurchasePaidRequest.Metadata, repeated)`
- `Casino.NotifyPurchasePaidRequest.payment_flow (string, optional)`
- … 19 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `LOT-20260827-A`:

- `AppServer.MakeInAppPurchase` — 16 (8 request, 8 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateShopRequest.expected_next_purchase` | 89 | 89 | 1 | constant-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.id.config_id` | 12 | 12 | 4 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.id.offer_type` | 12 | 12 | 1 | constant-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.config_id` | 12 | 12 | 4 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.created_at` | 12 | 12 | 1 | constant-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.item[].metadata[].key` | 12 | 184 | 17 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.item[].metadata[].value` | 12 | 184 | 31 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.item[].source` | 12 | 81 | 1 | constant-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.item[].type` | 12 | 81 | 9 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.item[].value` | 12 | 81 | 19 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.metadata[].key` | 12 | 20 | 2 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.metadata[].value` | 12 | 20 | 6 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.product_id` | 12 | 12 | 3 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.signature` | 12 | 12 | 4 | varying-in-session |
| `Casino.TriggerDirectPurchaseOfferRequest.paid_offer.source` | 12 | 12 | 1 | constant-in-session |
| `Casino.TriggerDirectPurchaseOfferResponse.status` | 12 | 12 | 2 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.big_chips_value.value` | 8 | 8 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.chips_value` | 8 | 8 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.local_currency_code` | 8 | 8 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.mode` | 8 | 8 | 2 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.product_id` | 8 | 8 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.request_id` | 8 | 8 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.status` | 8 | 8 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.checkout_localization_data` | 4 | n/a | n/a | not-assessed |
| `Casino.MakeInAppPurchaseRequest.data` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.diamonds_value` | 4 | 4 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.local_price` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.lottery_ticket_color` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.request_id` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.rewards_data.reward[].id` | 4 | 4 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseRequest.rewards_data.reward[].loyalty_points` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseRequest.store_iap_id` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.provider_purchase_id` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.reward[].id` | 4 | 8 | 2 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.reward[].inventory_delta.amount` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.reward[].inventory_delta.id` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.reward[].loyalty_points` | 4 | 4 | 4 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.state_info.extra_items.extra_items[].type` | 4 | 8 | 2 | varying-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.state_info.extra_items.extra_items[].value[].level.levels_amount` | 4 | 4 | 1 | constant-in-session |
| `Casino.MakeInAppPurchaseResponse.rewards_data.state_info.extra_items.extra_items[].value[].level.target_level` | 4 | 4 | 1 | constant-in-session |
| … | | | | 37 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: localize price/offer -> initiate `MakeInAppPurchase`/voucher purchase -> checkout response or external SDK handoff -> pending/paid notification -> reward delivery handled by shared reward messages.
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

- Open purchase detail and proceed only to the platform checkout preview, then cancel before authorization.
- Mark offer click, checkout shown and checkout cancelled separately.
- Inspect localized currency/price variants only through normal UI/account settings.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
