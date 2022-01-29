from stay_up import keep_up
import discord, os, time, requests, json, discord.ext
from discord_slash import SlashCommand
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^

client = discord.Client()

client = commands.Bot(command_prefix = 'ocular!') #put your own prefix here

slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("bot online") #will print "bot online" in the console when the bot is online

@slash.slash(description="Get a user's status")
async def status(ctx, user):
    if user == "":
      color = 0xff0000
      embed=discord.Embed(title="An error has been encountered", color=color)
      embed.add_field(name="Error", value="No user provided", inline=True)
      await ctx.send(embed=embed)
    url = "https://my-ocular.jeffalo.net/api/user/" + user
    response = json.loads(requests.get(url).text)
    if response:
      try:
        status = response["status"]
        if status == "":
          status = "This users status is empty"
      except:
        color = 0xff0000
        response = json.loads(requests.get("https://api.scratch.mit.edu/accounts/checkusername/" + user).text)
        if response["msg"] == "username exists":
          embed=discord.Embed(title="An error has been encountered", color=color)
          embed.add_field(name="Error", value=user + " does not have an Ocular status", inline=True)
          await ctx.send(embed=embed)
          return False
        embed=discord.Embed(title="An error has been encountered", color=color)
        embed.add_field(name="Error", value="No user named " + user, inline=True)
        await ctx.send(embed=embed)
      if response["color"] == None:
        color = 0xffffff
      else:
        color = int(response["color"].replace("#", ""), base=16)
      embed=discord.Embed(title=user + "'s Status", color=color)
      embed.add_field(name="Status", value=status, inline=True)
      await ctx.send(embed=embed)
    else:
      color = 0xff0000
      embed=discord.Embed(title="An error has been encountered", color=color)
      embed.add_field(name="Error", value=response.status_code, inline=True)
      await ctx.send(embed=embed)
keep_up()
client.run(os.getenv("TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!

# invite link - https://discord.com/api/oauth2/authorize?client_id=935764556003823667&permissions=2048&scope=bot%20applications.commands