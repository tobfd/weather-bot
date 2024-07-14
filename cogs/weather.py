import os

import discord
import ezcord
import pyowm.commons.exceptions
from discord import Interaction
from discord.commands import option, slash_command
from dotenv import load_dotenv
from ezcord import codeblock
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.weatherapi25 import Weather as WeatherClass
from translate import Translator

load_dotenv()
API_KEY = os.getenv("KEY")
COLORS_BY_TEMP = {
    35: discord.Color.dark_red(),
    30: discord.Color.red(),
    25: discord.Color.dark_orange(),
    20: discord.Color.orange(),
    10: discord.Color.blue(),
    0: discord.Color.dark_blue(),
}

owm = OWM(API_KEY)
mgr = owm.weather_manager()
CRAD = "°C"

translator = Translator(to_lang="de")


async def get_view(
    city: str,
    sunrise: str,
    sunset: str,
    forecast: bool = False,
    original_weather: WeatherClass | None = None,
) -> discord.ui.View:
    if forecast:
        label = "Jetzt"
        style = discord.ButtonStyle.secondary
    else:
        label = "Nächste 3 Stunden"
        style = discord.ButtonStyle.primary
    view = discord.ui.View(timeout=None, disable_on_timeout=True)
    view.add_item(
        ForecastButton(city, label, sunrise, sunset, style=style, weather=original_weather)
    )
    return view


async def get_weather_embed(
    weather: WeatherClass, city: str, sunrise: str, sunset: str, three_hours: bool = False
) -> discord.Embed:
    temperaturen = weather.temperature("celsius")
    temp = round(int(temperaturen.get("temp")))
    color = discord.Color.orange()
    for temperature in COLORS_BY_TEMP.keys():
        if temp >= temperature:
            color = COLORS_BY_TEMP[temperature]
            break
    embed = discord.Embed(
        title=f"🌤️ Wetter in {city.title()}{" in 3 Stunden" if three_hours else ""}", color=color
    )
    embed.add_field(name="🌡️ Temperatur", value=codeblock(str(temp) + CRAD))
    embed.add_field(
        name="🌡️ Fühlt sich an wie",
        value=codeblock(str(round(int(temperaturen.get("feels_like")))) + CRAD),
    )
    embed.add_field(name="", value="")  # Kategorisierung
    embed.add_field(name="", value="", inline=False)  # Abstand von Zeile 1 bis Zeile 2
    embed.add_field(name="💧 Luftfeuchtigkeit", value=codeblock(str(weather.humidity) + "%"))
    embed.add_field(
        name="🍃 Wind Geschwindigkeit",
        value=codeblock(str(round(int(weather.wind("km_hour").get("speed")))) + " Km/h"),
    )
    embed.add_field(name="", value="")  # Kategorisierung
    embed.add_field(name="", value="", inline=False)  # Abstand von Zeile 2 bis Zeile 3
    embed.add_field(name="🌄 Sonnenaufgang", value=sunrise)
    embed.add_field(name="🌇 Sonnenuntergang", value=sunset)
    embed.add_field(name="", value="")  # Kategorisierung
    embed.set_footer(
        text=translator.translate(weather.detailed_status), icon_url=weather.weather_icon_url()
    )
    embed.set_thumbnail(url=weather.weather_icon_url())
    return embed


class Weather(
    ezcord.Cog,
    group="Weather",
    emoji="🌤️",
    description="Mit diesen Commands wirst du immer übers Wetter informiert.",
):
    def __init__(self, bot: ezcord.Bot):
        self.bot = bot

    @slash_command(description="Hier erhältst du alle Informationen über das Wetter")
    @option(name="city", description="Von welcher Stadt möchtest du das Wetter wissen?")
    async def weather(self, ctx: ezcord.EzContext, city: str):
        try:
            observation = mgr.weather_at_place(city)
        except pyowm.commons.exceptions.NotFoundError:
            return await ctx.error(f"Die Stadt **{city}** konnte nicht gefunden werden.")
        weather: WeatherClass = observation.weather
        sunrise = discord.utils.format_dt(weather.sunrise_time(timeformat="date"), "T")
        sunset = discord.utils.format_dt(weather.sunset_time(timeformat="date"), "T")
        embed = await get_weather_embed(weather, city, sunrise, sunset)
        view = await get_view(city, sunrise, sunset, original_weather=weather)
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Weather(bot))


class ForecastButton(discord.ui.Button):
    def __init__(
        self,
        city: str,
        label: str,
        sunrise: str,
        sunset: str,
        weather: WeatherClass,
        style: discord.ButtonStyle | None = discord.ButtonStyle.primary,
    ):
        super().__init__(label=label, style=style, custom_id="forecast_button")
        self.city = city
        self.sunrise = sunrise
        self.sunset = sunset
        self.weather = weather

    async def callback(self, interaction: Interaction):
        if self.style == discord.ButtonStyle.secondary:
            weather = self.weather
            three_hours = False
        else:
            prognose = mgr.forecast_at_place(self.city, "3h")
            response: WeatherClass = prognose.get_weather_at(timestamps.next_three_hours())
            weather = response
            three_hours = True
        embed = await get_weather_embed(
            weather, self.city, sunrise=self.sunrise, sunset=self.sunset, three_hours=three_hours
        )
        view = await get_view(
            self.city,
            self.sunrise,
            self.sunset,
            forecast=three_hours,
            original_weather=self.weather,
        )
        await interaction.edit(embed=embed, view=view)
