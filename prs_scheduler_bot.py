import os
import discord
import requests
import re

from datetime import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
BASE_PATH = os.getenv('PRS_SCHEDULER_API')
LEAGUES_ENDPOINT = os.getenv('LEAGUES_ENDPOINT')
GAMES_ENDPOINT = os.getenv('GAMES_ENDPOINT')
NEXT_GAME_ENDPOINT = os.getenv('NEXT_GAME_ENDPOINT')
GAMES_IN_ENDPOINT = os.getenv('GAMES_IN_ENDPOINT')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

def addUrlVal(val):
    return str(val) + "/"

def checkPSLLink(url):
    urlCheck = re.fullmatch("https:\/\/pittsburghsportsleague\.leaguelab\.com\/team\/[0-9]*\/[-a-zA-z]*", url)
    if urlCheck != None:
        return True
    return False

def getLeaguesDict():
    leaguesDict = {}
    try:
        response = requests.get(BASE_PATH + LEAGUES_ENDPOINT)
    except:
        return leaguesDict
    for league in response.json():
        leaguesDict[league["id"]] = league["teamName"]
    return leaguesDict

@bot.command(brief='Get a list of teams', description='Returns a list of all teams in the database')
async def teams(ctx):
    try:
        response = requests.get(BASE_PATH + LEAGUES_ENDPOINT)
    except:
        await ctx.send(f"An error has occurred. Please try again.")
    strOutput = "Here are all given teams:\n\n"
    for league in response.json():
        strOutput += str(league["id"]) + ". " + league["league"] + " - " + league["teamName"] +"\n"
    await ctx.send(strOutput)

@bot.command(brief='Add a team', description='Give the bot the proper PSL link and it will add a new team to the database')
async def add(ctx, teamLink: str = commands.parameter(description="PSL link in the format of psl.leaguelab.com/team/<id>/<team name>")):
    if checkPSLLink(teamLink) is True:
        data = {
            "scheduleLink": teamLink
        }
        try:
            response = requests.post(BASE_PATH + LEAGUES_ENDPOINT, data=data)
        except:
            await ctx.send(f"An error has occurred. Please try again.")
        if response.ok is True:
            await ctx.send(f"Successfully added new team!")
        else:
            await ctx.send(f"The team could not be added. Please try again.")
    else:
        await ctx.send(f"This is an invalid URL. The format should match /team/<id>/<team name>")


@bot.command(brief='Get information for a specific team', description='Returns all information saved for a team')
async def teaminfo(ctx, teamId: int = commands.parameter(description="The id of the team")):
    try:
        response = requests.get(BASE_PATH + LEAGUES_ENDPOINT + addUrlVal(teamId))
    except:
        await ctx.send(f"An error has occurred. Please try again.")
    if response.ok is False:
        await ctx.send(f"Could not retrieve team information. Please try again.")  
    league = response.json()  
    strOutput = "Here's the info for the given team id:\n\n" + "league: " + league["league"] + "\nlocation: " + league["location"] + "\nsport: " + league["sport"] + "\nteam name: " + league["teamName"] + "\nurl: " + league["scheduleLink"]
    await ctx.send(strOutput)

#@bot.command(brief='Edit an added league', description='Edit any field of a league; include a league name, location, sport, team name, and PSL link')
#async def edit(ctx, leagueId: int = commands.parameter(description="The id of the league"), league: str= commands.parameter(description="The name of the league"), location: str= commands.parameter(description="The location of the league"), sport: str= commands.parameter(description="The sport for the league"), teamName: str= commands.parameter(description="The name of the team participating in the league")):
#    data = {
#        "league": league,
#        "location": location,
#        "sport": sport,
#        "teamName": teamName
#    }
#    
#    try:
#        response = requests.put(BASE_PATH + LEAGUES_ENDPOINT + addUrlVal(leagueId), data=data)
#    except:
#        await ctx.send(f"An error has occurred. Please try again.")
#    if response.ok is False:
#        await ctx.send(f"Could not update the league. Please try again.")
#    else:
#        await ctx.send(f"League successfully updated!")

@bot.command(brief='Get a list of games', description='Get a list of games when given a team id number (get the team Id with the $teams command)')
async def games(ctx, teamId: int = commands.parameter(description="The id of the team")):
    try:
        response = requests.get(BASE_PATH + GAMES_ENDPOINT + addUrlVal(teamId))
    except:
        await ctx.send(f"An error has occurred. Please try again.")
    if response.ok is False:
        await ctx.send(f"Could not retrieve the list of games. Please try again.")
    strOutput = "Here's the list of games:\n\n"
    for game in response.json():
        strOutput += datetime.strftime(datetime.strptime(game["gameDateTime"], "%Y-%m-%dT%H:%M:%SZ"), "%A, %B %d @ %I:%M %p") + "\n"
    await ctx.send(strOutput)

@bot.command(brief='Get the next game', description='Get the next game when given a team id number (get the team id with the $teams command)')
async def nextgame(ctx, teamId: int = commands.parameter(description="The id of the team")):
    try:
        response = requests.get(BASE_PATH + GAMES_ENDPOINT + NEXT_GAME_ENDPOINT + addUrlVal(teamId))
    except:
        await ctx.send(f"An error has occurred. Please try again.")
    if response.ok is False:
        await ctx.send(f"Could not retrieve next game. Please try again.")
    strOutput = "The next game is: " + datetime.strftime(datetime.strptime(response.json()["gameDateTime"], "%Y-%m-%dT%H:%M:%SZ"), "%A, %B %d @ %I:%M %p")
    await ctx.send(strOutput)

@bot.command(brief='Get all games over the next couple days', description='Given an amount of days, this will return all games from today to today + amount given')
async def gamein(ctx, days: int = commands.parameter(description="The amount of days ahead you want to check for games")):
    try:
        response = requests.get(BASE_PATH + GAMES_ENDPOINT + GAMES_IN_ENDPOINT + addUrlVal(days))
    except:
       await ctx.send(f"An error has occurred. Please try again.") 
    if response.ok is False:
        await ctx.send(f"Could not retrieve games for given days. Please try again.")
    leaguesDict = getLeaguesDict()
    if not leaguesDict:
        await ctx.send(f"An error has occurred. Please try again.") 
    strOutput = "Here's a list of games in the next " + str(days) + " days:\n\n"
    for game in response.json():
        league = leaguesDict[game["leagueId"]]
        strOutput += datetime.strftime(datetime.strptime(game["gameDateTime"], "%Y-%m-%dT%H:%M:%SZ"), "%A, %B %d @ %I:%M %p") + " - " + league + "\n"
    await ctx.send(strOutput)

@tasks.loop(hours=168)
async def checknextweek():
    try:
        response = requests.get(BASE_PATH + GAMES_ENDPOINT + GAMES_IN_ENDPOINT + addUrlVal(7))
    except:
       await ctx.send(f"Unable to automatically find games for next week.") 
    if response.ok is False:
        await ctx.send(f"Unable to automatically find games for next week.")
    leaguesDict = getLeaguesDict()
    if not leaguesDict:
        await ctx.send(f"An error has occurred. Please try again.") 
    strOutput = "Here's a list of games for this week:\n\n"
    for game in response.json():
        league = leaguesDict[game["leagueId"]]
        strOutput += datetime.strftime(datetime.strptime(game["gameDateTime"], "%Y-%m-%dT%H:%M:%SZ"), "%A, %B %d @ %I:%M %p") + " - " + league + "\n"
    await ctx.send(strOutput)

bot.run(TOKEN)