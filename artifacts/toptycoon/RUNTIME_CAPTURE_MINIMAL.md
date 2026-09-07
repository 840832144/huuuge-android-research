# Toy Tycoon Runtime Capture — Minimal Verification Results

> Goal: play → capture numeric values (spin bet/reward) for planner analysis.
> Reached a verified milestone: **game-thread C# method capture via
> il2cpp_runtime_invoke**, locating the slot business classes. Value-level
> field extraction is the next step.

## Verified capture path (2026-09-07)

Environment: topTycoon instance `127.0.0.1:5605`, root + x86_64 frida-server
(`127.0.0.1:27042`) + ARM64 Gadget (`127.0.0.1:27045`), game
`com.monopoly.dream.idle.king`.

**Key insight (from `android-houdini-injection` reference):** Under BlueStacks
Houdini, Frida's `Process.findModuleByName`/`Module API` only sees a few ARM64
libraries (libmain/libunity) and **not** libil2cpp.so after the gadget settles;
and **calling IL2CPP APIs from a non-game thread (or big enumeration loops)
crashes** the app due to Houdini TLS isolation. The reliable approach is:

1. `il2cpp_runtime_invoke` is **exported** by libil2cpp and is callable from Frida.
2. **`Interceptor.attach(il2cpp_runtime_invoke)`** runs on the game thread (correct
   TLS) — inside onEnter you can safely call `NativeFunction(...)` for il2cpp
   API and read method/class names without crashing.
3. **MethodInfo.methodPointer = `mi.readPointer()`** is the correct, attachable
   Houdini trampoline address (raw `il2cpp_class_from_name`+get_method return
   `(methodInfo, .readPointer()=trampoline)`); raw ARM addresses are NOT attachable.
4. Single-shot `il2cpp_class_from_name` / `il2cpp_class_get_method_from_name`
   are safe; **iterating methods/classes crashes** — avoid loops.

## Confirmed working captures (minimal verification)

- ARM64 Gadget `Process.arch = arm64`, sees libil2cpp/libunity/libmain (during
  the injection window).
- `il2cpp_runtime_invoke = 0x710af98a65d0` (session-dependent).
- `ProtobufRuntime.dll` image + `Google.Protobuf.CodedOutputStream` class found;
  write methods resolved via `il2cpp_class_get_method_from_name` →
  MethodInfo.methodPointer:
  - `WriteMessage=0x7109c83fb880`, `WriteString`, `WriteTag=0x710afbac4198`
    (methodPointer), `WriteUInt64`, `WriteInt32`, `WriteBytes`, `WriteRawBytes`.
- **`Interceptor.attach(il2cpp_runtime_invoke)` captures game-thread C# calls**:
  saw `RenderPipelineManager`, `UpdateFunction.Invoke`, `DOTweenComponent.FixedUpdate`,
  `SetupCoroutine`, `<AfterPhysics>d__38`, and — filtering business classes —
  **`BaseSlotsGame.SlotsGame.Update` / `BaseSlotsGame.SlotColumn.Update`**
  (6670+ business calls), confirming access to the slot game business logic.
- Business namespaces: `BaseSlotsGame` (SlotsGame, SlotColumn, SlotBehaviour),
  `Game.Hotfix.Gameplay.SlotsGameplay`, `Game.Hotfix.Storage.StorageSlotsGame`.

## Why value-level capture is the next step

Captured business calls are dominated by `Update` (render/loop). The actual
numeric values (bet/win/coins) live in **protobuf message fields** (e.g.
`Protos.House.*` like `CGRewardList`/`GC*CollectReward` with `rewardRank`,
`itemStr`) or player-currency messages (e.g. `player.cash`), not as standalone
spin method names. To read values you must extract protobuf message object
fields inside a `runtime_invoke` callback (game thread), targeting the specific
CG/GC message for spin.

## Reusable scripts (local, `C:\bigfish_research\toptycoon\`)

- `capture_biz_invoke.py` — captures game-thread business-class method calls
  (filters BaseSlotsGame/Protos/…), writes `biz_invoke.jsonl`.
- `hook_runtime_invoke.py` — attaches runtime_invoke, logs all method names.
- `bootstrap_gadget_tt.py` — injects ARM64 Gadget via Houdini (adapted Huuuge).
- Static protocol dict: `toytycoon_protocol_dict.json` (422 messages/1264 fields).

## Next step (value extraction)

Hook the spin CG/GC message class method on the game thread (runtime_invoke
callback), resolve its protobuf fields, and read the numeric field values
(bet/win/coins) from the message object. Requires mapping the same-room bonus
and reward fields from the static dict to concrete `Protos.House` spin messages.
