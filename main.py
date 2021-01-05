import discord

from mysecrets import DISCORD_TOKEN, SPOONACULAR_API_KEY
from food_commands.commands import Food_Commands

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!helloworld'):
        await message.channel.send('Hello discord bot world!')

    if message.content.lower().startswith('!whatsfordinner'):
        await message.channel.send('<This command is under construction>')
        await message.channel.send('Fetching dinner recipe. One moment please.')
        food_commands = Food_Commands()
        instructions = food_commands.getRecipe()
        await message.channel.send(instructions['result'])
        

client.run(DISCORD_TOKEN)