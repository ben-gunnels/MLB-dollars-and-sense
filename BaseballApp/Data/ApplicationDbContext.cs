using Microsoft.EntityFrameworkCore;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) 
        : base(options)
    {
    }

    public DbSet<BatterStats> Batters { get; set; }
    public DbSet<PitcherStats> Pitchers { get; set; }  // Add this if you also track pitchers
    public DbSet<TopBatterStats> TopBatters { get; set; }
    public DbSet<TopPitcherStats> TopPitchers { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configure entity mappings if needed
        modelBuilder.Entity<BatterStats>().ToTable("BatterStats");
        modelBuilder.Entity<PitcherStats>().ToTable("PitcherStats"); // If you have a pitcher model

        modelBuilder.Entity<TopBatterStats>().ToTable("TopBatters");
        modelBuilder.Entity<TopPitcherStats>().ToTable("TopPitchers"); // Store the top Batters and Pitchers by value in a separate table for now.
        // The table will be small as it contains 10 players of each. In the future this should be replaced by first unpacking the attributes from the player data. This is an adequate solution for now.
    }
}