public class RouteResponse
{
    // Use standard C# naming. The .NET JSON deserializer automatically handles camelCase from Python by defualt
    // in modern .NET.

    public int StartLocationId { get; set; }
    public int EndLocationId { get; set; }
    public List<int> StopIds { get; set; } = new();
    public double TotalDistanceMiles { get; set; }
}