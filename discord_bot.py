# bot.py

import pandas as pd
import discord
from dotenv import load_dotenv
from discord.ext import commands

y_sch = pd.read_csv(r's2.csv')




#load_dotenv()
TOKEN = ""

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

bot = commands.Bot(command_prefix='!')

@bot.command(name='create_wk', help='things.')
@commands.has_role('Admin')
async def create_wk(ctx, week):
    wk = int(week)
    if(wk != 1):
        d_wk = list(y_sch[y_sch['week'] == wk - 1]['delete'])
        for i in d_wk:
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, name=str(i).lower())
            if existing_channel is not None:
                await existing_channel.delete()
            else:
                await ctx.send(f'No channel named ' + str(i).lower() + ', was found for deletion')
    c_wk = list(y_sch[y_sch['week'] == wk]['create'])
    for i1 in c_wk:
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=str(i1).lower())
        category = discord.utils.get(ctx.guild.categories, name='Madden')
        if not existing_channel:
            print(f'Creating a new channel: ' + str(i1).lower())
            await guild.create_text_channel(str(i1).lower(), category=category)
        

@bot.command(name='create-channel')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    category = discord.utils.get(ctx.guild.categories, name='Madden')
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name, category=category)
        
@bot.command(name='delete-channel', help='delete a channel with the specified name')
@commands.has_role('Admin')
async def delete_channel(ctx, channel_name):
   # check if the channel exists
   guild = ctx.guild
   existing_channel = discord.utils.get(guild.channels, name=channel_name)
   
   # if the channel exists
   if existing_channel is not None:
      await existing_channel.delete()
   # if the channel does not exist, inform the user
   else:
      await ctx.send(f'No channel named, "{channel_name}", was found')
      
from discord.ext.commands import CommandNotFound

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error
    
bot.run(TOKEN)
