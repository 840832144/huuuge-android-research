# Huuuge Module Structure Catalog

This is the broad structural map of the Huuuge client. It combines recovered protobuf descriptors, service/method relationships, sanitized live-session counts/field presence, and APK ZPK filenames. It does not publish captured values or make final numerical conclusions.

## Catalog snapshot

- Independent module dossiers: **37**
- Live-confirmed modules: **21**
- Schema-only / live pending modules: **16**
- Inferred/static-only modules: **0**
- Recovered proto files: **36**
- Descriptor message types: **1028**; assigned to at least one dossier: **1028**
- Descriptor service methods: **356**
- Current live session: `20260901_160002`, **8398** sanitized message samples
- Descriptor SHA-256: `8e91f6f3b05e4ad01950d74650bdf8b00adda07ee5de6cb8c9c6d835b5aedf92`

Status meanings:

- **live-confirmed** — at least one primary module endpoint appeared in the session.
- **live-confirmed (cross-cutting/config only)** — populated fields appeared inside a shared/config message, but no dedicated module endpoint was exercised.
- **schema-only / live sample pending** — descriptor structure exists, but this session did not exercise it.
- **inferred/static / live sample pending** — current evidence is shared/static or organizational rather than a dedicated observed RPC family.

## Recovered schema and static backbone

Recovered files: `Adventure.proto`, `AppCharge.proto`, `AppClient.proto`, `AppServer.proto`, `Baccarat.proto`, `BattlePass.proto`, `Blackjack.proto`, `Clubs.proto`, `Common.proto`, `CommonGameClient.proto`, `ContactPoint.proto`, `ContentTournament.proto`, `Definition.proto`, `Elites.proto`, `GameHost.proto`, `GameServer.proto`, `Htf.proto`, `HtfApp.proto`, `HuuugeLogin.proto`, `Lottery.proto`, `MiniPass.proto`, `NonSpinBonusGame.proto`, `Offers.proto`, `PersonalAwards.proto`, `ProxyTestServer.proto`, `Purchases.proto`, `Race.proto`, `Roulette.proto`, `Rpc.proto`, `Services.proto`, `Slots.proto`, `Sweepstakes.proto`, `Texas.proto`, `Vault.proto`, `VideoPoker.proto`, `Vouchers.proto`

- `Services.proto` supplies the 34-service / 356-method RPC relationship map used by `endpoints.csv`.
- `libClawApp.so` supplies the recovered descriptors and preserves C++/Lua integration evidence; module-specific Lua/native ownership remains a future mapping layer.
- Base-APK ZPK filenames are attached to dossiers as static evidence without committing APK contents.

## Module map

| Module | Status | Structure snapshot | Live samples | Live endpoints | Completion | Highest-priority next action |
|---|---|---|---:|---:|---:|---|
| [Slots / Lobby / Spin / Jackpot](slots.md) | live-confirmed | 90 messages / 32 endpoints | 3118 | 12 | 90/100 | Open the slot lobby, enter two named machines, mark each entry and change the bet once. |
| [Lottery / Draw / Ticket](lottery.md) | live-confirmed (cross-cutting/config only) | 29 messages / 5 endpoints | 0 + 70 cross-cut | 0 | 65/100 | Open every visible lottery/draw/ticket screen and mark the screen name. |
| [Missions / Quests / Daily-Weekly Tasks](missions.md) | live-confirmed | 16 messages / 3 endpoints | 9 | 2 | 75/100 | Open daily, weekly and general mission/quest panels separately and mark each tab. |
| [Battle Pass](battle_pass.md) | live-confirmed | 27 messages / 9 endpoints | 46 | 2 | 75/100 | When an eligible account is available, open the Battle Pass main screen, reward track and daily/weekly mission tabs with markers. |
| [MiniPass](mini_pass.md) | schema-only / live sample pending | 24 messages / 10 endpoints | 0 | 0 | 30/100 | Open MiniPass main, missions and milestone/reward-track screens with separate markers. |
| [Vault](vault.md) | live-confirmed | 18 messages / 4 endpoints | 607 | 2 | 75/100 | Open Vault main/detail/help screens and mark each view. |
| [Collection / Collection Event / Club Set](collection.md) | live-confirmed (cross-cutting/config only) | 39 messages / 7 endpoints | 0 + 188 cross-cut | 0 | 65/100 | Open Collection Event, collection album/theme and any Club Set screen with markers. |
| [Conquest](conquest.md) | schema-only / live sample pending | 29 messages / 6 endpoints | 0 | 0 | 35/100 | Open the Conquest map, arena, slot/challenge and summary/leaderboard screens with markers. |
| [Charms / Trading](charms.md) | live-confirmed | 43 messages / 12 endpoints | 31 + 117 cross-cut | 1 | 75/100 | Open Charms collection, milestones, pack/box and trading screens with markers. |
| [Loyalty / VIP](loyalty.md) | live-confirmed | 7 messages / 3 endpoints | 63 + 210 cross-cut | 1 | 75/100 | Open the Loyalty/VIP overview, tier benefits and progress/history screens with markers. |
| [Clubs / Social Club Progression](clubs.md) | live-confirmed (cross-cutting/config only) | 79 messages / 28 endpoints | 0 + 27 cross-cut | 0 | 65/100 | Open club home, member list, wall/chat, events, league/season and donation screens with markers. |
| [Offers / Shop / Bundles](offers.md) | live-confirmed | 62 messages / 15 endpoints | 148 + 6 cross-cut | 8 | 90/100 | Open main shop, each offer family, bundle detail, personal offer, Offer Trail and Tile Shop with markers. |
| [Purchase / Checkout / Price Localization](purchases.md) | live-confirmed (cross-cutting/config only) | 32 messages / 9 endpoints | 0 + 74 cross-cut | 0 | 65/100 | Open purchase detail and proceed only to the platform checkout preview, then cancel before authorization. |
| [Rewards / Mystery / Hourly / Free Gift](rewards.md) | live-confirmed | 111 messages / 21 endpoints | 137 + 861 cross-cut | 5 | 90/100 | Open hourly/daily/shop bonus, mystery reward and free-gift surfaces with markers. |
| [Fame / Level / General Progression](progression.md) | live-confirmed | 54 messages / 8 endpoints | 761 + 814 cross-cut | 3 | 85/100 | Open profile, fame/level progress, rank benefits and any progression history screen with markers. |
| [Sweepstakes / Scheduled Draws](sweepstakes.md) | live-confirmed (cross-cutting/config only) | 14 messages / 6 endpoints | 0 + 1 cross-cut | 0 | 50/100 | Open sweepstakes/current draw, ticket balance and completed-draw/history screens with markers. |
| [Adventure](adventure.md) | live-confirmed | 21 messages / 5 endpoints | 3 | 2 | 75/100 | Open Adventure map/phase, difficulty, missions and milestone screens with markers. |
| [Content Tournaments](tournaments.md) | schema-only / live sample pending | 6 messages / 2 endpoints | 0 | 0 | 30/100 | Open every tournament screen, content item, rules/rewards and leaderboard with markers. |
| [Race](race.md) | schema-only / live sample pending | 14 messages / 3 endpoints | 0 | 0 | 30/100 | Open race overview, reward tiers and both leaderboard/detail views with markers. |
| [Elites / Play Together](elites.md) | schema-only / live sample pending | 25 messages / 8 endpoints | 0 | 0 | 30/100 | Open Elites event, missions/milestones, leaderboard and Play Together screens with markers. |
| [Personal Awards](personal_awards.md) | schema-only / live sample pending | 18 messages / 2 endpoints | 0 | 0 | 30/100 | Locate and open personal-award/achievement progress screens with markers. |
| [Vouchers](vouchers.md) | schema-only / live sample pending | 7 messages / 1 endpoints | 0 | 0 | 30/100 | Open voucher event/shop, balance, item detail and tutorial screens with markers. |
| [Non-Spin Bonus Games](non_spin_bonus.md) | schema-only / live sample pending | 13 messages / 7 endpoints | 0 | 0 | 35/100 | Enter a slot with a visible non-spin bonus and mark trigger/start/end. |
| [Baccarat](baccarat.md) | schema-only / live sample pending | 15 messages / 6 endpoints | 0 | 0 | 30/100 | Open a Baccarat room and mark join/config/betting/result. |
| [Blackjack](blackjack.md) | schema-only / live sample pending | 15 messages / 6 endpoints | 0 | 0 | 30/100 | Open a Blackjack room and mark betting/action/result states. |
| [Roulette](roulette.md) | schema-only / live sample pending | 14 messages / 6 endpoints | 0 | 0 | 30/100 | Open a Roulette room and mark ready/betting/result. |
| [Texas Poker](texas_poker.md) | schema-only / live sample pending | 19 messages / 10 endpoints | 0 | 0 | 30/100 | Open a Texas table/tournament and mark lobby, buy-in, hand and result. |
| [Video Poker](video_poker.md) | schema-only / live sample pending | 14 messages / 7 endpoints | 0 | 0 | 30/100 | Open Video Poker and mark first draw, hold selection, second draw and result. |
| [Currency / Balance / Economy Statistics](economy.md) | live-confirmed (cross-cutting/config only) | 17 messages / 2 endpoints | 0 + 4458 cross-cut | 0 | 65/100 | Mark visible balances before and after a spin, reward claim and shop preview in one marked session. |
| [Game Runtime / Host / Room State](game_runtime.md) | schema-only / live sample pending | 66 messages / 21 endpoints | 0 | 0 | 35/100 | Use markers for lobby entry, game join, room loaded, game leave and reconnect. |
| [Authentication / Account / Consent](authentication.md) | live-confirmed | 59 messages / 17 endpoints | 6 + 1 cross-cut | 4 | 90/100 | No deliberate re-login is needed for cataloging; capture only a natural cold start with manifest/markers. |
| [Player / Game / Lobby State](player_lobby.md) | live-confirmed | 55 messages / 29 endpoints | 3050 + 49 cross-cut | 9 | 90/100 | Mark cold-start lobby loaded, profile opened, friends/leaderboard opened and game-list navigation. |
| [Social Recommendations / Invites](social.md) | schema-only / live sample pending | 5 messages / 2 endpoints | 0 | 0 | 30/100 | Open any invite/recommendation/referral screen with a marker. |
| [Contact Point / Engagement Surface](contact_point.md) | live-confirmed | 4 messages / 2 endpoints | 1 | 1 | 60/100 | Open any inbox/contact/help/engagement surface that resembles a contact point and mark it. |
| [Other LiveOps / DCI / Tower / Balloons](liveops_events.md) | live-confirmed | 88 messages / 18 endpoints | 382 | 4 | 90/100 | Open Tower, Balloons and every unmatched live-event tile with distinct markers. |
| [HTF / Proxy / Test Infrastructure](platform_diagnostics.md) | schema-only / live sample pending | 74 messages / 11 endpoints | 0 | 0 | 30/100 | No gameplay action is required; keep this module schema-only unless naturally emitted diagnostic traffic appears. |
| [Other / Unclassified Protocol Families](other_protocol.md) | live-confirmed | 92 messages / 13 endpoints | 10 | 5 | 85/100 | Review new unknown endpoints after every marked capture and split coherent families into new dossiers. |

## Most structurally complete now

- [Authentication / Account / Consent](authentication.md) — 90/100, 6 primary live samples, 4 live endpoints.
- [Offers / Shop / Bundles](offers.md) — 90/100, 148 primary live samples, 8 live endpoints.
- [Other LiveOps / DCI / Tower / Balloons](liveops_events.md) — 90/100, 382 primary live samples, 4 live endpoints.
- [Player / Game / Lobby State](player_lobby.md) — 90/100, 3050 primary live samples, 9 live endpoints.
- [Rewards / Mystery / Hourly / Free Gift](rewards.md) — 90/100, 137 primary live samples, 5 live endpoints.
- [Slots / Lobby / Spin / Jackpot](slots.md) — 90/100, 3118 primary live samples, 12 live endpoints.
- [Fame / Level / General Progression](progression.md) — 85/100, 761 primary live samples, 3 live endpoints.
- [Other / Unclassified Protocol Families](other_protocol.md) — 85/100, 10 primary live samples, 5 live endpoints.
- [Adventure](adventure.md) — 75/100, 3 primary live samples, 2 live endpoints.
- [Battle Pass](battle_pass.md) — 75/100, 46 primary live samples, 2 live endpoints.

## Live sample pending

- [Baccarat](baccarat.md) — Open a Baccarat room and mark join/config/betting/result.
- [Blackjack](blackjack.md) — Open a Blackjack room and mark betting/action/result states.
- [Conquest](conquest.md) — Open the Conquest map, arena, slot/challenge and summary/leaderboard screens with markers.
- [Content Tournaments](tournaments.md) — Open every tournament screen, content item, rules/rewards and leaderboard with markers.
- [Elites / Play Together](elites.md) — Open Elites event, missions/milestones, leaderboard and Play Together screens with markers.
- [Game Runtime / Host / Room State](game_runtime.md) — Use markers for lobby entry, game join, room loaded, game leave and reconnect.
- [HTF / Proxy / Test Infrastructure](platform_diagnostics.md) — No gameplay action is required; keep this module schema-only unless naturally emitted diagnostic traffic appears.
- [MiniPass](mini_pass.md) — Open MiniPass main, missions and milestone/reward-track screens with separate markers.
- [Non-Spin Bonus Games](non_spin_bonus.md) — Enter a slot with a visible non-spin bonus and mark trigger/start/end.
- [Personal Awards](personal_awards.md) — Locate and open personal-award/achievement progress screens with markers.
- [Race](race.md) — Open race overview, reward tiers and both leaderboard/detail views with markers.
- [Roulette](roulette.md) — Open a Roulette room and mark ready/betting/result.
- [Social Recommendations / Invites](social.md) — Open any invite/recommendation/referral screen with a marker.
- [Texas Poker](texas_poker.md) — Open a Texas table/tournament and mark lobby, buy-in, hand and result.
- [Video Poker](video_poker.md) — Open Video Poker and mark first draw, hold selection, second draw and result.
- [Vouchers](vouchers.md) — Open voucher event/shop, balance, item detail and tutorial screens with markers.

## Machine-readable tables

- `modules.csv` — one row per module with status, coverage, proto/service scope and next action.
- `endpoints.csv` — every recovered service method with request/response types, flow role and live counts.
- `fields.csv` — schema field definitions plus sanitized live populated paths, counts and variability (never values).
- `module_specs.json` — maintained module boundaries, flow notes, static evidence and future actions.

## Rebuild

Descriptor + committed sanitized inventories only:

Run `scripts\sync_local_runtime.ps1` first if the ignored local descriptor binary is not present at its expected path.

```powershell
py scripts\build_module_catalog.py
```

To add local non-empty/distinct/variability counts and APK ZPK filenames without exporting values:

```powershell
py scripts\build_module_catalog.py --capture-session <local-session-dir> --apk <local-base.apk>
```

## Evidence limitations

- Current live data is unmarked, so endpoint-to-click correlation remains incomplete.
- `live-confirmed` means structural presence in this one session, not complete coverage or business interpretation.
- Field distinctness is calculated locally from decoded values and exported only as counts/labels; the values themselves remain uncommitted.
- Cross-cutting sample counts use exact unique sequences when the local capture is supplied; otherwise the builder uses a conservative per-payload estimate from sanitized field counts.
- Modules may share messages/fields. `endpoints.csv` assigns one primary module, while cross-cutting economy/reward field evidence may appear in multiple dossiers.
