# Knowledge Base: Umbraco 13 Docker Troubleshooting

This document summarizes the technical challenges and solutions encountered while setting up the Umbraco 13 (LTS) Proof of Concept in a Docker Desktop environment.

## 1. Issue: .NET SDK Version Mismatch (NETSDK1045)
**Symptom**: `error NETSDK1045: The current .NET SDK does not support targeting .NET 10.0. Either target .NET 8.0 or lower...`
- **Cause**: The command `dotnet new install Umbraco.Templates` pulls the absolute latest version (e.g., v17.x), which targets future .NET versions (like .NET 10.0) that are not supported by the .NET 8.0 SDK container.
- **Solution**: Pin the template installation to the version matching your SDK.
    - **Fix**: Replace `dotnet new install Umbraco.Templates` with `dotnet new install Umbraco.Templates::13.3.0`.

## 2. Issue: NuGet Connection Timeouts
**Symptom**: `The HTTP request to 'GET https://api.nuget.org/...' has timed out after 100000ms.`
- **Cause**: Docker Desktop's virtualized network stack can struggle with the high volume of concurrent HTTP requests made by `dotnet restore`.
- **Solution**: 
    1. **Sequential Restore**: Force NuGet to download packages one by one using the `--disable-parallel` flag.
    2. **Timeout Increase**: Explicitly increase the CLI and HTTP timeout limits.
    - **Fix**: Use `RUN dotnet restore --disable-parallel` and set `ENV DOTNET_RESTORE_TIMEOUT=600`.

## 3. Issue: Package Incompatibility (uSync.ContentEdition)
**Symptom**: `error: Package 'uSync.ContentEdition' is incompatible with 'all' frameworks in project...`
- **Cause**: In Umbraco 13, the functionality previously found in `uSync.ContentEdition` was integrated directly into the core `uSync` package. Attempting to install the legacy package for version 13 results in a resolution error.
- **Solution**: Use only the core `uSync` package for version 13.x.
    - **Fix**: Remove the `dotnet add package uSync.ContentEdition` command.

## 4. Issue: Project Directory Alignment
**Symptom**: `Unable to create dependency graph file for project...`
- **Cause**: The `dotnet new umbraco -n UmbracoApp` command creates a subfolder by default. If the Docker `WORKDIR` isn't aligned with this subfolder, subsequent `dotnet add` commands fail because they cannot find the `.csproj` file.
- **Solution**: Use the `--output .` flag to create the project files directly in the build root.
    - **Fix**: `RUN dotnet new umbraco --name UmbracoApp --output .`

---

*Last Updated: 2026-04-14*
