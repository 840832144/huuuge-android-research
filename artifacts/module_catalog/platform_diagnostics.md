# HTF / Proxy / Test Infrastructure

Client test automation, Lua/test-suite execution, driver controls and proxy transport test services; cataloged as platform infrastructure, not gameplay.

## Catalog status

- Evidence status: **schema-only / live sample pending**
- Structural completeness: **30/100 — schema skeleton**
- Primary live samples: **0** from `20260825_182300`
- Cross-cutting live samples: **0**
- Live endpoints / schema endpoints: **0 / 11**
- Live populated field paths: **0**

## Schema scope

- Proto files: `Definition.proto`, `Htf.proto`, `HtfApp.proto`, `ProxyTestServer.proto`, `Rpc.proto`, `Services.proto`
- Services: `ProxyTestServer`
- Related message types: **74**

- `Casino.BigNumber` (Definition.proto)
- `Casino.BigNumberExampleRequest` (ProxyTestServer.proto)
- `Casino.BigNumberExampleResponse` (ProxyTestServer.proto)
- `Casino.BigPayloadIn` (ProxyTestServer.proto)
- `Casino.BigPayloadOut` (ProxyTestServer.proto)
- `Casino.EmptyRequest` (Services.proto)
- `Casino.EmptyResponse` (Services.proto)
- `Casino.NestedBigNumberResponse` (ProxyTestServer.proto)
- `Casino.NestedBigNumberResponse.NestedObject` (ProxyTestServer.proto)
- `Casino.NestedData` (ProxyTestServer.proto)
- `Casino.ProxyExampleRequest` (ProxyTestServer.proto)
- `Casino.ProxyExampleResponse` (ProxyTestServer.proto)
- `Htf.AppInfo` (Htf.proto)
- `Htf.AppStatusResponse` (Htf.proto)
- `Htf.DriverGetControlsRequest` (Htf.proto)
- `Htf.DriverGetControlsResponse` (Htf.proto)
- `Htf.DriverIsBusyRequest` (Htf.proto)
- `Htf.DriverIsBusyResponse` (Htf.proto)
- `Htf.DriverLuaDynamicApiRequest` (Htf.proto)
- `Htf.DriverLuaDynamicApiResponse` (Htf.proto)
- `Htf.DriverLuaEvalRequest` (Htf.proto)
- `Htf.DriverLuaEvalResponse` (Htf.proto)
- `Htf.DriverPressKeyRequest` (Htf.proto)
- `Htf.DriverPressKeyResponse` (Htf.proto)
- `Htf.DriverRegGetRequest` (Htf.proto)
- `Htf.DriverRegGetResponse` (Htf.proto)
- `Htf.DriverRegSetRequest` (Htf.proto)
- `Htf.DriverRegSetResponse` (Htf.proto)
- `Htf.DriverSendTextInputRequest` (Htf.proto)
- `Htf.DriverSendTextInputResponse` (Htf.proto)
- `Htf.DriverSetEventRequest` (Htf.proto)
- `Htf.DriverUiClickRequest` (Htf.proto)
- `Htf.DriverUiClickResponse` (Htf.proto)
- `Htf.DriverUiSwipeRequest` (Htf.proto)
- `Htf.DriverUiSwipeResponse` (Htf.proto)
- `Htf.EmptyMessage` (Htf.proto)
- `Htf.ExecuteCommandRequest` (Htf.proto)
- `Htf.ExecuteCommandResponse` (Htf.proto)
- `Htf.ExecuteTestRequest` (Htf.proto)
- `Htf.ExecuteTestResponse` (Htf.proto)
- `Htf.HtfControl` (Htf.proto)
- `Htf.KeyValuePair` (Htf.proto)
- `Htf.LoadLuaFromDataRequest` (Htf.proto)
- `Htf.LoadLuaFromUrlRequest` (Htf.proto)
- `Htf.LoadTestSuiteFromDataRequest` (Htf.proto)
- `Htf.LoadTestSuiteFromUrlRequest` (Htf.proto)
- `Htf.LogRequest` (Htf.proto)
- `Htf.LuaApiData` (Htf.proto)
- `Htf.NativeControlFilter` (Htf.proto)
- `Htf.NativeControlsRequest` (Htf.proto)
- `Htf.PingRequest` (Htf.proto)
- `Htf.PingResponse` (Htf.proto)
- `Htf.PluginMethodCallRequest` (Htf.proto)
- `Htf.PluginMethodCallResponse` (Htf.proto)
- `Htf.RhinoParserAuthDataRequest` (Htf.proto)
- `Htf.RhinoParserAuthDataResponse` (Htf.proto)
- `Htf.RpcMessage` (Rpc.proto)
- `Htf.ScreenshotData` (Htf.proto)
- `Htf.ScreenshotRequest` (Htf.proto)
- `Htf.ScreenshotResponse` (Htf.proto)
- `Htf.SharedRegistryEntry` (Htf.proto)
- `Htf.SharedRegistryGetRequest` (Htf.proto)
- `Htf.SharedRegistryGetResponse` (Htf.proto)
- `Htf.SharedRegistryRemoveRequest` (Htf.proto)
- `Htf.SharedRegistryRemoveResponse` (Htf.proto)
- `Htf.SharedRegistrySetRequest` (Htf.proto)
- `Htf.SharedRegistrySetResponse` (Htf.proto)
- `Htf.TestCase` (Htf.proto)
- `Htf.TestCaseParameters` (Htf.proto)
- `Htf.TestCaseResultResponse` (Htf.proto)
- `Htf.TestCaseStartedResponse` (Htf.proto)
- `Htf.TestCaseStep` (Htf.proto)
- `Htf.VideoCaptureStartRequest` (Htf.proto)
- `Htf.VideoCaptureStopRequest` (Htf.proto)

## RPC and flow structure

Schema flow: diagnostic/test request -> controlled client/proxy operation -> response. These interfaces are static discoveries and are not used to alter gameplay or server state in this project.

| Service.method | Request | Response/update | Live req | Live resp | Evidence |
|---|---|---|---:|---:|---|
| `ProxyTestServer.ReturnOk` | `Casino.ProxyExampleRequest` | `Casino.ProxyExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.ReturnError` | `Casino.ProxyExampleRequest` | `Casino.ProxyExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.ThrowException` | `Casino.ProxyExampleRequest` | `Casino.ProxyExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.BigPayload` | `Casino.BigPayloadIn` | `Casino.BigPayloadOut` | 0 | 0 | schema-only |
| `ProxyTestServer.EmptyResponseBody` | `Casino.ProxyExampleRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.EmptyRequestBody` | `Casino.EmptyRequest` | `Casino.ProxyExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.VoidResponse` | `Casino.ProxyExampleRequest` | `Casino.EmptyResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.VoidRequest` | `Casino.EmptyRequest` | `Casino.ProxyExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.BigNumberTest` | `Casino.BigNumberExampleRequest` | `Casino.BigNumberExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.BigNumberResponse` | `Casino.BigNumberExampleResponse` | `Casino.BigNumberExampleResponse` | 0 | 0 | schema-only |
| `ProxyTestServer.NestedBigNumber` | `Casino.NestedBigNumberResponse` | `Casino.NestedBigNumberResponse` | 0 | 0 | schema-only |

## Structural fields

### Entity identifiers

- `Casino.BigNumberExampleRequest.player_id (int32, required)`
- `Casino.ProxyExampleRequest.request_id (int32, required)`
- `Htf.DriverPressKeyRequest.key (uint32, required)`
- `Htf.HtfControl.id (string, required)`
- `Htf.KeyValuePair.key (string, required)`
- `Htf.SharedRegistryEntry.key (string, required)`
- `Htf.SharedRegistryGetRequest.key (string, required)`
- `Htf.SharedRegistryRemoveRequest.key (string, required)`
- `Htf.SharedRegistryRemoveResponse.key (string, required)`

### Progression / state

- `Casino.BigNumberExampleRequest.points (Casino.BigNumber, required)`
- `Casino.BigNumberExampleResponse.points (Casino.BigNumber, optional)`
- `Casino.BigNumberExampleResponse.status (Casino.BigNumberExampleResponse.Status, required)`
- `Casino.BigPayloadOut.status (Casino.BigPayloadOut.Status, required)`
- `Casino.NestedBigNumberResponse.status (Casino.NestedBigNumberResponse.Status, required)`
- `Casino.ProxyExampleResponse.status (Casino.ProxyExampleResponse.Status, required)`
- `Htf.DriverIsBusyResponse.status (Htf.DriverIsBusyResponse.Status, required)`
- `Htf.DriverLuaDynamicApiResponse.status (Htf.DriverLuaDynamicApiResponse.Status, required)`
- `Htf.DriverLuaEvalResponse.status (Htf.DriverLuaEvalResponse.Status, required)`
- `Htf.DriverPressKeyResponse.status (Htf.DriverPressKeyResponse.Status, required)`
- `Htf.DriverRegGetResponse.status (Htf.DriverRegGetResponse.Status, required)`
- `Htf.DriverRegSetResponse.status (Htf.DriverRegSetResponse.Status, required)`
- `Htf.DriverSendTextInputResponse.status (Htf.DriverSendTextInputResponse.Status, required)`
- `Htf.DriverUiClickResponse.status (Htf.DriverUiClickResponse.Status, required)`
- `Htf.DriverUiSwipeResponse.status (Htf.DriverUiSwipeResponse.Status, required)`
- `Htf.ExecuteCommandResponse.status (Htf.ExecuteCommandResponse.Status, required)`
- `Htf.PluginMethodCallResponse.status (Htf.PluginMethodCallResponse.Status, required)`
- `Htf.RhinoParserAuthDataResponse.status (Htf.RhinoParserAuthDataResponse.Status, required)`
- `Htf.ScreenshotResponse.status (Htf.ScreenshotResponse.Status, required)`
- `Htf.SharedRegistryGetResponse.status (Htf.SharedRegistryGetResponse.Status, required)`
- `Htf.SharedRegistryRemoveResponse.status (Htf.SharedRegistryRemoveResponse.Status, required)`
- `Htf.SharedRegistrySetResponse.status (Htf.SharedRegistrySetResponse.Status, required)`
- `Htf.TestCaseResultResponse.status (Htf.TestCaseResultResponse.Status, required)`
- `Htf.TestCaseStep.depthLevel (uint32, optional)`

### Cost / input

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Currency / balance

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Reward / output

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Timing / reset / expiry

- `Htf.DriverIsBusyResponse.timeToEnd (uint32, optional)`
- `Htf.DriverPressKeyRequest.duration (uint32, required)`
- `Htf.DriverSetEventRequest.clientTime (uint32, required)`
- `Htf.DriverSetEventRequest.sessionTime (uint32, required)`
- `Htf.DriverUiClickRequest.duration (uint32, optional)`
- `Htf.DriverUiSwipeRequest.duration (uint32, required)`

### Segment / eligibility / limit

- No dedicated field was classified in this role from the assigned schema; live evidence is still pending.

### Other structural fields

- `Casino.BigNumber.value (bytes, required)`
- `Casino.BigNumberExampleResponse.error_code (int32, optional)`
- `Casino.BigPayloadIn.data (string, required)`
- `Casino.BigPayloadOut.data (string, optional)`
- `Casino.BigPayloadOut.error_code (int32, optional)`
- `Casino.NestedBigNumberResponse.NestedObject.nestedData (Casino.NestedData, optional)`
- `Casino.NestedBigNumberResponse.NestedObject.nestedNumber (Casino.BigNumber, required)`
- `Casino.NestedBigNumberResponse.bigNumber (Casino.BigNumber, optional)`
- `Casino.NestedBigNumberResponse.error_code (int32, optional)`
- `Casino.NestedBigNumberResponse.nested (Casino.NestedBigNumberResponse.NestedObject, optional)`
- `Casino.NestedBigNumberResponse.nestedData (Casino.NestedData, optional)`
- `Casino.NestedData.nestedNumber (Casino.BigNumber, required)`
- `Casino.ProxyExampleRequest.message (string, required)`
- `Casino.ProxyExampleResponse.error_code (int32, optional)`
- `Casino.ProxyExampleResponse.message (string, optional)`
- `Htf.AppInfo.app_version (string, required)`
- `Htf.AppInfo.apps_launches (string, required)`
- `Htf.AppInfo.assets_latest (string, required)`
- `Htf.AppInfo.build_version (string, required)`
- `Htf.AppInfo.platform (string, required)`
- `Htf.AppInfo.sku (string, required)`
- `Htf.AppStatusResponse.ready (bool, required)`
- `Htf.DriverGetControlsResponse.controls (Htf.HtfControl, repeated)`
- `Htf.DriverIsBusyResponse.isBusy (bool, required)`
- `Htf.DriverIsBusyResponse.taskName (string, optional)`
- `Htf.DriverLuaDynamicApiRequest.data (Htf.LuaApiData, required)`
- `Htf.DriverLuaDynamicApiRequest.methodId (string, required)`
- `Htf.DriverLuaDynamicApiResponse.data (Htf.LuaApiData, required)`
- `Htf.DriverLuaDynamicApiResponse.methodId (string, required)`
- `Htf.DriverLuaEvalRequest.code (string, required)`
- `Htf.DriverLuaEvalResponse.message (string, optional)`
- `Htf.DriverPressKeyResponse.message (string, optional)`
- `Htf.DriverRegGetRequest.path (string, required)`
- `Htf.DriverRegGetResponse.message (string, optional)`
- `Htf.DriverRegGetResponse.value (string, required)`
- `Htf.DriverRegSetRequest.path (string, required)`
- `Htf.DriverRegSetRequest.value (string, required)`
- `Htf.DriverRegSetResponse.message (string, optional)`
- `Htf.DriverSendTextInputRequest.checkFocus (bool, optional)`
- `Htf.DriverSendTextInputRequest.text (string, required)`
- … 86 more rows in `fields.csv`

## Live-session coverage

No primary endpoint for this module appeared in the current session; live sample pending.

## Evidence ledger

### Observed-live

- None in the current session.

### Schema-only

- Unobserved endpoints, message relationships, field names, numbers, cardinalities, and types come from the recovered descriptor set.
- Schema presence proves client support, not that the feature is enabled for this account/build at capture time.

### Inferred

- Flow interpretation: Schema flow: diagnostic/test request -> controlled client/proxy operation -> response. These interfaces are static discoveries and are not used to alter gameplay or server state in this project.
- Field semantic roles are name-based catalog heuristics and must be checked against future marked live samples before business conclusions.

## Static / additional evidence channels

- No module-specific ZPK filename match was found in the current base APK inventory.
- Shared runtime evidence: `libClawApp.so` contains C++/Lua integration; module-specific Lua/native ownership is not yet mapped unless stated above.

## Missing data and next user actions

- No gameplay action is required; keep this module schema-only unless naturally emitted diagnostic traffic appears.
- Do not invoke command/Lua/test endpoints against the live game for research convenience.
- Use action markers in the next capture so request bursts can be correlated with exact screens/actions.
- If RPCs do not expose required structure, inspect the named ZPK assets, Lua state, or game-server/native state as a separate evidence channel.

This dossier is structural. It intentionally makes no RTP, EV, purchase-value, or reward-efficiency conclusion.
