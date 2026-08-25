# Slots / Lobby / Spin / Jackpot

Slot lobby discovery, machine entry, spin/free-spin/bonus decisions, reel stops, personal/shared state and jackpot flows.

## Catalog status

- Evidence status: **live-confirmed**
- Structural completeness: **90/100 — substantial live structure**
- Primary live samples: **288** from `20260825_182300`
- Cross-cutting live samples: **1**
- Live endpoints / schema endpoints: **9 / 32**
- Live populated field paths: **71**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Clubs.proto`, `GameHost.proto`, `NonSpinBonusGame.proto`, `Services.proto`, `Slots.proto`, `VideoPoker.proto`
- Services: `AppServer`, `GameHost`, `SlotsGameClient`, `SlotsGameServer`
- Related message types: **90**

- `Casino.AddDciEventRequest.BoxForSpinConfig` (AppClient.proto)
- `Casino.AddDciEventRequest.BoxForSpinConfig.BetChance` (AppClient.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsRequest` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor` (Clubs.proto)
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus` (Clubs.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.GameCategoryEntry` (AppServer.proto)
- `Casino.GameData.JackpotDefData` (GameHost.proto)
- `Casino.GetGamePlayerCountRequest` (AppServer.proto)
- `Casino.GetGamePlayerCountResponse` (AppServer.proto)
- `Casino.GetJackpotValuesRequest` (AppServer.proto)
- `Casino.GetJackpotValuesResponse` (AppServer.proto)
- `Casino.JackpotGetRequest` (GameHost.proto)
- `Casino.JackpotGetResponse` (GameHost.proto)
- `Casino.JackpotHitRequest` (GameHost.proto)
- `Casino.JackpotHitRequest.Jackpot` (GameHost.proto)
- `Casino.JackpotHitResponse` (GameHost.proto)
- `Casino.JackpotHitResponse.Jackpot` (GameHost.proto)
- `Casino.JackpotIncrRequest` (GameHost.proto)
- `Casino.JackpotIncrRequest.Jackpot` (GameHost.proto)
- `Casino.JackpotInitRequest` (GameHost.proto)
- `Casino.JackpotInitRequest.Jackpot` (GameHost.proto)
- `Casino.JoinGameRequest` (AppServer.proto)
- `Casino.JoinGameResponse` (AppServer.proto)
- `Casino.LeaveGameResponse` (AppServer.proto)
- `Casino.ListGamesRequest` (AppServer.proto)
- `Casino.ListGamesResponse` (AppServer.proto)
- `Casino.ListGamesResponse.ListGamesEntry` (AppServer.proto)
- `Casino.ListGamesResponse.ListGamesEntry.Jackpot` (AppServer.proto)
- `Casino.ListGamesResponse.PromoFrame` (AppServer.proto)
- `Casino.NonSpinBonusGameProto` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BonusResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BuyBonusRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.BuyBonusResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.Data` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetDataRequest` (NonSpinBonusGame.proto)
- `Casino.NonSpinBonusGameProto.GetDataResponse` (NonSpinBonusGame.proto)
- `Casino.PinGameRequest` (AppServer.proto)
- `Casino.PinGameResponse` (AppServer.proto)
- `Casino.PinnedGame` (AppServer.proto)
- `Casino.QueryGameEntry` (AppServer.proto)
- `Casino.QueryGameEntry.Jackpot` (AppServer.proto)
- `Casino.QueryGameFamilyRequest` (AppServer.proto)
- `Casino.QueryGameFamilyResponse` (AppServer.proto)
- `Casino.QueryGamePlayerRequest` (AppServer.proto)
- `Casino.QueryGamePlayerResponse` (AppServer.proto)
- `Casino.QueryGamePlayerResponse.GamePlayer` (AppServer.proto)
- `Casino.QueryGameRequest` (AppServer.proto)
- `Casino.QueryGameResponse` (AppServer.proto)
- `Casino.SlotsProto` (Slots.proto)
- `Casino.SlotsProto.AwardInfo` (Slots.proto)
- `Casino.SlotsProto.BonusId` (Slots.proto)
- `Casino.SlotsProto.BonusInfo` (Slots.proto)
- `Casino.SlotsProto.ChoiceSelection` (Slots.proto)
- `Casino.SlotsProto.CounterInfo` (Slots.proto)
- `Casino.SlotsProto.ExplosionInfo` (Slots.proto)
- `Casino.SlotsProto.JackpotInfo` (Slots.proto)
- `Casino.SlotsProto.JackpotList` (Slots.proto)
- `Casino.SlotsProto.JackpotList.Jackpot` (Slots.proto)
- `Casino.SlotsProto.MultiplierInfo` (Slots.proto)
- `Casino.SlotsProto.PayruleInfo` (Slots.proto)
- `Casino.SlotsProto.PayruleInfo.Position` (Slots.proto)
- `Casino.SlotsProto.PersonalState` (Slots.proto)
- `Casino.SlotsProto.PlayBonusDecision` (Slots.proto)
- `Casino.SlotsProto.SharedFreeSpins` (Slots.proto)
- `Casino.SlotsProto.SocialBonus` (Slots.proto)
- `Casino.SlotsProto.SocialBonus.Player` (Slots.proto)
- `Casino.SlotsProto.SpinInfo` (Slots.proto)
- `Casino.SlotsProto.SpinInfoRequest` (Slots.proto)
- `Casino.SlotsProto.SpinRequest` (Slots.proto)
- `Casino.SlotsProto.SpinResponse` (Slots.proto)
- `Casino.SlotsProto.SpinResponse.Bonus` (Slots.proto)
- `Casino.SlotsProto.SpinResponse.FreeSpins` (Slots.proto)
- `Casino.SlotsProto.SpinResponse.PayruleRandomSpinAction` (Slots.proto)
- `Casino.SlotsProto.SpinResponse.SubsymbolIndex` (Slots.proto)
- `Casino.SlotsProto.SymbolInfo` (Slots.proto)
- `Casino.SlotsProto.SymbolInfo.Property` (Slots.proto)
- `Casino.SlotsProto.Timer` (Slots.proto)
- `Casino.SlotsProto.TimerList` (Slots.proto)
- `Casino.SlotsProto.UpdateTimersRequest` (Slots.proto)
- `Casino.SlotsProto.User` (Slots.proto)
- `Casino.SlotsProto.UserList` (Slots.proto)
- `Casino.UnlockGameRequest` (AppServer.proto)
- `Casino.UnlockGameResponse` (AppServer.proto)
- `Casino.VideoPokerProto.JackpotList` (VideoPoker.proto)
- `Casino.VideoPokerProto.JackpotList.Jackpot` (VideoPoker.proto)

## RPC and flow structure

Inferred flow: lobby list/query -> join machine -> `Spin`/`FreeSpin` or bonus decision -> `SpinResponse` plus asynchronous jackpot/personal-state updates -> leave game. Jackpot host operations form a related server-side lifecycle.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.JoinGame` | `Casino.JoinGameRequest` | `Casino.JoinGameResponse` | 2 | 2 | observed-live |
| `AppServer.LeaveGame` | `Casino.EmptyRequest` | `Casino.LeaveGameResponse` | 2 | 2 | observed-live |
| `AppServer.ListGames` | `Casino.ListGamesRequest` | `Casino.ListGamesResponse` | 2 | 2 | observed-live |
| `AppServer.QueryGamePlayer` | `Casino.QueryGamePlayerRequest` | `Casino.QueryGamePlayerResponse` | 2 | 2 | observed-live |
| `AppServer.QueryGame` | `Casino.QueryGameRequest` | `Casino.QueryGameResponse` | 6 | 6 | observed-live |
| `AppServer.GetJackpotValues` | `Casino.GetJackpotValuesRequest` | `Casino.GetJackpotValuesResponse` | 30 | 30 | observed-live |
| `AppServer.GetGamePlayerCount` | `Casino.GetGamePlayerCountRequest` | `Casino.GetGamePlayerCountResponse` | 0 | 0 | schema-only |
| `AppServer.PinGame` | `Casino.PinGameRequest` | `Casino.PinGameResponse` | 0 | 0 | schema-only |
| `AppServer.UnlockGame` | `Casino.UnlockGameRequest` | `Casino.UnlockGameResponse` | 0 | 0 | schema-only |
| `AppServer.QueryGameFamily` | `Casino.QueryGameFamilyRequest` | `Casino.QueryGameFamilyResponse` | 0 | 0 | schema-only |
| `GameHost.JackpotInit` | `Casino.JackpotInitRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.JackpotIncr` | `Casino.JackpotIncrRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `GameHost.JackpotGet` | `Casino.JackpotGetRequest` | `Casino.JackpotGetResponse` | 0 | 0 | schema-only |
| `GameHost.JackpotHit` | `Casino.JackpotHitRequest` | `Casino.JackpotHitResponse` | 0 | 0 | schema-only |
| `GameHost.SpinResult` | `Casino.SlotsProto.SpinInfoRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.Spin` | `Casino.SlotsProto.SpinRequest` | `Casino.SlotsProto.SpinResponse` | 29 | 29 | observed-live |
| `SlotsGameServer.FreeSpin` | `Casino.EmptyRequest` | `Casino.SlotsProto.SpinResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.BonusChoicesWithPrizes` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.BonusFinished` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameServer.ChoiceBonus` | `Casino.SlotsProto.ChoiceSelection` | `Casino.SlotsProto.SpinResponse.FreeSpins` | 0 | 0 | schema-only |
| `SlotsGameServer.PlayBonus` | `Casino.SlotsProto.PlayBonusDecision` | `Casino.SlotsProto.SpinResponse.Bonus` | 0 | 0 | schema-only |
| `SlotsGameServer.UpdateTimers` | `Casino.SlotsProto.UpdateTimersRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.RoomUsers` | `Casino.SlotsProto.UserList` | `Casino.EmptyResponse` | 116 | 0 | observed-live |
| `SlotsGameClient.UpdateJackpot` | `Casino.SlotsProto.JackpotList` | `Casino.EmptyResponse` | 26 | 0 | observed-live |
| `SlotsGameClient.HitJackpot` | `Casino.SlotsProto.JackpotList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.HitSharedJackpot` | `Casino.SlotsProto.JackpotList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.UpdateSharedFreeSpins` | `Casino.SlotsProto.SharedFreeSpins` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.HitSharedFreeSpins` | `Casino.SlotsProto.SharedFreeSpins` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.UpdateSocialBonus` | `Casino.SlotsProto.SocialBonus` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.HitSocialBonus` | `Casino.SlotsProto.SocialBonus` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.UpdatePersonalState` | `Casino.SlotsProto.PersonalState` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `SlotsGameClient.UpdateTimers` | `Casino.SlotsProto.TimerList` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.GameData.JackpotDefData.jackpot_id (uint32, repeated)`
- `Casino.GetJackpotValuesRequest.jackpot_id (uint32, repeated)`
- `Casino.JackpotGetRequest.jackpot_id (uint32, repeated)`
- `Casino.JackpotHitRequest.Jackpot.id (uint32, required)`
- `Casino.JackpotIncrRequest.Jackpot.id (uint32, required)`
- `Casino.JackpotInitRequest.Jackpot.id (uint32, required)`
- `Casino.JoinGameRequest.other_user_id (int64, optional)`
- `Casino.JoinGameRequest.room_id (uint64, optional)`
- `Casino.JoinGameRequest.server_id (int64, optional)`
- `Casino.ListGamesResponse.ListGamesEntry.Jackpot.id (uint32, required)`
- `Casino.ListGamesResponse.ListGamesEntry.game (Casino.GameDef, required)`
- `Casino.ListGamesResponse.game (Casino.ListGamesResponse.ListGamesEntry, repeated)`
- `Casino.PinGameRequest.game (Casino.PinnedGame, required)`
- `Casino.QueryGameEntry.Jackpot.id (uint32, required)`
- `Casino.QueryGameEntry.game (Casino.GameDef, required)`
- `Casino.QueryGamePlayerRequest.user_id (int64, repeated)`
- `Casino.QueryGamePlayerResponse.GamePlayer.locked_feature_id (uint32, repeated)`
- `Casino.QueryGamePlayerResponse.player (Casino.QueryGamePlayerResponse.GamePlayer, repeated)`
- `Casino.SlotsProto.BonusInfo.bonus_id (Casino.SlotsProto.BonusId, optional)`
- `Casino.SlotsProto.BonusInfo.spin_id (string, optional)`
- `Casino.SlotsProto.BonusInfo.win_bonus_id (Casino.SlotsProto.BonusId, repeated)`
- `Casino.SlotsProto.JackpotInfo.id (uint32, optional)`
- `Casino.SlotsProto.JackpotInfo.payrule_id (uint32, optional)`
- `Casino.SlotsProto.JackpotList.Jackpot.id (uint32, required)`
- `Casino.SlotsProto.PayruleInfo.bonus_id (Casino.SlotsProto.BonusId, repeated)`
- `Casino.SlotsProto.PayruleInfo.jackpot_id (uint32, optional)`
- `Casino.SlotsProto.PayruleInfo.line_id (int32, optional)`
- `Casino.SlotsProto.PayruleInfo.rule_id (uint32, optional)`
- `Casino.SlotsProto.SocialBonus.Player.user_id (int64, required)`
- `Casino.SlotsProto.SocialBonus.player (Casino.SlotsProto.SocialBonus.Player, repeated)`
- `Casino.SlotsProto.SpinInfo.spin_id (string, required)`
- `Casino.SlotsProto.SpinRequest.event_ids (uint32, repeated)`
- `Casino.SlotsProto.SpinResponse.PayruleRandomSpinAction.payrule_id (uint32, required)`
- `Casino.SlotsProto.SpinResponse.PayruleRandomSpinAction.spin_action_id (uint32, required)`
- `Casino.SlotsProto.SpinResponse.mystery_id (uint32, optional)`
- `Casino.SlotsProto.SymbolInfo.Property.key (string, optional)`
- `Casino.SlotsProto.Timer.id (uint32, required)`
- `Casino.SlotsProto.User.user_id (int64, required)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.id (uint32, required)`

### Progression / state

- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.count (uint32, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.status (Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Status, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.count (uint32, required)`
- `Casino.GetGamePlayerCountResponse.status (Casino.GetGamePlayerCountResponse.Status, required)`
- `Casino.GetGamePlayerCountResponse.user_count (uint64, repeated)`
- `Casino.GetJackpotValuesResponse.status (Casino.GetJackpotValuesResponse.Status, required)`
- `Casino.JoinGameResponse.status (Casino.JoinGameResponse.Status, required)`
- `Casino.LeaveGameResponse.status (Casino.LeaveGameResponse.Status, required)`
- `Casino.ListGamesResponse.ListGamesEntry.user_count (uint64, optional)`
- `Casino.ListGamesResponse.status (Casino.ListGamesResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusResponse.status (Casino.NonSpinBonusGameProto.BuyBonusResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.Data.count (uint32, required)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.status (Casino.NonSpinBonusGameProto.GetBonusInfoResponse.Status, required)`
- `Casino.NonSpinBonusGameProto.GetDataResponse.status (Casino.NonSpinBonusGameProto.GetDataResponse.Status, required)`
- `Casino.PinGameResponse.status (Casino.PinGameResponse.Status, required)`
- `Casino.QueryGameFamilyResponse.status (Casino.QueryGameFamilyResponse.Status, required)`
- `Casino.QueryGamePlayerResponse.status (Casino.QueryGamePlayerResponse.Status, required)`
- `Casino.QueryGameResponse.status (Casino.QueryGameResponse.Status, required)`
- `Casino.SlotsProto.AwardInfo.progress (int64, optional)`
- `Casino.SlotsProto.CounterInfo.legacy_progress (int64, optional)`
- `Casino.SlotsProto.CounterInfo.progress (Casino.BigNumber, optional)`
- `Casino.SlotsProto.PayruleInfo.counter (Casino.SlotsProto.CounterInfo, repeated)`
- `Casino.SlotsProto.PersonalState.counters (Casino.PersonalAwardsProto.PersonalCounter, repeated)`
- `Casino.SlotsProto.PersonalState.counters_list (Casino.PersonalAwardsProto.PersonalCounterList, repeated)`
- `Casino.SlotsProto.PersonalState.states (Casino.PersonalAwardsProto.PersonalState, repeated)`
- `Casino.SlotsProto.PersonalState.states_list (Casino.PersonalAwardsProto.PersonalStateList, repeated)`
- `Casino.SlotsProto.SocialBonus.Player.points (uint64, required)`
- `Casino.SlotsProto.SpinInfo.counter (Casino.SlotsProto.CounterInfo, repeated)`
- `Casino.SlotsProto.SpinResponse.FreeSpins.spin_count (uint32, required)`
- `Casino.SlotsProto.Timer.progress (uint32, required)`
- `Casino.UnlockGameResponse.status (Casino.UnlockGameResponse.Status, required)`

### Cost / input

- `Casino.AddDciEventRequest.BoxForSpinConfig.BetChance.bet (int64, required)`
- `Casino.AddDciEventRequest.BoxForSpinConfig.bet_chance (Casino.AddDciEventRequest.BoxForSpinConfig.BetChance, repeated)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.bb_amount (double, required)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.bb_amount (double, required)`
- `Casino.JackpotHitRequest.Jackpot.bet (uint64, required)`
- `Casino.JackpotHitRequest.Jackpot.max_bet (uint64, required)`
- `Casino.JackpotInitRequest.Jackpot.max_bet (uint64, required)`
- `Casino.NonSpinBonusGameProto.BonusResponse.bet (uint64, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.price (Casino.Chips, optional)`
- `Casino.NonSpinBonusGameProto.Data.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.bet (uint64, optional)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoResponse.price (Casino.Chips, optional)`
- `Casino.NonSpinBonusGameProto.GetDataResponse.bet (uint64, optional)`
- `Casino.SlotsProto.BonusInfo.bet (Casino.Chips, optional)`
- `Casino.SlotsProto.BonusInfo.played_bet (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinInfo.bet (Casino.Chips, required)`
- `Casino.SlotsProto.SpinInfo.fee (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinInfo.played_bet (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinRequest.bet (uint64, required)`
- `Casino.SlotsProto.SpinRequest.max_bet_btn (bool, optional)`

### Currency / balance

- `Casino.SlotsProto.AwardInfo.chips (Casino.Chips, optional)`
- `Casino.SlotsProto.SocialBonus.legacy_total_cash (uint64, required)`
- `Casino.SlotsProto.SocialBonus.total_cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.Bonus.cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.Bonus.legacy_cash (uint64, required)`
- `Casino.SlotsProto.SpinResponse.FreeSpins.cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.FreeSpins.legacy_cash (uint64, required)`
- `Casino.SlotsProto.SpinResponse.cash (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinResponse.legacy_cash (uint64, required)`
- `Casino.SlotsProto.User.cash (Casino.Chips, optional)`
- `Casino.SlotsProto.User.event_cash (Casino.Chips, optional)`
- `Casino.SlotsProto.User.legacy_cash (int64, optional)`
- `Casino.SlotsProto.User.legacy_event_cash (int64, optional)`
- `Casino.UnlockGameResponse.diamonds_delta (int64, optional)`

### Reward / output

- `Casino.JackpotHitResponse.Jackpot.legacy_win (uint64, required)`
- `Casino.JackpotHitResponse.Jackpot.win (Casino.Chips, optional)`
- `Casino.JoinGameResponse.non_spin_bonus_game (Casino.NonSpinBonusGameProto.Data, repeated)`
- `Casino.NonSpinBonusGameProto.BonusResponse.bonus (Casino.SlotsProto.SpinResponse.Bonus, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusRequest.bonus_name (string, required)`
- `Casino.NonSpinBonusGameProto.BuyBonusResponse.non_spin_bonus_game (Casino.NonSpinBonusGameProto.Data, optional)`
- `Casino.NonSpinBonusGameProto.Data.bonus_name (string, required)`
- `Casino.NonSpinBonusGameProto.GetBonusInfoRequest.bonus_name (string, required)`
- `Casino.NonSpinBonusGameProto.GetDataRequest.bonus_name (string, required)`
- `Casino.SlotsProto.BonusInfo.payout (Casino.Chips, optional)`
- `Casino.SlotsProto.BonusInfo.reward_type (Casino.SlotsProto.BonusInfo.RewardType, repeated)`
- `Casino.SlotsProto.BonusInfo.win_celebration (Casino.SlotsProto.WinCelebration, optional)`
- `Casino.SlotsProto.JackpotInfo.win (Casino.Chips, optional)`
- `Casino.SlotsProto.JackpotList.Jackpot.legacy_user_payouts (int64, repeated)`
- `Casino.SlotsProto.JackpotList.Jackpot.legacy_win (uint64, optional)`
- `Casino.SlotsProto.JackpotList.Jackpot.user_payouts (Casino.Chips, repeated)`
- `Casino.SlotsProto.JackpotList.Jackpot.win (Casino.Chips, optional)`
- `Casino.SlotsProto.PayruleInfo.applied_payout_multiplier (double, optional)`
- `Casino.SlotsProto.PayruleInfo.award (Casino.SlotsProto.AwardInfo, repeated)`
- `Casino.SlotsProto.PayruleInfo.payout (Casino.Chips, optional)`
- `Casino.SlotsProto.PayruleInfo.reward_type (Casino.SlotsProto.PayruleInfo.RewardType, repeated)`
- `Casino.SlotsProto.PayruleInfo.winning_symbol (Casino.SlotsProto.SymbolInfo, repeated)`
- `Casino.SlotsProto.PersonalState.awards (Casino.PersonalAwardsProto.PersonalAward, repeated)`
- `Casino.SlotsProto.PersonalState.awards_list (Casino.PersonalAwardsProto.PersonalAwardList, repeated)`
- `Casino.SlotsProto.PersonalState.bucket_awards (Casino.PersonalAwardsProto.PersonalBucketAward, repeated)`
- `Casino.SlotsProto.SocialBonus.Player.legacy_win (uint64, optional)`
- `Casino.SlotsProto.SocialBonus.Player.win (Casino.Chips, optional)`
- `Casino.SlotsProto.SpinInfo.award (Casino.SlotsProto.AwardInfo, repeated)`
- `Casino.SlotsProto.SpinInfo.payout (Casino.Chips, required)`
- `Casino.SlotsProto.SpinInfoRequest.bonus (Casino.SlotsProto.BonusInfo, optional)`
- `Casino.SlotsProto.SpinResponse.bonus (Casino.SlotsProto.SpinResponse.Bonus, repeated)`
- `Casino.SlotsProto.SpinResponse.payrules_with_disabled_bonus (uint32, repeated)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.legacy_win (uint64, optional)`
- `Casino.VideoPokerProto.JackpotList.Jackpot.win (Casino.Chips, optional)`

### Timing / reset / expiry

- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.end_time (uint32, required)`
- `Casino.NonSpinBonusGameProto.Data.end_time (uint32, required)`
- `Casino.SlotsProto.BonusInfo.timestamp (uint64, optional)`
- `Casino.SlotsProto.SocialBonus.time_to_bonus (uint32, required)`
- `Casino.SlotsProto.SpinInfo.timestamp (uint64, optional)`
- `Casino.SlotsProto.SpinResponse.timer (Casino.SlotsProto.Timer, repeated)`
- `Casino.SlotsProto.Timer.end_time (uint64, optional)`
- `Casino.SlotsProto.TimerList.timer (Casino.SlotsProto.Timer, repeated)`

### Segment / eligibility / limit

- `Casino.SlotsProto.JackpotList.Jackpot.eligible_users (int64, repeated)`
- `Casino.SlotsProto.SharedFreeSpins.eligible_users (int64, repeated)`

### Other structural fields

- `Casino.AddDciEventRequest.BoxForSpinConfig.BetChance.chance (double, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsRequest.type (uint32, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor.avatar (Casino.Avatar, required)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.contributors (Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.Contributor, repeated)`
- `Casino.ClubsProto.ClubWallGetJackpotBonusDetailsResponse.error_code (int32, optional)`
- `Casino.ClubsProto.ClubWallGetResponse.CumulativeJackpotBonus.type (uint32, required)`
- `Casino.GameCategoryEntry.flags (int32, optional)`
- `Casino.GameCategoryEntry.game_category (Casino.GameCategory, required)`
- `Casino.GameCategoryEntry.game_subcategory (Casino.GameSubcategory, optional)`
- `Casino.GameCategoryEntry.lobby_size (int32, optional)`
- `Casino.GetGamePlayerCountRequest.game_name (string, repeated)`
- `Casino.GetGamePlayerCountResponse.error_code (int32, optional)`
- `Casino.GetJackpotValuesResponse.error_code (int32, optional)`
- `Casino.GetJackpotValuesResponse.legacy_value (uint64, repeated)`
- `Casino.GetJackpotValuesResponse.value (Casino.Chips, repeated)`
- `Casino.JackpotGetResponse.legacy_value (uint64, repeated)`
- `Casino.JackpotGetResponse.value (Casino.Chips, repeated)`
- `Casino.JackpotHitRequest.Jackpot.legacy_min_value (uint64, required)`
- `Casino.JackpotHitRequest.Jackpot.min_value (Casino.Chips, optional)`
- `Casino.JackpotHitRequest.jackpot (Casino.JackpotHitRequest.Jackpot, repeated)`
- `Casino.JackpotHitResponse.Jackpot.club_share (double, optional)`
- `Casino.JackpotHitResponse.Jackpot.legacy_value (uint64, required)`
- `Casino.JackpotHitResponse.Jackpot.value (Casino.Chips, optional)`
- `Casino.JackpotHitResponse.jackpot (Casino.JackpotHitResponse.Jackpot, repeated)`
- `Casino.JackpotIncrRequest.Jackpot.increment (uint64, required)`
- `Casino.JackpotIncrRequest.Jackpot.legacy_max_value (uint64, required)`
- `Casino.JackpotIncrRequest.Jackpot.max_value (Casino.Chips, optional)`
- `Casino.JackpotIncrRequest.jackpot (Casino.JackpotIncrRequest.Jackpot, repeated)`
- `Casino.JackpotInitRequest.Jackpot.legacy_max_value (uint64, optional)`
- `Casino.JackpotInitRequest.Jackpot.legacy_min_value (uint64, required)`
- `Casino.JackpotInitRequest.Jackpot.max_value (Casino.Chips, optional)`
- `Casino.JackpotInitRequest.Jackpot.min_value (Casino.Chips, optional)`
- `Casino.JackpotInitRequest.jackpot (Casino.JackpotInitRequest.Jackpot, repeated)`
- `Casino.JoinGameRequest.create_game_mode (Casino.GameMode, optional)`
- `Casino.JoinGameRequest.game_def_hash (bytes, optional)`
- `Casino.JoinGameRequest.game_name (string, required)`
- `Casino.JoinGameRequest.reconnect (bool, optional)`
- `Casino.JoinGameResponse.error_code (int32, optional)`
- `Casino.JoinGameResponse.game_def_url (string, repeated)`
- `Casino.JoinGameResponse.game_event (Casino.GameEvent, repeated)`
- … 113 more rows in `fields.csv`

## Live-session coverage

Observed endpoint samples in `20260825_182300`:

- `SlotsGameClient.RoomUsers` — 116 (116 request, 0 response)
- `AppServer.GetJackpotValues` — 60 (30 request, 30 response)
- `SlotsGameServer.Spin` — 58 (29 request, 29 response)
- `SlotsGameClient.UpdateJackpot` — 26 (26 request, 0 response)
- `AppServer.QueryGame` — 12 (6 request, 6 response)
- `AppServer.JoinGame` — 4 (2 request, 2 response)
- `AppServer.LeaveGame` — 4 (2 request, 2 response)
- `AppServer.ListGames` — 4 (2 request, 2 response)
- `AppServer.QueryGamePlayer` — 4 (2 request, 2 response)

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
| `Casino.SlotsProto.UserList.user[].cash.value` | 116 | 119 | 90 | varying-in-session |
| `Casino.SlotsProto.UserList.user[].legacy_cash` | 116 | 119 | 90 | varying-in-session |
| `Casino.SlotsProto.UserList.user[].user_id` | 116 | 119 | 5 | varying-in-session |
| `Casino.GetJackpotValuesRequest.jackpot_id[]` | 30 | 2584 | 1163 | varying-in-session |
| `Casino.GetJackpotValuesResponse.legacy_value[]` | 30 | 2584 | 1748 | varying-in-session |
| `Casino.GetJackpotValuesResponse.status` | 30 | 30 | 1 | constant-in-session |
| `Casino.GetJackpotValuesResponse.value[].value` | 30 | 2584 | 2409 | varying-in-session |
| `Casino.SlotsProto.SpinRequest.auto` | 29 | 29 | 2 | varying-in-session |
| `Casino.SlotsProto.SpinRequest.bet` | 29 | 29 | 1 | constant-in-session |
| `Casino.SlotsProto.SpinRequest.max_bet_btn` | 29 | 29 | 2 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.cash.value` | 29 | 29 | 28 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.jackpot` | 29 | 29 | 1 | constant-in-session |
| `Casino.SlotsProto.SpinResponse.legacy_cash` | 29 | 29 | 28 | varying-in-session |
| `Casino.SlotsProto.SpinResponse.stop[]` | 29 | 117 | 50 | varying-in-session |
| `Casino.SlotsProto.JackpotList.jackpot[].id` | 26 | 26 | 1 | constant-in-session |
| `Casino.SlotsProto.JackpotList.jackpot[].legacy_value` | 26 | 26 | 25 | varying-in-session |
| `Casino.SlotsProto.JackpotList.jackpot[].value.value` | 26 | 26 | 25 | varying-in-session |
| `Casino.QueryGameRequest.game_name` | 6 | 6 | 2 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.category` | 6 | 6 | 1 | constant-in-session |
| `Casino.QueryGameResponse.game_entry.game.name` | 6 | 6 | 2 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].jackpot_id[]` | 6 | 6 | 2 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].key` | 6 | 102 | 17 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].value_bet[]` | 6 | 126 | 21 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].value_bytes` | 6 | 6 | 2 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].value_double` | 6 | 18 | 5 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].value_int` | 6 | 30 | 5 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.game.params.element[].value_string` | 6 | 36 | 11 | varying-in-session |
| `Casino.QueryGameResponse.status` | 6 | 6 | 1 | constant-in-session |
| `Casino.QueryGameRequest.include_jackpot` | 4 | 4 | 1 | constant-in-session |
| `Casino.QueryGameResponse.game_entry.jackpot[].id` | 4 | 4 | 2 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.jackpot[].legacy_value` | 4 | 4 | 4 | varying-in-session |
| `Casino.QueryGameResponse.game_entry.jackpot[].value.value` | 4 | 4 | 4 | varying-in-session |
| `Casino.JoinGameRequest.game_def_hash` | 2 | 2 | 2 | varying-in-session |
| `Casino.JoinGameRequest.game_name` | 2 | 2 | 2 | varying-in-session |
| `Casino.JoinGameRequest.reconnect` | 2 | 2 | 1 | constant-in-session |
| `Casino.JoinGameResponse.game_mode` | 2 | 2 | 1 | constant-in-session |
| `Casino.JoinGameResponse.status` | 2 | 2 | 1 | constant-in-session |
| `Casino.LeaveGameResponse.status` | 2 | 2 | 1 | constant-in-session |
| `Casino.ListGamesRequest.category` | 2 | 2 | 1 | constant-in-session |
| `Casino.ListGamesResponse.frame[].name` | 2 | 2 | 1 | constant-in-session |
| … | | | | 31 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260825_182300`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Inferred flow: lobby list/query -> join machine -> `Spin`/`FreeSpin` or bonus decision -> `SpinResponse` plus asynchronous jackpot/personal-state updates -> leave game. Jackpot host operations form a related server-side lifecycle.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_ingame_cards_1_etc2.zpk`
- ZPK asset: `assets/atlas_ingame_cards_2_etc2.zpk`
- ZPK asset: `assets/atlas_ingame_common_1_etc2.zpk`
- ZPK asset: `assets/atlas_ingame_common_2_etc2.zpk`
- ZPK asset: `assets/atlas_slots_classic_diamonds_2_etc2.zpk`
- ZPK asset: `assets/atlas_slots_classic_ui_2_etc2.zpk`
- ZPK asset: `assets/atlas_slots_effects_2_etc2.zpk`
- ZPK asset: `assets/data-slots-effects.zpk`
- ZPK asset: `assets/data-slots.zpk`
- ZPK asset: `assets/data-slots_classic_diamonds.zpk`
- ZPK asset: `assets/data-slots_classic_ui.zpk`
- ZPK asset: `assets/slots_classic_diamonds_background_2_etc2.zpk`
- ZPK asset: `assets/sound_ingame.zpk`
- ZPK asset: `assets/sound_ingame_vo_male.zpk`
- ZPK asset: `assets/sound_slots.zpk`
- ZPK asset: `assets/sound_slots_classic_diamonds.zpk`
- ZPK asset: `assets/sound_slots_vo_male.zpk`
- `data-games.zpk`, `data-slots.zpk` and slot/ingame atlases confirm substantial static configuration/assets.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open the slot lobby, enter two named machines, mark each entry and change the bet once.
- Perform normal spins and, when naturally available, a free-spin, choice bonus, non-spin bonus or jackpot-related state.
- Mark lobby return and machine leave so lobby/game bursts can be separated.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
