import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    channel = client.get_channel(1020721546932793467)
    await channel.send('Daily Results!', file=discord.File("out.csv"))
    await client.close()
    exit()
    # await channel.send([1,2,3,4])
    # print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('hello'):
#         await message.channel.send('Hello!')

client.run(os.environ['DISCORD_KEY'])