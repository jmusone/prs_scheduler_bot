import os
import discord
import json

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def leagues(ctx):
    #make API call here: GET /prs_scheduler/leagues/
    await ctx.send(f"You tried retrieving all leagues")

@bot.command()
async def add(ctx, league: str, location: str, sport: str, teamName: str, captain: str, teamLink: str):
    data = {
        "league": league,
        "location": location,
        "sport": sport,
        "teamName": teamName,
        "captain": captain,
        "teamLink": teamLink
    }
    
    jsonData = json.dumps(data)
    #make API call here : POST /prs_scheduler/leagues/
    await ctx.send(f"You tried adding {league}")

@bot.command()
async def edit(ctx, leagueId: int, league: str, location: str, sport: str, teamName: str, captain: str, teamLink: str):
    data = {
        "league": league,
        "location": location,
        "sport": sport,
        "teamName": teamName,
        "captain": captain,
        "teamLink": teamLink
    }
    
    jsonData = json.dumps(data)
    #make API call here: PUT /prs_scheduler/leagues/(league_id)
    await ctx.send(f"You tried editing leagueId {leagueId}")

@bot.command()
async def games(ctx, leagueId: int):
    #make API call here: GET /prs_scheduler/schedule/(league_id)
    await ctx.send(f"You tried getting games for leagueId =  {leagueId}")

@bot.command()
async def nextgame(ctx, leagueId: int):
    #make API call here: NOT IMPLEMENTED YET
    await ctx.send(f"You tried getting the next game")

@bot.command()
async def gamein(ctx, days: int):
    #make API call here: NOT IMPLEMENTED YET
    await ctx.send(f"You tried finding the games in the next {days} days")

bot.run(TOKEN)