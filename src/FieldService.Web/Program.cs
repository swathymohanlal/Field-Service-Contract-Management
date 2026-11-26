var builder = WebApplication.CreateBuilder(args);
builder.Services.AddHealthChecks();

var app = builder.Build();
app.UseDefaultFiles();
app.UseStaticFiles();

app.MapHealthChecks("/health/live");
app.MapGet("/api/v1/platform", () => TypedResults.Ok(new
{
    product = "Field Service & Contract Management",
    phase = "P00",
    profile = "foundation",
    version = typeof(Program).Assembly.GetName().Version?.ToString(3)
}));

app.Run();
