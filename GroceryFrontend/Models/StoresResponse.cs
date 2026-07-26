// This DTO is for the top level wrapper in the JSON response for an API call getting a store(s) object.
public class StoresResponse
{
    public List<StoreDTO> Stores { get; set; } = new();
}