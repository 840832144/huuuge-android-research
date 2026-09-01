# Authentication / Account / Consent

Connect/login/logout, external authentication mappings, refresh tokens, direct webshop login links, device registration and consent state.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **90/100 — substantial live structure**
- Primary live samples: **6** from `20260901_160002`
- Cross-cutting live samples: **1**
- Live endpoints / schema endpoints: **4 / 17**
- Live populated field paths: **186**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `HuuugeLogin.proto`, `Services.proto`, `Sweepstakes.proto`
- Services: `AppClient`, `AppServer`, `HuuugeLogin`
- Related message types: **59**

- `Casino.AcceptedUserCentricsTagRequest` (AppClient.proto)
- `Casino.AuthenticationRefreshTokenRequest` (AppServer.proto)
- `Casino.AuthenticationRefreshTokenResponse` (AppServer.proto)
- `Casino.ConnectFacebookRequest` (AppServer.proto)
- `Casino.ConnectFacebookResponse` (AppServer.proto)
- `Casino.ConnectWithFirebaseRequest` (AppServer.proto)
- `Casino.ConnectWithFirebaseResponse` (AppServer.proto)
- `Casino.DirectWebshopLoginLinkRequest` (HuuugeLogin.proto)
- `Casino.DirectWebshopLoginLinkResponse` (HuuugeLogin.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.ExternalAuthMappingList` (AppServer.proto)
- `Casino.FacebookLoginData` (AppServer.proto)
- `Casino.IdfaConsentRequest` (AppServer.proto)
- `Casino.IdfaConsentResponse` (AppServer.proto)
- `Casino.LoginRequest` (AppServer.proto)
- `Casino.LoginResponse` (AppServer.proto)
- `Casino.LoginResponse.AdminBonus` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ClubGuard` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.CollectiblesMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.VaultMissedInfo` (AppServer.proto)
- `Casino.LoginResponse.NotFinishedPayment` (AppServer.proto)
- `Casino.LoginResponse.PurchaseSupportedCountry` (AppServer.proto)
- `Casino.LoginResponse.RecommendedGame` (AppServer.proto)
- `Casino.LoginResponse.ScalabilityMultipliers` (AppServer.proto)
- `Casino.LoginResponse.ScalabilityMultipliers.MultiplierData` (AppServer.proto)
- `Casino.LoginResponse.ScalabilityMultipliers.MultiplierEntry` (AppServer.proto)
- `Casino.LoginResponse.ServerInfo` (AppServer.proto)
- `Casino.LoginResponse.Tutorial` (AppServer.proto)
- `Casino.LoginResponse.WebSupportedCountry` (AppServer.proto)
- `Casino.LoginResponse.WebSupportedCountryResolution` (AppServer.proto)
- `Casino.LoginViaGameRequest` (AppServer.proto)
- `Casino.LoginViaGameResponse` (AppServer.proto)
- `Casino.LogoutRequest` (AppServer.proto)
- `Casino.LogoutResponse` (AppServer.proto)
- `Casino.PersonalizedAdsPostponeConsent` (AppServer.proto)
- `Casino.PersonalizedAdsPostponeConsentRequest` (AppServer.proto)
- `Casino.RegisterDeviceRequest` (AppServer.proto)
- `Casino.RegisterDeviceResponse` (AppServer.proto)
- `Casino.SignInWithAppleCredentials` (AppServer.proto)
- `Casino.SignInWithAppleLinkInfoRequest` (AppClient.proto)
- `Casino.SignInWithAppleRequest` (AppServer.proto)
- `Casino.SignInWithAppleResponse` (AppServer.proto)
- `Casino.SignInWithIDToken` (AppServer.proto)
- `Casino.SweepstakesUpdatePublishWinnerDataConsentRequest` (Sweepstakes.proto)
- `Casino.SweepstakesUpdatePublishWinnerDataConsentResponse` (Sweepstakes.proto)
- `Casino.UpdateExternalAuthMappingRequest` (AppClient.proto)
- `Casino.UpdateUserCentricsTagRequest` (AppServer.proto)
- `Casino.UserConsent` (AppServer.proto)
- `Casino.UserConsentsRequest` (AppServer.proto)

## RPC and flow structure

Schema flow: connect/login/auth refresh establishes session/profile/missed info -> device/consent/auth mappings update -> optional webshop link generation -> logout/disconnect ends session.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.Login` | `Casino.LoginRequest` | `Casino.LoginResponse` | 1 | 1 | observed-live |
| `AppServer.ConnectFacebook` | `Casino.ConnectFacebookRequest` | `Casino.ConnectFacebookResponse` | 0 | 0 | schema-only |
| `AppServer.RegisterDevice` | `Casino.RegisterDeviceRequest` | `Casino.RegisterDeviceResponse` | 1 | 1 | observed-live |
| `AppServer.SetUserConsents` | `Casino.UserConsentsRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.SignInWithApple` | `Casino.SignInWithAppleRequest` | `Casino.SignInWithAppleResponse` | 0 | 0 | schema-only |
| `AppServer.PersonalizedAdsPostponeConsent` | `Casino.PersonalizedAdsPostponeConsentRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.IdfaConsent` | `Casino.IdfaConsentRequest` | `Casino.IdfaConsentResponse` | 0 | 0 | schema-only |
| `AppServer.LoginViaGame` | `Casino.LoginViaGameRequest` | `Casino.LoginViaGameResponse` | 0 | 0 | schema-only |
| `AppServer.ConnectWithFirebase` | `Casino.ConnectWithFirebaseRequest` | `Casino.ConnectWithFirebaseResponse` | 0 | 0 | schema-only |
| `AppServer.AuthenticationRefreshToken` | `Casino.AuthenticationRefreshTokenRequest` | `Casino.AuthenticationRefreshTokenResponse` | 0 | 0 | schema-only |
| `AppServer.Logout` | `Casino.LogoutRequest` | `Casino.LogoutResponse` | 0 | 0 | schema-only |
| `AppServer.UpdateUserCentricsTag` | `Casino.UpdateUserCentricsTagRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.SignInWithAppleLinkInfo` | `Casino.SignInWithAppleLinkInfoRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.AcceptedUserCentricsTag` | `Casino.AcceptedUserCentricsTagRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.NotAcceptedUserCentricsTag` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.UpdateExternalAuthMapping` | `Casino.UpdateExternalAuthMappingRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `HuuugeLogin.GenerateDirectWebshopLoginLink` | `Casino.DirectWebshopLoginLinkRequest` | `Casino.DirectWebshopLoginLinkResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.FacebookLoginData.client_id (string, required)`
- `Casino.LoginRequest.user_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.milestone_id (int32, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.challenge_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.conquest_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.challenge_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.conquest_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.conquest_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.game_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.game_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.VaultMissedInfo.vault_id (int64, required)`
- `Casino.LoginResponse.NotFinishedPayment.product_id (string, required)`
- `Casino.LoginResponse.NotFinishedPayment.request_id (string, required)`
- `Casino.LoginResponse.NotFinishedPayment.stripe_payment_id (string, optional)`
- `Casino.LoginResponse.user_id (int64, optional)`
- `Casino.SignInWithAppleLinkInfoRequest.apple_user_id (string, optional)`
- `Casino.SweepstakesUpdatePublishWinnerDataConsentRequest.draw_id (string, required)`

### Progression / state

- `Casino.AuthenticationRefreshTokenResponse.status (Casino.AuthenticationRefreshTokenResponse.Status, required)`
- `Casino.ConnectFacebookResponse.email_marketing_status (Casino.EmailMarketingStatus, optional)`
- `Casino.ConnectFacebookResponse.name_changes_count (int32, optional)`
- `Casino.ConnectFacebookResponse.status (Casino.ConnectFacebookResponse.Status, required)`
- `Casino.ConnectWithFirebaseResponse.status (Casino.ConnectWithFirebaseResponse.Status, required)`
- `Casino.DirectWebshopLoginLinkResponse.status (Casino.DirectWebshopLoginLinkResponse.Status, optional)`
- `Casino.IdfaConsentResponse.status (Casino.IdfaConsentResponse.Status, required)`
- `Casino.LoginRequest.tutorial (bool, optional)`
- `Casino.LoginResponse.MissedInfo.CollectiblesMissedInfo.new_theme_level (int32, optional)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.eventCompleted (bool, optional)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.milestones_count (int32, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.challenge_progress (Casino.ConquestChallengeProgress, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.event_progress (Casino.ConquestEventProgress, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.event_completed (bool, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.lap_completed (bool, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.event_completed (bool, optional)`
- `Casino.LoginResponse.ScalabilityMultipliers.MultiplierEntry.minLevel (int32, required)`
- `Casino.LoginResponse.ServerInfo.count (int32, required)`
- `Casino.LoginResponse.collection_event_state (Casino.CollectionEventState, optional)`
- `Casino.LoginResponse.email_marketing_status (Casino.EmailMarketingStatus, optional)`
- `Casino.LoginResponse.friend_count (int32, optional)`
- `Casino.LoginResponse.friend_request_notification_count (int32, optional)`
- `Casino.LoginResponse.idfa_count (int32, optional)`
- `Casino.LoginResponse.in_app_completed (int64, optional)`
- `Casino.LoginResponse.name_changes_count (int32, optional)`
- `Casino.LoginResponse.purchase_supported_countries (Casino.LoginResponse.PurchaseSupportedCountry, repeated)`
- `Casino.LoginResponse.rate_us_trigger_level (uint64, optional)`
- `Casino.LoginResponse.session_count (int64, optional)`
- `Casino.LoginResponse.status (Casino.LoginResponse.Status, required)`
- `Casino.LoginResponse.tutorial (Casino.LoginResponse.Tutorial, optional)`
- `Casino.LoginResponse.web_supported_countries (Casino.LoginResponse.WebSupportedCountry, repeated)`
- `Casino.LoginViaGameResponse.status (Casino.LoginViaGameResponse.Status, required)`
- `Casino.LogoutResponse.status (Casino.LogoutResponse.Status, required)`
- `Casino.PersonalizedAdsPostponeConsent.count (uint32, optional)`
- `Casino.RegisterDeviceResponse.status (Casino.RegisterDeviceResponse.Status, required)`
- `Casino.SignInWithAppleResponse.status (Casino.SignInWithAppleResponse.Status, required)`
- `Casino.SweepstakesUpdatePublishWinnerDataConsentResponse.status (Casino.SweepstakesUpdatePublishWinnerDataConsentResponse.Status, required)`

### Cost / input

- `Casino.AuthenticationRefreshTokenRequest.refresh_token (string, required)`
- `Casino.AuthenticationRefreshTokenResponse.access_and_refresh_token (Casino.AccessAndRefreshToken, optional)`
- `Casino.ConnectWithFirebaseRequest.id_token (string, required)`
- `Casino.FacebookLoginData.facebook_token (string, required)`
- `Casino.LoginRequest.access_token (string, optional)`
- `Casino.LoginRequest.push_notification_token (string, optional)`
- `Casino.LoginRequest.sign_in_with_id_token (Casino.SignInWithIDToken, optional)`
- `Casino.LoginResponse.NotFinishedPayment.price_point (uint64, required)`
- `Casino.LoginResponse.access_and_refresh_token (Casino.AccessAndRefreshToken, optional)`
- `Casino.LoginResponse.sweepstakes_update (Casino.SweepstakesUpdateRequest, optional)`
- `Casino.LoginViaGameRequest.token (string, required)`
- `Casino.LogoutRequest.refresh_token (string, required)`
- `Casino.RegisterDeviceRequest.push_notification_token (string, optional)`
- `Casino.SignInWithAppleCredentials.id_token (string, required)`
- `Casino.SignInWithIDToken.id_token (string, required)`

### Currency / balance

- `Casino.ConnectFacebookResponse.big_chips_delta (Casino.Chips, optional)`
- `Casino.ConnectFacebookResponse.chips_delta (int64, optional)`
- `Casino.ConnectWithFirebaseResponse.big_chips_delta (Casino.Chips, optional)`
- `Casino.ConnectWithFirebaseResponse.chips_delta (int64, optional)`
- `Casino.LoginResponse.AdminBonus.chips (int64, optional)`
- `Casino.LoginResponse.AdminBonus.diamonds (int64, optional)`
- `Casino.LoginResponse.MissedInfo.chips (Casino.Chips, optional)`
- `Casino.LoginResponse.MissedInfo.legacy_chips (int64, optional)`
- `Casino.LoginResponse.free_diamonds_collected (bool, optional)`
- `Casino.LoginResponse.piggy_bank_chips (uint64, optional)`
- `Casino.SignInWithAppleResponse.big_chips_delta (Casino.Chips, optional)`
- `Casino.SignInWithAppleResponse.chips_delta (int64, optional)`

### Reward / output

- `Casino.IdfaConsentResponse.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.challenge_reward (Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.event_reward (Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.VaultMissedInfo.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.rewards_data (Casino.RewardsData, optional)`
- `Casino.LoginResponse.MissedInfo.rewards_info (Casino.PlayerRewardInfo, repeated)`
- `Casino.LoginResponse.admin_bonus (Casino.LoginResponse.AdminBonus, optional)`
- `Casino.LoginResponse.bank_bonus (Casino.BankBonus, repeated)`
- `Casino.LoginResponse.big_facebook_bonus (Casino.Chips, optional)`
- `Casino.LoginResponse.daily_bonus (Casino.DailyBonus, optional)`
- `Casino.LoginResponse.facebook_bonus (int64, optional)`
- `Casino.LoginResponse.ftue_completion_reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.hourly_bonus_video_ad_watched (bool, optional)`
- `Casino.LoginResponse.mystery_pending_rewards (int32, optional)`
- `Casino.LoginResponse.mystery_reward_level (int64, optional)`
- `Casino.LoginResponse.next_mystery_reward (Casino.NextMysteryReward, optional)`
- `Casino.LoginResponse.rate_us_bonus (bool, optional)`
- `Casino.LoginResponse.rewards_data (Casino.RewardsData, optional)`

### Timing / reset / expiry

- `Casino.LoginRequest.time_zone (int32, required)`
- `Casino.LoginResponse.create_account_timestamp (int32, optional)`
- `Casino.LoginResponse.daily_bonus_timer (int32, optional)`
- `Casino.LoginResponse.last_purchase_timestamp (int32, optional)`
- `Casino.LoginResponse.piggy_bank_timer (uint32, optional)`
- `Casino.LoginResponse.shop_bonus_timer (int32, optional)`
- `Casino.LoginResponse.time_ms (int64, optional)`
- `Casino.PersonalizedAdsPostponeConsent.timestamp (uint32, optional)`

### Segment / eligibility / limit

- `Casino.FacebookLoginData.limited_login (bool, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.is_eligible (bool, optional)`
- `Casino.LoginResponse.MissedInfo.unlocked_feature (Casino.LockedFeature, repeated)`
- `Casino.LoginResponse.PurchaseSupportedCountry.country_code (string, optional)`
- `Casino.LoginResponse.PurchaseSupportedCountry.country_name (string, optional)`
- `Casino.LoginResponse.WebSupportedCountry.country_code (string, required)`
- `Casino.LoginResponse.WebSupportedCountry.country_name (string, required)`
- `Casino.LoginResponse.WebSupportedCountryResolution.country_code (string, required)`
- `Casino.LoginResponse.country (string, optional)`
- `Casino.LoginResponse.us_country_state (string, optional)`
- `Casino.LoginResponse.web_supported_country_resolution (Casino.LoginResponse.WebSupportedCountryResolution, optional)`

### Other structural fields

- `Casino.AcceptedUserCentricsTagRequest.tag (string, required)`
- `Casino.AuthenticationRefreshTokenResponse.error_code (int32, optional)`
- `Casino.ConnectFacebookRequest.facebook_login_data (Casino.FacebookLoginData, required)`
- `Casino.ConnectFacebookRequest.relink (bool, optional)`
- `Casino.ConnectFacebookResponse.error_code (int32, optional)`
- `Casino.ConnectFacebookResponse.facebook_data (Casino.FacebookData, repeated)`
- `Casino.ConnectFacebookResponse.profile (Casino.PlayerProfile, optional)`
- `Casino.ConnectWithFirebaseRequest.relink (bool, optional)`
- `Casino.ConnectWithFirebaseResponse.error_code (int32, optional)`
- `Casino.ConnectWithFirebaseResponse.profile (Casino.PlayerProfile, optional)`
- `Casino.DirectWebshopLoginLinkRequest.is_vip (bool, optional)`
- `Casino.DirectWebshopLoginLinkResponse.error_code (int32, optional)`
- `Casino.DirectWebshopLoginLinkResponse.redirect_url (string, optional)`
- `Casino.ExternalAuthMappingList.player_auths (Casino.ExternalAuthMappingList.SupportedAuth, repeated)`
- `Casino.IdfaConsentRequest.idfa (string, required)`
- `Casino.IdfaConsentResponse.error_code (int32, optional)`
- `Casino.LoginRequest.apple_credentials (Casino.SignInWithAppleCredentials, optional)`
- `Casino.LoginRequest.common_config_hash (bytes, optional)`
- `Casino.LoginRequest.device_model (string, required)`
- `Casino.LoginRequest.device_os_version (string, required)`
- `Casino.LoginRequest.facebook_login_data (Casino.FacebookLoginData, optional)`
- `Casino.LoginRequest.language (string, required)`
- `Casino.LoginRequest.password (string, optional)`
- `Casino.LoginRequest.platform_config_hash (bytes, optional)`
- `Casino.LoginRequest.reconnect (bool, optional)`
- `Casino.LoginResponse.AdminBonus.inventory (Casino.InventoryEntry, repeated)`
- `Casino.LoginResponse.MissedInfo.ClubGuard.action (Casino.ClubsProto.ClubNotificationRequest.ClubGuard, optional)`
- `Casino.LoginResponse.MissedInfo.ClubGuard.club_autodeleted (bool, optional)`
- `Casino.LoginResponse.MissedInfo.CollectionEventMissedInfo.gfx_set (int32, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup.club_info (Casino.ClubInfo, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup.club_info (Casino.ClubInfo, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup.tournament_place (int32, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.club_info (Casino.ClubInfo, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.challenge_popup (Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengePopup, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.event_popup (Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventPopup, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.milestone_idx (int32, repeated)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.moves_used (int32, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameBulkMissedInfo.steps_moved (int32, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.milestone (Casino.MiniGameMilestone, required)`
- `Casino.LoginResponse.MissedInfo.black_lottery (Casino.BlackLotteryMissedInfo, repeated)`
- … 86 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260901_160002`:

- `AppServer.Login` — 2 (1 request, 1 response)
- `AppServer.RegisterDevice` — 2 (1 request, 1 response)
- `AppClient.NotAcceptedUserCentricsTag` — 1 (1 request, 0 response)
- `AppClient.UpdateExternalAuthMapping` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.LoginRequest.common_config_hash` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.device_model` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.device_os_version` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.language` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.password` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.platform_config_hash` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.reconnect` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.time_zone` | 1 | 1 | 1 | single-observation |
| `Casino.LoginRequest.user_id` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.additional_data` | 1 | n/a | n/a | not-assessed |
| `Casino.LoginResponse.benefits_not_shown` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_join_incentive` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_season.club_season_id` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_season.end_time` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_season.reward[].reward[].action` | 1 | 26 | 2 | single-observation |
| `Casino.LoginResponse.club_season.reward[].reward[].from_place` | 1 | 56 | 5 | single-observation |
| `Casino.LoginResponse.club_season.reward[].reward[].lobby_bonuses_frac_delta` | 1 | 56 | 56 | single-observation |
| `Casino.LoginResponse.consent[].type` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.consent[].version` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.country` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.create_account_timestamp` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.daily_bonus_timer` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.econ_stats.stat[].key` | 1 | 36 | 36 | single-observation |
| `Casino.LoginResponse.econ_stats.stat[].value_double` | 1 | 12 | 12 | single-observation |
| `Casino.LoginResponse.econ_stats.stat[].value_int` | 1 | 24 | 1 | single-observation |
| `Casino.LoginResponse.email_marketing_status` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.end_of_day` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.external_auth_mapping.player_auths[]` | 1 | 2 | 2 | single-observation |
| `Casino.LoginResponse.external_tag[]` | 1 | 3 | 3 | single-observation |
| `Casino.LoginResponse.facebook_data[].facebook_app_id` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.facebook_data[].facebook_id` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.free_diamonds_collected` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.friend_request_notification_count` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.ftue` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.game_category[].flags` | 1 | 7 | 1 | single-observation |
| `Casino.LoginResponse.game_category[].game_category` | 1 | 7 | 6 | single-observation |
| `Casino.LoginResponse.game_category[].game_subcategory` | 1 | 2 | 2 | single-observation |
| `Casino.LoginResponse.game_category[].lobby_size` | 1 | 7 | 2 | single-observation |
| `Casino.LoginResponse.idfa_count` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.in_app_completed` | 1 | 1 | 1 | single-observation |
| … | | | | 146 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: connect/login/auth refresh establishes session/profile/missed info -> device/consent/auth mappings update -> optional webshop link generation -> logout/disconnect ends session.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/data-splash-assets.zpk`
- ZPK asset: `assets/data-splash-i18n.zpk`
- ZPK asset: `assets/data-splash.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- No deliberate re-login is needed for cataloging; capture only a natural cold start with manifest/markers.
- Open account/settings/consent screens without exposing credentials in committed artifacts.
- Keep tokens, account ids and identity fields local and redacted.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
