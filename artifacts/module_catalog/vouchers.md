# Vouchers

Voucher shop items, voucher-priced purchases, response/reward state and tutorial acknowledgement.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `LOT-20260827-A`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 1**
- Live populated field paths: **0**

## Schema scope

- Proto files: `AppClient.proto`, `Services.proto`, `Vouchers.proto`
- Services: `AppServer`
- Related message types: **7**

- `Casino.AddDciEventRequest.VouchersEvent` (AppClient.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.VouchersMakePurchaseRequest` (Vouchers.proto)
- `Casino.VouchersMakePurchaseResponse` (Vouchers.proto)
- `Casino.VouchersShopItem` (Vouchers.proto)
- `Casino.VouchersWalletItem` (Vouchers.proto)

## RPC and flow structure

Schema flow: event/shop configuration publishes voucher balance/items -> purchase consumes voucher input -> response returns state/reward -> tutorial acknowledgement.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.VouchersTutorialShown` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.VouchersMakePurchaseRequest.item_id (int32, required)`
- `Casino.VouchersShopItem.badge_id (Casino.VouchersBadgeId, required)`
- `Casino.VouchersShopItem.item_id (int32, required)`
- `Casino.VouchersShopItem.text_id (string, required)`
- `Casino.VouchersWalletItem.text_id (string, required)`

### Progression / state

- `Casino.AddDciEventRequest.VouchersEvent.points (int64, required)`
- `Casino.AddDciEventRequest.VouchersEvent.tutorial_completed (bool, optional)`
- `Casino.VouchersMakePurchaseResponse.status (Casino.VouchersMakePurchaseResponse.Status, required)`

### Cost / input

- `Casino.VouchersMakePurchaseRequest.expected_price (int64, required)`
- `Casino.VouchersShopItem.price (int64, required)`
- `Casino.VouchersWalletItem.price (int64, optional)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.VouchersMakePurchaseRequest.expected_reward (Casino.Reward, repeated)`
- `Casino.VouchersMakePurchaseResponse.rewards_data (Casino.RewardsData, optional)`
- `Casino.VouchersShopItem.reward (Casino.Reward, repeated)`
- `Casino.VouchersWalletItem.reward (Casino.Reward, repeated)`

### Timing / reset / expiry

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.AddDciEventRequest.VouchersEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.VouchersEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.VouchersEvent.shop_item (Casino.VouchersShopItem, repeated)`
- `Casino.AddDciEventRequest.VouchersEvent.wallet_item (Casino.VouchersWalletItem, repeated)`
- `Casino.VouchersMakePurchaseResponse.error_code (int32, optional)`
- `Casino.VouchersMakePurchaseResponse.plus_point_delta (int64, optional)`
- `Casino.VouchersMakePurchaseResponse.wallet_item (Casino.VouchersWalletItem, optional)`
- `Casino.VouchersShopItem.art_path (string, repeated)`
- `Casino.VouchersShopItem.text_path (string, repeated)`
- `Casino.VouchersShopItem.total_usd_value (double, optional)`
- `Casino.VouchersWalletItem.art_path (string, repeated)`
- `Casino.VouchersWalletItem.purchase_date (int64, required)`
- `Casino.VouchersWalletItem.text_path (string, repeated)`
- `Casino.VouchersWalletItem.total_usd_value (double, optional)`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: event/shop configuration publishes voucher balance/items -> purchase consumes voucher input -> response returns state/reward -> tutorial acknowledgement.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open voucher event/shop, balance, item detail and tutorial screens with markers.
- Inspect cost, limits and expiry for several items.
- Make one normal voucher purchase only if already intended, marking before/after.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
