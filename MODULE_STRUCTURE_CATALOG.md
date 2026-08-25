# Module Structure Catalog

## Purpose

The current priority is to build a broad structural map of Huuuge Casino systems before deeply modeling any single module.

The user will continue playing different parts of the game over time. Each new capture should enrich the corresponding module dossier rather than forcing a complete model immediately.

## Core rule

**Structure first, values later.**

For every observed or statically recovered module, organize what is known into a reusable module dossier. Do not make Slots, Battle Pass, Lottery, or any other single system the global blocker.

## Module dossier contract

For each module, maintain at minimum:

- module/domain name;
- confidence/status: observed-live / schema-only / inferred / not-yet-observed;
- related proto files, services and message types;
- observed RPC service.method endpoints and directions;
- request/response/update relationships;
- important protobuf field hierarchy;
- likely entity identifiers (game/event/mission/offer/etc. ids);
- progression/state fields;
- cost/input fields;
- reward/output fields;
- timing/reset/expiry fields;
- eligibility/segment/limit fields;
- observed sample count and session references;
- what values are already available locally;
- what is still missing and what future user action would help fill it;
- whether extra evidence may be needed from GameServer, Lua, native state, or ZPK/static config.

Do not commit sensitive raw values or account/session identifiers. Sanitized field names, types, relationships, counts, confidence, and structural conclusions may be versioned.

## Initial catalog domains

At minimum maintain dossiers for:

1. Slots / slot lobby / spin / jackpot
2. Lottery / draw / ticket systems
3. Missions / quests / daily-weekly tasks
4. Battle Pass / MiniPass / reward tracks
5. Vault and other live-event/milestone systems
6. Collection / collectibles / collection events
7. Conquest and other event systems
8. Offers / shop / bundles / purchase / free gifts
9. Rewards / hourly bonus / mystery reward / reward bundles
10. Loyalty / VIP / fame / progression
11. Clubs / social progression
12. Charms / trading / collectible-related progression
13. Player/game/lobby state
14. Currency / balances / economy statistics where observable
15. Other / unknown RPC families

Add new dossiers whenever schemas or live traffic reveal another distinct system.

## Current-session use

Use local capture `20260825_182300` plus the recovered descriptor set to populate as many dossiers as possible now.

For modules observed live, combine schema structure with the 741-message session to identify real endpoints and actually populated field paths.

For modules not observed live (for example Lottery or Battle Pass in the current session), still build a schema-level dossier from recovered protobuf definitions and label it clearly as `schema-only / live sample pending` instead of leaving it absent.

## Desired output

Create a human-readable module index plus machine-readable structural tables, for example:

```text
artifacts/module_catalog/
  MODULE_INDEX.md
  modules.csv
  fields.csv
  endpoints.csv
  slots.md
  lottery.md
  missions.md
  battle_pass.md
  mini_pass.md
  vault.md
  offers.md
  loyalty.md
  ...
```

The index should make it easy to answer:

- What systems have been identified?
- What is the structure of each system?
- Which parts are confirmed from live traffic?
- Which parts only come from static schema recovery?
- Which modules need more gameplay samples?
- What exact user actions would fill each gap?

## Modeling order

Do not build deep numerical extractors until the module catalog is reasonably broad.

After the catalog exists, future captures should update the relevant dossiers. When the user chooses a module for detailed research, build a normalized extractor and presentation layer for that module using accumulated raw evidence.
