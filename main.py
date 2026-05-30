#pip install discord.py



import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random as rd
from PIL import Image, ImageDraw, ImageFont


echo_users = {}
updown_games = {}

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ASCII_CHARS = "@%#*+=- "








def text_to_ascii(text, font_path, font_size=50, output_width=80, scale=0.45):
   font = ImageFont.truetype(font_path, font_size)

   temp_img = Image.new("L", (1, 1), 255)
   temp_draw = ImageDraw.Draw(temp_img)

   bbox = temp_draw.textbbox((0, 0), text, font=font)

   text_width = bbox[2] - bbox[0]
   text_height = bbox[3] - bbox[1]

   img = Image.new("L", (text_width + 30, text_height + 30), 255)
   draw = ImageDraw.Draw(img)

   draw.text((15, 15), text, font=font, fill=0)

   new_width = output_width
   new_height = int(img.height / img.width * new_width * scale)

   if new_height < 1:
       new_height = 1

   img = img.resize((new_width, new_height))

   pixels = img.getdata()
   ascii_text = ""

   for i, pixel in enumerate(pixels):
       index = pixel * (len(ASCII_CHARS) - 1) // 255
       ascii_text += ASCII_CHARS[index]

       if (i + 1) % new_width == 0:
           ascii_text += "\n"

   return ascii_text

@bot.event
async def on_ready():
    print("봇이 실행 되었습니다.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if message.content == "안녕":
        while True:
            await message.channel.send("안녕하세요1")

    if message.author.id in echo_users:
        await message.channel.send(message.content)
        return

    if message.author.id in updown_games:
        if not message.content.isdigit():
            await message.channel.send("숫자 입력.")
            return

        guess = int(message.content)
        answer = updown_games[message.author.id]["answer"]

        updown_games[message.author.id]["count"] += 1
        count = updown_games[message.author.id]["count"]

        if guess < answer:
            await message.channel.send("UP")
        elif guess > answer:
            await message.channel.send("DOWN")
        else:
            await message.channel.send(f"정답입니다.\n 총 시도 횟수: {count}")
            del updown_games[message.author.id]

    await bot.process_commands(message)






@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def logo(ctx, *, text):
    if len(text) > 6:
        await ctx.send("6글자 이하로 작성")
        return
    font_path = "C:/Windows/Fonts/malgun.ttf"

    ascii_logo = text_to_ascii(text, font_path)
    await ctx.send(f"{ascii_logo}")

@bot.command()
async def echo(ctx, *, nickname=None):
    if nickname is None:
        target = ctx.guild.members #nickname
    else:
        target = None

    for member in ctx.guild.members:
        if member.display_name == nickname or member.name == nickname:
            target = member
            break
    if target is None:
        await ctx.send("해당 닉네임을 찾을 수 없습니다.")
        return
    echo_users[target.id] = True
    await ctx.send(f"{target.name}님을 따라해요.")

@bot.command()
async def noecho(ctx, *, nickname = None):
    if nickname is None:
        target = ctx.author
    else:
        target = None

    for member in ctx.guild.members:
        if member.display_name == nickname or member.name == nickname:
            target = member
            break
    if target is None:
        await ctx.send("해당 닉네임을 찾을 수 없습니다.")
        return

    if target.id in echo_users:
        del echo_users[target.id]
        await ctx.send(f"{target.display_name}님을 그만 따라해요.")
    else:
        await ctx.send("따라말하기가 켜져있지 않아요.")

@bot.command()
async def game_updown(ctx):
    answer = rd.randint(1, 100)

    updown_games[ctx.author.id] = {
        "answer" : answer,
        "count" : 0
    }

    await ctx.send(
        "업다운 게임 시작\n"
        "1~100\n"
        "채팅창에 숫자만 입력\n"
    )

@bot.command()
async def fin_updown(ctx):
    if ctx.author.id in updown_games:
        del updown_games[ctx.author.id]
        await ctx.send("종료되었습니다")

    else:
        await ctx.send("진행중이지 않습니다.")
bot.run(TOKEN)
