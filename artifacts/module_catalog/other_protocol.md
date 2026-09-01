# Other / Unclassified Protocol Families

Transport and endpoints not yet assigned to a stable gameplay/business module; retained so unknown structure is never discarded.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **85/100 — substantial live structure**
- Primary live samples: **10** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **5 / 13**
- Live populated field paths: **20**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Rpc.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **92**

- `Casino.AccessAndRefreshToken` (AppServer.proto)
- `Casino.AddCetRequest` (AppClient.proto)
- `Casino.AdditionalData` (Common.proto)
- `Casino.Art` (Common.proto)
- `Casino.Art.Package` (Common.proto)
- `Casino.Avatar` (Common.proto)
- `Casino.Banner` (AppClient.proto)
- `Casino.Banner.DisplayScenario` (AppClient.proto)
- `Casino.BannerBase` (AppClient.proto)
- `Casino.BillingAddress` (AppServer.proto)
- `Casino.Bundle` (Common.proto)
- `Casino.Card` (Common.proto)
- `Casino.Cdn` (AppServer.proto)
- `Casino.ConfigHbiData` (Common.proto)
- `Casino.ConfigValue` (Common.proto)
- `Casino.CustomFields` (Common.proto)
- `Casino.DciConfigInfo` (Common.proto)
- `Casino.DciConfigurationId` (Common.proto)
- `Casino.EconomyStats` (Common.proto)
- `Casino.EditProfileRequest.AvatarFrame` (AppServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.ExecuteCommandRequest` (Common.proto)
- `Casino.ExecuteCommandResponse` (Common.proto)
- `Casino.Experimental` (Common.proto)
- `Casino.ExtraItem` (Common.proto)
- `Casino.ExtraItem.ExtraItemLevelLimited` (Common.proto)
- `Casino.ExtraItem.ExtraItemTimeLimited` (Common.proto)
- `Casino.ExtraItemsData` (Common.proto)
- `Casino.ExtraItemsQueue` (Common.proto)
- `Casino.FacebookData` (Common.proto)
- `Casino.ForceUpdate` (AppServer.proto)
- `Casino.FullScreenBanner` (AppClient.proto)
- `Casino.FullScreenBanner.DisplayScenario` (AppClient.proto)
- `Casino.Game` (Common.proto)
- `Casino.GameDef` (Common.proto)
- `Casino.GameInfo` (Common.proto)
- `Casino.GenericError` (Services.proto)
- `Casino.GetExtraItemsRequest` (AppServer.proto)
- `Casino.GetExtraItemsResponse` (AppServer.proto)
- `Casino.GetPushNotificationCategoriesResponse` (AppServer.proto)
- `Casino.HbiData` (Common.proto)
- `Casino.InvalidFieldError` (AppServer.proto)
- `Casino.InventoryEntry` (Common.proto)
- `Casino.Item` (Common.proto)
- `Casino.KeyValue` (Common.proto)
- `Casino.KeyValueElement` (Common.proto)
- `Casino.KeyValueMap` (Common.proto)
- `Casino.KeyValuePair` (Common.proto)
- `Casino.Leaderboard` (AppServer.proto)
- `Casino.LevelRange` (Common.proto)
- `Casino.LockedFeature` (AppServer.proto)
- `Casino.LogMessageRequest` (AppClient.proto)
- `Casino.LuaIntConversionOptions` (Common.proto)
- `Casino.MessageBoardEntry` (AppServer.proto)
- `Casino.Metadata` (Common.proto)
- `Casino.MiniGameMilestone` (Common.proto)
- `Casino.MissedInfoReadRequest` (AppServer.proto)
- `Casino.MissedInfoReadResponse` (AppServer.proto)
- `Casino.NewsFeedBanner` (AppClient.proto)
- `Casino.PaymentLocation` (AppServer.proto)
- `Casino.PendingItemsSet` (Common.proto)
- `Casino.PlayerDBProfile` (AppServer.proto)
- `Casino.ProfileStatistic` (AppServer.proto)
- `Casino.PromoLeaderboard` (AppServer.proto)
- `Casino.PromoLeaderboard.Title` (AppServer.proto)
- `Casino.RpcMessage` (Services.proto)
- `Casino.SendChatMessageRequest` (AppServer.proto)
- `Casino.SetPushNotificationCategoriesRequest` (AppServer.proto)
- `Casino.SetPushNotificationCategoriesResponse` (AppServer.proto)
- `Casino.SimpleRateUsInitRequest` (AppClient.proto)
- `Casino.SimpleRateUsState` (Common.proto)
- `Casino.SimpleRateUsTriggeredRequest` (AppServer.proto)
- `Casino.SimpleRateUsTriggeredResponse` (AppServer.proto)
- `Casino.StripeCustomerData` (AppServer.proto)
- `Casino.StripeData` (AppServer.proto)
- `Casino.Text` (Common.proto)
- `Casino.Token` (Common.proto)
- `Casino.UpdateBetsRequest.BetsOnFireConfig` (AppClient.proto)
- `Casino.UpdateFacebookTokenRequest` (AppServer.proto)
- `Casino.UpdateFacebookTokenResponse` (AppServer.proto)
- `Casino.UpdatePushNotificationStatusRequest` (AppServer.proto)
- `Casino.UpdatePushNotificationStatusResponse` (AppServer.proto)
- `Casino.ValidationError` (AppServer.proto)
- `Casino.VerifyPlayerIdentityRequest` (AppServer.proto)
- `Casino.VerifyPlayerIdentityRequest.Form` (AppServer.proto)
- `Casino.VerifyPlayerIdentityRequest.Form.IdentityDocument` (AppServer.proto)
- `Casino.VerifyPlayerIdentityRequest.Form.Person` (AppServer.proto)
- `Casino.VerifyPlayerIdentityRequest.Form.Person.Address` (AppServer.proto)
- `Casino.VerifyPlayerIdentityRequest.Form.Person.Email` (AppServer.proto)
- `Casino.VerifyPlayerIdentityResponse` (AppServer.proto)
- `Htf.RpcMessage` (Rpc.proto)

## RPC and flow structure

No single lifecycle is inferred. Each endpoint remains individually visible in `endpoints.csv` until live markers/static evidence justify moving it to a dedicated dossier.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.UpdateFacebookToken` | `Casino.UpdateFacebookTokenRequest` | `Casino.UpdateFacebookTokenResponse` | 1 | 1 | observed-live |
| `AppServer.SendChatMessage` | `Casino.SendChatMessageRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.ExecuteCommand` | `Casino.ExecuteCommandRequest` | `Casino.ExecuteCommandResponse` | 0 | 0 | schema-only |
| `AppServer.MissedInfoRead` | `Casino.MissedInfoReadRequest` | `Casino.MissedInfoReadResponse` | 0 | 0 | schema-only |
| `AppServer.UpdatePushNotificationStatus` | `Casino.UpdatePushNotificationStatusRequest` | `Casino.UpdatePushNotificationStatusResponse` | 0 | 0 | schema-only |
| `AppServer.GetPushNotificationCategories` | `Casino.EmptyRequest` | `Casino.GetPushNotificationCategoriesResponse` | 0 | 0 | schema-only |
| `AppServer.SetPushNotificationCategories` | `Casino.SetPushNotificationCategoriesRequest` | `Casino.SetPushNotificationCategoriesResponse` | 0 | 0 | schema-only |
| `AppServer.VerifyPlayerIdentity` | `Casino.VerifyPlayerIdentityRequest` | `Casino.VerifyPlayerIdentityResponse` | 0 | 0 | schema-only |
| `AppServer.GetExtraItems` | `Casino.GetExtraItemsRequest` | `Casino.GetExtraItemsResponse` | 2 | 2 | observed-live |
| `AppServer.SimpleRateUsTriggered` | `Casino.SimpleRateUsTriggeredRequest` | `Casino.SimpleRateUsTriggeredResponse` | 1 | 1 | observed-live |
| `AppClient.LogMessage` | `Casino.LogMessageRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.AddCet` | `Casino.AddCetRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.SimpleRateUsInit` | `Casino.SimpleRateUsInitRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |

## Structural fields

### Entity identifiers

- `Casino.Avatar.avatar_id (int64, required)`
- `Casino.Avatar.user_id (int64, required)`
- `Casino.Banner.DisplayScenario.id (int32, required)`
- `Casino.Banner.token_id (string, optional)`
- `Casino.Bundle.id (string, optional)`
- `Casino.ConfigHbiData.config_uuid (string, optional)`
- `Casino.ConfigHbiData.freeze_id (int32, optional)`
- `Casino.DciConfigInfo.segment_id (int64, required)`
- `Casino.DciConfigurationId.config_id (int64, required)`
- `Casino.EditProfileRequest.AvatarFrame.id (int32, optional)`
- `Casino.FacebookData.facebook_app_id (string, required)`
- `Casino.FacebookData.facebook_id (int64, required)`
- `Casino.FullScreenBanner.DisplayScenario.id (int32, required)`
- `Casino.GameInfo.room_id (uint64, optional)`
- `Casino.GameInfo.server_id (int64, required)`
- `Casino.HbiData.id (int64, optional)`
- `Casino.InventoryEntry.id (int32, required)`
- `Casino.KeyValue.key (int32, required)`
- `Casino.KeyValueElement.jackpot_id (uint32, repeated)`
- `Casino.KeyValueElement.key (int32, required)`
- `Casino.KeyValuePair.key (string, required)`
- `Casino.Leaderboard.player (Casino.LeaderboardPlayer, repeated)`
- `Casino.LockedFeature.id (uint32, required)`
- `Casino.Metadata.key (string, optional)`
- `Casino.MissedInfoReadRequest.black_lottery_id (int64, optional)`
- `Casino.MissedInfoReadRequest.collectibles_raffle_id (int64, optional)`
- `Casino.MissedInfoReadRequest.conquest_id (int64, optional)`
- `Casino.MissedInfoReadRequest.lottery_id (int64, optional)`
- `Casino.MissedInfoReadRequest.player_reward_id (int64, optional)`
- `Casino.MissedInfoReadRequest.tower_id (int64, optional)`
- `Casino.MissedInfoReadRequest.vault_id (int64, optional)`
- `Casino.PendingItemsSet.id (int64, optional)`
- `Casino.RpcMessage.user_id (int64, optional)`
- `Casino.SendChatMessageRequest.emot_id (int32, optional)`
- `Casino.SimpleRateUsState.last_triggered_id (int32, optional)`
- `Casino.SimpleRateUsTriggeredRequest.trigger_id (int32, optional)`
- `Casino.StripeData.payment_id (string, required)`
- `Casino.StripeData.secret_client_payment_id (string, required)`
- `Casino.UpdatePushNotificationStatusRequest.push_notification_id (string, required)`
- `Casino.VerifyPlayerIdentityRequest.Form.IdentityDocument.document_id (string, required)`

### Progression / state

- `Casino.Avatar.level (int32, optional)`
- `Casino.Card.rank (Casino.Card.CardRank, required)`
- `Casino.ExecuteCommandResponse.status (Casino.ExecuteCommandResponse.Status, required)`
- `Casino.ExtraItem.ExtraItemLevelLimited.target_level (int32, optional)`
- `Casino.ExtraItem.level (Casino.ExtraItem.ExtraItemLevelLimited, optional)`
- `Casino.GenericError.status (Casino.GenericError.Status, required)`
- `Casino.GetExtraItemsResponse.status (Casino.GetExtraItemsResponse.Status, required)`
- `Casino.GetPushNotificationCategoriesResponse.status (Casino.GetPushNotificationCategoriesResponse.Status, required)`
- `Casino.InventoryEntry.level (int32, optional)`
- `Casino.Leaderboard.own_rank (int64, optional)`
- `Casino.Leaderboard.own_rank_relative (int64, optional)`
- `Casino.LockedFeature.level (int64, required)`
- `Casino.MissedInfoReadResponse.status (Casino.MissedInfoReadResponse.Status, required)`
- `Casino.SetPushNotificationCategoriesResponse.status (Casino.SetPushNotificationCategoriesResponse.Status, required)`
- `Casino.SimpleRateUsInitRequest.state (Casino.SimpleRateUsState, optional)`
- `Casino.SimpleRateUsTriggeredResponse.state (Casino.SimpleRateUsState, optional)`
- `Casino.SimpleRateUsTriggeredResponse.status (Casino.SimpleRateUsTriggeredResponse.Status, required)`
- `Casino.UpdateBetsRequest.BetsOnFireConfig.spins_to_level_up (int32, required)`
- `Casino.UpdateFacebookTokenResponse.status (Casino.UpdateFacebookTokenResponse.Status, required)`
- `Casino.UpdatePushNotificationStatusResponse.status (Casino.UpdatePushNotificationStatusResponse.Status, required)`
- `Casino.VerifyPlayerIdentityResponse.status (Casino.VerifyPlayerIdentityResponse.Status, required)`

### Cost / input

- `Casino.AccessAndRefreshToken.access_token (string, required)`
- `Casino.AccessAndRefreshToken.refresh_token (string, required)`
- `Casino.ExtraItem.ExtraItemLevelLimited.levels_amount (int32, optional)`
- `Casino.InventoryEntry.amount (int64, optional)`
- `Casino.KeyValueElement.value_bet (int64, repeated)`
- `Casino.Token.token (string, required)`
- `Casino.UpdateBetsRequest.BetsOnFireConfig.level_requirement (int32, required)`

### Currency / balance

- `Casino.KeyValue.value_chips (Casino.Chips, optional)`
- `Casino.StripeData.currency (string, required)`
- `Casino.UpdateBetsRequest.BetsOnFireConfig.balance_factor (double, required)`

### Reward / output

- `Casino.AddCetRequest.lobby_bonuses (int64, required)`
- `Casino.Avatar.gift (Casino.Gift, optional)`
- `Casino.KeyValue.value_reward (Casino.Reward, repeated)`
- `Casino.MiniGameMilestone.reward (Casino.Reward, repeated)`
- `Casino.MissedInfoReadResponse.rewards_data (Casino.RewardsData, optional)`

### Timing / reset / expiry

- `Casino.Banner.active_cooldown_timestamp (int32, optional)`
- `Casino.Banner.cooldown (int32, optional)`
- `Casino.Cdn.timeout (uint32, required)`
- `Casino.ExtraItem.ExtraItemTimeLimited.duration (int32, optional)`
- `Casino.ExtraItem.ExtraItemTimeLimited.expire_time (int64, optional)`
- `Casino.ExtraItem.time (Casino.ExtraItem.ExtraItemTimeLimited, optional)`
- `Casino.FullScreenBanner.active_cooldown_timestamp (int32, optional)`
- `Casino.FullScreenBanner.cooldown (int32, optional)`
- `Casino.MessageBoardEntry.timestamp (uint32, required)`
- `Casino.SimpleRateUsState.cooldown_end_date (int64, optional)`

### Segment / eligibility / limit

- `Casino.Avatar.country_flag (int32, optional)`
- `Casino.Banner.display_limit (int32, optional)`
- `Casino.BillingAddress.country (string, required)`
- `Casino.ForceUpdate.country_code (string, optional)`
- `Casino.FullScreenBanner.display_limit (int32, optional)`
- `Casino.PaymentLocation.country_code (string, required)`
- `Casino.StripeCustomerData.selected_country (string, optional)`
- `Casino.VerifyPlayerIdentityRequest.Form.IdentityDocument.country (string, required)`
- `Casino.VerifyPlayerIdentityRequest.Form.Person.Address.country (string, required)`

### Other structural fields

- `Casino.AdditionalData.data (Casino.KeyValue, repeated)`
- `Casino.Art.Package.path (string, required)`
- `Casino.Art.Package.reskin_name (string, required)`
- `Casino.Art.Package.type (string, required)`
- `Casino.Art.Package.version (int32, required)`
- `Casino.Art.expiration_date (int64, required)`
- `Casino.Art.package (Casino.Art.Package, repeated)`
- `Casino.Avatar.avatar_frame (Casino.InventoryEntry, optional)`
- `Casino.Avatar.club_division (uint32, optional)`
- `Casino.Avatar.friend (bool, optional)`
- `Casino.Avatar.game_category (Casino.GameCategory, optional)`
- `Casino.Avatar.name (string, required)`
- `Casino.Avatar.online (bool, optional)`
- `Casino.Banner.DisplayScenario.display_priority (int32, required)`
- `Casino.Banner.branch_url_link (string, optional)`
- `Casino.Banner.cta_text (string, optional)`
- `Casino.Banner.deep_link (string, optional)`
- `Casino.Banner.scenario (Casino.Banner.DisplayScenario, repeated)`
- `Casino.Banner.url (string, repeated)`
- `Casino.Banner.url_link (string, optional)`
- `Casino.BannerBase.branch_url_link (string, optional)`
- `Casino.BannerBase.cta_text (string, optional)`
- `Casino.BannerBase.deep_link (string, optional)`
- `Casino.BannerBase.url (string, repeated)`
- `Casino.BannerBase.url_link (string, optional)`
- `Casino.BillingAddress.city (string, required)`
- `Casino.BillingAddress.line1 (string, required)`
- `Casino.BillingAddress.line2 (string, optional)`
- `Casino.BillingAddress.postal_code (string, required)`
- `Casino.BillingAddress.region (string, optional)`
- `Casino.Bundle.item (Casino.Item, repeated)`
- `Casino.Bundle.metadata (Casino.Metadata, repeated)`
- `Casino.Bundle.pending_items_set (Casino.PendingItemsSet, repeated)`
- `Casino.Bundle.source (string, optional)`
- `Casino.Card.suit (Casino.Card.CardSuit, required)`
- `Casino.Cdn.retry (uint32, required)`
- `Casino.Cdn.url (string, required)`
- `Casino.ConfigHbiData.config_identifier (int64, optional)`
- `Casino.ConfigHbiData.config_identifier_str (string, optional)`
- `Casino.ConfigHbiData.config_type (string, required)`
- … 158 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260901_160002`:

- `AppServer.GetExtraItems` — 4 (2 request, 2 response)
- `AppServer.UpdateFacebookToken` — 2 (1 request, 1 response)
- `AppServer.SimpleRateUsTriggered` — 2 (1 request, 1 response)
- `AppClient.LogMessage` — 1 (1 request, 0 response)
- `AppClient.SimpleRateUsInit` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.GetExtraItemsRequest.type` | 2 | 2 | 1 | constant-in-session |
| `Casino.GetExtraItemsResponse.extra_items.extra_items[].type` | 2 | 4 | 2 | varying-in-session |
| `Casino.GetExtraItemsResponse.extra_items.extra_items[].value[].time.duration` | 2 | 3 | 3 | varying-in-session |
| `Casino.GetExtraItemsResponse.extra_items.extra_items[].value[].time.expire_time` | 2 | 2 | 2 | varying-in-session |
| `Casino.GetExtraItemsResponse.extra_items.extra_items[].value[].time.value` | 2 | 3 | 1 | constant-in-session |
| `Casino.GetExtraItemsResponse.extra_items.extra_items[].value[].type` | 2 | 3 | 1 | constant-in-session |
| `Casino.GetExtraItemsResponse.status` | 2 | 2 | 1 | constant-in-session |
| `Casino.LogMessageRequest.text` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsInitRequest.state.cooldown_end_date` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsInitRequest.state.last_triggered_id` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsInitRequest.state.min_gap_end_date` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsTriggeredRequest.trigger_id` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsTriggeredResponse.state.cooldown_end_date` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsTriggeredResponse.state.last_triggered_id` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsTriggeredResponse.state.min_gap_end_date` | 1 | 1 | 1 | single-observation |
| `Casino.SimpleRateUsTriggeredResponse.status` | 1 | 1 | 1 | single-observation |
| `Casino.UpdateFacebookTokenRequest.facebook_login_data.client_id` | 1 | 1 | 1 | single-observation |
| `Casino.UpdateFacebookTokenRequest.facebook_login_data.facebook_token` | 1 | 1 | 1 | single-observation |
| `Casino.UpdateFacebookTokenRequest.facebook_login_data.limited_login` | 1 | 1 | 1 | single-observation |
| `Casino.UpdateFacebookTokenResponse.status` | 1 | 1 | 1 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: No single lifecycle is inferred. Each endpoint remains individually visible in `endpoints.csv` until live markers/static evidence justify moving it to a dedicated dossier.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Review new unknown endpoints after every marked capture and split coherent families into new dossiers.
- Preserve undecoded/empty/control messages as first-class evidence rather than dropping them.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
