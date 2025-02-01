using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json;

public class PlayerStats 
{
    [Key]
    public int Id { get; set; }  // Primary Key
    public string Name { get; set; }
    public string Year { get; set; }
    // public string Position { get; set; }
    // public int Age { get; set; }
    // public string TeamNameAbbr { get; set; }
    // public double SalaryInfo { get; set; }  
    // This will store the dictionary as a JSON string in the database
    public string PlayerYearJson { get; set; }

    [NotMapped]
    public Dictionary<string, object> PlayerYear
    {
        get
        {
            if (string.IsNullOrEmpty(PlayerYearJson))
                return null;
            return JsonSerializer.Deserialize<Dictionary<string, object>>(PlayerYearJson);
        }
        set
        {
            PlayerYearJson = JsonSerializer.Serialize(value);
        }
    }
}