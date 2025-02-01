using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;

namespace BaseballApp.Pages;

public class IndexModel : PageModel
{
    private readonly ILogger<IndexModel> _logger;

    public IndexModel(ILogger<IndexModel> logger, ApplicationDbContext context)
    {
        _logger = logger;
        _context = context;
    }


    private readonly ApplicationDbContext _context;

    public List<TopBatterStats> TopBatters { get; set; }
    public List<TopPitcherStats> TopPitchers { get; set; }

    public async Task OnGetAsync()
    {
        TopBatters = await _context.TopBatters.ToListAsync();
        TopPitchers = await _context.TopPitchers.ToListAsync();
    }
}
