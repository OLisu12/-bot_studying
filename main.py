#pip install discord.py



import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random as rd

echo_users = {}
updown_games = {}

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
async def echo(ctx, *, nickname = None):
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