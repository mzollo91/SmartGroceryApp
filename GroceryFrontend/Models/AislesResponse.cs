// This DTO is for the top level wrapper in the JSON response for an API call getting an aisle(s) object.
public class AislesResponse
{
    public List<AisleDTO> Aisles { get; set; } = new();
}