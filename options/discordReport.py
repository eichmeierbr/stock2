#!/usr/bin/python
import discord
import os

import json


def createDiscordReport():
    intents = discord.Intents.default()
    intents.message_content = True

    with open("config.json", "r") as read_file:
        data = json.load(read_file)

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(data['discordChannel'])
        filelist = [ f for f in os.listdir("options/data") if f.endswith(".csv") ]
        
        ## Write file as text
        with open(f"options/data/{filelist[0]}", "r", newline="") as f:
            output_text = ''
            for line in f:
                line = line.replace(',','\t')
                output_text += f"{line}\n"
                if len(output_text) > 1900:
                    await channel.send(output_text)
                    output_text = ''
        
        # Upload File
        await channel.send('Daily Results!', file=discord.File(f"options/data/{filelist[0]}"))

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

    client.run(data['discordKey'])

if __name__=="__main__":
    createDiscordReport()