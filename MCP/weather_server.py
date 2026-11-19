from mcp.server.fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP(
    "Weather Server",
    host="127.0.0.1",
    port=8000
)


@mcp.tool()
async def get_weather(city: str) -> dict:
    """
    Get the current weather information for a specified city.
    Input: city name, such as Lahore or London.
    Returns: temperature, humidity, wind speed and weather conditions.
    """

    async with httpx.AsyncClient(timeout=20.0) as client:

        # Step 1: Find city coordinates
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {"error": f"City not found: {city}"}

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get current weather
        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            }
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        return {
            "city": location["name"],
            "country": location.get("country"),
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "precipitation": current["precipitation"],
            "weather_code": current["weather_code"],
            "time": current["time"],
            "timezone": weather_data["timezone"]
        }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
