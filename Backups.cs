
public class BatterStats : PlayerStats
{
    // Calculated metrics
    public float BWARPerDollar { get; set; }
    public float BHPerDollar { get; set; }
    public float BHRPerDollar { get; set; }
    public float BDoublesPerDollar { get; set; }
    public float BTriplesPerDollar { get; set; }
    public float BSBPerDollar { get; set; }
    public float BBBPerDollar { get; set; }
    public float BTBPerDollar { get; set; }
    public float BGamesPerDollar { get; set; }
    public float OPSPlusPerDollar { get; set; }

    public float BBattingAvgScore { get; set; }
    public float BOnbasePercentageScrore { get; set; }
    public float BSluggingPercentageScore { get; set; }
    public float BOPSScore { get; set; }
    public float BOPSPlusScore { get; set; }
    public float BROBAScore { get; set; }
    public float BRBatPlusScore { get; set; }
    public float BTBScore { get; set; }
    public float BGIDPScore { get; set; }
    public float BHBPScore { get; set; }
    public float BSFScore { get; set; }
    public float BIBBScore { get; set; }
    public float BWARPerDollarScore { get; set; }
    public float BHPerDollarScore { get; set; }
    public float BHRPerDollarScore { get; set; }
    public float BDoublesPerDollarScore { get; set; }
    public float BTriplesPerDollarScore { get; set; }
    public float BSBPerDollarScore { get; set; }
    public float BBBPerDollarScore { get; set; }
    public float BTBPerDollarScore { get; set; }
    public float BGamesPerDollarScore { get; set; }
    public float BOPSPlusPerDollarScore { get; set; }

    public BatterStats(string name, string year, Dictionary<string, object> playerYear) 
    {
        this.BWARPerDollar = (float)playerYear["b_war_per_dollar"];
        this.BHPerDollar = (float)playerYear["b_h_per_dollar"];
        this.BHRPerDollar = (float)playerYear["b_hr_per_dollar"];
        this.BDoublesPerDollar = (float)playerYear["b_doubles_per_dollar"];
        this.BTriplesPerDollar = (float)playerYear["b_triples_per_dollar"];
        this.BSBPerDollar = (float)playerYear["b_sb_per_dollar"];
        this.BBBPerDollar = (float)playerYear["b_bb_per_dollar"];
        this.BTBPerDollar = (float)playerYear["b_tb_per_dollar"];
        this.BGamesPerDollar = (float)playerYear["b_games_per_dollar"];
        this.OPSPlusPerDollar = (float)playerYear["ops_plus_per_dollar"];

        this.BBattingAvgScore = (float)playerYear["b_batting_avg_score"];
        this.BOnbasePercentageScrore = (float)playerYear["b_onbase_perc_score"];
        this.BSluggingPercentageScore = (float)playerYear["b_sluggin_perc_score"];
        this.BOPSScore = (float)playerYear["b_on_base_plus_sluggin_score"];
        this.BOPSPlusScore = (float)playerYear["b_on_base_plus_sluggin_plus_score"];
        this.BROBAScore = (float)playerYear["b_roba_score"];
        this.BRBatPlusScore = (float)playerYear["b_rbat_plus_score"];
        this.BTBScore = (float)playerYear["b_tb_score"];
        this.BGIDPScore = (float)playerYear["b_gidp_score"];
        this.BHBPScore = (float)playerYear["b_hbp_score"];
        this.BSFScore = (float)playerYear["b_sf_score"];
        this.BIBBScore = (float)playerYear["b_ibb_score"];
        this.BWARPerDollarScore = (float)playerYear["b_war_per_dollar_score"];
        this.BHPerDollarScore = (float)playerYear["b_h_per_dollar_score"];
        this.BHRPerDollarScore = (float)playerYear["b_hr_per_dollar_score"];
        this.BDoublesPerDollarScore = (float)playerYear["b_doubles_per_dollar_score"];
        this.BTriplesPerDollarScore = (float)playerYear["b_triples_per_dollar_score"];
        this.BSBPerDollarScore = (float)playerYear["b_sb_per_dollar_score"];
        this.BBBPerDollarScore = (float)playerYear["b_bb_per_dollar_score"];
        this.BTBPerDollarScore = (float)playerYear["b_tb_per_dollar_score"];
        this.BGamesPerDollarScore = (float)playerYear["b_games_per_dollar_score"];
        this.BOPSPlusPerDollarScore = (float)playerYear["ops_plus_per_dollar_score"];
        
        // Default properties
        this.Name = name;
        this.Year = year;
        this.Position = "batting";
        this.Age = (int)playerYear["age"];
        this.TeamNameAbbr = (string)playerYear["team_name_abbr"];
        this.SalaryInfo = (double)playerYear["salary_info"];

        this.PlayerYear = playerYear;
    } 

    
}

public class PitcherStats : PlayerStats 
{
    float PWARPerDollar { get; set; }
    float PGPerDollar { get; set; }
    float PWPerDollar { get; set; }
    float PIPPerDollar { get; set; }
    float PSOPerDollar { get; set; }
    float PSOPerNinePerDollar { get; set; }
    float PERAPlusPerNinePerDollar { get; set; }
    float PWARScore { get; set; }
    float PWScore { get; set; }
    float PWinLossPercentageScore { get; set; }
    float PERAScore { get; set; }
    float PGScore { get; set; }
    float PCGScore { get; set; }
    float PIPScore { get; set; }
    float PERAPlusScore { get; set; }
    float PFIPScore { get; set; }
    float PWHIPScore { get; set; }
    float PHPerNineScore { get; set; }
    float PHRPerNineScore { get; set; }
    float PBBerNineScore { get; set; }
    float PSOPerNineScore { get; set; }
    float PSOPerBBScore { get; set; }
    float PGPerDollarScore { get; set; }
    float PWARPerDollarScore { get; set; }
    float PWPerDollarScore { get; set; }
    float PIPPerDollarScore { get; set; }
    float PSOPerDollarScore { get; set; }
    float PSOPerNinePerDollarScore { get; set; }
    float PERAPlusPlusPerDollarScore { get; set; }
    public PitcherStats(string name, string year, Dictionary<string, object> playerYear) 
    {
        this.PWARPerDollar = (float)playerYear["p_war_per_dollar"];
        this.PGPerDollar = (float)playerYear["p_g_per_dollar"];
        this.PWPerDollar = (float)playerYear["p_w_per_dollar"];
        this.PIPPerDollar = (float)playerYear["p_ip_per_dollar"];
        this.PSOPerDollar = (float)playerYear["p_so_per_dollar"];
        this.PSOPerNinePerDollar = (float)playerYear["p_so_per_nine_per_dollar"];
        this.PERAPlusPerNinePerDollar = (float)playerYear["p_earned_run_avg_plus_per_dollar"];
        this.PWARScore = (float)playerYear["p_war_score"];
        this.PWScore = (float)playerYear["p_w_score"];
        this.PWinLossPercentageScore = (float)playerYear["p_win_loss_perc_score"];
        this.PERAScore = (float)playerYear["p_earned_run_avg_score"];
        this.PGScore = (float)playerYear["p_g_score"];
        this.PCGScore = (float)playerYear["p_cg_score"];
        this.PIPScore = (float)playerYear["p_ip_score"];
        this.PERAPlusScore = (float)playerYear["p_earned_run_avg_plus_score"];
        this.PFIPScore = (float)playerYear["p_fip_score"];
        this.PWHIPScore = (float)playerYear["p_whip_score"];
        this.PHPerNineScore = (float)playerYear["p_hits_per_nine_score"];
        this.PHRPerNineScore = (float)playerYear["p_hr_per_nine_score"];
        this.PBBerNineScore = (float)playerYear["p_bb_per_nine_score"];
        this.PSOPerNineScore = (float)playerYear["p_so_per_nine_score"];
        this.PSOPerBBScore = (float)playerYear["p_strikeouts_per_base_on_balls_score"];
        this.PGPerDollarScore = (float)playerYear["p_hits_per_nine_score"];
        this.PWARPerDollarScore = (float)playerYear["p_war_per_dollar_score"];
        this.PWPerDollarScore = (float)playerYear["p_w_per_dollar_score"];
        this.PIPPerDollarScore = (float)playerYear["p_ip_per_dollar_score"];
        this.PSOPerDollarScore = (float)playerYear["p_so_per_dollar_score"];
        this.PSOPerNinePerDollarScore = (float)playerYear["p_so_per_nine_per_dollar_score"];
        this.PERAPlusPlusPerDollarScore = (float)playerYear["p_earned_run_avg_plus_per_dollar_score"];

        // Default properties
        this.Name = name;
        this.Year = year;
        this.Position = "pitching";
        this.Age = (int)playerYear["age"];
        this.TeamNameAbbr = (string)playerYear["team_name_abbr"];
        this.SalaryInfo = (double)playerYear["salary_info"];

        this.PlayerYear = playerYear;


    }

    
}

/*
"ConnectionStrings": {
    "DefaultConnection": "Server=YOUR_SERVER;Database=YOUR_DB;User Id=YOUR_USER;Password=YOUR_PASSWORD;TrustServerCertificate=True;"
  }

*/