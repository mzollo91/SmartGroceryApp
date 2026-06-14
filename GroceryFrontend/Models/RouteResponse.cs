public class RouteResponse
{
    // Use standard C# naming. The .NET JSON deserializer automatically handles camelCase from Python by defualt
    // in modern .NET.

    public string StartLocation { get; set; } = string.Empty;
    public string EndLocation { get; set; } = string.Empty;
    public List<string> Stops { get; set; } = new();
    public double TotalDistanceMiles { get; set; }
}