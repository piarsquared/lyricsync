# lyricsync by piarsquared 1/4/26
## Removes the cuteness stuff, professional bot version essentially.

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from lyrics_services import LyricsService

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def get_lyrics_pages(song: str, artist: str):
    result = await LyricsService.fetch_lyrics(song, artist)

    if not result:
        return None, None, None, f"Could not find lyrics for '{song}' by '{artist}'."

    lyrics_text = result.get("plainLyrics", "Instrumental")

    lines = lyrics_text.splitlines()
    pages = []
    buffer = ""

    for line in lines:
        if len(buffer) + len(line) + 1 > 1900:
            pages.append(buffer.strip())
            buffer = line + "\n"
        else:
            buffer += line + "\n"

    if buffer:
        pages.append(buffer.strip())

    title = f"{result.get('name', song)} - {result.get('artistName', artist)}"
    source = result.get("source", "lrclib.net")

    return pages, title, source, None

@bot.tree.command(name="lyrics", description="Display lyrics for a song")
async def lyrics_slash(interaction: discord.Interaction, song: str, artist: str):
    await interaction.response.defer()

    pages, title, source, error = await get_lyrics_pages(song, artist)

    if error:
        return await interaction.followup.send(error)

    view = LyricsView(pages, title, source)
    await interaction.followup.send(embed=view.create_embed(), view=view)

@bot.command(name="lyrics")
async def lyrics_prefix(ctx, song: str, artist: str):
    async with ctx.typing():
        pages, title, source, error = await get_lyrics_pages(song, artist)

        if error:
            return await ctx.send(error)

        view = LyricsView(pages, title, source)
        await ctx.send(embed=view.create_embed(), view=view)

class LyricsView(discord.ui.View):
    def __init__(self, pages, title, source):
        super().__init__(timeout=180)
        self.pages = pages
        self.title = title
        self.source = source
        self.current_page = 0

    def create_embed(self):
        embed = discord.Embed(
            title=self.title,
            description=self.pages[self.current_page],
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text=f"Page {self.current_page + 1}/{len(self.pages)} • Source: {self.source}"
        )

        return embed

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.create_embed())
        else:
            await interaction.response.send_message(
                "Already on the first page.", ephemeral=True
            )

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.create_embed())
        else:
            await interaction.response.send_message(
                "Already on the last page.", ephemeral=True
            )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="music"
        )
    )

bot.run(TOKEN)
