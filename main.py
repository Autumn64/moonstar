import json
import time
import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
import random
from random import randint
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
from discord.ext.commands import has_permissions
from itertools import cycle
from discord.ui import Select, View, Button
import datetime
import variables
import unidecode
from lxml import etree
from discord import Option
import bolaocho
from linereader import copen
import os
from math import sqrt
import csv

config: dict
"""reddit = asyncpraw.Reddit(client_id='ID',
                  client_secret='SECRET',
                  user_agent='AGENT')"""

with open ("config.json", "r") as f:
  config = json.load(f)

os.environ['TZ'] = 'America/Mexico_City'
time.tzset()
intents = discord.Intents.all()
moon = commands.Bot(intents=intents)
translator = Translator()

@moon.event
async def on_ready():
    ställd: bool = False
    print(" Copyright (c) 2023, Mónica Gómez (Autumn64)\n Licensed under BSD-3-Clause license. More information at https://opensource.org/license/BSD-3-clause/.")
    print(f'\n Logged in as {moon.user} at {datetime.datetime.now()}')
    print('\n')
    while True:
      time: int = int(datetime.datetime.now().strftime("%S"))
      if time >= 0 and time <= 30:
        if ställd == False:
          await moon.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=datetime.datetime.now().strftime("%Y.%m.%d %H:%M") + " CST"))
          ställd = True
      elif time >= 31 and time <= 60:
        if ställd == True:
          await moon.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Type / to see available commands!"))
          ställd = False
      await asyncio.sleep(1)

@moon.slash_command(name="translate", description="Translate from and to any language! To see available languages, type /languages")
async def translate(ctx, message: str, language: str = ''):
    await ctx.defer()
    async with ctx.typing():
      await asyncio.sleep(1)
    author: str = ctx.author.name
    msg: list = message.split("/")
    if "discord.com" in msg:
      melding = await ctx.fetch_message(int(msg[6]))
      message: str = melding.content
      author: str = melding.author.name
    if language == "":
        language = 'en'
    try:
      for key,value in variables.LANGUAGES.items():
        if language.lower() == value.lower():
          language = key
      if language.lower() == "chinese":
        language = 'zh-cn'
      elif language.lower() == "simplified chinese":
        language = 'zh-cn'
      elif language.lower() == "traditional chinese":
        language = 'zh-tw'
      for key,value in variables.LANGUAGESSP.items():
        value = unidecode.unidecode(value)
        language = unidecode.unidecode(language)
        if language.lower() == value.lower():
          language = key
      if language.lower() == "chino":
        language = 'zh-cn'
      elif language.lower() == "chino simplificado":
        language = 'zh-cn'
      elif language.lower() == "chino tradicional":
        language = 'zh-tw'
      else:
        translation = translator.translate(message, dest=language)
        traduccion: str = f"{translation.text}"
        idioma: str = f"{translation.src}"
        embed = discord.Embed(title="Translation from " + variables.LANGUAGES[idioma] + " to " + variables.LANGUAGES[language] + ":",
                              color=discord.Colour.random(),
                              url="https://translate.google.com/?sl=auto&tl=" + language + "&text="+ message.replace(" ", "%20")
        )
        embed.add_field(name=author + " wrote:", value=message, inline=False)
        embed.add_field(name="Which translates to:", value=traduccion, inline=False)
        embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/web-store-crayons-volume-1/256/Language-512.png")
        await ctx.respond(embed=embed)
    except Exception as e:
      if str(e) == "invalid destination language":
        await ctx.respond("Sorry, I can't speak `" + language +"`. Write /languages to see all available languages.", ephemeral=True)
      else:
        await ctx.respond("Error: `" + str(e) + "`. This incident will be reported.", ephemeral=True)
        with open('errors.rld', 'a') as file:
          file.write(str(datetime.datetime.now()) + " " + str(e) + ". Command used: " + "/translate " + message + " " + language)

@moon.slash_command(name="languages", description="Shows available languages for translation.")
async def languages(ctx):
  res: str = ""
  for values in variables.LANGUAGES.values():
    res = res + "\n" + values
  embed = discord.Embed(title="Available languages",
                        description=res, 
                        color=discord.Colour.random())
  await ctx.respond(embed=embed, ephemeral=True)
    
@moon.slash_command(name="ping" ,description="Shows bot's latency.")
async def ping(ctx):
  p: int = int(moon.latency * 1000)
  await ctx.respond("Pong! Ping is " + str(p) + " ms")

@moon.slash_command(name="avatar", description="Shows the avatar from the specified user.")
async def avatar(ctx, member: discord.Member = ''):
    await ctx.defer()
    if member != "":
      if member.id == config["autumn_id"]:
        await ctx.respond("No, not she :3", ephemeral=True)
      else:
        usuario = await moon.fetch_user(member.id)
        embed = discord.Embed(title=usuario.name + "'s Avatar", 
                              url=usuario.avatar,
                              color=discord.Colour.random())
        embed.set_image(url=usuario.avatar)
        embed.set_footer(text=f"Requested by: {ctx.author.name}")
        await ctx.respond(embed=embed)
    else:
      embed = discord.Embed(title=ctx.author.name + "'s Avatar",
                            url=ctx.author.avatar,
                            color=discord.Colour.random())
                #username = user.name
      embed.set_image(url=ctx.author.avatar)
      async with ctx.typing():
        await asyncio.sleep(1)
      await ctx.respond(embed=embed)

@moon.slash_command(name="pic", description="Search any picture from the internet!")
async def pic(ctx, picture: str):
  try:
    await ctx.defer()
    resp = requests.get("https://www.bing.com/images/search?q=" + picture.replace(" ", "+"))
    soup = BeautifulSoup(resp.text, 'lxml')
    resimg: list = []
    for i in soup.find_all('a', {"class":"iusc"}):
      resimg.append(i['m'])
    res: list = random.sample(resimg, len(resimg))
    res = random.sample(res, len(res))
    dataa: str = random.choice(res)
    u: list = str(dataa).split('"murl":"')
    uu: list = str(u[1]).split('",')
    embed = discord.Embed(title="Picture finder: " + picture, 
                      url="https://www.bing.com/images/search?q=" + picture.replace(" ", "+"),
                      color=discord.Colour.random())
    embed.set_image(url=uu[0])
    embed.set_footer(text=f"Requested by: {ctx.author.name}")
    await ctx.respond(embed=embed)
  except IndexError:
    await ctx.respond("I couldn't find anything for `" + picture + "`. Try again or use different keywords.", ephemeral=True)

@moon.slash_command(name="ball", description="Question game.")
async def ball(ctx, question: str):
  respuestas: list = bolaocho.responses
  respuestas = random.sample(respuestas, len(respuestas))
  respuestas = random.sample(respuestas, len(respuestas))
  response: str = random.choice(respuestas)
  embed = discord.Embed(title=":8ball: MoonByul 8ball",
                        color=discord.Colour.random())
  embed.add_field(name=f":question: {ctx.author.name} asks:",
                  value=question,
                  inline=False)
  embed.add_field(name=":100: MoonByul answers:",
                  value=response,
                  inline=False)
  await ctx.respond(embed=embed)

@moon.slash_command(name="pride", description="Proud of who we are!")
async def pride(ctx):
  urls: list = random.sample(variables.lgbtqplus, len(variables.lgbtqplus))
  urls = random.sample(urls, len(urls))
  url: str = random.choice(urls)
  embed = discord.Embed(title="Pride", 
                    color=discord.Colour.random())
  embed.set_image(url=url)
  await ctx.respond(embed=embed, ephemeral=True)

"""@moon.slash_command(name="meme", description="Send a random meme!")
async def meme(ctx):
    await ctx.defer()
    imgs: list = []
    subrdd: list = ["dankmemes", "memes", "terriblefacebookmemes", "MemesESP", "MemesEspanol"]
    subrdd = random.sample(subrdd, len(subrdd))
    subr: str = random.choice(subrdd)
    memes = await reddit.subreddit(subr)
    async for submission in memes.hot(limit=100):
      imgs.append(submission.url)
    imgs = random.sample(imgs, len(imgs))
    imgs = random.sample(imgs, len(imgs))
    url: str = random.choice(imgs)
    await ctx.respond("Meme from r/" + subr + "\n" + url)"""

@moon.slash_command(name="hug", description="Hug your friends!")
async def hug(ctx, member: discord.Member = ""):
  if member != "" and member != ctx.author.mention:
    if member.id == config["bot_id"]:
      async with ctx.typing():
          await asyncio.sleep(1)
      await ctx.respond(ctx.author.mention + " thank you! <3.")
    else:
      huggs: list = random.sample(variables.hugs, len(variables.hugs))
      huggs = random.sample(huggs, len(huggs))
      pic: str = random.choice(huggs)
      nh: int = hugcsv(member.id)
      embed = discord.Embed(color=discord.Colour.random())
      embed.set_footer(text=member.name + " has been hugged " + str(nh) + " times!")
      embed.set_image(url=pic)
      async with ctx.typing():
          await asyncio.sleep(1)
      await ctx.respond(ctx.author.mention + " has hugged " + member.mention + "!", embed=embed)   
  else:
    async with ctx.typing():
      await asyncio.sleep(1)
    await ctx.respond(ctx.author.mention + " has hugged themselves!")

def hugcsv(memberr) -> int:
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

@moon.slash_command(name="cry", description="Sometimes it's okay to cry and vent about your feelings :( <3")
async def cry(ctx, reason: str = ""):
  cryy: list = random.sample(variables.cryings, len(variables.cryings))
  cryy = random.sample(cryy, len(cryy))
  pic: str = random.choice(cryy)
  embed = discord.Embed(description=ctx.author.mention + " is crying! 😭", 
                        color=discord.Colour.random())
  embed.set_image(url=pic)
  async with ctx.typing():
    await asyncio.sleep(1)
  await ctx.respond(embed=embed)
  if reason != "":
      user = await moon.fetch_user(ctx.author.id)
      huggs: list = random.sample(variables.hugs, len(variables.hugs))
      huggs = random.sample(huggs, len(huggs))
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

@moon.slash_command(name="caramelldansen", description="Caramelldansen!")
async def caramelldansen(ctx):
  dansen: list = random.sample(variables.caramell, len(variables.caramell))
  dansen = random.sample(dansen, len(dansen))
  pic: str = random.choice(dansen)
  roll: list = ["https://youtu.be/xMHJGd3wwZk", "https://youtu.be/78ngmG_-Yck"]
  roll = random.sample(roll, len(roll))
  rick: str = random.choice(roll)
  embed = discord.Embed(title="Caramelldansen", 
                        description="Dansa med oss, klappa era händer\ngör som vi gör, ta några steg åt vänster.\nLyssna och lär, missa inte chansen\n_**nu är vi här med caramelldansen**_ ^^.\n\n _oa oa oa oooa_",
                        url=rick,
                        color=discord.Colour.random())
  embed.set_image(url=pic)
  embed.set_footer(text=ctx.author.name + " has gained Swedish citizenship! /j")
  async with ctx.typing():
    await asyncio.sleep(1)
  await ctx.respond(embed=embed)

@moon.slash_command(name="math", description="Do simple arithmetic operations!")
async def math(ctx, expression: str):
  try:
    expresion = expression.replace('x', '*').replace('÷', '/').replace('^', '**')
    result = eval(expresion)
    embed = discord.Embed(title="MOONSTAR Math",
                          color = discord.Colour.random())
    embed.set_thumbnail(url="https://webstockreview.net/images/clipart-math-icon-10.png")
    embed.add_field(name=f"{ctx.author.name} entered:", value="```python\n" + expression + "```", inline=False)
    embed.add_field(name="The result is:", value="```python\n" + str(result) + "```", inline=False)
    await ctx.respond(embed=embed)
  except:
    await ctx.respond("Sorry, I can only solve simple arithmetical operations. If you're trying to solve a square root, please use `sqrt()` instead of `√`", ephemeral = True)

@moon.slash_command(name="kick", description="Kick a specified member.")
async def kick(ctx, member: discord.Member, reason=None):
  if not ctx.author.guild_permissions.kick_members:
    await ctx.respond("You don't have enough permissions to do that!", ephemeral = True)
  else:
    await member.kick(reason=reason)
    if reason == None:
      await ctx.respond("** " + member.name + "** has been kicked for no reason.")
    else:
      await ctx.respond("** " + member.name + "** has been kicked for the reason: `" + reason + "`.")

@moon.slash_command(name="ban", description="Kick a specified member.")
async def ban(ctx, member: discord.Member, reason=None):
  if not ctx.author.guild_permissions.ban_members:
    await ctx.respond("You don't have enough permissions to do that!", ephemeral = True)
  else:
    await member.ban(reason=reason)
    if reason == None:
      await ctx.respond("** " + member.name + "** has been banned for no reason.")
    else:
      await ctx.respond("** " + member.name + "** has been banned for the reason: `" + reason + "`.")

@moon.slash_command(name="confess", description="Confess your secrets anonymously!")
async def confess(ctx, confession: str):
  embed = discord.Embed(title="Confession: ",
                        description="_" + confession + "_",
                        colour=discord.Colour.random())
  embed.set_footer(text="Anonymous confessions from " + ctx.guild.name + " server.")
  await ctx.respond("_ _")
  await ctx.delete()
  await ctx.send(embed=embed)

@moon.slash_command(name="about", description="About MOONSTAR")
async def about(ctx):
  await ctx.respond("""# MOONSTAR\n
## An open-source slash commands-supporting bot for Discord.\n
Copyright (c) 2023, Mónica Gómez (Autumn64)
Licensed under BSD-3-Clause license. More information at https://codeberg.org/Autumn64/moonstar.""")  

if __name__ == "__main__":
  moon.run(config["token"])