using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Sqlite;  // For SQLite-specific functionality
using System.Text.Json;
using System;
using System.Collections.Generic;
using System.IO;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

const string CURRENT_YEAR = "2024";

// Configure logging to write to file
// builder.Host.UseSerilog((context, services, configuration) => configuration
//     .WriteTo.Console()  // Log to the console
//     .WriteTo.File("logs/log.txt", rollingInterval: RollingInterval.Day)  // Log to a file, creating a new file each day
//     .ReadFrom.Configuration(context.Configuration)  // Read logging configuration from appsettings.json
// );

// Add services to the container.
builder.Services.AddRazorPages();

// // Register Entity Framework Core with SQL Server
// builder.Services.AddDbContext<ApplicationDbContext>(options =>
//     options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Configure SQLite with DbContext
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite("Data Source=MlbPlayer.db")
           .LogTo(Console.WriteLine, LogLevel.Information)); 

// Build the app
var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthorization();

app.MapStaticAssets();
app.MapRazorPages().WithStaticAssets();

// Seed the database when the app starts
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    var dbContext = services.GetRequiredService<ApplicationDbContext>();

    dbContext.Database.EnsureCreated(); // Ensure DB exists

    try
    {
        dbContext.Batters.RemoveRange(dbContext.Batters);
        dbContext.Pitchers.RemoveRange(dbContext.Pitchers);
        dbContext.TopBatters.RemoveRange(dbContext.TopBatters);
        dbContext.TopPitchers.RemoveRange(dbContext.TopPitchers);

        dbContext.SaveChanges();
        // Seed the database
        SeedDatabase(dbContext);
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error seeding database: {ex.Message}");
    }
}

app.Run();

// Function to load JSON data and populate the database
void SeedDatabase(ApplicationDbContext dbContext)
{
    string allPlayerFilePath = "./scrapers/static_data/all_player_data.json"; // Adjust path if needed
    string topBattersFilePath = $"./scrapers/static_data/batting_leaders_{CURRENT_YEAR}.json";
    string topPitchersFilePath = $"./scrapers/static_data/pitching_leaders_{CURRENT_YEAR}.json";
    Console.WriteLine($"Seeding database....");

    if (!File.Exists(allPlayerFilePath))
    {
        Console.WriteLine("All Player file not found.");
        return;
    }

    if (!File.Exists(topBattersFilePath))
    {
        Console.WriteLine("Top Batters file not found.");
        return;
    }

    if (!File.Exists(topPitchersFilePath))
    {
        Console.WriteLine("Top Pitchers file not found.");
        return;
    }

    string allPlayerDataString = File.ReadAllText(allPlayerFilePath);
    string topBattersDataString = File.ReadAllText(topBattersFilePath);
    string topPitchersDataString = File.ReadAllText(topPitchersFilePath);

    // Deserialize JSON to List of Dictionary
    var playersData = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, Dictionary<string, object>>>>(allPlayerDataString);
    var topBattersData = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, object>>>(topBattersDataString);
    var topPitchersData = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, object>>>(topPitchersDataString);

    List<BatterStats> batterStatsList = new List<BatterStats>();
    List<PitcherStats> pitcherStatsList = new List<PitcherStats>();
    List<TopBatterStats> topBatterStatsList = new List<TopBatterStats>();
    List<TopPitcherStats> topPitcherStatsList = new List<TopPitcherStats>();

    foreach (var player in playersData)
    {
        string playerName = player.Key;
        foreach (var yearData in player.Value)
        {
            string year = yearData.Key;
            if (yearData.Value["position"].ToString().Trim().Equals("batting"))
            {
                // Create BatterStats and serialize PlayerYear data
                BatterStats batter = new BatterStats
                {
                    Name = playerName,
                    Year = year,
                    PlayerYear = yearData.Value // This will be serialized automatically
                };
                batterStatsList.Add(batter);
            }
            else
            {
                // Create PitcherStats and serialize PlayerYear data
                PitcherStats pitcher = new PitcherStats
                {
                    Name = playerName,
                    Year = year,
                    PlayerYear = yearData.Value // This will be serialized automatically
                };
                pitcherStatsList.Add(pitcher);
            }
        }
    }

    foreach (var player in topBattersData) 
    {
        string playerName = player.Key;
        string year = CURRENT_YEAR;
        TopBatterStats batter = new TopBatterStats
        {
            Name = playerName,
            Year = year,
            PlayerYear = player.Value // Year value will be redundant in this data
        };
        topBatterStatsList.Add(batter);
    }

    foreach (var player in topPitchersData)
    {
        string playerName = player.Key;
        Console.Write($"Adding top player {playerName}");
        string year = CURRENT_YEAR;
        TopPitcherStats pitcher = new TopPitcherStats
        {
            Name = playerName,
            Year = year,
            PlayerYear = player.Value // Year value will be redundant in this data
        };
        topPitcherStatsList.Add(pitcher);
    }

    // Add Batters to database if not already seeded
    if (!dbContext.Batters.Any())
    {
        dbContext.Batters.AddRange(batterStatsList);
        dbContext.SaveChanges();
        Console.WriteLine("Batters seeded successfully!");
    }
    else
    {
        Console.WriteLine("Batters already exist. Skipping seed.");
    }

    // Add Pitchers to database if not already seeded
    if (!dbContext.Pitchers.Any())
    {
        dbContext.Pitchers.AddRange(pitcherStatsList);
        dbContext.SaveChanges();
        Console.WriteLine("Pitchers seeded successfully!");
    }
    else
    {
        Console.WriteLine("Pitchers already exist. Skipping seed.");
    }

    if (!dbContext.TopBatters.Any())
    {
        dbContext.TopBatters.AddRange(topBatterStatsList);
        dbContext.SaveChanges();
        Console.WriteLine("Pitchers seeded successfully!");
    }
    else
    {
        Console.WriteLine("Top batters already exist. Skipping seed.");
    }
    
    if (!dbContext.TopPitchers.Any())
    {
        dbContext.TopPitchers.AddRange(topPitcherStatsList);
        dbContext.SaveChanges();
        Console.WriteLine("Pitchers seeded successfully!");
    }
    else
    {
        Console.WriteLine("Top pitchers already exist. Skipping seed.");
    }
}


// Debug
// void SeedDatabase(ApplicationDbContext dbContext)
// {
//     if (!dbContext.Batters.Any())  // Check if database is empty
//     {
//         Console.WriteLine("Seeding database...");

//         dbContext.Batters.AddRange(new List<BatterStats>
//         {
//             new BatterStats { Name = "Mike Trout", Year = "2024" },
//             new BatterStats { Name = "Shohei Ohtani", Year = "2024" }
//         });

//         dbContext.SaveChanges();
//     }
//     else
//     {
//         Console.WriteLine("Database already contains data.");
//     }
// }