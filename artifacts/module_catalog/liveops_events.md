# Other LiveOps / DCI / Tower / Balloons

Cross-cutting DCI event containers, announcements, Tower, Balloons, other promotions, reskins/texts and mini-game event state not owned by another dossier.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **90/100 — substantial live structure**
- Primary live samples: **382** from `20260901_160002`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **4 / 18**
- Live populated field paths: **270**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **88**

- `Casino.AddDciEventRequest` (AppClient.proto)
- `Casino.AddDciEventRequest.BalloonsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.BoxForSpinConfig` (AppClient.proto)
- `Casino.AddDciEventRequest.BoxForSpinConfig.BetChance` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.RewardPromo` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.StarsPerRarity` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.Trading` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId` (AppClient.proto)
- `Casino.AddDciEventRequest.CharmsEvent.Tutorial` (AppClient.proto)
- `Casino.AddDciEventRequest.ClubSetEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.CollectionEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.CollectionEvent.Milestone` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef` (AppClient.proto)
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef` (AppClient.proto)
- `Casino.AddDciEventRequest.ContactPointEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.PuzzleBoardMultiplier` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureFlags` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureMultipliers` (AppClient.proto)
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent.LotteryMachine` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoFrame` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoRibbon` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.OfferSaleBadge` (AppClient.proto)
- `Casino.AddDciEventRequest.ReskinsAndTextsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.ReskinsAndTextsEvent.CommunityTile` (AppClient.proto)
- `Casino.AddDciEventRequest.ReskinsAndTextsEvent.FunctionTile` (AppClient.proto)
- `Casino.AddDciEventRequest.ReskinsAndTextsEvent.PyroEffect` (AppClient.proto)
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial` (AppClient.proto)
- `Casino.AddDciEventRequest.TowerEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.TowerEvent.TutorialData` (AppClient.proto)
- `Casino.AddDciEventRequest.VaultEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.VaultPromoEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.VideoAdsEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.VideoAdsEvent.AdsPlacement` (AppClient.proto)
- `Casino.AddDciEventRequest.VideoAdsEvent.Impressions` (AppClient.proto)
- `Casino.AddDciEventRequest.VouchersEvent` (AppClient.proto)
- `Casino.AdditionalDataRequest` (AppClient.proto)
- `Casino.BalloonsMilestone` (Common.proto)
- `Casino.BalloonsResultResponse` (AppServer.proto)
- `Casino.BalloonsStartResponse` (AppServer.proto)
- `Casino.BalloonsStartResponse.PopResult` (AppServer.proto)
- `Casino.BalloonsStartTimerResponse` (AppServer.proto)
- `Casino.BalloonsState` (Common.proto)
- `Casino.BalloonsSyncRequest` (AppServer.proto)
- `Casino.BalloonsSyncResponse` (AppServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo` (AppServer.proto)
- `Casino.MiniGameTutorialCompleteRequest` (AppServer.proto)
- `Casino.MiniGameTutorialCompleteResponse` (AppServer.proto)
- `Casino.MinigameEventTrail` (Common.proto)
- `Casino.MinigameEventTrail.Step` (Common.proto)
- `Casino.RemoveDciEventRequest` (AppClient.proto)
- `Casino.RemoveDciEventRequest.TowerEvent` (AppClient.proto)
- `Casino.TowerGrabAndGoResponse` (AppServer.proto)
- `Casino.TowerHandleZonkRequest` (AppServer.proto)
- `Casino.TowerHandleZonkResponse` (AppServer.proto)
- `Casino.TowerMissedInfo` (AppServer.proto)
- `Casino.TowerOpenDoorRequest` (AppServer.proto)
- `Casino.TowerOpenDoorResponse` (AppServer.proto)
- `Casino.TowerOpenDoorResponse.DoorLoot` (AppServer.proto)
- `Casino.TowerRunProgress` (Common.proto)
- `Casino.TowerSet` (Common.proto)
- `Casino.TowerSet.Tower` (Common.proto)
- `Casino.TowerSet.Tower.Floor` (Common.proto)
- `Casino.TowerSetTutorialStateRequest` (AppServer.proto)
- `Casino.TowerStartRunResponse` (AppServer.proto)
- `Casino.TriggerAnnouncementRequest` (AppServer.proto)
- `Casino.TriggerAnnouncementResponse` (AppServer.proto)
- `Casino.UpdateAnnouncementsRequest` (AppClient.proto)
- `Casino.UpdateAnnouncementsRequest.Announcement` (AppClient.proto)
- `Casino.UpdateProgressRequest.MiniGameEventProgress` (AppClient.proto)
- `Casino.UpdateProgressRequest.TowerKeyProgress` (AppClient.proto)

## RPC and flow structure

Observed/schema flow: DCI add/remove and announcements configure live content -> feature-specific start/sync/result/progress operations -> completion/reward surfaces -> event removal/expiry.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.TriggerAnnouncement` | `Casino.TriggerAnnouncementRequest` | `Casino.TriggerAnnouncementResponse` | 4 | 4 | observed-live |
| `AppServer.MiniGameTutorialComplete` | `Casino.MiniGameTutorialCompleteRequest` | `Casino.MiniGameTutorialCompleteResponse` | 0 | 0 | schema-only |
| `AppServer.TowerStartRun` | `Casino.EmptyRequest` | `Casino.TowerStartRunResponse` | 0 | 0 | schema-only |
| `AppServer.TowerOpenDoor` | `Casino.TowerOpenDoorRequest` | `Casino.TowerOpenDoorResponse` | 0 | 0 | schema-only |
| `AppServer.TowerHandleZonk` | `Casino.TowerHandleZonkRequest` | `Casino.TowerHandleZonkResponse` | 0 | 0 | schema-only |
| `AppServer.TowerGrabAndGo` | `Casino.EmptyRequest` | `Casino.TowerGrabAndGoResponse` | 0 | 0 | schema-only |
| `AppServer.TowerSetTutorialState` | `Casino.TowerSetTutorialStateRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.BalloonsStart` | `Casino.EmptyRequest` | `Casino.BalloonsStartResponse` | 0 | 0 | schema-only |
| `AppServer.BalloonsSync` | `Casino.BalloonsSyncRequest` | `Casino.BalloonsSyncResponse` | 0 | 0 | schema-only |
| `AppServer.BalloonsResult` | `Casino.EmptyRequest` | `Casino.BalloonsResultResponse` | 0 | 0 | schema-only |
| `AppServer.BalloonsStartTimer` | `Casino.EmptyRequest` | `Casino.BalloonsStartTimerResponse` | 0 | 0 | schema-only |
| `AppClient.UpdateAnnouncements` | `Casino.UpdateAnnouncementsRequest` | `Casino.EmptyResponse` | 1 | 0 | observed-live |
| `AppClient.SendAdditionalData` | `Casino.AdditionalDataRequest` | `Casino.EmptyResponse` | 295 | 0 | observed-live |
| `AppClient.AddDciEvent` | `Casino.AddDciEventRequest` | `Casino.EmptyResponse` | 78 | 0 | observed-live |
| `AppClient.RemoveDciEvent` | `Casino.RemoveDciEventRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.NoVideoAdsForPlayer` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.NoReskinsOrTextsForPlayer` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppClient.FeaturesInitialized` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData.theme_id (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId.charm_id (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_charm_id (Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId, repeated)`
- `Casino.AddDciEventRequest.CollectionEvent.gfx_set_id (int32, required)`
- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress.challenge_id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.conquest_cluster_id (int64, optional)`
- `Casino.AddDciEventRequest.ConquestEvent.distributed_event_id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.division_id (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.instance_id (int64, required)`
- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent.event_id (int64, required)`
- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.product (Casino.IapProduct, repeated)`
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureFlags.feature_id (int32, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.FeatureMultipliers.feature_id (int32, optional)`
- `Casino.AddDciEventRequest.MiniGameEvent.game_id (int64, required)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.event_id (int64, required)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.theme_id (int64, required)`
- `Casino.AddDciEventRequest.VideoAdsEvent.AdsPlacement.placement_id (int32, required)`
- `Casino.AddDciEventRequest.VideoAdsEvent.ad_unit_id (string, required)`
- `Casino.AddDciEventRequest.VideoAdsEvent.configuration_id (int64, required)`
- `Casino.AddDciEventRequest.event_id (int64, required)`
- `Casino.BalloonsResultResponse.session_id (int32, optional)`
- `Casino.BalloonsState.current_milestone_id (int32, optional)`
- `Casino.BalloonsState.session_id (int32, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.event_id (int64, required)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.game_id (int64, required)`
- `Casino.MiniGameTutorialCompleteRequest.event_id (int64, required)`
- `Casino.RemoveDciEventRequest.event_id (int64, required)`
- `Casino.TowerMissedInfo.event_id (int64, required)`
- `Casino.TowerMissedInfo.missed_info_id (int64, required)`
- `Casino.TriggerAnnouncementRequest.id (Casino.OfferId, required)`
- `Casino.UpdateProgressRequest.MiniGameEventProgress.event_id (int64, required)`
- `Casino.UpdateProgressRequest.TowerKeyProgress.event_id (int64, required)`

### Progression / state

- `Casino.AddDciEventRequest.BalloonsEvent.state (Casino.BalloonsState, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.CharmsPrimaryData.theme_level (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.duplicates_state (Casino.CollectiblesDuplicatesState, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.progress_data (Casino.CharmsProgressData, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.tutorial (Casino.AddDciEventRequest.CharmsEvent.Tutorial, optional)`
- `Casino.AddDciEventRequest.ClubSetEvent.progress_data (Casino.ClubSetProgressData, optional)`
- `Casino.AddDciEventRequest.CollectionEvent.state (Casino.CollectionEventState, optional)`
- `Casino.AddDciEventRequest.ConquestEvent.player_progress (Casino.AddDciEventRequest.ConquestEvent.PlayerProgress, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier.level (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.show_tutorial (bool, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.points_to_keep_status (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.Tier.required_points (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.can_collect_points (bool, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.current_tier_label (string, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.points (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.tiers (Casino.AddDciEventRequest.LoyaltyEvent.Tier, repeated)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.show_tutorial (bool, optional)`
- `Casino.AddDciEventRequest.MiniGameEvent.mini_game_progress_state (Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState, required)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.tutorial (Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial, optional)`
- `Casino.AddDciEventRequest.TowerEvent.TutorialData.state (int32, required)`
- `Casino.AddDciEventRequest.TowerEvent.key_progress (double, required)`
- `Casino.AddDciEventRequest.TowerEvent.tower_run_progress (Casino.TowerRunProgress, required)`
- `Casino.AddDciEventRequest.TowerEvent.tutorial_data (Casino.AddDciEventRequest.TowerEvent.TutorialData, optional)`
- `Casino.AddDciEventRequest.VideoAdsEvent.Impressions.count (int32, required)`
- `Casino.AddDciEventRequest.VouchersEvent.points (int64, required)`
- `Casino.AddDciEventRequest.VouchersEvent.tutorial_completed (bool, optional)`
- `Casino.BalloonsResultResponse.status (Casino.BalloonsResultResponse.Status, optional)`
- `Casino.BalloonsStartResponse.progress (int32, optional)`
- `Casino.BalloonsStartResponse.state (Casino.BalloonsState, optional)`
- `Casino.BalloonsStartResponse.status (Casino.BalloonsStartResponse.Status, optional)`
- `Casino.BalloonsStartTimerResponse.status (Casino.BalloonsStartTimerResponse.Status, optional)`
- `Casino.BalloonsState.milestone_progress (int32, optional)`
- `Casino.BalloonsState.recompletion_level (int32, optional)`
- `Casino.BalloonsState.tutorial (bool, optional)`
- `Casino.BalloonsSyncRequest.progress (int32, optional)`
- `Casino.BalloonsSyncResponse.status (Casino.BalloonsSyncResponse.Status, optional)`
- `Casino.LoginResponse.MissedInfo.MiniGameEventMissedInfo.event_completed (bool, optional)`
- `Casino.MiniGameTutorialCompleteResponse.status (Casino.MiniGameTutorialCompleteResponse.Status, required)`
- `Casino.TowerGrabAndGoResponse.status (Casino.TowerGrabAndGoResponse.Status, required)`
- `Casino.TowerGrabAndGoResponse.tower_run_progress (Casino.TowerRunProgress, optional)`
- … 13 more rows in `fields.csv`

### Cost / input

- `Casino.AddDciEventRequest.BoxForSpinConfig.BetChance.bet (int64, required)`
- `Casino.AddDciEventRequest.BoxForSpinConfig.bet_chance (Casino.AddDciEventRequest.BoxForSpinConfig.BetChance, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.TokenDeltaForCharmId.token_delta (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_duplicate_charm (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_missing_charm (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_new_charm (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.token_delta_for_request_creation (int32, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.ticket_color (Casino.LotteryColor, required)`
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.ticket_color (Casino.LotteryColor, required)`
- `Casino.AddDciEventRequest.LotteryEvent.free_ticket (Casino.LotteryFreeTicketState, required)`
- `Casino.AddDciEventRequest.LotteryEvent.ticket_balance (Casino.InventoryEntry, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.tickets_products (Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts, repeated)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.current_sum_of_bets (Casino.Chips, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.MiniGameProgressState.required_sum_of_bets (Casino.Chips, required)`
- `Casino.UpdateProgressRequest.MiniGameEventProgress.current_sum_of_bets (Casino.Chips, required)`
- `Casino.UpdateProgressRequest.MiniGameEventProgress.required_sum_of_bets (Casino.Chips, required)`

### Currency / balance

- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.chips_to_flag (int64, required)`

### Reward / output

- `Casino.AddDciEventRequest.CharmsEvent.Tutorial.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.reward_promo_main (Casino.AddDciEventRequest.CharmsEvent.RewardPromo, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.reward_promo_milestone (Casino.AddDciEventRequest.CharmsEvent.RewardPromo, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.reward_promo_set (Casino.AddDciEventRequest.CharmsEvent.RewardPromo, optional)`
- `Casino.AddDciEventRequest.CharmsEvent.set_reward (Casino.CollectiblesSetReward, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.theme_reward (Casino.CharmsThemeReward, repeated)`
- `Casino.AddDciEventRequest.CollectionEvent.Milestone.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.challenge_reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.tournament_reward (Casino.ConquestReward, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.reward (Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.ticket_reward (Casino.AddDciEventRequest.LotteryEvent.TicketReward, repeated)`
- `Casino.AddDciEventRequest.LoyaltyEvent.tutorial_reward (Casino.Reward, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.Tutorial.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.main_reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.main_reward_for_all_rounds (Casino.TimeBasedCharmsMainReward, repeated)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.milestone_reward (Casino.TimeBasedCharmsMilestoneReward, repeated)`
- `Casino.AddDciEventRequest.VideoAdsEvent.AdsPlacement.reward (Casino.Reward, repeated)`
- `Casino.BalloonsMilestone.reward (Casino.Reward, repeated)`
- `Casino.BalloonsResultResponse.milestone_rewards_data (Casino.RewardsData, optional)`
- `Casino.BalloonsResultResponse.rewards_data (Casino.RewardsData, optional)`
- `Casino.BalloonsStartResponse.PopResult.reward (Casino.Reward, repeated)`
- `Casino.MinigameEventTrail.Step.reward (Casino.Reward, repeated)`
- `Casino.MinigameEventTrail.rewards_multiplier (double, required)`
- `Casino.TowerGrabAndGoResponse.awarded_loot (Casino.TowerMissedInfo, optional)`
- `Casino.TowerHandleZonkResponse.awarded_loot (Casino.TowerMissedInfo, optional)`
- `Casino.TowerMissedInfo.grand_reward (Casino.Reward, repeated)`
- `Casino.TowerMissedInfo.loot_reward (Casino.Reward, repeated)`
- `Casino.TowerOpenDoorResponse.awarded_loot (Casino.TowerMissedInfo, optional)`
- `Casino.TowerSet.Tower.grand_reward (Casino.Reward, repeated)`

### Timing / reset / expiry

- `Casino.AddDciEventRequest.CharmsEvent.RewardPromo.expire (int64, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.request_duration (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.number_of_resets (int32, optional)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.end_time (int32, required)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef.start_time (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent.expire (int64, required)`
- `Casino.AddDciEventRequest.LotteryEvent.free_ticket_timestamp (int32, required)`
- `Casino.AddDciEventRequest.LoyaltyEvent.reset_timestamp (int64, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.tier_before_reset (string, optional)`
- `Casino.AddDciEventRequest.LoyaltyEvent.year_reset (bool, optional)`
- `Casino.AddDciEventRequest.TimeBasedCharmsEvent.number_of_resets (int32, optional)`
- `Casino.AddDciEventRequest.VideoAdsEvent.AdsPlacement.cooldown (int32, optional)`
- `Casino.AddDciEventRequest.expire (int64, required)`
- `Casino.AddDciEventRequest.time_based_charms (Casino.AddDciEventRequest.TimeBasedCharmsEvent, optional)`
- `Casino.BalloonsStartResponse.duration (int32, optional)`
- `Casino.BalloonsStartResponse.time_left_ms (int32, optional)`
- `Casino.UpdateAnnouncementsRequest.Announcement.timer (Casino.OfferTimer, optional)`

### Segment / eligibility / limit

- `Casino.AddDciEventRequest.CharmsEvent.Trading.daily_limit (int32, required)`
- `Casino.AddDciEventRequest.CharmsEvent.Trading.temporary_unlocked_charms (int32, repeated)`
- `Casino.AddDciEventRequest.CharmsEvent.unlock_level (int32, optional)`
- `Casino.AddDciEventRequest.LotteryEvent.bulk_play_cap (int32, required)`
- `Casino.AddDciEventRequest.MiniGameEvent.bulk_play_cap (int32, optional)`
- `Casino.AddDciEventRequest.TowerEvent.key_cap (int32, required)`
- `Casino.BalloonsResultResponse.recompletion_available (bool, optional)`

### Other structural fields

- `Casino.AddDciEventRequest.BalloonsEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.BalloonsEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.BalloonsEvent.inventory_delta (Casino.InventoryEntry, repeated)`
- `Casino.AddDciEventRequest.BalloonsEvent.lost_lives (int32, optional)`
- `Casino.AddDciEventRequest.BoxForSpinConfig.BetChance.chance (double, required)`
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
- `Casino.AddDciEventRequest.ClubSetEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.ClubSetEvent.config_data (Casino.ClubSetConfigData, optional)`
- `Casino.AddDciEventRequest.ClubSetEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.CollectionEvent.Milestone.items_to_collect (int64, required)`
- `Casino.AddDciEventRequest.CollectionEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.CollectionEvent.balloons (Casino.AddDciEventRequest.BalloonsEvent, optional)`
- `Casino.AddDciEventRequest.CollectionEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.CollectionEvent.milestone (Casino.AddDciEventRequest.CollectionEvent.Milestone, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.PlayerProgress.player_challenge_flags (int64, required)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.definition (Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.ChallengeDef, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef.family_name (string, required)`
- `Casino.AddDciEventRequest.ConquestEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.ConquestEvent.challenge_definition (Casino.AddDciEventRequest.ConquestEvent.SlotChallengeDef, repeated)`
- `Casino.AddDciEventRequest.ConquestEvent.chat_history (Casino.ClubsProto.ClubNotificationRequest, repeated)`
- `Casino.AddDciEventRequest.ContactPointEvent.hmac (string, required)`
- `Casino.AddDciEventRequest.ContactPointEvent.is_vip (bool, required)`
- `Casino.AddDciEventRequest.ContactPointEvent.show_ftue (bool, optional)`
- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier.multiplier (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.PuzzleBoardMultiplier.color (int32, required)`
- … 139 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260901_160002`:

- `AppClient.SendAdditionalData` — 295 (295 request, 0 response)
- `AppClient.AddDciEvent` — 78 (78 request, 0 response)
- `AppServer.TriggerAnnouncement` — 8 (4 request, 4 response)
- `AppClient.UpdateAnnouncements` — 1 (1 request, 0 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.AdditionalDataRequest.additional_data.data[].key` | 295 | 297 | 3 | varying-in-session |
| `Casino.AdditionalDataRequest.additional_data.data[].value_string` | 295 | 297 | 27 | varying-in-session |
| `Casino.AddDciEventRequest.event_id` | 78 | 78 | 5 | varying-in-session |
| `Casino.AddDciEventRequest.expire` | 78 | 78 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.hbi_data.custom_fields` | 78 | n/a | n/a | not-assessed |
| `Casino.AddDciEventRequest.hbi_data.id` | 78 | 78 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.art_config.expiration_date` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.art_config.package[].path` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.art_config.package[].reskin_name` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.art_config.package[].type` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.art_config.package[].version` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.bulk_play_cap` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.config_hbi_data[].config_identifier` | 68 | 408 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.config_hbi_data[].config_type` | 68 | 408 | 6 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.config_hbi_data[].hbi_data.id` | 68 | 408 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.free_ticket.progress` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.free_ticket.threshold` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.free_ticket.ticket_color` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.free_ticket_timestamp` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.lottery_multiplier.level` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.lottery_multiplier.multiplier` | 68 | 68 | 2 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.puzzle_board[].position` | 68 | 272 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.puzzle_board[].puzzle_color` | 68 | 272 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.puzzle_board[].reward.big_chips_delta.value` | 68 | 272 | 7 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.puzzle_board[].reward.chips_delta` | 68 | 272 | 7 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.puzzle_board[].reward.id` | 68 | 272 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.show_tutorial` | 68 | 68 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_balance[].amount` | 68 | 272 | 11 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_balance[].id` | 68 | 272 | 4 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].big_chips_delta.value` | 68 | 2924 | 61 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].chips_delta` | 68 | 2924 | 61 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.box_id` | 68 | 408 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.box_type` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.raffle_id` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.source` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.theme_id` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box.type` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.box_id` | 68 | 408 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.box_type` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.event_type` | 68 | 408 | 1 | constant-in-session |
| … | | | | 230 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Observed/schema flow: DCI add/remove and announcements configure live content -> feature-specific start/sync/result/progress operations -> completion/reward surfaces -> event removal/expiry.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_liveops_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/atlas_tiles_reskinned_sku_hc_2_etc2.zpk`
- ZPK asset: `assets/sound_balloons.zpk`
- ZPK asset: `assets/sound_minigames.zpk`
- ZPK asset: `assets/sound_tower.zpk`
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open Tower, Balloons and every unmatched live-event tile with distinct markers.
- Mark event start, one interaction, result and exit for each accessible mini-game.
- Capture announcement/detail screens and event expiry/removal when naturally observed.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
