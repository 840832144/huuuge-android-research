# Research Data Architecture

## Project objective

Build a reusable numerical-research pipeline for the Huuuge Casino Android client. Battle Pass is only the first end-to-end validation target; it is **not** the final scope.

The system should preserve enough raw evidence to reconstruct and compare multiple gameplay/economy systems over time, then generate focused reports only when the user asks for a specific system.

## Target system coverage

The collector and schema index should be designed for, at minimum:

- slot machines / spin sessions / bets / wins / feature triggers / jackpots where observable;
- lottery and draw systems;
- missions / quests / daily and weekly tasks;
- Battle Pass / MiniPass / reward tracks;
- live events, milestones, collections, conquest-style systems, charms and loyalty systems;
- offers, bundles, prices, purchase-related configuration and reward composition;
- currencies, balances and reward grants when exposed in observed client messages;
- VIP / clubs / progression / level-gated systems where present in recovered schemas;
- other systems discovered later through `service_index`, `method_index`, message names, static configs, Lua or ZPK resources.

Do not hard-code the pipeline around the systems listed above. Unknown or newly introduced RPCs must still be retained.

## Three-layer design

### 1. Capture layer — lossless first

The runtime collector should save **all observable `Casino.RpcMessage` traffic**, not only Battle Pass or currently understood systems.

Console filters are allowed for readability, but filters must not discard captured data.

For every observed RPC, retain whenever available:

- timestamp with sub-second precision;
- direction (`client->server` / `server->client`);
- RPC wrapper type;
- `service_index`;
- resolved service name;
- `method_index`;
- resolved method name;
- sequence number;
- user id only when needed locally for correlation; do not commit personal identifiers;
- compression metadata;
- original wrapper bytes;
- original payload bytes;
- decoded protobuf JSON when schema resolution succeeds;
- decode failure / unknown-schema reason when it does not;
- client/game version and descriptor version for the capture session.

Unknown messages and undecodable payloads are first-class research data and must be preserved for later schema recovery.

### 2. Interpretation layer — system model

Do not immediately flatten all protobuf fields into one giant spreadsheet.

Maintain a normalized event/fact layer first, for example:

```text
session_id
capture_time
direction
service
method
message_type
system
entity_id
field_path
value
raw_ref
context_tag
```

Then build system-specific models/extractors on top of it.

Examples:

#### Slots

Potential research dimensions, when observable:

```text
game_id / machine_id
bet
bet_multiplier
coin_value
win
win_multiplier
spin_result
feature / free-spin trigger
feature progress
jackpot contribution / win
balance before / after
session counters
```

Do not assume every spin outcome is transmitted through the same RPC. If important slot state lives in a game-server stream, native object, Lua state, or static table, add that as a separate source rather than forcing it into the generic AppServer/AppClient RPC model.

#### Lottery

```text
lottery_id
ticket price
ticket count / entries
draw schedule
reward tiers
odds / weights when exposed
result / payout
progress / free entries
```

#### Missions / quests

```text
mission_id
set / segment
action_type
requirement
progress
limitations
reward / reward_bundle
reset / expiry
skip cost / skip balance
```

#### Passes / milestones / events

```text
event_id
level / stage
requirement
free reward
paid reward
premium/deluxe reward
event currency
progress
start/end/expiry
prestige / repeat loop
```

#### Offers / economy

```text
offer_id
product_id
price / currency
reward contents
quantity
multiplier / bonus label
segment / eligibility
purchase limit
expiry
```

### 3. Presentation layer — query on demand

Raw capture should be broad; presentation should be narrow.

When the user asks to inspect one system, generate only that view, for example:

- one slot machine's bet/win/feature/RTP experience;
- lottery ticket cost, reward tiers and expected-value structure;
- mission requirement/reward efficiency;
- Battle Pass free vs paid reward-track value;
- event milestone marginal cost and reward value;
- offer price-to-resource conversion tables.

Presentation outputs may be CSV, Excel, charts or concise analysis tables, but they should be generated from preserved raw/normalized data rather than requiring a new capture each time whenever possible.

## Additional evidence channels

RPC capture is the primary runtime channel, but the complete numerical model may require three evidence sources:

1. **Runtime RPC / protobuf** — server configuration, state updates, rewards, progress, offers, etc.
2. **Static client data** — recovered protobuf descriptors, Lua, native constants, ZPK/config assets.
3. **Interaction context** — lightweight user/action markers such as `open_slots_lobby`, `spin_machine_X`, `open_lottery`, `claim_mission`, used to correlate message bursts with visible actions.

A later collector should support adding context markers without relying on long video OCR.

## Session layout

Recommended capture structure:

```text
captures/<session_id>/
  manifest.json
  index.csv
  messages.jsonl
  raw/
    *.rpc.bin
  json/
    *.json
  markers.jsonl
  decode_errors.jsonl
```

`manifest.json` should record the game version, package version code, Frida version, descriptor fingerprint, device/emulator identifier and capture start/end times.

## Non-negotiable design rules

1. **Capture broadly, filter only the display.**
2. **Never discard unknown RPCs just because no exporter exists yet.**
3. **Battle Pass is the first validation target only.**
4. **System-specific exporters are downstream modules, not capture-time filters.**
5. **Keep raw bytes so schemas/interpretations can be corrected later.**
6. **Record version metadata because live-ops values and schemas change over time.**
7. **Separate confirmed fields from inferred business meaning.**
8. **Do not modify game/server state for research.**
9. **Do not commit sensitive account/session identifiers or unsanitized raw captures to Git.**

## Near-term implementation order

1. Establish privileged Frida attach in the isolated research environment.
2. Prove generic lossless `Casino.RpcMessage` capture.
3. Use Battle Pass as the first decoded validation case.
4. Verify the capture still stores unrelated RPCs during the same session.
5. Build a service/method inventory from a normal browse/play session.
6. Classify observed traffic into systems: slots, lottery, missions, passes/events, offers/economy, clubs/VIP, other.
7. Add system-specific extractors one at a time without changing the raw capture contract.
8. Add action/context markers and a normalized analytical fact layer.
