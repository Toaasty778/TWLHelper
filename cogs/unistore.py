import discord
import requests

from discord.ext import commands
from utils.utils import web_name


class UniStore(commands.Cog):
    """Commands related to UniStore searching"""

    def __init__(self, bot):
        self.bot = bot

    async def udb_embed(self, ctx, title, app=""):
        unistore = requests.get("https://raw.githubusercontent.com/Universal-Team/db/master/docs/data/full.json").json()
        embed = discord.Embed(title=title)
        embed.set_author(name="Universal-Team")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/49733679?s=400&v=4")
        embed.description = "A database of DS and 3DS homebrew"
        embed.url = "https://db.universal-team.net/"
        if app != "":
            for appid in unistore:
                if appid["title"].lower().find(app.lower()) != -1:
                    embed.set_author(name=appid["author"])
                    embed.set_thumbnail(url=appid["icon"])
                    embed.title = appid["title"]
                    embed.description = appid["description"]
                    embed.url += appid["systems"][0].lower() + "/" + web_name(appid["title"])
                    await ctx.send(embed=embed)
                    return
            await ctx.send("App cannot be found. Please try again.")
            return
        await ctx.send(embed=embed)

    async def skin_embed(self, ctx, title, extension, skin=""):
        unistore = requests.get("https://raw.githubusercontent.com/DS-Homebrew/twlmenu-extras/master/docs/data/full.json").json()
        embed = discord.Embed(title=title)
        embed.set_author(name="DS-Homebrew Wiki")
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/46971470?s=400&v=4")
        if extension == "Unlaunch":
            embed.description = "Custom backgrounds for Unlaunch"
        elif extension == "Nintendo DSi":
            embed.description = "Custom skins for TWiLight Menu++'s DSi Menu theme"
        elif extension == "R4 Original":
            embed.description = "Custom skins for TWiLight Menu++'s R4 Original Menu theme"
        elif extension == "Nintendo 3DS":
            embed.description = "Custom skins for TWiLight Menu++'s 3DS Menu theme"
        embed.url = "https://skins.ds-homebrew.com/" + web_name(extension) + "/"
        if skin != "":
            for skinid in unistore:
                if skinid["title"].lower().find(skin.lower()) != -1 and skinid["console"] == extension:
                    embed.set_author(name=skinid["author"])
                    embed.set_thumbnail(url=skinid["icon"])
                    embed.title = skinid["title"]
                    embed.description = skinid["description"]
                    embed.url += web_name(skinid["title"])
                    await ctx.send(embed=embed)
                    return
            await ctx.send("Skin '" + skin + "' cannot be found. Please try again.")
            return
        await ctx.send(embed=embed)

    @commands.command(aliases=["universaldb"])
    async def udb(self, ctx, app=""):
        await self.udb_embed(ctx, "Universal-DB", app)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def skins(self, ctx):
        """Links and/or information on installing apps"""
        await ctx.send_help(ctx.command)

    @skins.command(name="unlaunch")
    async def skin_unlaunch(self, ctx, skin=""):
        """Links to the Unlaunch skins page"""
        await self.skin_embed(ctx, "Unlaunch Backgrounds", "Unlaunch", skin)

    @skins.command(name="dsi", aliases=["dsimenu"])
    async def skin_dsimenu(self, ctx, skin=""):
        await self.skin_embed(ctx, "DSi Menu Skins", "Nintendo DSi", skin)

    @skins.command(name="3ds", aliases=["3dsmenu"])
    async def skin_3dsmenu(self, ctx, skin=""):
        await self.skin_embed(ctx, "3DS Menu Skins", "Nintendo 3DS", skin)

    @skins.command(name="r4", aliases=["r4theme"])
    async def skin_r4menu(self, ctx, skin=""):
        await self.skin_embed(ctx, "R4 Original Menu Skins", "R4 Original", skin)


def setup(bot):
    bot.add_cog(UniStore(bot))