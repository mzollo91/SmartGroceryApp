public class RouteResponse
{
    // Use standard C# naming. The .NET JSON deserializer automatically handles camelCase from Python by defualt.
    // Important to note that a mismatch in what the C# model expects and what the backend provides does not throw an exception. It will fail silently.
    // in modern .NET.

    public int StartLocation { get; set; }
    public int EndLocation { get; set; }
    public List<int> Path { get; set; } = new();
    public double? TotalDistanceFeet { get; set; }
    public Dictionary<int, string> Stores { get; set; } = new();
    public Dictionary<int, string> Aisle { get; set; } = new();

}