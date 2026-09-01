# Clubs / Social Club Progression

Club membership, roles, applications/invites, donations, chat/wall, events, leagues/seasons, rewards and jackpot bonuses.

## Catalog status

- Evidence status: **live-confirmed (cross-cutting/config only)**
- Structural completeness: **65/100 — partial live structure**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **27**
- Live endpoints / schema endpoints: **0 / 28**
- Live populated field paths: **10**

## Schema scope

- Proto files: `Clubs.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **79**

- `Casino.ClubEventDef` (Common.proto)
- `Casino.ClubEventDef.Param` (Common.proto)
- `Casino.ClubInfo` (Common.proto)
- `Casino.ClubsProto` (Clubs.proto)
- `Casino.ClubsProto.Club` (Clubs.proto)
- `Casino.ClubsProto.Club.Donation` (Clubs.proto)
- `Casino.ClubsProto.Club.Requester` (Clubs.proto)
- `Casino.ClubsProto.ClubAcceptRequesterRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubAcceptRequesterResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubChangeRoleRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubChangeRoleResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubCreateRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubCreateResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubDef` (Clubs.proto)
- `Casino.ClubsProto.ClubDonateRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubDonateResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubEditRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubEditResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubEvent` (Clubs.proto)
- `Casino.ClubsProto.ClubEvent.ClubEventReward` (Clubs.proto)
- `Casino.ClubsProto.ClubEvent.LeaderboardEntry` (Clubs.proto)
- `Casino.ClubsProto.ClubEventsUpdate` (Clubs.proto)
- `Casino.ClubsProto.ClubEventsUpdate.Entry` (Clubs.proto)
- `Casino.ClubsProto.ClubInvitationRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubInviteListResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubInviteRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubInviteResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubJoinRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubJoinResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubJoinedRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubKickRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubKickResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubLeaderboardRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubLeaderboardResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubLeaguesInfoResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubLeaveResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubListEntry` (Clubs.proto)
- `Casino.ClubsProto.ClubListEntry.RankDelta` (Clubs.proto)
- `Casino.ClubsProto.ClubListResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubMember` (Clubs.proto)
- `Casino.ClubsProto.ClubNotificationRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubNotificationRequest.ChatMessage` (Clubs.proto)
- `Casino.ClubsProto.ClubNotificationRequest.ClubGuard` (Clubs.proto)
- `Casino.ClubsProto.ClubNotificationRequest.ClubSeasonData` (Clubs.proto)
- `Casino.ClubsProto.ClubNotificationRequest.ClubWallBonus` (Clubs.proto)
- `Casino.ClubsProto.ClubProfileInfo` (Clubs.proto)
- `Casino.ClubsProto.ClubQueryRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubQueryResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubRejectRequesterRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubRejectRequesterResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubSearchRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubSearchResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubSeason` (Clubs.proto)
- `Casino.ClubsProto.ClubSeason.DivisionReward` (Clubs.proto)
- `Casino.ClubsProto.ClubSeason.PlaceReward` (Clubs.proto)
- `Casino.ClubsProto.ClubSendChatMessageRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallCollectBonusRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallCollectBonusResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetResponse.BonusSummary` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem.Bonus` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem.ClubEventInfo` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem.RaceLeaderboardMessage` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem.RaceLeaderboardMessage.Entry` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem.Text` (Clubs.proto)
- `Casino.ClubsProto.ClubWallPostRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallPostResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallReadRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallReadResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallSetFilterRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallSetFilterResponse` (Clubs.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)

## RPC and flow structure

Schema flow: list/search/query -> join/create/invite/request -> member role/donation/chat operations -> asynchronous notifications/wall updates -> event/season/league progress and rewards.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.ClubCreate` | `Casino.ClubsProto.ClubCreateRequest` | `Casino.ClubsProto.ClubCreateResponse` | 0 | 0 | schema-only |
| `AppServer.ClubList` | `Casino.EmptyRequest` | `Casino.ClubsProto.ClubListResponse` | 0 | 0 | schema-only |
| `AppServer.ClubJoin` | `Casino.ClubsProto.ClubJoinRequest` | `Casino.ClubsProto.ClubJoinResponse` | 0 | 0 | schema-only |
| `AppServer.ClubLeave` | `Casino.EmptyRequest` | `Casino.ClubsProto.ClubLeaveResponse` | 0 | 0 | schema-only |
| `AppServer.ClubQuery` | `Casino.ClubsProto.ClubQueryRequest` | `Casino.ClubsProto.ClubQueryResponse` | 0 | 0 | schema-only |
| `AppServer.ClubLeaderboard` | `Casino.ClubsProto.ClubLeaderboardRequest` | `Casino.ClubsProto.ClubLeaderboardResponse` | 0 | 0 | schema-only |
| `AppServer.ClubEdit` | `Casino.ClubsProto.ClubEditRequest` | `Casino.ClubsProto.ClubEditResponse` | 0 | 0 | schema-only |
| `AppServer.ClubChangeRole` | `Casino.ClubsProto.ClubChangeRoleRequest` | `Casino.ClubsProto.ClubChangeRoleResponse` | 0 | 0 | schema-only |
| `AppServer.ClubKick` | `Casino.ClubsProto.ClubKickRequest` | `Casino.ClubsProto.ClubKickResponse` | 0 | 0 | schema-only |
| `AppServer.ClubSendChatMessage` | `Casino.ClubsProto.ClubSendChatMessageRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.ClubSearch` | `Casino.ClubsProto.ClubSearchRequest` | `Casino.ClubsProto.ClubSearchResponse` | 0 | 0 | schema-only |
| `AppServer.ClubDonate` | `Casino.ClubsProto.ClubDonateRequest` | `Casino.ClubsProto.ClubDonateResponse` | 0 | 0 | schema-only |
| `AppServer.ClubAcceptRequester` | `Casino.ClubsProto.ClubAcceptRequesterRequest` | `Casino.ClubsProto.ClubAcceptRequesterResponse` | 0 | 0 | schema-only |
| `AppServer.ClubRejectRequester` | `Casino.ClubsProto.ClubRejectRequesterRequest` | `Casino.ClubsProto.ClubRejectRequesterResponse` | 0 | 0 | schema-only |
| `AppServer.ClubInvite` | `Casino.ClubsProto.ClubInviteRequest` | `Casino.ClubsProto.ClubInviteResponse` | 0 | 0 | schema-only |
| `AppServer.ClubInviteList` | `Casino.EmptyRequest` | `Casino.ClubsProto.ClubInviteListResponse` | 0 | 0 | schema-only |
| `AppServer.ClubWallGet` | `Casino.ClubsProto.ClubWallGetRequest` | `Casino.ClubsProto.ClubWallGetResponse` | 0 | 0 | schema-only |
| `AppServer.ClubWallRead` | `Casino.ClubsProto.ClubWallReadRequest` | `Casino.ClubsProto.ClubWallReadResponse` | 0 | 0 | schema-only |
| `AppServer.ClubWallCollectBonus` | `Casino.ClubsProto.ClubWallCollectBonusRequest` | `Casino.ClubsProto.ClubWallCollectBonusResponse` | 0 | 0 | schema-only |
| `AppServer.ClubWallPost` | `Casino.ClubsProto.ClubWallPostRequest` | `Casino.ClubsProto.ClubWallPostResponse` | 0 | 0 | schema-only |
| `AppServer.ClubLeaguesInfo` | `Casino.EmptyRequest` | `Casino.ClubsProto.ClubLeaguesInfoResponse` | 0 | 0 | schema-only |
| `AppServer.ClubWallSetFilter` | `Casino.ClubsProto.ClubWallSetFilterRequest` | `Casino.ClubsProto.ClubWallSetFilterResponse` | 0 | 0 | schema-only |
| `AppServer.ClubWallGetJackpotBonusDetails` | `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsRequest` | `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse` | 0 | 0 | schema-only |
| `AppClient.ClubNotification` | `Casino.ClubsProto.ClubNotificationRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ClubJoined` | `Casino.ClubsProto.ClubJoinedRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ClubInvitation` | `Casino.ClubsProto.ClubInvitationRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ClubSeason` | `Casino.ClubsProto.ClubSeason` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ClubEventsUpdate` | `Casino.ClubsProto.ClubEventsUpdate` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.ClubEventDef.Param.key (uint32, required)`
- `Casino.ClubInfo.club_id (uint64, required)`
- `Casino.ClubsProto.Club.latest_wall_item_id (uint64, optional)`
- `Casino.ClubsProto.ClubAcceptRequesterRequest.user_id (int64, required)`
- `Casino.ClubsProto.ClubChangeRoleRequest.user_id (int64, required)`
- `Casino.ClubsProto.ClubCreateResponse.club_id (uint64, optional)`
- `Casino.ClubsProto.ClubEvent.LeaderboardEntry.user_id (int64, required)`
- `Casino.ClubsProto.ClubEvent.club_event_id (uint64, optional)`
- `Casino.ClubsProto.ClubEventsUpdate.Entry.id (uint64, required)`
- `Casino.ClubsProto.ClubInvitationRequest.club_id (uint64, required)`
- `Casino.ClubsProto.ClubInviteRequest.user_id (int64, required)`
- `Casino.ClubsProto.ClubJoinRequest.club_id (uint64, required)`
- `Casino.ClubsProto.ClubKickRequest.user_id (int64, required)`
- `Casino.ClubsProto.ClubListEntry.club_id (uint64, required)`
- `Casino.ClubsProto.ClubNotificationRequest.ChatMessage.msg_id (uint64, required)`
- `Casino.ClubsProto.ClubNotificationRequest.club_event_id (uint64, optional)`
- `Casino.ClubsProto.ClubNotificationRequest.user_id (int64, optional)`
- `Casino.ClubsProto.ClubProfileInfo.club_id (uint64, required)`
- `Casino.ClubsProto.ClubQueryRequest.club_id (uint64, required)`
- `Casino.ClubsProto.ClubRejectRequesterRequest.user_id (int64, required)`
- `Casino.ClubsProto.ClubSeason.club_season_id (uint64, optional)`
- `Casino.ClubsProto.ClubWallCollectBonusRequest.item_id (uint64, optional)`
- `Casino.ClubsProto.ClubWallGetRequest.from_item_id (uint64, optional)`
- `Casino.ClubsProto.ClubWallItem.RaceLeaderboardMessage.Entry.user_id (int64, required)`
- `Casino.ClubsProto.ClubWallItem.RaceLeaderboardMessage.race_id (string, required)`
- `Casino.ClubsProto.ClubWallItem.item_id (uint64, required)`
- `Casino.ClubsProto.ClubWallReadRequest.item_id (uint64, required)`

### Progression / state

- `Casino.ClubsProto.Club.Donation.level (uint32, required)`
- `Casino.ClubsProto.Club.club_bank_on_level (uint64, optional)`
- `Casino.ClubsProto.Club.club_bank_to_level_up (uint64, optional)`
- `Casino.ClubsProto.Club.league_points (Casino.BigNumber, optional)`
- `Casino.ClubsProto.Club.legacy_league_points (uint64, optional)`
- `Casino.ClubsProto.Club.level (uint32, required)`
- `Casino.ClubsProto.Club.max_coleaders_on_next_level (uint32, optional)`
- `Casino.ClubsProto.Club.max_members_on_next_level (uint32, optional)`
- `Casino.ClubsProto.Club.rank (uint32, optional)`
- `Casino.ClubsProto.ClubAcceptRequesterResponse.status (Casino.ClubsProto.ClubAcceptRequesterResponse.Status, required)`
- `Casino.ClubsProto.ClubChangeRoleResponse.status (Casino.ClubsProto.ClubChangeRoleResponse.Status, required)`
- `Casino.ClubsProto.ClubCreateResponse.status (Casino.ClubsProto.ClubCreateResponse.Status, required)`
- `Casino.ClubsProto.ClubDonateResponse.status (Casino.ClubsProto.ClubDonateResponse.Status, required)`
- `Casino.ClubsProto.ClubEditResponse.status (Casino.ClubsProto.ClubEditResponse.Status, required)`
- `Casino.ClubsProto.ClubEvent.ClubEventReward.progress_treshold (uint64, required)`
- `Casino.ClubsProto.ClubEvent.LeaderboardEntry.progress (uint64, required)`
- `Casino.ClubsProto.ClubEvent.LeaderboardEntry.progress_big_int (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubEvent.progress (uint64, optional)`
- `Casino.ClubsProto.ClubEvent.progress_big_int (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubEventsUpdate.active (Casino.ClubsProto.ClubEventsUpdate.Entry, repeated)`
- `Casino.ClubsProto.ClubEventsUpdate.completed (Casino.ClubsProto.ClubEventsUpdate.Entry, repeated)`
- `Casino.ClubsProto.ClubInviteListResponse.status (Casino.ClubsProto.ClubInviteListResponse.Status, required)`
- `Casino.ClubsProto.ClubInviteResponse.status (Casino.ClubsProto.ClubInviteResponse.Status, required)`
- `Casino.ClubsProto.ClubJoinResponse.status (Casino.ClubsProto.ClubJoinResponse.Status, required)`
- `Casino.ClubsProto.ClubKickResponse.status (Casino.ClubsProto.ClubKickResponse.Status, required)`
- `Casino.ClubsProto.ClubLeaderboardResponse.status (Casino.ClubsProto.ClubLeaderboardResponse.Status, required)`
- `Casino.ClubsProto.ClubLeaguesInfoResponse.status (Casino.ClubsProto.ClubLeaguesInfoResponse.Status, required)`
- `Casino.ClubsProto.ClubLeaveResponse.status (Casino.ClubsProto.ClubLeaveResponse.Status, required)`
- `Casino.ClubsProto.ClubListEntry.league_points (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubListEntry.legacy_league_points (uint64, required)`
- `Casino.ClubsProto.ClubListEntry.rank_delta (Casino.ClubsProto.ClubListEntry.RankDelta, optional)`
- `Casino.ClubsProto.ClubListResponse.status (Casino.ClubsProto.ClubListResponse.Status, required)`
- `Casino.ClubsProto.ClubMember.league_points (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubMember.legacy_league_points (uint64, required)`
- `Casino.ClubsProto.ClubNotificationRequest.club_event_progress (uint32, optional)`
- `Casino.ClubsProto.ClubNotificationRequest.level (uint32, optional)`
- `Casino.ClubsProto.ClubProfileInfo.league_points (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubProfileInfo.legacy_league_points (uint64, optional)`
- `Casino.ClubsProto.ClubProfileInfo.rank (uint32, optional)`
- `Casino.ClubsProto.ClubQueryResponse.status (Casino.ClubsProto.ClubQueryResponse.Status, required)`
- … 14 more rows in `fields.csv`

### Cost / input

- `Casino.ClubsProto.ClubEvent.ClubEventReward.progress_threshold_big_int (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallGetResponse.BonusSummary.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallItem.Bonus.bb_amount (double, optional)`

### Currency / balance

- `Casino.ClubsProto.ClubCreateResponse.chips_delta (int32, optional)`
- `Casino.ClubsProto.ClubDonateResponse.chips_delta (int64, optional)`

### Reward / output

- `Casino.ClubsProto.ClubEvent.ClubEventReward.reward (Casino.Reward, required)`
- `Casino.ClubsProto.ClubEvent.reward (Casino.ClubsProto.ClubEvent.ClubEventReward, repeated)`
- `Casino.ClubsProto.ClubNotificationRequest.ClubWallBonus.reward (Casino.Reward, optional)`
- `Casino.ClubsProto.ClubNotificationRequest.club_wall_bonus (Casino.ClubsProto.ClubNotificationRequest.ClubWallBonus, optional)`
- `Casino.ClubsProto.ClubQueryResponse.league_points_bonus (Casino.Item, optional)`
- `Casino.ClubsProto.ClubSeason.DivisionReward.reward (Casino.ClubsProto.ClubSeason.PlaceReward, repeated)`
- `Casino.ClubsProto.ClubSeason.PlaceReward.lobby_bonuses_frac_delta (double, optional)`
- `Casino.ClubsProto.ClubSeason.reward (Casino.ClubsProto.ClubSeason.DivisionReward, repeated)`
- `Casino.ClubsProto.ClubWallCollectBonusRequest.jackpot_bonus_type (uint32, optional)`
- `Casino.ClubsProto.ClubWallCollectBonusResponse.reward (Casino.Reward, repeated)`
- `Casino.ClubsProto.ClubWallGetResponse.bonus_summary (Casino.ClubsProto.ClubWallGetResponse.BonusSummary, repeated)`
- `Casino.ClubsProto.ClubWallGetResponse.cumulative_jackpot_bonus (Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus, repeated)`
- `Casino.ClubsProto.ClubWallGetResponse.non_spin_bonus_game_bonus (Casino.NonSpinBonusGameProto.Data, repeated)`
- `Casino.ClubsProto.ClubWallItem.bonus (Casino.ClubsProto.ClubWallItem.Bonus, optional)`
- `Casino.ClubsProto.ClubWallItem.club_event_reward (Casino.Reward, optional)`

### Timing / reset / expiry

- `Casino.ClubsProto.Club.Donation.cooldown (uint32, optional)`
- `Casino.ClubsProto.ClubEvent.end_time (int32, optional)`
- `Casino.ClubsProto.ClubEvent.start_time (int32, optional)`
- `Casino.ClubsProto.ClubNotificationRequest.ChatMessage.timestamp (int32, required)`
- `Casino.ClubsProto.ClubNotificationRequest.ClubGuard.time (uint32, optional)`
- `Casino.ClubsProto.ClubSeason.end_time (int32, optional)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.end_time (uint32, required)`
- `Casino.ClubsProto.ClubWallItem.Bonus.end_time (uint32, optional)`
- `Casino.ClubsProto.ClubWallItem.RaceLeaderboardMessage.end_time (uint32, optional)`

### Segment / eligibility / limit

- `Casino.ClubsProto.ClubSearchRequest.available_for_me (bool, optional)`

### Other structural fields

- `Casino.ClubEventDef.Param.value_bool (bool, optional)`
- `Casino.ClubEventDef.Param.value_float (float, optional)`
- `Casino.ClubEventDef.Param.value_int (int64, optional)`
- `Casino.ClubEventDef.Param.value_params (Casino.KeyValueMap, optional)`
- `Casino.ClubEventDef.Param.value_string (string, optional)`
- `Casino.ClubEventDef.param (Casino.ClubEventDef.Param, repeated)`
- `Casino.ClubEventDef.type (uint32, required)`
- `Casino.ClubInfo.name (string, optional)`
- `Casino.ClubInfo.symbol (uint32, optional)`
- `Casino.ClubsProto.Club.Donation.done_today (uint64, optional)`
- `Casino.ClubsProto.Club.Requester.avatar (Casino.Avatar, required)`
- `Casino.ClubsProto.Club.Requester.fame (Casino.BigNumber, optional)`
- `Casino.ClubsProto.Club.Requester.legacy_fame (uint64, required)`
- `Casino.ClubsProto.Club.club_bank (uint64, required)`
- `Casino.ClubsProto.Club.club_event (Casino.ClubsProto.ClubEvent, repeated)`
- `Casino.ClubsProto.Club.club_wall_product (string, optional)`
- `Casino.ClubsProto.Club.def (Casino.ClubsProto.ClubDef, required)`
- `Casino.ClubsProto.Club.division (uint32, optional)`
- `Casino.ClubsProto.Club.donation (Casino.ClubsProto.Club.Donation, optional)`
- `Casino.ClubsProto.Club.instance (uint32, optional)`
- `Casino.ClubsProto.Club.invite_pending (bool, optional)`
- `Casino.ClubsProto.Club.kicks_left (uint32, optional)`
- `Casino.ClubsProto.Club.max_coleaders (uint32, optional)`
- `Casino.ClubsProto.Club.max_members (uint32, required)`
- `Casino.ClubsProto.Club.member (Casino.ClubsProto.ClubMember, repeated)`
- `Casino.ClubsProto.Club.request_pending (bool, optional)`
- `Casino.ClubsProto.Club.requester (Casino.ClubsProto.Club.Requester, repeated)`
- `Casino.ClubsProto.ClubAcceptRequesterResponse.club (Casino.ClubsProto.Club, optional)`
- `Casino.ClubsProto.ClubAcceptRequesterResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubChangeRoleRequest.mode (Casino.ClubsProto.ClubChangeRoleRequest.Mode, required)`
- `Casino.ClubsProto.ClubChangeRoleResponse.club (Casino.ClubsProto.Club, optional)`
- `Casino.ClubsProto.ClubChangeRoleResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubCreateRequest.def (Casino.ClubsProto.ClubDef, required)`
- `Casino.ClubsProto.ClubCreateResponse.chat_history (Casino.ClubsProto.ClubNotificationRequest, repeated)`
- `Casino.ClubsProto.ClubCreateResponse.club (Casino.ClubsProto.Club, optional)`
- `Casino.ClubsProto.ClubCreateResponse.club_events_update (Casino.ClubsProto.ClubEventsUpdate, optional)`
- `Casino.ClubsProto.ClubCreateResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubDef.club_guard (uint32, optional)`
- `Casino.ClubsProto.ClubDef.description (string, optional)`
- `Casino.ClubsProto.ClubDef.min_fame (uint32, required)`
- … 128 more rows in `fields.csv`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.QueryGamePlayerResponse.player[].avatar.club_division` | 13 | 15 | 8 | varying-in-session |
| `Casino.GetPlayerListResponse.entry[].avatar.club_division` | 10 | 27 | 8 | varying-in-session |
| `Casino.QueryPlayerResponse.profile.avatar.club_division` | 3 | 3 | 2 | varying-in-session |
| `Casino.QueryPlayerResponse.profile.club.club_id` | 3 | 3 | 2 | varying-in-session |
| `Casino.LoginResponse.club_join_incentive` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_season.club_season_id` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_season.end_time` | 1 | 1 | 1 | single-observation |
| `Casino.LoginResponse.club_season.reward[].reward[].action` | 1 | 26 | 2 | single-observation |
| `Casino.LoginResponse.club_season.reward[].reward[].from_place` | 1 | 56 | 5 | single-observation |
| `Casino.LoginResponse.club_season.reward[].reward[].lobby_bonuses_frac_delta` | 1 | 56 | 56 | single-observation |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: list/search/query -> join/create/invite/request -> member role/donation/chat operations -> asynchronous notifications/wall updates -> event/season/league progress and rewards.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_clubs2_characters_2_etc2.zpk`
- ZPK asset: `assets/atlas_clubs2_common_2_etc2.zpk`
- ZPK asset: `assets/atlas_clubs2_popups_2_etc2.zpk`
- ZPK asset: `assets/atlas_clubs2_symbols_2_etc2.zpk`
- ZPK asset: `assets/atlas_clubs2_tutorial_2_etc2.zpk`
- ZPK asset: `assets/atlas_clubs2_ui_2_etc2.zpk`
- ZPK asset: `assets/sound_club_set.zpk`
- Multiple `atlas_clubs2_*` and Club Set ZPKs confirm a broad club UI/content surface.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open club home, member list, wall/chat, events, league/season and donation screens with markers.
- Query/search a club and inspect one member/profile without changing membership.
- Collect a naturally available wall/event bonus or make a normal intended donation, marking before/after.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
