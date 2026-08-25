# Player / Game / Lobby State

Player profiles/lists, friends/social presence, game lobby state, inactivity/focus/time sync, invitations, leaderboards and lobby navigation.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **90/100 — substantial live structure**
- Primary live samples: **245** from `20260825_182300`
- Cross-cutting live samples: **4**
- Live endpoints / schema endpoints: **7 / 29**
- Live populated field paths: **77**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **55**

- `Casino.AddFriendRequest` (AppServer.proto)
- `Casino.AddFriendResponse` (AppServer.proto)
- `Casino.ChatMessageHistoryRequest` (Common.proto)
- `Casino.ChatMessageRequest` (Common.proto)
- `Casino.CheckFriendsRequest` (AppServer.proto)
- `Casino.CheckFriendsResponse` (AppServer.proto)
- `Casino.ConnectRequest` (AppServer.proto)
- `Casino.ConnectResponse` (AppServer.proto)
- `Casino.DelayedReconnectionRequest` (AppClient.proto)
- `Casino.DisconnectRequest` (Common.proto)
- `Casino.DisconnectResponse` (Common.proto)
- `Casino.EditProfileRequest` (AppServer.proto)
- `Casino.EditProfileResponse` (AppServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.FocusChangeRequest` (AppServer.proto)
- `Casino.ForceLeaveGameRequest` (AppClient.proto)
- `Casino.Friend` (AppServer.proto)
- `Casino.Friend.Subscriber` (AppServer.proto)
- `Casino.FriendOnlineRequest` (AppClient.proto)
- `Casino.FriendRequestNotificationRequest` (AppClient.proto)
- `Casino.GameCategoryEntry` (AppServer.proto)
- `Casino.GameInvite` (AppServer.proto)
- `Casino.GameInviteRequest` (AppClient.proto)
- `Casino.GetFriendRequestsResponse` (AppServer.proto)
- `Casino.GetFriendsResponse` (AppServer.proto)
- `Casino.GetLeaderboardRequest` (AppServer.proto)
- `Casino.GetLeaderboardResponse` (AppServer.proto)
- `Casino.GetPlayerListRequest` (AppServer.proto)
- `Casino.GetPlayerListResponse` (AppServer.proto)
- `Casino.HandshakeRequest` (AppClient.proto)
- `Casino.HandshakeResponse` (AppClient.proto)
- `Casino.InviteFriendToGameRequest` (AppServer.proto)
- `Casino.InviteFriendToGameResponse` (AppServer.proto)
- `Casino.LeaderboardPlayer` (AppServer.proto)
- `Casino.LikeNotifyRequest` (AppClient.proto)
- `Casino.LikePlayerRequest` (AppServer.proto)
- `Casino.LikePlayerResponse` (AppServer.proto)
- `Casino.MutePlayerRequest` (AppServer.proto)
- `Casino.MutePlayerResponse` (AppServer.proto)
- `Casino.PinnedGame` (AppServer.proto)
- `Casino.PlayerListEntry` (AppServer.proto)
- `Casino.PlayerProfile` (AppServer.proto)
- `Casino.PlayerProfile.FameInfo` (AppServer.proto)
- `Casino.PlayerProfile.Rank` (AppServer.proto)
- `Casino.QueryPlayerRequest` (AppServer.proto)
- `Casino.QueryPlayerResponse` (AppServer.proto)
- `Casino.ReadMessageBoardRequest` (AppServer.proto)
- `Casino.ReadMessageBoardResponse` (AppServer.proto)
- `Casino.RemoveFriendRequest` (AppServer.proto)
- `Casino.RemoveFriendResponse` (AppServer.proto)
- `Casino.ResetUserInactivityRequest` (Common.proto)
- `Casino.SubscribeFriendNotificationsRequest` (AppServer.proto)
- `Casino.SubscribeFriendNotificationsResponse` (AppServer.proto)
- `Casino.SyncTimeResponse` (AppServer.proto)

## RPC and flow structure

Observed/schema flow: handshake/connect/login -> lobby/player/friend/game lists -> invitations/chat/likes/profile changes -> focus/inactivity/time sync keep state current -> join-game handoff to the game module.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.Connect` | `Casino.ConnectRequest` | `Casino.ConnectResponse` | 0 | 0 | schema-only |
| `AppServer.Disconnect` | `Casino.DisconnectRequest` | `Casino.DisconnectResponse` | 0 | 0 | schema-only |
| `AppServer.QueryPlayer` | `Casino.QueryPlayerRequest` | `Casino.QueryPlayerResponse` | 1 | 1 | observed-live |
| `AppServer.EditProfile` | `Casino.EditProfileRequest` | `Casino.EditProfileResponse` | 0 | 0 | schema-only |
| `AppServer.GetPlayerList` | `Casino.GetPlayerListRequest` | `Casino.GetPlayerListResponse` | 48 | 48 | observed-live |
| `AppServer.LikePlayer` | `Casino.LikePlayerRequest` | `Casino.LikePlayerResponse` | 1 | 1 | observed-live |
| `AppServer.GetLeaderboard` | `Casino.GetLeaderboardRequest` | `Casino.GetLeaderboardResponse` | 0 | 0 | schema-only |
| `AppServer.GetFriends` | `Casino.EmptyRequest` | `Casino.GetFriendsResponse` | 0 | 0 | schema-only |
| `AppServer.AddFriend` | `Casino.AddFriendRequest` | `Casino.AddFriendResponse` | 0 | 0 | schema-only |
| `AppServer.GetFriendRequests` | `Casino.EmptyRequest` | `Casino.GetFriendRequestsResponse` | 0 | 0 | schema-only |
| `AppServer.RemoveFriend` | `Casino.RemoveFriendRequest` | `Casino.RemoveFriendResponse` | 0 | 0 | schema-only |
| `AppServer.InviteFriendToGame` | `Casino.InviteFriendToGameRequest` | `Casino.InviteFriendToGameResponse` | 0 | 0 | schema-only |
| `AppServer.CheckFriends` | `Casino.CheckFriendsRequest` | `Casino.CheckFriendsResponse` | 0 | 0 | schema-only |
| `AppServer.SyncTime` | `Casino.EmptyRequest` | `Casino.SyncTimeResponse` | 1 | 1 | observed-live |
| `AppServer.ResetUserInactivity` | `Casino.ResetUserInactivityRequest` | `Casino.EmptyResponse` | 140 | 0 | observed-live |
| `AppServer.ReadMessageBoard` | `Casino.ReadMessageBoardRequest` | `Casino.ReadMessageBoardResponse` | 0 | 0 | schema-only |
| `AppServer.MutePlayer` | `Casino.MutePlayerRequest` | `Casino.MutePlayerResponse` | 0 | 0 | schema-only |
| `AppServer.SubscribeFriendNotifications` | `Casino.SubscribeFriendNotificationsRequest` | `Casino.SubscribeFriendNotificationsResponse` | 0 | 0 | schema-only |
| `AppServer.FocusChange` | `Casino.FocusChangeRequest` | `Casino.EmptyResponse` | 2 | 0 | observed-live |
| `AppClient.Handshake` | `Casino.HandshakeRequest` | `Casino.HandshakeResponse` | 0 | 0 | schema-only |
| `AppClient.FriendRequestNotification` | `Casino.FriendRequestNotificationRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.GameInvite` | `Casino.GameInviteRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ChatMessage` | `Casino.ChatMessageRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.Disconnect` | `Casino.DisconnectRequest` | `Casino.DisconnectResponse` | 0 | 0 | schema-only |
| `AppClient.LikeNotify` | `Casino.LikeNotifyRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.ForceLeaveGame` | `Casino.ForceLeaveGameRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.FriendOnline` | `Casino.FriendOnlineRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ChatMessageHistory` | `Casino.ChatMessageHistoryRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.DelayedReconnection` | `Casino.DelayedReconnectionRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddFriendRequest.user_id (int64, required)`
- `Casino.ChatMessageRequest.emot_id (int32, optional)`
- `Casino.ChatMessageRequest.user_id (int64, required)`
- `Casino.CheckFriendsRequest.user_id (int64, repeated)`
- `Casino.ConnectRequest.device_id (string, optional)`
- `Casino.ConnectResponse.assets_id (string, optional)`
- `Casino.ConnectResponse.test_group_id (uint32, optional)`
- `Casino.EditProfileRequest.avatar_id (int64, optional)`
- `Casino.ForceLeaveGameRequest.disconnect_request_id (int32, required)`
- `Casino.Friend.locked_feature_id (uint32, repeated)`
- `Casino.FriendOnlineRequest.user_id (int64, required)`
- `Casino.GetPlayerListResponse.remove_user_id (int64, repeated)`
- `Casino.InviteFriendToGameRequest.user_id (int64, required)`
- `Casino.LikeNotifyRequest.receiver_user_id (int64, required)`
- `Casino.LikeNotifyRequest.sender_user_id (int64, required)`
- `Casino.LikePlayerRequest.user_id (int64, required)`
- `Casino.MutePlayerRequest.user_id (int64, required)`
- `Casino.PlayerProfile.FameInfo.fame_req_id (int32, required)`
- `Casino.QueryPlayerRequest.user_id (int64, required)`
- `Casino.QueryPlayerResponse.locked_feature_id (uint32, repeated)`
- `Casino.RemoveFriendRequest.user_id (int64, required)`
- `Casino.SubscribeFriendNotificationsRequest.user_id (int64, required)`

### Progression / state

- `Casino.AddFriendResponse.status (Casino.AddFriendResponse.Status, required)`
- `Casino.CheckFriendsResponse.status (Casino.CheckFriendsResponse.Status, required)`
- `Casino.ConnectResponse.status (Casino.ConnectResponse.Status, required)`
- `Casino.ConnectResponse.tutorial (bool, optional)`
- `Casino.EditProfileResponse.status (Casino.EditProfileResponse.Status, required)`
- `Casino.GetFriendRequestsResponse.status (Casino.GetFriendRequestsResponse.Status, required)`
- `Casino.GetFriendsResponse.status (Casino.GetFriendsResponse.Status, required)`
- `Casino.GetLeaderboardResponse.status (Casino.GetLeaderboardResponse.Status, required)`
- `Casino.GetPlayerListResponse.status (Casino.GetPlayerListResponse.Status, required)`
- `Casino.InviteFriendToGameResponse.status (Casino.InviteFriendToGameResponse.Status, required)`
- `Casino.LikePlayerResponse.status (Casino.LikePlayerResponse.Status, required)`
- `Casino.MutePlayerResponse.status (Casino.MutePlayerResponse.Status, required)`
- `Casino.PlayerProfile.Rank.rank (int32, required)`
- `Casino.PlayerProfile.Rank.rank_req_value (int64, repeated)`
- `Casino.PlayerProfile.rank (Casino.PlayerProfile.Rank, required)`
- `Casino.PlayerProfile.xp_level (double, optional)`
- `Casino.QueryPlayerResponse.status (Casino.QueryPlayerResponse.Status, required)`
- `Casino.ReadMessageBoardResponse.status (Casino.ReadMessageBoardResponse.Status, required)`
- `Casino.RemoveFriendResponse.status (Casino.RemoveFriendResponse.Status, required)`
- `Casino.SubscribeFriendNotificationsResponse.status (Casino.SubscribeFriendNotificationsResponse.Status, required)`
- `Casino.SyncTimeResponse.status (Casino.SyncTimeResponse.Status, required)`

### Cost / input

- `Casino.ConnectResponse.compression_threshold (uint32, optional)`

### Currency / balance

- `Casino.ConnectResponse.legacy_ftue_idfa_chips (Casino.Chips, optional)`
- `Casino.PlayerProfile.chips (Casino.Chips, optional)`
- `Casino.PlayerProfile.diamonds (int64, optional)`
- `Casino.PlayerProfile.fame_chips_ratio (double, required)`
- `Casino.PlayerProfile.legacy_chips (int64, required)`

### Reward / output

- `Casino.ConnectResponse.update_reward (int64, optional)`
- `Casino.ConnectResponse.update_reward_bb (double, optional)`

### Timing / reset / expiry

- `Casino.ChatMessageRequest.time (int32, optional)`
- `Casino.LikePlayerResponse.like_cooldown (int32, optional)`
- `Casino.PlayerProfile.like_cooldown (int32, optional)`
- `Casino.ReadMessageBoardRequest.timestamp (uint32, required)`
- `Casino.SyncTimeResponse.time_ms (int64, optional)`

### Segment / eligibility / limit

- `Casino.ConnectResponse.update_available (bool, optional)`
- `Casino.DelayedReconnectionRequest.allowed_reconnect_point (Casino.DelayedReconnectionRequest.ReconnectPoint, repeated)`
- `Casino.EditProfileRequest.country_flag (int32, optional)`
- `Casino.Friend.Subscriber.game_invite_allowed (bool, optional)`
- `Casino.GetLeaderboardRequest.limit (uint32, optional)`
- `Casino.LikeNotifyRequest.friends_limit_reached (bool, optional)`

### Other structural fields

- `Casino.AddFriendResponse.error_code (int32, optional)`
- `Casino.AddFriendResponse.fame_delta (int64, optional)`
- `Casino.ChatMessageHistoryRequest.chat_message_history (Casino.ChatMessageRequest, repeated)`
- `Casino.ChatMessageRequest.flag (Casino.ChatFlag, optional)`
- `Casino.ChatMessageRequest.message (string, optional)`
- `Casino.CheckFriendsResponse.error_code (int32, optional)`
- `Casino.CheckFriendsResponse.friend (bool, repeated)`
- `Casino.ConnectRequest.client_platform (Casino.ClientPlatform, optional)`
- `Casino.ConnectRequest.client_version (string, optional)`
- `Casino.ConnectRequest.client_version_number (uint32, optional)`
- `Casino.ConnectRequest.protocol_version (int32, required)`
- `Casino.ConnectRequest.triggered_by_test_emulator (bool, optional)`
- `Casino.ConnectResponse.assets_cdn (Casino.Cdn, repeated)`
- `Casino.ConnectResponse.assets_url (string, optional)`
- `Casino.ConnectResponse.env_name (string, optional)`
- `Casino.ConnectResponse.error_code (int32, optional)`
- `Casino.ConnectResponse.force_update_pak (Casino.ForceUpdate, optional)`
- `Casino.ConnectResponse.qa (bool, optional)`
- `Casino.ConnectResponse.redirect (string, optional)`
- `Casino.ConnectResponse.reskins_cdn (Casino.Cdn, repeated)`
- `Casino.DelayedReconnectionRequest.enable (bool, required)`
- `Casino.DisconnectRequest.reason (Casino.DisconnectRequest.Reason, required)`
- `Casino.EditProfileRequest.age (int32, optional)`
- `Casino.EditProfileRequest.avatar_frame (Casino.EditProfileRequest.AvatarFrame, optional)`
- `Casino.EditProfileRequest.comment (string, optional)`
- `Casino.EditProfileRequest.email_marketing_accepted (bool, optional)`
- `Casino.EditProfileRequest.gender (Casino.Gender, optional)`
- `Casino.EditProfileRequest.location (string, optional)`
- `Casino.EditProfileRequest.name (string, optional)`
- `Casino.EditProfileResponse.error_code (int32, optional)`
- `Casino.FocusChangeRequest.focus (bool, required)`
- `Casino.ForceLeaveGameRequest.redirect (Casino.GameInfo, optional)`
- `Casino.Friend.avatar (Casino.Avatar, required)`
- `Casino.Friend.current_game (Casino.GameDef, optional)`
- `Casino.Friend.subscriber (Casino.Friend.Subscriber, optional)`
- `Casino.FriendRequestNotificationRequest.notification_delta (sint32, required)`
- `Casino.FriendRequestNotificationRequest.requester (Casino.Avatar, optional)`
- `Casino.GameCategoryEntry.flags (int32, optional)`
- `Casino.GameCategoryEntry.game_category (Casino.GameCategory, required)`
- `Casino.GameCategoryEntry.game_subcategory (Casino.GameSubcategory, optional)`
- … 60 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260825_182300`:

- `AppServer.ResetUserInactivity` — 140 (140 request, 0 response)
- `AppServer.GetPlayerList` — 96 (48 request, 48 response)
- `AppServer.QueryPlayer` — 2 (1 request, 1 response)
- `AppServer.LikePlayer` — 2 (1 request, 1 response)
- `AppServer.SyncTime` — 2 (1 request, 1 response)
- `AppServer.FocusChange` — 2 (2 request, 0 response)
- `AppClient.LikeNotify` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.ResetUserInactivityRequest.mode` | 140 | 140 | 3 | varying-in-session |
| `Casino.GetPlayerListRequest.category` | 48 | 48 | 2 | varying-in-session |
| `Casino.GetPlayerListRequest.max_results` | 48 | 48 | 2 | varying-in-session |
| `Casino.GetPlayerListResponse.players_number` | 48 | 48 | 43 | varying-in-session |
| `Casino.GetPlayerListResponse.status` | 48 | 48 | 1 | constant-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.avatar_id` | 17 | 57 | 44 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.club_division` | 17 | 56 | 11 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.country_flag` | 17 | 57 | 19 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.level` | 17 | 57 | 44 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.name` | 17 | 57 | 44 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.user_id` | 17 | 57 | 44 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.avatar_frame.id` | 15 | 50 | 15 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.avatar_frame.level` | 15 | 50 | 1 | constant-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.game_category` | 13 | 45 | 2 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.gift.expire` | 7 | 16 | 14 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.gift.gift_id` | 7 | 16 | 6 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].event_flags` | 6 | 6 | 2 | varying-in-session |
| `Casino.GetPlayerListResponse.remove_user_id[]` | 4 | 4 | 4 | varying-in-session |
| `Casino.FocusChangeRequest.focus` | 2 | 2 | 2 | varying-in-session |
| `Casino.QueryGamePlayerRequest.user_id[]` | 2 | 5 | 5 | varying-in-session |
| `Casino.QueryGamePlayerResponse.player[].avatar.avatar_id` | 2 | 5 | 5 | varying-in-session |
| `Casino.QueryGamePlayerResponse.player[].avatar.club_division` | 2 | 3 | 3 | varying-in-session |
| `Casino.QueryGamePlayerResponse.player[].avatar.country_flag` | 2 | 5 | 5 | varying-in-session |
| `Casino.QueryGamePlayerResponse.player[].avatar.level` | 2 | 5 | 5 | varying-in-session |
| `Casino.QueryGamePlayerResponse.player[].avatar.name` | 2 | 5 | 5 | varying-in-session |
| `Casino.QueryGamePlayerResponse.player[].avatar.user_id` | 2 | 5 | 5 | varying-in-session |
| `Casino.QueryGamePlayerResponse.status` | 2 | 2 | 1 | constant-in-session |
| `Casino.LikeNotifyRequest.friend` | 1 | 1 | 1 | single-observation |
| `Casino.LikeNotifyRequest.receiver_user_id` | 1 | 1 | 1 | single-observation |
| `Casino.LikeNotifyRequest.sender_user_id` | 1 | 1 | 1 | single-observation |
| `Casino.LikePlayerRequest.user_id` | 1 | 1 | 1 | single-observation |
| `Casino.LikePlayerResponse.like_cooldown` | 1 | 1 | 1 | single-observation |
| `Casino.LikePlayerResponse.status` | 1 | 1 | 1 | single-observation |
| `Casino.QueryGamePlayerResponse.player[].avatar.avatar_frame.id` | 1 | 2 | 2 | single-observation |
| `Casino.QueryGamePlayerResponse.player[].avatar.avatar_frame.level` | 1 | 2 | 1 | single-observation |
| `Casino.QueryPlayerRequest.user_id` | 1 | 1 | 1 | single-observation |
| `Casino.QueryPlayerResponse.current_game_joinable` | 1 | 1 | 1 | single-observation |
| `Casino.QueryPlayerResponse.profile.avatar.avatar_id` | 1 | 1 | 1 | single-observation |
| `Casino.QueryPlayerResponse.profile.avatar.country_flag` | 1 | 1 | 1 | single-observation |
| `Casino.QueryPlayerResponse.profile.avatar.level` | 1 | 1 | 1 | single-observation |
| … | | | | 37 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260825_182300`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: handshake/connect/login -> lobby/player/friend/game lists -> invitations/chat/likes/profile changes -> focus/inactivity/time sync keep state current -> join-game handoff to the game module.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_avatars_2_etc2.zpk`
- ZPK asset: `assets/atlas_custom_tiles_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_promo_tiles_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles2_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles3_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles4_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles_reskinned_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/menu_background_1_etc2.zpk`
- ZPK asset: `assets/menu_background_2_etc2.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Mark cold-start lobby loaded, profile opened, friends/leaderboard opened and game-list navigation.
- Inspect one player/profile and one leaderboard without changing social state.
- Mark entry/return transitions between lobby and modules.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
