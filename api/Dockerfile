# Multi-stage build for .NET Core Web API
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore as distinct layers
COPY ["JABizTown.API.csproj", "./"]
RUN dotnet restore "./JABizTown.API.csproj"

# Copy everything else and build
COPY . .
WORKDIR "/src/."
RUN dotnet build "JABizTown.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "JABizTown.API.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Final stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "JABizTown.API.dll"]
