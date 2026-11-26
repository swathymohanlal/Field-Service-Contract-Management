FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /source
COPY global.json ./
COPY src/FieldService.Web/FieldService.Web.csproj src/FieldService.Web/
RUN dotnet restore src/FieldService.Web/FieldService.Web.csproj
COPY src/FieldService.Web/ src/FieldService.Web/
RUN dotnet publish src/FieldService.Web/FieldService.Web.csproj -c Release -o /out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0
WORKDIR /app
COPY --from=build /out ./
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "FieldService.Web.dll"]
