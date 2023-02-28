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
from bs4 import BeautifulSoup
import requests
from itertools import cycle
import datetime
import variables
import unidecode
from lxml import etree
from discord import Option
import bolaocho
from linereader import copen
import asyncpraw

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)
translator = Translator()
status = cycle(["Type / to see available commands!", datetime.date.today().strftime("%Y.%m.%d")])
reddit = asyncpraw.Reddit(client_id='ID',
                  client_secret='SECRET',
                  user_agent='AGENT')

@tasks.loop(seconds=60)
async def changeStatus():
  await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=next(status)))

@bot.event
async def on_ready():
    changeStatus.start()
    print(" 안녕하세요 여러분 문별이다")
    print('\n {0.user}으로서 봇이 성공적으로 로그인했습니다'.format(bot))
    print('\n')


@bot.slash_command(name="translate", description="Translate from and to any language! To see available languages, type /languages")
async def translate(ctx, message, language = ''):
    async with ctx.typing():
      await asyncio.sleep(1)
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
        traduccion = f"{translation.text}"
        idioma = f"{translation.src}"
        embed = discord.Embed(title="Translation from " + variables.LANGUAGES[idioma] + " to " + variables.LANGUAGES[language] + ":",
                              color=discord.Colour.random(),
                              url="https://translate.google.com/?sl=auto&tl=" + language + "&text="+ message.replace(" ", "%20")
        )
        embed.add_field(name=f"{ctx.author.name} wrote:", value=message, inline=False)
        embed.add_field(name="Which translates to:", value=traduccion, inline=False)
        embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/web-store-crayons-volume-1/256/Language-512.png")
        await ctx.respond(embed=embed)
    except Exception as e:
      if str(e) == "invalid destination language":
        await ctx.respond("Sorry, I can't speak `" + language +"`. Write /languages to see all available languages.", ephemeral=True)
      else:
        await ctx.respond("Error: `" + str(e) + "`. This incident will be reported.", ephemeral=True)
        with open('log.txt', 'a') as file:
          file.write(str(datetime.datetime.now()) + " " + str(e) + ". Command used: " + "/translate " + message + " " + language)

@bot.slash_command(name="languages", description="Shows available languages for translation.")
async def languages(ctx):
  res = ""
  for values in variables.LANGUAGES.values():
    res = res + "\n" + values
  embed = discord.Embed(title="Available languages",
                        description=res, 
                        color=discord.Colour.random())
  await ctx.respond(embed=embed, ephemeral=True)
    
@bot.slash_command(name="ping" ,description="Shows bot's latency.")
async def ping(ctx):
  p = int(bot.latency * 1000)
  await ctx.respond("Pong! Ping is " + str(p) + " ms")

@bot.slash_command(name="avatar", description="Shows the avatar from the specified user.")
async def avatar(ctx, member=''):
  await ctx.defer()
  async with ctx.typing():
    await asyncio.sleep(1)
  try:
    if member == "":
      persona = ctx.author.name
      pfp = str(ctx.author.avatar)
      nombre3 = persona + "'s Avatar"
      embed = discord.Embed(title=nombre3,
                            url=pfp,
                            color=discord.Colour.random())
                #username = user.name
      embed.set_image(url=pfp)
      await ctx.respond(embed=embed)
    else:
      miembro = []
      for letter in member:
        miembro.append(letter)
      del miembro[-1]
      del miembro[0]
      del miembro [0]
      mm = int(''.join(miembro))
      if mm == 1079060605194993715:
        await ctx.respond("No, not she :3", ephemeral=True)
      else:
          usuario = await bot.fetch_user(mm)
          persona = usuario.name
          nombre3 = persona + "'s Avatar"
          peticion = f"Requested by: {ctx.author.name}"
          pfp = str(usuario.avatar)
          embed = discord.Embed(title=nombre3,
                                url=pfp,
                                color=discord.Colour.random())
                  #username = user.name
          embed.set_image(url=pfp)
          embed.set_footer(text=peticion)
          await ctx.respond(embed=embed)
  except:
    persona = ctx.author.name
    pfp = str(ctx.author.avatar)
    nombre3 = persona + "'s Avatar"
    embed = discord.Embed(title=nombre3,
                          url=pfp,
                          color=discord.Colour.random())
                #username = user.name
    embed.set_image(url=pfp)
    await ctx.respond(embed=embed)   

@bot.slash_command(name="pic", description="Search any picture from the internet!")
async def pic(ctx, picture):
  try:
    await ctx.defer()
    resp = requests.get("https://www.bing.com/images/search?q=" + picture.replace(" ", "+"))
    soup = BeautifulSoup(resp.text, 'lxml')
    resimg = []
    for i in soup.find_all('img', {"class":"mimg rms_img"}):
      resimg.append(i['src'])
    res = random.sample(resimg, len(resimg))
    res = random.sample(res, len(res))
    url = random.choice(res)
    embed = discord.Embed(title="Picture finder: " + picture, 
                      url="https://www.bing.com/images/search?q=" + picture.replace(" ", "+"),
                      color=discord.Colour.random())
    embed.set_image(url=url)
    embed.set_footer(text=f"Requested by: {ctx.author.name}")
    await ctx.respond(embed=embed)
  except IndexError:
    await ctx.respond("I couldn't find anything for `" + picture + "`. Try again or use different keywords.", ephemeral=True)

@bot.slash_command(name="ball", description="Question game.")
async def ball(ctx, question):
  respuestas = bolaocho.responses
  respuestas = random.sample(respuestas, len(respuestas))
  respuestas = random.sample(respuestas, len(respuestas))
  response = random.choice(respuestas)
  embed = discord.Embed(title=":8ball: MoonByul 8ball",
                        color=discord.Colour.random())
  embed.add_field(name=f":question: {ctx.author.name} asks:",
                  value=question,
                  inline=False)
  embed.add_field(name=":100: MoonByul answers:",
                  value=response,
                  inline=False)
  await ctx.respond(embed=embed)

@bot.slash_command(name="pride", description="Proud of who we are!")
async def pride(ctx):
  urls = random.sample(variables.lgbtqplus, len(variables.lgbtqplus))
  urls = random.sample(urls, len(urls))
  url = random.choice(urls)
  embed = discord.Embed(title="Pride", 
                    color=discord.Colour.random())
  embed.set_image(url=url)
  await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="meme", description="Send a random meme!")
async def meme(ctx):
    await ctx.defer()
    imgs = []
    subrdd = ["dankmemes", "memes", "terriblefacebookmemes", "MemesESP", "MemesEspanol"]
    subrdd = random.sample(subrdd, len(subrdd))
    subr = random.choice(subrdd)
    memes = await reddit.subreddit(subr)
    async for submission in memes.hot(limit=100):
      imgs.append(submission.url)
    imgs = random.sample(imgs, len(imgs))
    imgs = random.sample(imgs, len(imgs))
    url = random.choice(imgs)
    await ctx.respond(url)

@bot.slash_command(name="hug", description="Hug your friends!")
async def hug(ctx, member = ""):
  if member != "" and member != ctx.author.mention:
    if member == "<@1079100634952909000>":
      async with ctx.typing():
          await asyncio.sleep(1)
      await ctx.respond(ctx.author.mention + " thank you! <3.")
    else:
      huggs = random.sample(variables.hugs, len(variables.hugs))
      huggs = random.sample(huggs, len(huggs))
      pic = random.choice(huggs)
      embed = discord.Embed(description= ctx.author.mention + " has hugged " + member + "!",
                            color=discord.Colour.random()
                            )
      embed.set_image(url=pic)
      async with ctx.typing():
          await asyncio.sleep(1)
      await ctx.respond(embed=embed)
  else:
    async with ctx.typing():
      await asyncio.sleep(1)
    await ctx.respond(ctx.author.mention + " has hugged themselves!")

@bot.slash_command(name="cry", description="Sometimes it's okay to cry and vent about your feelings :( <3")
async def cry(ctx, reason = ""):
  cryy = random.sample(variables.cryings, len(variables.cryings))
  cryy = random.sample(cryy, len(cryy))
  pic = random.choice(cryy)
  embed = discord.Embed(description=ctx.author.mention + " is crying! 😭", 
                        color=discord.Colour.random())
  embed.set_image(url=pic)
  async with ctx.typing():
    await asyncio.sleep(1)
  await ctx.respond(embed=embed)
  if reason != "":
      user = await bot.fetch_user(ctx.author.id)
      huggs = random.sample(variables.hugs, len(variables.hugs))
      huggs = random.sample(huggs, len(huggs))
      pic = random.choice(huggs)
      embed = discord.Embed(title="Sending my hugs to you!", 
                            color=discord.Colour.random())
      embed.set_image(url=pic)
      async with ctx.typing():
        await asyncio.sleep(1)
      try:
        await user.send("Keep it up! I hope everything gets better for you <3 Ily.", embed=embed)
      except:
        await ctx.respond(ctx.author.mention + " Keep it up! I hope everything gets better for you <3 Ily.", embed=embed, ephemeral=True)

@bot.slash_command(name="caramelldansen", description="Caramelldansen!")
async def caramelldansen(ctx):
  dansen = random.sample(variables.caramell, len(variables.caramell))
  dansen = random.sample(dansen, len(dansen))
  pic = random.choice(dansen)
  embed = discord.Embed(description="Dansa med oss, klappa era händer\ngör som vi gör, ta några steg åt vanster.\nLyssna och lär, missa inte chansen\n_**nu är vi här med caramelldansen**_ ^^.",
                        color=discord.Colour.random())
  embed.set_image(url=pic)
  embed.set_footer(text=ctx.author.name + " has gained Swedish citizenship! /j")
  async with ctx.typing():
    await asyncio.sleep(1)
  await ctx.respond(embed=embed)
  
bot.run("TOKEN")