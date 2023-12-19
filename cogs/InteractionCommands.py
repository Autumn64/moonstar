import json
import csv
import random
import asyncio
import discord
import variables
from discord.ext import commands

class InteractionCommands(commands.Cog):
    def __init__(self, moon, config):
        self.moon = moon
        self.config = config

    @discord.slash_command(name="avatar", description="Shows the avatar from the specified user.")
    async def avatar(self, ctx, member: discord.Member = ''):
        await ctx.defer()
        if member != "":
            if member.id == self.config["owner_id"]:
                await ctx.respond("No, not she :3", ephemeral=True)
                return
            usuario = await self.moon.fetch_user(member.id)
            embed = discord.Embed(title=usuario.name + "'s Avatar", 
                                url=usuario.avatar,
                                color=discord.Colour.random())
            embed.set_image(url=usuario.avatar)
            embed.set_footer(text=f"Requested by: {ctx.author.name}")
        else:
            embed = discord.Embed(title=ctx.author.name + "'s Avatar",
                                    url=ctx.author.avatar,
                                    color=discord.Colour.random())
            embed.set_image(url=ctx.author.avatar)
        async with ctx.typing():
            await asyncio.sleep(1)
        await ctx.respond(embed=embed) #Don't repeat yourself

    @discord.slash_command(name="hug", description="Hug your friends!")
    async def hug(self, ctx, member: discord.Member = ""):
        if member == "" or member == ctx.author.mention:
            async with ctx.typing():
                await asyncio.sleep(1)
            await ctx.respond(f"{ctx.author.mention} has hugged themselves!")
            return

        if member.id == self.config["bot_id"]:
            async with ctx.typing():
                await asyncio.sleep(1)
            await ctx.respond(f"{ctx.author.mention} thank you! <3.")
            return

        huggs: list = random.sample(variables.hugs, len(variables.hugs)); huggs = random.sample(huggs, len(huggs))
        pic: str = random.choice(huggs)
        nh: int = self.hugcsv(member.id)
        embed = discord.Embed(color=discord.Colour.random())
        embed.set_footer(text=f"{member.name} has been hugged {nh} times!")
        embed.set_image(url=pic)
        async with ctx.typing():
            await asyncio.sleep(1)
        await ctx.respond(f"{ctx.author.mention} has hugged {member.mention} !", embed=embed)   
            

    def hugcsv(self, memberr) -> int:
        huglist: list = []
        count: int = 0
        with open ("hugscount.csv", "r+") as f:
            hugs = csv.reader(f)
            huglist.extend(hugs)
            for row in huglist:
                if str(memberr) in row:
                    row[1] = str(int(row[1]) + 1)
                    value: int = int(row[1])
                    count = 1
            if count == 0:
                huglist.append([memberr, 1])
                value: int = 1
        with open("hugscount.csv", "w+") as f:
            hugscsv = csv.writer(f, lineterminator='\n')
            hugscsv.writerows(huglist)
        return value

    @discord.slash_command(name="cry", description="Sometimes it's okay to cry and vent about your feelings :( <3")
    async def cry(self, ctx, reason: str = ""):
        cryy: list = random.sample(variables.cryings, len(variables.cryings)); cryy = random.sample(cryy, len(cryy))
        pic: str = random.choice(cryy)
        embed = discord.Embed(description=ctx.author.mention + " is crying! 😭", 
                                color=discord.Colour.random())
        embed.set_image(url=pic)
        async with ctx.typing():
            await asyncio.sleep(1)
        await ctx.respond(embed=embed)

        if reason != "":
            user = await self.moon.fetch_user(ctx.author.id)
            huggs: list = random.sample(variables.hugs, len(variables.hugs)); huggs = random.sample(huggs, len(huggs))
            pic: str = random.choice(huggs)
            embed = discord.Embed(title="Sending my hugs to you!", 
                                    color=discord.Colour.random())
            embed.set_image(url=pic)
            async with ctx.typing():
                await asyncio.sleep(1)
            try:
                await user.send("Keep it up! I hope everything gets better for you <3 Ily.", embed=embed)
            except:
                await ctx.respond(ctx.author.mention + " Keep it up! I hope everything gets better for you <3 Ily.", embed=embed, ephemeral=True)

def setup(moon):
    with open ("config.json", "r") as f:
        config = json.load(f)
    moon.add_cog(InteractionCommands(moon, config))