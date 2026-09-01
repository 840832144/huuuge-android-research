# Lottery / Draw / Ticket

Lottery tickets, toss/draw state, puzzle boards, multipliers, missed information and related ticket-shop configuration.

## Catalog status

- Evidence status: **live-confirmed (cross-cutting/config only)**
- Structural completeness: **65/100 — partial live structure**
- Primary live samples: **0** from `20260901_160002`
- Cross-cutting live samples: **70**
- Live endpoints / schema endpoints: **0 / 5**
- Live populated field paths: **54**

## Schema scope

- Proto files: `AppClient.proto`, `AppServer.proto`, `Common.proto`, `Lottery.proto`, `Services.proto`
- Services: `AppClient`, `AppServer`
- Related message types: **29**

- `Casino.AddDciEventRequest.LotteryEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.PuzzleBoardMultiplier` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward` (AppClient.proto)
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward` (AppClient.proto)
- `Casino.AddDciEventRequest.MiniGameEvent.LotteryMachine` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoFrame` (AppClient.proto)
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoRibbon` (AppClient.proto)
- `Casino.AddPromotionRequest.PromoLottery` (AppClient.proto)
- `Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier` (AppClient.proto)
- `Casino.BlackLotteryMissedInfo` (Lottery.proto)
- `Casino.CollectFreeTicketResponse` (AppServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.LotteryFreeTicketState` (Lottery.proto)
- `Casino.LotteryMissedInfo` (Lottery.proto)
- `Casino.LotteryPuzzleBoard` (Lottery.proto)
- `Casino.LotteryPuzzleBoardReward` (Lottery.proto)
- `Casino.LotteryState` (Lottery.proto)
- `Casino.LotteryTossData` (Lottery.proto)
- `Casino.LotteryTossRequest` (Lottery.proto)
- `Casino.LotteryTossResponse` (Lottery.proto)
- `Casino.MiniGameLotteryMachineRequest` (AppServer.proto)
- `Casino.MiniGameLotteryMachineResponse` (AppServer.proto)
- `Casino.MiniGameLotteryMachineResponse.State` (AppServer.proto)
- `Casino.NotifyBlackLotteryMissedInfoRequest` (Lottery.proto)
- `Casino.Reward.LotteryPuzzle` (Common.proto)

## RPC and flow structure

Inferred flow: event/config update establishes lottery state and ticket sources -> collect/buy ticket -> toss/join draw -> response updates puzzle/reward/state -> missed-info/update messages reconcile later results.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `AppServer.CollectFreeTicket` | `Casino.EmptyRequest` | `Casino.CollectFreeTicketResponse` | 0 | 0 | schema-only |
| `AppServer.LotteryToss` | `Casino.LotteryTossRequest` | `Casino.LotteryTossResponse` | 0 | 0 | schema-only |
| `AppServer.LotteryTutorialShown` | `Casino.EmptyRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `AppServer.MiniGameLotteryMachine` | `Casino.MiniGameLotteryMachineRequest` | `Casino.MiniGameLotteryMachineResponse` | 0 | 0 | schema-only |
| `AppClient.NotifyBlackLotteryMissedInfo` | `Casino.NotifyBlackLotteryMissedInfoRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent.event_id (int64, required)`
- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.product (Casino.IapProduct, repeated)`
- `Casino.BlackLotteryMissedInfo.black_lottery_missed_info_id (int64, required)`
- `Casino.BlackLotteryMissedInfo.event_id (int64, required)`
- `Casino.LotteryMissedInfo.black_lottery_event_id (int64, optional)`
- `Casino.LotteryMissedInfo.event_id (int64, required)`
- `Casino.LotteryMissedInfo.lottery_id (int64, required)`
- `Casino.LotteryTossResponse.missed_info_id (int64, optional)`
- `Casino.MiniGameLotteryMachineRequest.event_id (int64, required)`

### Progression / state

- `Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier.level (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.show_tutorial (bool, optional)`
- `Casino.CollectFreeTicketResponse.status (Casino.CollectFreeTicketResponse.Status, required)`
- `Casino.LotteryFreeTicketState.progress (int32, required)`
- `Casino.LotteryTossResponse.state (Casino.LotteryState, required)`
- `Casino.LotteryTossResponse.status (Casino.LotteryTossResponse.Status, required)`
- `Casino.MiniGameLotteryMachineResponse.state (Casino.MiniGameLotteryMachineResponse.State, optional)`
- `Casino.MiniGameLotteryMachineResponse.status (Casino.MiniGameLotteryMachineResponse.Status, required)`
- `Casino.NotifyBlackLotteryMissedInfoRequest.state (Casino.LotteryState, required)`

### Cost / input

- `Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts.ticket_color (Casino.LotteryColor, required)`
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.ticket_color (Casino.LotteryColor, required)`
- `Casino.AddDciEventRequest.LotteryEvent.free_ticket (Casino.LotteryFreeTicketState, required)`
- `Casino.AddDciEventRequest.LotteryEvent.ticket_balance (Casino.InventoryEntry, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.tickets_products (Casino.AddDciEventRequest.LotteryEvent.LotteryTicketShopProducts, repeated)`
- `Casino.LotteryFreeTicketState.threshold (int32, required)`
- `Casino.LotteryFreeTicketState.ticket_collected (Casino.LotteryColor, repeated)`
- `Casino.LotteryFreeTicketState.ticket_color (Casino.LotteryColor, required)`
- `Casino.LotteryState.free_ticket_state (Casino.LotteryFreeTicketState, optional)`
- `Casino.LotteryState.ticket_balance (Casino.InventoryEntry, repeated)`
- `Casino.LotteryTossData.ticket_color (Casino.LotteryColor, required)`
- `Casino.LotteryTossData.ticket_number (int32, required)`

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward.reward (Casino.Reward, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.TicketReward.reward (Casino.AddDciEventRequest.LotteryEvent.TicketReward.MultipleReward, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.ticket_reward (Casino.AddDciEventRequest.LotteryEvent.TicketReward, repeated)`
- `Casino.BlackLotteryMissedInfo.puzzle_board_completed_reward (Casino.LotteryPuzzleBoardReward, repeated)`
- `Casino.BlackLotteryMissedInfo.reward (Casino.Reward, repeated)`
- `Casino.LotteryMissedInfo.puzzle_board_completed_reward (Casino.LotteryPuzzleBoardReward, repeated)`
- `Casino.LotteryMissedInfo.reward (Casino.Reward, repeated)`
- `Casino.LotteryPuzzleBoard.reward (Casino.Reward, required)`
- `Casino.LotteryPuzzleBoardReward.reward (Casino.Reward, required)`
- `Casino.LotteryState.puzzle_board_completed_reward (Casino.LotteryPuzzleBoardReward, repeated)`
- `Casino.LotteryTossResponse.lottery_reward (Casino.RewardsData, optional)`
- `Casino.MiniGameLotteryMachineResponse.rewards_data (Casino.RewardsData, optional)`

### Timing / reset / expiry

- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent.expire (int64, required)`
- `Casino.AddDciEventRequest.LotteryEvent.free_ticket_timestamp (int32, required)`
- `Casino.CollectFreeTicketResponse.free_ticket_timer (int32, optional)`

### Segment / eligibility / limit

- `Casino.AddDciEventRequest.LotteryEvent.bulk_play_cap (int32, required)`

### Other structural fields

- `Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier.multiplier (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.PuzzleBoardMultiplier.color (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.PuzzleBoardMultiplier.multiplier_percent (int32, required)`
- `Casino.AddDciEventRequest.LotteryEvent.art_config (Casino.Art, optional)`
- `Casino.AddDciEventRequest.LotteryEvent.black_lottery (Casino.AddDciEventRequest.LotteryEvent.BlackLotteryEvent, optional)`
- `Casino.AddDciEventRequest.LotteryEvent.config_hbi_data (Casino.ConfigHbiData, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.lottery_multiplier (Casino.AddDciEventRequest.LotteryEvent.LotteryMultiplier, required)`
- `Casino.AddDciEventRequest.LotteryEvent.puzzle_board (Casino.LotteryPuzzleBoard, repeated)`
- `Casino.AddDciEventRequest.LotteryEvent.puzzle_board_multiplier (Casino.AddDciEventRequest.LotteryEvent.PuzzleBoardMultiplier, repeated)`
- `Casino.AddDciEventRequest.MiniGameEvent.LotteryMachine.result (int32, repeated)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoFrame.show_promo_frame (bool, required)`
- `Casino.AddDciEventRequest.OtherPromotionsEvent.LotteryPromoRibbon.show_promo_ribbon (string, required)`
- `Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier.color (int32, required)`
- `Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier.multiplier (double, required)`
- `Casino.AddPromotionRequest.PromoLottery.multiplier (Casino.AddPromotionRequest.PromoLottery.PuzzleMultiplier, repeated)`
- `Casino.BlackLotteryMissedInfo.data (Casino.LotteryTossData, required)`
- `Casino.BlackLotteryMissedInfo.previous (bool, required)`
- `Casino.CollectFreeTicketResponse.error_code (int32, optional)`
- `Casino.LotteryMissedInfo.data (Casino.LotteryTossData, required)`
- `Casino.LotteryPuzzleBoard.position (int32, required)`
- `Casino.LotteryPuzzleBoard.puzzle_color (Casino.LotteryColor, required)`
- `Casino.LotteryPuzzleBoardReward.color (Casino.LotteryColor, required)`
- `Casino.LotteryState.puzzle_board (Casino.LotteryPuzzleBoard, repeated)`
- `Casino.LotteryTossRequest.data (Casino.LotteryTossData, required)`
- `Casino.LotteryTossResponse.data (Casino.LotteryTossData, optional)`
- `Casino.LotteryTossResponse.error_code (int32, optional)`
- `Casino.MiniGameLotteryMachineRequest.moves (int32, optional)`
- `Casino.MiniGameLotteryMachineResponse.State.lottery_machine_position_idx (int32, required)`
- `Casino.MiniGameLotteryMachineResponse.State.moves (int32, required)`
- `Casino.MiniGameLotteryMachineResponse.State.spin_idx (int32, required)`
- `Casino.MiniGameLotteryMachineResponse.State.step_idx (int32, required)`
- `Casino.MiniGameLotteryMachineResponse.bulk_play (bool, optional)`
- `Casino.MiniGameLotteryMachineResponse.error_code (int32, optional)`
- `Casino.MiniGameLotteryMachineResponse.milestone_idx (int32, repeated)`
- `Casino.MiniGameLotteryMachineResponse.moves_used (int32, optional)`
- `Casino.MiniGameLotteryMachineResponse.new_lap (Casino.MinigameEventTrail, optional)`
- `Casino.MiniGameLotteryMachineResponse.steps_moved (int32, optional)`
- `Casino.NotifyBlackLotteryMissedInfoRequest.missed_info (Casino.BlackLotteryMissedInfo, required)`
- `Casino.Reward.LotteryPuzzle.color (int32, required)`
- … 1 more rows in `fields.csv`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

Populated field-path evidence (values withheld):

| Message.field path | Messages | Non-empty occurrences | Distinct values | Variability |
|---|---:|---:|---:|---|
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
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.highest_guaranteed_rarity` | 68 | 408 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.highest_guaranteed_rarity_items_count` | 68 | 408 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].collectibles_box_info.items_count` | 68 | 408 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].extra_item_boost.time.duration` | 68 | 680 | 3 | varying-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].extra_item_boost.time.expire_time` | 68 | 680 | 1 | constant-in-session |
| `Casino.AddDciEventRequest.lottery.ticket_reward[].reward[].reward[].extra_item_boost.time.value` | 68 | 680 | 2 | varying-in-session |
| … | | | | 14 more rows in `fields.csv` |

## Evidence ledger

### Observed-live

- The live counts and populated-field statistics above are directly derived from sanitized inventory plus local decoded session `20260901_160002`.
- Values, account identifiers, signatures, and raw payloads remain local and are not reproduced here.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Inferred flow: event/config update establishes lottery state and ticket sources -> collect/buy ticket -> toss/join draw -> response updates puzzle/reward/state -> missed-info/update messages reconcile later results.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- ZPK asset: `assets/atlas_lottery_2_etc2.zpk`
- `atlas_lottery_2_etc2.zpk` confirms a packaged lottery UI even though no dedicated lottery endpoint was exercised in the current session.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- Open every visible lottery/draw/ticket screen and mark the screen name.
- Inspect ticket balance/shop and collect a free ticket if naturally available.
- Perform one toss/draw/entry and reopen the result/history screen.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
