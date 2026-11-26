# Field Service & Contract Management · P00

Version 0.1.0 · Engineering foundation for review

The ASP.NET Core 10 host serves a system status page, process liveness at `GET /health/live`, and platform metadata at `GET /api/v1/platform`. The future work-order route is intentionally absent in the foundation.

## Run and verify

From the extracted project root with .NET 10 SDK 10.0.404 or a compatible newer .NET 10 feature band:

```sh
dotnet build FieldService.slnx -c Release
dotnet run --project src/FieldService.Web -c Release -- --urls http://127.0.0.1:5080
```

Open http://127.0.0.1:5080. From a second terminal run `python3 scripts/smoke.py`. For a publish rehearsal, run `dotnet publish src/FieldService.Web -c Release --no-build -o artifacts/publish`. Start `dotnet FieldService.Web.dll --urls http://127.0.0.1:5080` from the publish directory and repeat smoke from the source root.

The Docker recipe is available with `docker build -t field-service:p00 .` and `docker run --rm -p 127.0.0.1:5080:8080 field-service:p00`. Repeat smoke against that host if container execution is in scope.

## Product handoff

The proposed first profile is a commercial HVAC service company operating reactive repairs and recurring maintenance under contract. The proposed second profile is a solar operations and maintenance contractor. Proposed workflows include asset register, entitlements and SLA, work orders, dispatch, site execution, parts, sign-off and billing handoff. P00 has no business persistence, external providers, or customer data.

This uses the established Workforce P00 host pattern. Record the accepted repository commit and generate a fresh sanitized Repomix for the next implementation phase. The companion Sets 01–05 define what later implementation and acceptance must cover.

## Verification record

| Check | Result |
|---|---|
| .NET SDK 10.0.404, Release build | Passed with zero warnings and errors |
| Release publish and startup from output | Passed |
| HTTP smoke for status, liveness, metadata, assets and future-route 404 | Passed |
| JavaScript syntax | Passed |
| Browser visual/accessibility verification | Pending. Chromium could not start in the execution environment. |
| Container image and runtime | Pending. A container engine was unavailable. |
