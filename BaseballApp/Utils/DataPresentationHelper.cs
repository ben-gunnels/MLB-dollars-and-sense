

/*
    Map data value to a color gradient along the Green and Red axes.
    The value for green and red goes between 0 and 255.
    If a player has a minimum score of -2.0 the color should be completely red.
    The score should map to the function y = -(255/4) + (-510/4) + 255 = 255 for red.
    If a player has a maximum score of 2.0 the color should be completely green.
    The score should map to the function y = (4/255) + (-510/4) + 255 = 255 for green. 
    Notice green has positive slope of red.
*/
using MathNet.Numerics.Distributions;

public static class DataPresentationHelper 
{
    private static double maxScore = 2.0f;
    private static double maxColor = 255.0f;
    private static double slopeRed = -(maxColor / (2*maxScore));
    private static double slopeGreen = (maxColor / (2*maxScore));
    private static double yInt = -((2*maxColor) / (2*maxScore)) + maxColor;

    public static double[] ColorData(double data) 
    {
        double red, green;
        data = CapScore(data);

        red = (slopeRed * data) +  yInt;
        green = (slopeGreen * data) + yInt;
        double[] redAndGreenValues = [red, green];
        return redAndGreenValues;

    }

    public static double CapScore(double score) {
        score = Math.Min(score, maxScore); // Cap maximum score at 2.0
        score = Math.Max(score, -maxScore); // Cap minimum score at -2.0
        return score;
    }

    public static double ZScoreToPercentile(double z)
    {
        return Normal.CDF(0, 1, z); // Standard normal CDF
    }

    public static string CapitalizeName(string name)
    {
        if (string.IsNullOrWhiteSpace(name)) return string.Empty;

        return string.Join(" ", name.Split(' ', StringSplitOptions.RemoveEmptyEntries)
            .Select(word => word.Length > 1 ? char.ToUpper(word[0]) + word.Substring(1).ToLower() : word.ToUpper()));
    }


}