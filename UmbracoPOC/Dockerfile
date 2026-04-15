# Stage 1: Build & Initialize Umbraco
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

ENV DOTNET_CLI_TELEMETRY_OPTOUT=1
ENV DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
# Increase NuGet timeout and retry count to handle slow networks
ENV DOTNET_RESTORE_TIMEOUT=600
ENV NUGET_CERT_REVOCATION_MODE=offline

# Install Umbraco 13 Templates (LTS for .NET 8)
RUN dotnet new install Umbraco.Templates::13.3.0

# Create the project
RUN dotnet new umbraco -n UmbracoApp -o UmbracoApp
WORKDIR /src/UmbracoApp

# Install uSync 13.x (Includes Content/Media syncing in v13)
# We run restore with --disable-parallel to prevent network timeouts 
RUN dotnet add package uSync --version 13.3.1

# Explicitly restore dependencies sequentially to ensure stability
RUN dotnet restore --disable-parallel

# Build and publish
RUN dotnet publish -c Release -o /app/publish --no-restore

# Stage 2: Final Runtime Image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

ENV ASPNETCORE_ENVIRONMENT=Development
ENV ASPNETCORE_URLS=http://+:8080

RUN mkdir -p /app/umbraco/Data && \
    mkdir -p /app/umbraco/Logs && \
    mkdir -p /app/wwwroot/media

COPY --from=build /app/publish .

EXPOSE 8080

ENTRYPOINT ["dotnet", "UmbracoApp.dll"]
