# Big Fish Spin + Same-Room Shared Win — F4 Protocol Analysis

> Derived from a real multi-player YoYeti slot session on the isolated
> research emulator (BlueStacks, `com.selfawaregames.acecasino` 21.3.8 / 1293).
> Evidence captured read-only via the JS `SANetworkInterface.serverRequest`
> wrapper; all raw/value-bearing data remains local (see `C:\bigfish_research`).

## Transport (how to capture Big Fish HTTP JSON)

- Big Fish is a Cocos Creator 3.x JS client (SpiderMonkey). All API traffic is
  HTTP JSON through `SANetworkInterface.serverRequest`.
- Two reliable capture transports (both verified):
  1. **logcat** (`--mode logcat`): `cc.log`/`console.log` land in logcat tags
     `Cobra Log` and `cocos2d-x debug info` with prefix
     `__CODEX_BIGFISH_HTTP_V1__`. NOTE: large responses are truncated by logcat
     (single line ~4KB), so partial JSON may appear.
  2. **file sink** (`agent_filesink.js`): re-injects a collector that appends
     JSON events to the app writable path `files/bf_capture.jsonl` via
     `cc.FileUtils`. **The file is UTF-16LE** — decode it as `utf-16`. No logcat
     truncation. This is the preferred transport for spin analysis.
- The game creates a fresh JS global context per scene. The collector must be
  (re)injected into the **machine (slots2) context**, not just the lobby. The
  class-based re-inject (`agent_reinject.js`) checks `__codexBigFishFileSinkV1`
  and installs if absent.

## Spin endpoint (Core)

- Request: `SANetworkInterface.serverRequest({controller:'slots', method:'spin', ...})`
- Request params shape:
  `[comboID, tableID, betCents?, lineCount?, <bet-level..., isAutoSpinning>]`
  Example observed params: `["92508025.138…", 198921351, 45296, 314, 43, 50, 50, 1]`
- Request `post_object`: `{"data": {"isAutoSpinning":1, "tournamentUIOpen":false, ...}}`
- Related machine endpoints (all `controller:'slots'`):
  - `poll` — periodic room/message stream (jackpot.update, player.cash, etc.)
  - `spinFinished` — sent after the spin animation completes
  - `isEligibleToJoin`, `leave`, `rate`, `chat`

## Spin response message types (observed, 23 spin responses)

Each spin response `{"messages": [...]}` carries a broadcast set:

| message | target | meaning |
|---|---|---|
| `jackpot.update` | `to:0` | Live jackpot pool values (grand/major/main/minor/mini) |
| `jackpot.win` | **array of room player IDs** | Someone hit a jackpot; room players get a payout |
| `player.win` | `to:0` | A room player won chips (broadcast) |
| `player.cash2` | `to:[characterID]` | Player balance change (chips) |
| `player.winningstoday` | `to:0` | Room player today's winnings |
| `spin.result` | `to:[characterID]` | Reel-stop offsets (the spin outcome) |
| `spin.hits` | room | Hit line info |
| `prize.award.allPrizes` | `to:0` | Awarded prizes (jackpot/feature) |
| `player.boosters.update`, `sale`, `tournament.ranks`, `currency`, `player.xp`, `sticker.collection.active`, `tutorial.spin`, `time.based.progress.data`, `metamorphic.hit`, `dynamic.symbols`, `slot.mode` | | machine state |

## SAME-ROOM SHARED WIN — the target feature (F4 confirmed)

`jackpot.win` is the shared-win message. Observed complete structure:

```json
{
  "id": 45356,
  "name": "jackpot.win",
  "to": [92508025, 91590746, 92355722],
  "data": {
    "player": 92508167,
    "jackpotType": "mini",
    "wonAmount": 0,
    "seedAmount": 450000000,
    "boostedWonAmount": 0,
    "hitLine": {"count": 0, "line": 0},
    "otherPlayerWonAmount": 15000
  }
}
```

Key finding:
- `data.player` = the characterID who hit the jackpot (92508167).
- `data.jackpotType` = which pool (`mini`, could be grand/major/main/minor/mini).
- `data.otherPlayerWonAmount` = **the payout each OTHER room player receives**
  (15000 in this sample). This is the "给同房间在线玩家发金币" mechanism.
- `to` = the list of same-room players who receive this message (the audience).

Corroborating room broadcasts (same set of room player IDs across `player.win`
and `jackpot.win`):

- Room players observed: `92508025` (us), `92508167`, `91590746`, `92355722`,
  `92508172`.
- `player.win` examples (broadcast to room, `to:0`):
  - `{characterID:92355722, chipsWon:450000, betAmount:500000}`
  - `{characterID:91590746, chipsWon:550000, betAmount:500000}`
  - `{characterID:92508025, chipsWon:12500, betAmount:5000}`
  - `{characterID:92508172, chipsWon:400, betAmount:1000}`
- Two bet tiers coexist in the same room (5000-level and 500000/1000000-level
  players) — room players can be at different stake levels.

## Conclusion (F4 evidence)

The "slot machine room jackpot → coins to same-room online players" feature
**exists and is confirmed**:

1. When a room player hits a jackpot, the client receives `jackpot.win`.
2. `data.otherPlayerWonAmount` is the amount granted to the other same-room
   online players (`to` list).
3. Same-room play is a real broadcast room: `player.win`, `player.winningstoday`
   and `jackpot.update` are all broadcast to every room player, showing other
   players' names / balances / Today winnings in the client UI.
4. A separate `prize.award.allPrizes` message carries the awarded prize list
   (`jackpot`, `MetamorphicPotBurst`, etc.) for the winner's client.

## Known limits

- One room / one session; not establishing trigger probability, exact payout
  ratios per jackpot tier, or the across-account (server-side) settlement model.
- `wonAmount: 0` in the sample is the winner's own annuity/seed draw; the
  `otherPlayerWonAmount` is the distributed room share. Full per-tier rules need
  more samples across jackpotType values.
- No Raw / account balances / full value-bearing data committed; everything
  above is schema + bounded field structure.
