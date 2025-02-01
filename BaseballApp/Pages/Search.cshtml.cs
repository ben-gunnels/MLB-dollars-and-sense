using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace BaseballApp.Pages;
public class SearchModel : PageModel
{
    private readonly ApplicationDbContext _context;

    public SearchModel(ApplicationDbContext context)
    {
        _context = context;
    }

    public List<BatterStats> Batter { get; set; }
    public List<PitcherStats> Pitcher { get; set; }

    public string PlayerName { get; set; }  

    public List<string> SuggestedPlayers { get; set; }  = new List<string>();

    public async Task<JsonResult> OnGetSearchSuggestionsAsync(string query)
    {
        if (string.IsNullOrWhiteSpace(query))
            return new JsonResult(new List<string>());

        var players = await _context.Batters
            .Where(b => b.Name.StartsWith(query))
            .Select(b => b.Name)
            .Union(_context.Pitchers.Where(p => p.Name.StartsWith(query)).Select(p => p.Name))
            .Distinct()
            .OrderBy(n => n)
            .Take(10)
            .ToListAsync();

        return new JsonResult(players);
    }

    public async Task OnGetAsync(string playerName)
    {
        PlayerName = playerName;

        // Fetch player suggestions (autocomplete)
        SuggestedPlayers = await _context.Batters
            .Select(b => b.Name)
            .Union(_context.Pitchers.Select(p => p.Name)) // Combine both batters and pitchers
            .Distinct()
            .OrderBy(n => n)
            .Take(10)
            .ToListAsync();  // Adjust `Take(10)` as needed

        if (!string.IsNullOrEmpty(playerName))
        {
            Batter = await _context.Batters
                .Where(b => EF.Functions.Like(b.Name, $"%{playerName}%"))
                .ToListAsync();

            // Search in PitcherStats
            Pitcher = await _context.Pitchers
                .Where(b => EF.Functions.Like(b.Name, $"%{playerName}%"))
                .ToListAsync();

            Console.WriteLine($"{Batter.Count}, {Pitcher.Count}");
        }
    }
}