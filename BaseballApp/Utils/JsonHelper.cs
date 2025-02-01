using System.Text.Json;

public static class JsonHelper
{
    public static float GetFloatFromJsonElement(object value)
    {
        if (value is JsonElement jsonElement)
        {
            if (jsonElement.TryGetSingle(out var floatValue))
            {
                return floatValue;
            }
            return 0f;
        }
        return 0f;
    }
}