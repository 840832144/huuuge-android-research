# Rewards / Mystery / Hourly / Free Gift

Generic reward payloads, reward bundles, mystery rewards, hourly/daily/shop/bank bonuses, free gifts/tickets/diamonds/chips and claim responses.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **90/100 — substantial live structure**
- Primary live samples: **163** from `LOT-20260827-A`
- Cross-cutting live samples: **1386**
- Live endpoints / schema endpoints: **8 / 21**
- Live populated field paths: **1014**

## Schema scope

- Proto files: `Adventure.proto`, `AppClient.proto`, `AppServer.proto`, `BattlePass.proto`, `Clubs.proto`, `Common.proto`, `CommonGameClient.proto`, `GameHost.proto`, `Lottery.proto`, `MiniPass.proto`, `NonSpinBonusGame.proto`, `Race.proto`, `Services.proto`, `Slots.proto`, `Sweepstakes.proto`
- Services: `AppClient`, `AppServer`, `CommonGameClient`, `GameHost`
- Related message types: **111**

- `Casino.AddDciEventRequest.CharmsEvent.RewardPromo` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward` (AppClient.proto)
- `Casino.BankBonus` (AppServer.proto)
- `Casino.BattlePassReward` (BattlePass.proto)
- `Casino.BreakPiggyBankRequest` (AppServer.proto)
- `Casino.BuyGiftRequest` (AppServer.proto)
- `Casino.BuyGiftResponse` (AppServer.proto)
- `Casino.CharmsThemeReward` (Common.proto)
- `Casino.ClaimRewardBundleBulkRequest` (AppServer.proto)
- `Casino.ClaimRewardBundleBulkResponse` (AppServer.proto)
- `Casino.ClaimRewardBundleRequest` (AppServer.proto)
- `Casino.ClaimRewardBundleResponse` (AppServer.proto)
- `Casino.ClubSetDuplicatesReward` (Common.proto)
- `Casino.ClubSetGrandReward` (Common.proto)
- `Casino.ClubSetMilestoneReward` (Common.proto)
- `Casino.ClubsProto.ClubEvent.ClubEventReward` (Clubs.proto)
- `Casino.ClubsProto.ClubNotificationRequest.ClubWallBonus` (Clubs.proto)
- `Casino.ClubsProto.ClubSeason.DivisionReward` (Clubs.proto)
- `Casino.ClubsProto.ClubSeason.PlaceReward` (Clubs.proto)
- `Casino.ClubsProto.ClubWallCollectBonusRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallCollectBonusResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetResponse.BonusSummary` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus` (Clubs.proto)
- `Casino.ClubsProto.ClubWallItem.Bonus` (Clubs.proto)
- `Casino.CollectBankBonusResponse` (AppServer.proto)
- `Casino.CollectBankBonusResponse.BankBonus` (AppServer.proto)
- `Casino.CollectDailyBonusResponse` (AppServer.proto)
- `Casino.CollectFreeDiamondsResponse` (AppServer.proto)
- `Casino.CollectHourlyBonusResponse` (AppServer.proto)
- `Casino.CollectMysteryRewardResponse` (AppServer.proto)
- `Casino.CollectRateUsBonusResponse` (AppServer.proto)
- `Casino.CollectShopBonusResponse` (AppServer.proto)
- `Casino.CollectiblesSetReward` (Common.proto)
- `Casino.ConfirmFreeGiftRoundRequest` (AppClient.proto)
- `Casino.ConfirmFreeGiftRoundResponse` (AppClient.proto)
- `Casino.ConquestReward` (Common.proto)
- `Casino.ConsumeTokenRequest` (AppServer.proto)
- `Casino.ConsumeTokenResponse` (AppServer.proto)
- `Casino.ConsumeTokenResponse.TokenReward` (AppServer.proto)
- `Casino.DailyBonus` (AppServer.proto)
- `Casino.DailyBonus.DailyReward` (AppServer.proto)
- `Casino.DailyWheelOffer` (AppServer.proto)
- `Casino.DailyWheelOffer.Promotion` (AppServer.proto)
- `Casino.DailyWheelOffer.Wedge` (AppServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.Gift` (Common.proto)
- `Casino.GiveFreeGiftRoundRequest` (GameHost.proto)
- `Casino.IapProduct.RewardData` (Common.proto)
- `Casino.LeaguePointBonus` (CommonGameClient.proto)
- `Casino.LiteModeCollectFreeChipsResponse` (AppServer.proto)
- `Casino.LoginResponse.AdminBonus` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward` (AppServer.proto)
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward` (AppServer.proto)
- `Casino.LotteryPuzzleBoardReward` (Lottery.proto)
- `Casino.MilestoneReward` (Adventure.proto)
- `Casino.MiniPassReward` (MiniPass.proto)
- `Casino.NextMysteryReward` (AppServer.proto)
- `Casino.NonSpinBonusGameProto` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BonusResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BuyBonusRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BuyBonusResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.Data` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetDataRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetDataResponse` (NonSpinBonusGame.proto)
- `Casino.NotifyRewardBundlesRequest` (AppClient.proto)
- `Casino.PlayerRewardInfo` (AppServer.proto)
- `Casino.PlayerRewardInfo.PopupInfo` (AppServer.proto)
- `Casino.PlayerRewardInfo.PopupInfo.TextVariableEntry` (AppServer.proto)
- `Casino.RaceProto.PlaceReward` (Race.proto)
- `Casino.ReceiveRewardRequest` (AppClient.proto)
- `Casino.Reward` (Common.proto)
- `Casino.Reward.AdventureSkipToken` (Common.proto)
- `Casino.Reward.BattlePassPoints` (Common.proto)
- `Casino.Reward.BattlePassPremium` (Common.proto)
- `Casino.Reward.CashPrize` (Common.proto)
- `Casino.Reward.ClubSeasonData` (Common.proto)
- `Casino.Reward.GameToUnlock` (Common.proto)
- `Casino.Reward.GemSubscription` (Common.proto)
- `Casino.Reward.LeaguePointsBonus` (Common.proto)
- `Casino.Reward.LotteryPuzzle` (Common.proto)
- `Casino.Reward.MgapEntry` (Common.proto)
- `Casino.Reward.MiniGameMoves` (Common.proto)
- `Casino.Reward.MiniPassPoints` (Common.proto)
- `Casino.Reward.MiniPassSubscription` (Common.proto)
- `Casino.Reward.MissionsData` (Common.proto)
- `Casino.Reward.SweepstakesTickets` (Common.proto)
- `Casino.RewardsData` (Common.proto)
- `Casino.RewardsStateInfo` (Common.proto)
- `Casino.SlotsProto.BonusId` (Slots.proto)
- `Casino.SlotsProto.BonusInfo` (Slots.proto)
- `Casino.SlotsProto.PlayBonusDecision` (Slots.proto)
- `Casino.SlotsProto.SocialBonus` (Slots.proto)
- `Casino.SlotsProto.SocialBonus.Player` (Slots.proto)
- `Casino.SlotsProto.SpinResponse.Bonus` (Slots.proto)
- `Casino.SurpriseRequest` (AppClient.proto)
- `Casino.SweepstakesOpenDraw.DrawReward` (Sweepstakes.proto)
- `Casino.TimeBasedCharmsMainReward` (Common.proto)
- `Casino.TimeBasedCharmsMilestoneReward` (Common.proto)
- `Casino.UpdateAssignmentEventsRequest.Assignment.StreakParams.StepRewards` (AppClient.proto)
- `Casino.UpdateBankBonusRequest` (AppServer.proto)
- `Casino.UpdateGiftRequest` (AppServer.proto)
- `Casino.UpdateGiftRequest.Receiver` (AppServer.proto)
- `Casino.UpdateNextMysteryRewardRequest` (AppClient.proto)
- `Casino.UpdateShopRequest.ShopPromotion.PromoIap.PromoReward` (Common.proto)

## RPC and flow structure

Observed/schema flow: config/update announces reward availability -> claim/collect request -> response returns reward/state -> client update/notification confirms delivery; bulk reward bundles aggregate multiple claims.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.BuyGift` | `Casino.BuyGiftRequest` | `Casino.BuyGiftResponse` | 0 | 0 | schema-only |
| `AppServer.CollectHourlyBonus` | `Casino.EmptyRequest` | `Casino.CollectHourlyBonusResponse` | 1 | 1 | observed-live |
| `AppServer.CollectDailyBonus` | `Casino.EmptyRequest` | `Casino.CollectDailyBonusResponse` | 0 | 0 | schema-only |
| `AppServer.CollectRateUsBonus` | `Casino.EmptyRequest` | `Casino.CollectRateUsBonusResponse` | 0 | 0 | schema-only |
| `AppServer.ConsumeToken` | `Casino.ConsumeTokenRequest` | `Casino.ConsumeTokenResponse` | 0 | 0 | schema-only |
| `AppServer.CollectMysteryReward` | `Casino.EmptyRequest` | `Casino.CollectMysteryRewardResponse` | 69 | 69 | observed-live |
| `AppServer.CollectFreeDiamonds` | `Casino.EmptyRequest` | `Casino.CollectFreeDiamondsResponse` | 0 | 0 | schema-only |
| `AppServer.CollectBankBonus` | `Casino.EmptyRequest` | `Casino.CollectBankBonusResponse` | 0 | 0 | schema-only |
| `AppServer.ClaimRewardBundle` | `Casino.ClaimRewardBundleRequest` | `Casino.ClaimRewardBundleResponse` | 3 | 3 | observed-live |
| `AppServer.ClaimRewardBundleBulk` | `Casino.ClaimRewardBundleBulkRequest` | `Casino.ClaimRewardBundleBulkResponse` | 5 | 5 | observed-live |
| `AppServer.LiteModeCollectFreeChips` | `Casino.EmptyRequest` | `Casino.LiteModeCollectFreeChipsResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateGift` | `Casino.UpdateGiftRequest` | `Casino.EmptyResponse` | 2 | 0 | observed-live |
| `AppClient.ConfirmFreeGiftRound` | `Casino.ConfirmFreeGiftRoundRequest` | `Casino.ConfirmFreeGiftRoundResponse` | 1 | 1 | observed-live |
| `AppClient.Surprise` | `Casino.SurpriseRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.ReceiveReward` | `Casino.ReceiveRewardRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.BreakPiggyBank` | `Casino.BreakPiggyBankRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateBankBonus` | `Casino.UpdateBankBonusRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.NotifyRewardBundles` | `Casino.NotifyRewardBundlesRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.UpdateNextMysteryReward` | `Casino.UpdateNextMysteryRewardRequest` | `Casino.EmptyResponse` | 2 | 0 | observed-live |
| `GameHost.GiveFreeGiftRound` | `Casino.GiveFreeGiftRoundRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `CommonGameClient.SendLeaguePointBonusData` | `Casino.LeaguePointBonus` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.BattlePassReward.reward_bundle_id (string, optional)`
- `Casino.BreakPiggyBankRequest.granted_extra_items_ids (int32, repeated)`
- `Casino.BuyGiftRequest.gift_id (int32, required)`
- `Casino.BuyGiftRequest.user_id (int64, repeated)`
- `Casino.BuyGiftResponse.actual_receiver_id (int64, repeated)`
- `Casino.ClaimRewardBundleRequest.alternative_reward_id (int64, repeated)`
- `Casino.ClaimRewardBundleRequest.bundle_id (string, required)`
- `Casino.ClubSetGrandReward.bundle_id (string, optional)`
- `Casino.ClubSetMilestoneReward.bundle_id (string, optional)`
- `Casino.ClubsProto.ClubWallCollectBonusRequest.item_id (uint64, optional)`
- `Casino.CollectiblesSetReward.id (int32, required)`
- `Casino.DailyBonus.DailyReward.gift_id (int32, optional)`
- `Casino.DailyWheelOffer.Promotion.iap_id (string, optional)`
- `Casino.DailyWheelOffer.Promotion.segment_id (int64, required)`
- `Casino.DailyWheelOffer.event_id (int64, required)`
- `Casino.DailyWheelOffer.iap_id (string, required)`
- `Casino.DailyWheelOffer.segment_id (int64, required)`
- `Casino.Gift.gift_id (int32, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.challenge_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.conquest_id (int64, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.distributed_event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.conquest_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.distributed_event_id (int64, required)`
- `Casino.MilestoneReward.bundle_id (string, optional)`
- `Casino.MilestoneReward.milestone_id (int32, optional)`
- `Casino.MiniPassReward.reward_bundle_id (string, optional)`
- `Casino.PlayerRewardInfo.PopupInfo.TextVariableEntry.id (int32, required)`
- `Casino.PlayerRewardInfo.PopupInfo.campaign_id (string, optional)`
- `Casino.PlayerRewardInfo.PopupInfo.content_text_id (int32, required)`
- `Casino.PlayerRewardInfo.id (int64, required)`
- `Casino.Reward.BattlePassPremium.battle_pass_id (string, required)`
- `Casino.Reward.ClubSeasonData.id (uint64, required)`
- `Casino.Reward.GameToUnlock.game_id (string, required)`
- `Casino.Reward.MgapEntry.id (string, required)`
- `Casino.Reward.MiniPassPoints.event_id (string, required)`
- `Casino.Reward.MiniPassPoints.phase_id (string, optional)`
- `Casino.Reward.MiniPassSubscription.event_id (string, required)`
- `Casino.Reward.MiniPassSubscription.phase_id (string, optional)`
- `Casino.Reward.club_event_id (uint64, optional)`
- `Casino.Reward.club_tournament_id (uint64, optional)`
- … 10 more rows in `fields.csv`

### Progression / state

- `Casino.BreakPiggyBankRequest.active_extra_items (Casino.ExtraItem, repeated)`
- `Casino.BuyGiftResponse.status (Casino.BuyGiftResponse.Status, required)`
- `Casino.CharmsThemeReward.level (int32, optional)`
- `Casino.ClaimRewardBundleBulkResponse.state_info (Casino.RewardsStateInfo, optional)`
- `Casino.ClaimRewardBundleBulkResponse.status (Casino.ClaimRewardBundleBulkResponse.Status, required)`
- `Casino.ClaimRewardBundleResponse.state_info (Casino.RewardsStateInfo, optional)`
- `Casino.ClaimRewardBundleResponse.status (Casino.ClaimRewardBundleResponse.Status, required)`
- `Casino.ClubsProto.ClubEvent.ClubEventReward.progress_treshold (uint64, required)`
- `Casino.ClubsProto.ClubWallCollectBonusResponse.status (Casino.ClubsProto.ClubWallCollectBonusResponse.Status, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.count (uint32, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.status (Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Status, required)`
- `Casino.ClubsProto.ClubWallGetResponse.BonusSummary.count (uint32, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.count (uint32, required)`
- `Casino.ClubsProto.ClubWallItem.Bonus.state (uint32, optional)`
- `Casino.CollectBankBonusResponse.status (Casino.CollectBankBonusResponse.Status, required)`
- `Casino.CollectDailyBonusResponse.status (Casino.CollectDailyBonusResponse.Status, required)`
- `Casino.CollectFreeDiamondsResponse.status (Casino.CollectFreeDiamondsResponse.Status, required)`
- `Casino.CollectHourlyBonusResponse.status (Casino.CollectHourlyBonusResponse.Status, required)`
- `Casino.CollectMysteryRewardResponse.status (Casino.CollectMysteryRewardResponse.Status, required)`
- `Casino.CollectRateUsBonusResponse.status (Casino.CollectRateUsBonusResponse.Status, required)`
- `Casino.CollectShopBonusResponse.status (Casino.CollectShopBonusResponse.Status, required)`
- `Casino.CollectiblesSetReward.level (int32, optional)`
- `Casino.ConsumeTokenResponse.TokenReward.status (Casino.ConsumeTokenResponse.TokenReward.TokenStatus, required)`
- `Casino.ConsumeTokenResponse.status (Casino.ConsumeTokenResponse.Status, required)`
- `Casino.DailyWheelOffer.Promotion.active_promotion (Casino.DailyWheelOffer.Promotion.Type, required)`
- `Casino.LiteModeCollectFreeChipsResponse.status (Casino.LiteModeCollectFreeChipsResponse.Status, required)`
- `Casino.NextMysteryReward.level (int64, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusResponse.status (Casino.NonSpinBonusGameProto.BuyBonusResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.Data.count (uint32, required)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.status (Casino.NonSpinBonusGameProto.GetBonusInfoResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.GetDataResponse.status (Casino.NonSpinBonusGameProto.GetDataResponse.Status, required)`
- `Casino.Reward.ClubSeasonData.league_points (uint64, optional)`
- `Casino.Reward.club_league_points_delta (int64, optional)`
- `Casino.Reward.club_league_points_delta_big (Casino.BigNumber, optional)`
- `Casino.Reward.loyalty_points (int64, optional)`
- `Casino.Reward.mini_pass_points (Casino.Reward.MiniPassPoints, optional)`
- `Casino.Reward.plus_points (int64, optional)`
- `Casino.RewardsData.state_info (Casino.RewardsStateInfo, optional)`
- `Casino.SlotsProto.SocialBonus.Player.points (uint64, required)`

### Cost / input

- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.ticket_color (Casino.LotteryColor, required)`
- `Casino.ClubsProto.ClubEvent.ClubEventReward.progress_threshold_big_int (Casino.BigNumber, optional)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallGetResponse.BonusSummary.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallItem.Bonus.bb_amount (double, optional)`
- `Casino.ConsumeTokenRequest.token (Casino.Token, repeated)`
- `Casino.ConsumeTokenResponse.TokenReward.token (string, required)`
- `Casino.NonSpinBonusGameProto.BonusResponse.bet (uint64, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.price (Casino.Chips, optional)`
- `Casino.NonSpinBonusGameProto.Data.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.price (Casino.Chips, optional)`
- `Casino.NonSpinBonusGameProto.GetDataResponse.bet (uint64, optional)`
- `Casino.Reward.AdventureSkipToken.amount (int64, required)`
- `Casino.Reward.BattlePassPoints.amount (int64, required)`
- `Casino.Reward.MiniGameMoves.amount (uint32, required)`
- `Casino.Reward.MiniPassPoints.amount (int64, required)`
- `Casino.Reward.SweepstakesTickets.amount (int64, required)`
- `Casino.Reward.adventure_skip_token (Casino.Reward.AdventureSkipToken, optional)`
- `Casino.Reward.charms_trade_token_delta (uint32, optional)`
- `Casino.Reward.sweepstakes_tickets (Casino.Reward.SweepstakesTickets, optional)`
- `Casino.SlotsProto.BonusInfo.bet (Casino.Chips, optional)`
- `Casino.SlotsProto.BonusInfo.played_bet (Casino.Chips, optional)`

### Currency / balance

- `Casino.BreakPiggyBankRequest.chips_delta (int64, required)`
- `Casino.BuyGiftResponse.big_chips_delta (Casino.Chips, optional)`
- `Casino.BuyGiftResponse.chips_delta (int64, optional)`
- `Casino.BuyGiftResponse.diamonds_delta (int64, optional)`
- `Casino.CollectHourlyBonusResponse.chips_delta (int64, optional)`
- `Casino.CollectHourlyBonusResponse.piggy_bank_chips_delta (int64, optional)`
- `Casino.CollectRateUsBonusResponse.chips_delta (int64, optional)`
- `Casino.CollectShopBonusResponse.chips_delta (Casino.Chips, optional)`
- `Casino.ConsumeTokenResponse.TokenReward.chips_delta (int64, optional)`
- `Casino.DailyBonus.DailyReward.chips (Casino.Chips, required)`
- `Casino.LiteModeCollectFreeChipsResponse.chips (Casino.Chips, optional)`
- `Casino.LoginResponse.AdminBonus.chips (int64, optional)`
- `Casino.LoginResponse.AdminBonus.diamonds (int64, optional)`
- `Casino.Reward.GemSubscription.chips (Casino.Chips, optional)`
- `Casino.Reward.GemSubscription.diamonds (int64, optional)`
- `Casino.Reward.MgapEntry.base_chips (Casino.Chips, required)`
- `Casino.Reward.big_chips_delta (Casino.Chips, optional)`
- `Casino.Reward.chips_delta (int64, optional)`
- `Casino.Reward.club_bank_chips_delta (int64, optional)`
- `Casino.Reward.club_bank_chips_delta_big (Casino.Chips, optional)`
- `Casino.Reward.d2c_chips (Casino.Chips, optional)`
- `Casino.Reward.diamonds_delta (int64, optional)`
- `Casino.Reward.gem_subscription (Casino.Reward.GemSubscription, optional)`
- `Casino.Reward.piggy_bank_chips_delta (int64, optional)`
- `Casino.SlotsProto.SocialBonus.legacy_total_cash (uint64, required)`
- `Casino.SlotsProto.SocialBonus.total_cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.Bonus.cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.Bonus.legacy_cash (uint64, required)`
- `Casino.SurpriseRequest.chips_delta (int64, required)`

### Reward / output

- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.reward (Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward, repeated)`
- `Casino.BankBonus.reward (Casino.Reward, repeated)`
- `Casino.BattlePassReward.reward (Casino.Reward, repeated)`
- `Casino.CharmsThemeReward.reward (Casino.Reward, repeated)`
- `Casino.ClubSetDuplicatesReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetGrandReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetGrandReward.user_reward (Casino.Reward, repeated)`
- `Casino.ClubSetMilestoneReward.club_reward (Casino.Reward, repeated)`
- `Casino.ClubSetMilestoneReward.user_reward (Casino.Reward, repeated)`
- `Casino.ClubsProto.ClubEvent.ClubEventReward.reward (Casino.Reward, required)`
- `Casino.ClubsProto.ClubNotificationRequest.ClubWallBonus.reward (Casino.Reward, optional)`
- `Casino.ClubsProto.ClubSeason.DivisionReward.reward (Casino.ClubsProto.ClubSeason.PlaceReward, repeated)`
- `Casino.ClubsProto.ClubSeason.PlaceReward.lobby_bonuses_frac_delta (double, optional)`
- `Casino.ClubsProto.ClubWallCollectBonusRequest.jackpot_bonus_type (uint32, optional)`
- `Casino.ClubsProto.ClubWallCollectBonusResponse.reward (Casino.Reward, repeated)`
- `Casino.CollectBankBonusResponse.BankBonus.reward (Casino.Reward, repeated)`
- `Casino.CollectBankBonusResponse.bank_bonus (Casino.CollectBankBonusResponse.BankBonus, repeated)`
- `Casino.CollectBankBonusResponse.rewards_state_info (Casino.RewardsStateInfo, optional)`
- `Casino.CollectDailyBonusResponse.daily_bonus (Casino.DailyBonus, optional)`
- `Casino.CollectDailyBonusResponse.hourly_bonus_video_ad_watched (bool, optional)`
- `Casino.CollectMysteryRewardResponse.mystery_pending_rewards (int32, optional)`
- `Casino.CollectMysteryRewardResponse.mystery_reward_level (int64, optional)`
- `Casino.CollectMysteryRewardResponse.next_mystery_reward (Casino.NextMysteryReward, optional)`
- `Casino.CollectMysteryRewardResponse.rewards_data (Casino.RewardsData, optional)`
- `Casino.CollectiblesSetReward.reward (Casino.Reward, repeated)`
- `Casino.ConquestReward.reward (Casino.Reward, repeated)`
- `Casino.ConsumeTokenResponse.TokenReward.reward (Casino.Reward, repeated)`
- `Casino.ConsumeTokenResponse.rewards_state_info (Casino.RewardsStateInfo, optional)`
- `Casino.ConsumeTokenResponse.token_reward (Casino.ConsumeTokenResponse.TokenReward, repeated)`
- `Casino.DailyBonus.additionalRewards (Casino.Reward, repeated)`
- `Casino.DailyBonus.reward (int32, required)`
- `Casino.DailyBonus.rewards (Casino.DailyBonus.DailyReward, repeated)`
- `Casino.DailyWheelOffer.Wedge.reward (Casino.Reward, repeated)`
- `Casino.DailyWheelOffer.additional_reward (Casino.Reward, optional)`
- `Casino.GiveFreeGiftRoundRequest.win_multiplier (double, optional)`
- `Casino.IapProduct.RewardData.reward (Casino.Reward, required)`
- `Casino.LeaguePointBonus.bonus_percent (uint32, optional)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.ChallengeReward.reward (Casino.Reward, repeated)`
- `Casino.LoginResponse.MissedInfo.ConquestMissedInfo.EventReward.reward (Casino.Reward, repeated)`
- … 35 more rows in `fields.csv`

### Timing / reset / expiry

- `Casino.AddDciEventRequest.CharmsEvent.RewardPromo.expire (int64, required)`
- `Casino.BreakPiggyBankRequest.hourly_bonus_timer (int32, optional)`
- `Casino.BreakPiggyBankRequest.piggy_bank_timer (int32, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.end_time (uint32, required)`
- `Casino.ClubsProto.ClubWallItem.Bonus.end_time (uint32, optional)`
- `Casino.CollectDailyBonusResponse.daily_bonus_timer (int32, optional)`
- `Casino.CollectDailyBonusResponse.hourly_bonus_timer (int32, optional)`
- `Casino.CollectHourlyBonusResponse.hourly_bonus_timer (int32, optional)`
- `Casino.CollectShopBonusResponse.shop_bonus_timer (int32, optional)`
- `Casino.ConfirmFreeGiftRoundRequest.duration (int32, required)`
- `Casino.ConfirmFreeGiftRoundRequest.expire (int32, required)`
- `Casino.Gift.expire (int32, required)`
- `Casino.NonSpinBonusGameProto.Data.end_time (uint32, required)`
- `Casino.Reward.LeaguePointsBonus.expiration_time_in_millis (int64, required)`
- `Casino.Reward.MissionsData.club_missions_end_time (int32, optional)`
- `Casino.Reward.battle_pass_points (Casino.Reward.BattlePassPoints, optional)`
- `Casino.Reward.battle_pass_premium (Casino.Reward.BattlePassPremium, optional)`
- `Casino.Reward.club_wall_bonus_expire (int32, optional)`
- `Casino.RewardsStateInfo.hourly_bonus_timer (int32, optional)`
- `Casino.SlotsProto.BonusInfo.timestamp (uint64, optional)`
- `Casino.SlotsProto.SocialBonus.time_to_bonus (uint32, required)`

### Segment / eligibility / limit

- `Casino.BankBonus.available (bool, optional)`
- `Casino.Reward.game_to_unlock (Casino.Reward.GameToUnlock, optional)`

### Other structural fields

- `Casino.BankBonus.day (uint32, optional)`
- `Casino.BankBonus.days (uint32, optional)`
- `Casino.BankBonus.free_activated (bool, optional)`
- `Casino.BankBonus.type (int32, required)`
- `Casino.BattlePassReward.collected (bool, optional)`
- `Casino.BuyGiftResponse.error_code (int32, optional)`
- `Casino.CharmsThemeReward.promo (bool, optional)`
- `Casino.ClaimRewardBundleBulkRequest.request (Casino.ClaimRewardBundleRequest, repeated)`
- `Casino.ClaimRewardBundleBulkResponse.bundle (Casino.Bundle, repeated)`
- `Casino.ClaimRewardBundleBulkResponse.error_code (int32, optional)`
- `Casino.ClaimRewardBundleResponse.bundle (Casino.Bundle, optional)`
- `Casino.ClaimRewardBundleResponse.error_code (int32, optional)`
- `Casino.ClubSetMilestoneReward.step (int32, optional)`
- `Casino.ClubsProto.ClubEvent.ClubEventReward.disabled (bool, optional)`
- `Casino.ClubsProto.ClubNotificationRequest.ClubWallBonus.type (uint32, optional)`
- `Casino.ClubsProto.ClubSeason.PlaceReward.action (Casino.SeasonAction, optional)`
- `Casino.ClubsProto.ClubSeason.PlaceReward.from_place (uint32, required)`
- `Casino.ClubsProto.ClubWallCollectBonusResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsRequest.type (uint32, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.avatar (Casino.Avatar, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.contributors (Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor, repeated)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubWallGetResponse.BonusSummary.type (uint32, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.type (uint32, required)`
- `Casino.CollectBankBonusResponse.BankBonus.day_collected (int32, required)`
- `Casino.CollectBankBonusResponse.BankBonus.type (int32, required)`
- `Casino.CollectBankBonusResponse.error_code (int32, optional)`
- `Casino.CollectDailyBonusResponse.daily_wheel_offer (Casino.DailyWheelOffer, optional)`
- `Casino.CollectDailyBonusResponse.error_code (int32, optional)`
- `Casino.CollectFreeDiamondsResponse.error_code (int32, optional)`
- `Casino.CollectHourlyBonusResponse.error_code (int32, optional)`
- `Casino.CollectMysteryRewardResponse.error_code (int32, optional)`
- `Casino.CollectRateUsBonusResponse.error_code (int32, optional)`
- `Casino.CollectShopBonusResponse.error_code (int32, optional)`
- `Casino.CollectiblesSetReward.promo (bool, optional)`
- `Casino.ConfirmFreeGiftRoundResponse.confirm (bool, required)`
- `Casino.ConsumeTokenResponse.TokenReward.item (Casino.Item, repeated)`
- `Casino.ConsumeTokenResponse.TokenReward.reason (string, optional)`
- `Casino.ConsumeTokenResponse.TokenReward.type (int32, required)`
- `Casino.ConsumeTokenResponse.error_code (int32, optional)`
- … 101 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `LOT-20260827-A`:

- `AppServer.CollectMysteryReward` — 138 (69 request, 69 response)
- `AppServer.ClaimRewardBundleBulk` — 10 (5 request, 5 response)
- `AppServer.ClaimRewardBundle` — 6 (3 request, 3 response)
- `AppServer.CollectHourlyBonus` — 2 (1 request, 1 response)
- `AppClient.UpdateGift` — 2 (2 request, 0 response)
- `AppClient.ConfirmFreeGiftRound` — 2 (1 request, 1 response)
- `AppClient.UpdateNextMysteryReward` — 2 (2 request, 0 response)
- `AppClient.NotifyRewardBundles` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].type` | 587 | 1174 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.levels_amount` | 587 | 587 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.target_level` | 587 | 587 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].level.value` | 587 | 587 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].type` | 587 | 1129 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].time.duration` | 365 | 542 | 2 | varying-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].time.expire_time` | 365 | 365 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.extra_items.extra_items[].value[].time.value` | 365 | 542 | 1 | constant-in-session |
| `Casino.UpdateProgressRequest.rewards_data.state_info.hourly_bonus_timer` | 365 | 365 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.reward[].id` | 346 | 354 | 6 | varying-in-session |
| `Casino.LotteryTossResponse.state.puzzle_board[].reward.big_chips_delta.value` | 346 | 1384 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.state.puzzle_board[].reward.chips_delta` | 346 | 1384 | 4 | varying-in-session |
| `Casino.LotteryTossResponse.state.puzzle_board[].reward.id` | 346 | 1384 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].type` | 333 | 666 | 2 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].level.levels_amount` | 333 | 333 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].level.target_level` | 333 | 333 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].level.value` | 333 | 333 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].type` | 333 | 777 | 2 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].time.duration` | 331 | 444 | 3 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].time.expire_time` | 331 | 331 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.extra_items.extra_items[].value[].time.value` | 331 | 444 | 1 | constant-in-session |
| `Casino.LotteryTossResponse.lottery_reward.state_info.hourly_bonus_timer` | 331 | 331 | 2 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.reward[].big_chips_delta.value` | 318 | 318 | 42 | varying-in-session |
| `Casino.LotteryTossResponse.lottery_reward.reward[].chips_delta` | 318 | 318 | 42 | varying-in-session |
| `Casino.UpdateShopRequest.product[].bank_bonus_days` | 153 | 153 | 1 | constant-in-session |
| `Casino.UpdateShopRequest.product[].bank_bonus_type` | 153 | 153 | 1 | constant-in-session |
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
| … | | | | 988 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `LOT-20260827-A`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: config/update announces reward availability -> claim/collect request -> response returns reward/state -> client update/notification confirms delivery; bulk reward bundles aggregate multiple claims.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_dailybonus_2_etc2.zpk`
- ZPK asset: `assets/atlas_dailybonus_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_free_drinks_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_paidwheel_2_etc2.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open hourly/daily/shop bonus, mystery reward and free-gift surfaces with markers.
- Claim one naturally available reward of each visible family and mark before/after.
- Open reward detail/bundle contents before claiming when the UI allows it.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
