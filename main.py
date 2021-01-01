import discord

from secrets import DISCORD_TOKEN, SPOONACULAR_API_KEY

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(f'Client: {client}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!helloWorld'):
        await message.channel.send('hello discord bot world!')

    if message.content.startswith('!getRecipe'):
        await message.channel.send('<This command is under construction>')
        await message.channel.send('Fetching dinner recipe...')
        

client.run(DISCORD_TOKEN)