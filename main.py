"""
With this commit, I end the work of 3 years of development of bots for Discord. From my first bot, called 'Thel Vadam, which I started in 2020,
to Citlalmina, which was an evolution of 'Thel Vadam and that I started developing in 2021, to Lagertha, an unreleased bot that was my first bot to
ever use a ctx environment instead of a on_message one, to Fatima, a bot I first created for a muslim friend from the Philippines, that after some time became my first bot to
benefit from the back then newly implemented slash command functionalities, until here. Until MOONSTAR. MOONSTAR is, by far, the most advanced bot I have ever created.
Not only I learnt a lot about stuff like web scraping, file manipulation and the way Python works in general, but I also was able to provide a wonderful
experience to those who used my bot and praised its capabilities that were rather unusual and also more complex on popular mainstream bots.
For some people my bot made their lives easier, for some others, my bot was a way they could find a bit of fun on their daily lives, while for others,
MOONSTAR served as their company, like a close friend that always was there for them and always helped them to get over their own problems and situations.
As for me, MOONSTAR was what made me feel sure about what I wanted to do in my future life; developing is my passion, and MOONSTAR made me see that's what
I want to earn a living from, because that's what makes me happy and what fills my life and gives a sense to it. Maybe I don't have the best syntax, maybe the bot
is not quite optimized and maybe the bot isn't on its best state possible, but it works. And it works flawlessly, at least for the users who appreciated my work.

Thank you so much for being a part of this story! I appreciate so much all of the things we went through together, and I'll always keep in my heart everythng I learnt and
those little things that made this work possible. MOONSTAR won't die though, I'll move most of its commands and functionalities to my webpage, where they'll continue working
indefenitely and (perhaps) forever. Again, thank you so much for making this possible, and I hope we can keep counting on y'all for future projects <3.

- Aurora Flores, 2023.
"""
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
import asyncpraw
import os
from math import sqrt
import csv

os.environ['TZ'] = 'America/Mexico_City'
time.tzset()
intents = discord.Intents.all()
moon = commands.Bot(intents=intents)
translator = Translator()
reddit = asyncpraw.Reddit(client_id='ID',
                  client_secret='SECRET',
                  user_agent='AGENT')

@moon.event
async def on_ready():
    ställd = False
    print(" 안녕하세요 여러분 문별이다")
    print('\n {0.user}으로서 봇이 성공적으로 로그인했습니다'.format(moon))
    print('\n')
    while True:
      time = int(datetime.datetime.now().strftime("%S"))
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
async def translate(ctx, message, language = ''):
    await ctx.defer()
    async with ctx.typing():
      await asyncio.sleep(1)
    author = ctx.author.name
    msg = message.split("/")
    if "discord.com" in msg:
      melding = await ctx.fetch_message(int(msg[6]))
      message = melding.content
      author = melding.author.name
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
        embed.add_field(name=author + " wrote:", value=message, inline=False)
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

@moon.slash_command(name="languages", description="Shows available languages for translation.")
async def languages(ctx):
  res = ""
  for values in variables.LANGUAGES.values():
    res = res + "\n" + values
  embed = discord.Embed(title="Available languages",
                        description=res, 
                        color=discord.Colour.random())
  await ctx.respond(embed=embed, ephemeral=True)
    
@moon.slash_command(name="ping" ,description="Shows bot's latency.")
async def ping(ctx):
  p = int(moon.latency * 1000)
  await ctx.respond("Pong! Ping is " + str(p) + " ms")

@moon.slash_command(name="avatar", description="Shows the avatar from the specified user.")
async def avatar(ctx, member: discord.Member = ''):
    await ctx.defer()
    if member != "":
      if member.id == 0000000000000000000:
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
async def pic(ctx, picture):
  try:
    await ctx.defer()
    resp = requests.get("https://www.bing.com/images/search?q=" + picture.replace(" ", "+"))
    soup = BeautifulSoup(resp.text, 'lxml')
    resimg = []
    for i in soup.find_all('a', {"class":"iusc"}):
      resimg.append(i['m'])
    res = random.sample(resimg, len(resimg))
    res = random.sample(res, len(res))
    dataa = random.choice(res)
    u = str(dataa).split('"murl":"')
    uu = str(u[1]).split('",')
    embed = discord.Embed(title="Picture finder: " + picture, 
                      url="https://www.bing.com/images/search?q=" + picture.replace(" ", "+"),
                      color=discord.Colour.random())
    embed.set_image(url=uu[0])
    embed.set_footer(text=f"Requested by: {ctx.author.name}")
    await ctx.respond(embed=embed)
  except IndexError:
    await ctx.respond("I couldn't find anything for `" + picture + "`. Try again or use different keywords.", ephemeral=True)

@moon.slash_command(name="ball", description="Question game.")
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

@moon.slash_command(name="pride", description="Proud of who we are!")
async def pride(ctx):
  urls = random.sample(variables.lgbtqplus, len(variables.lgbtqplus))
  urls = random.sample(urls, len(urls))
  url = random.choice(urls)
  embed = discord.Embed(title="Pride", 
                    color=discord.Colour.random())
  embed.set_image(url=url)
  await ctx.respond(embed=embed, ephemeral=True)

@moon.slash_command(name="meme", description="Send a random meme!")
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
    await ctx.respond("Meme from r/" + subr + "\n" + url)

@moon.slash_command(name="hug", description="Hug your friends!")
async def hug(ctx, member: discord.Member = ""):
  if member != "" and member != ctx.author.mention:
    if member.id == 0000000000000000000:
      async with ctx.typing():
          await asyncio.sleep(1)
      await ctx.respond(ctx.author.mention + " thank you! <3.")
    else:
      huggs = random.sample(variables.hugs, len(variables.hugs))
      huggs = random.sample(huggs, len(huggs))
      pic = random.choice(huggs)
      nh = hugcsv(member.id)
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

def hugcsv(memberr):
  huglist = []
  count = 0
  with open ("hugscount.csv", "r+") as f:
    hugs = csv.reader(f)
    huglist.extend(hugs)
    for row in huglist:
      if str(memberr) in row:
        row[1] = str(int(row[1]) + 1)
        value = row[1]
        count = 1
    if count == 0:
      huglist.append([memberr, 1])
      value = 1
  with open("hugscount.csv", "w+") as f:
    hugscsv = csv.writer(f, lineterminator='\n')
    hugscsv.writerows(huglist)
  return value

@moon.slash_command(name="cry", description="Sometimes it's okay to cry and vent about your feelings :( <3")
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
      user = await moon.fetch_user(ctx.author.id)
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

@moon.slash_command(name="caramelldansen", description="Caramelldansen!")
async def caramelldansen(ctx):
  dansen = random.sample(variables.caramell, len(variables.caramell))
  dansen = random.sample(dansen, len(dansen))
  pic = random.choice(dansen)
  roll = ["https://youtu.be/xMHJGd3wwZk", "https://youtu.be/78ngmG_-Yck"]
  roll = random.sample(roll, len(roll))
  rick = random.choice(roll)
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
async def math(ctx, expression):
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

@moon.slash_command(name="flag", description="Play a flag trivia game!")
async def flag(ctx):
  responded = False
  countries = random.sample(variables.countries, len(variables.countries))
  countries = random.sample(countries, len(countries))
  choice = random.choice(countries)
  options = [random.choice(countries)]
  options.insert(random.randint(0, len(options)), choice)
  options.insert(random.randint(0, len(options)), random.choice(countries))
  options.insert(random.randint(0, len(options)), random.choice(countries))
  options = random.sample(options, len(options))

  button = Button(label=options[0], style=discord.ButtonStyle.primary)
  button2 = Button(label=options[1], style=discord.ButtonStyle.primary)
  button3 = Button(label=options[2], style=discord.ButtonStyle.primary)
  button4 = Button(label=options[3], style=discord.ButtonStyle.primary)

  buttons = [button, button2, button3, button4]
  
  async def bc(interaction):
    if interaction.user == ctx.author:
      nonlocal responded
      responded = True
      for item in buttons:
        if interaction.data["custom_id"] == item.custom_id:
          pressed = item
      if pressed.label == choice:
        embed.add_field(name="✅ Result:", value="You got it right! <a:hearts:1087081508302508204> 🎊", inline=False)
        pressed.style = discord.ButtonStyle.success
      else:
        embed.add_field(name="<:tache:1088935369787060414> Result:", value="Whoops, you got it wrong. The correct answer was **" + choice + "** <:thatcat:1087081229381292112> ❌", inline=False)
        pressed.style = discord.ButtonStyle.danger
        for item in buttons:
          if item.label == choice:
            item.style = discord.ButtonStyle.success
      for item in buttons:
        item.disabled = True
      await interaction.response.edit_message(embed=embed, view=view)
    else:
      await interaction.response.send_message("Hey! Only who sent the command can click the button.", ephemeral = True)
  button.callback = bc
  button2.callback = bc
  button3.callback = bc
  button4.callback = bc
  view = View(timeout=15)
  view.add_item(button)
  view.add_item(button2)
  view.add_item(button3)
  view.add_item(button4)
  embed = discord.Embed(title="Which country does this flag belong to? 👀",
                        description="You have 10 seconds to answer.",
                        color = discord.Colour.random()
  )
  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
  embed.set_image(url="https://flagpedia.net/data/flags/w702/" + variables.COUNTRIESDIC[choice] + ".webp")
  await ctx.respond(embed=embed, view=view)
  await asyncio.sleep(10)
  if responded == False:
    for item in buttons:
      item.disabled = True
    embed.add_field(name="<:tache:1088935369787060414>", value="Whoops, time is up! <:thatcat:1087081229381292112> ❌", inline=False)
    await ctx.edit(embed=embed, view=view)

moon.run("TOKEN")