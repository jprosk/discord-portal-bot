import asyncio
import discord
import logging
import re
import datetime
from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()
env = getenv('ENV')
token = getenv('TOKEN')

# Configure logging
if env == 'dev':
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Configure events that I'll respond to
intents = discord.Intents.default()
intents.message_content = True

# Create client
client = discord.Client(intents=intents)

# Say something when I'm connected
@client.event
async def on_ready():
    print(f'tudo beleza. logged in as {client.user}')

# Respond to messages
last_stare_time = None
@client.event
async def on_message(message):
    global last_stare_time

    # Ignore messages from myself
    if message.author == client.user:
        return
    
    # Check if message starts with my name (case-insensitive)
    if re.search(r'^lua\b', message.content, re.IGNORECASE):
        # If the next word is 'redirect', redirect the message to a different channel
        if re.search(r'^lua\b\W+redirect\b', message.content, re.IGNORECASE):
            # Get the channel name using regex
            channel_name = re.search(r'\<\#(\d+)\>', message.content, re.IGNORECASE).group(1)
            # If the channel exists, redirect the message
            if channel_name is not None:
                # Find the channel
                tgt_channel = client.get_channel(int(channel_name))
                if tgt_channel == message.channel:
                    await message.channel.send(f'meu parceiro. that is the channel we\'re in. i will bite you')
                    return
                # Check if I have access to the channel
                me = tgt_channel.guild.get_member(client.user.id)
                if tgt_channel.permissions_for(me).send_messages:
                    # Create portal exit
                    exit = await tgt_channel.send(f'conversation redirected from: <#{channel_name}>')
                    # Create portal entrance
                    entrance = await message.channel.send(f'continue conversation here: {exit.jump_url}')
                    # Edit portal exit to include link to entrance
                    await exit.edit(content=f'conversation redirected from: {entrance.jump_url}')

                else:
                    await message.channel.send(f'im not allowed in that channel, babaca')

            # If the channel doesn't exist, say so
            else:
                await message.channel.send(f'sorry, cant find that channel ({channel_name})')
        
        # If the next word is 'kill', go feral
        elif re.search(r'^lua\b\W+kill\b', message.content, re.IGNORECASE):
            await message.channel.send('entendido')
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('<:feral2:1072017040275161228>')
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('<:feral1:1072189361556303932>')
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('<a:youdied:1200593379898175488>')

        # If the next words are 'good girl', wag tail
        elif re.search(r'^lua\b\W+good\b\W+girl\b', message.content, re.IGNORECASE):
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('\U0001F612 <a:wag1:1200581198850822195>')
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('...obrigada')
        
        # If the next words are 'how big is that dick', say 'small, leave me alone'
        elif re.search(r'^lua\b\W+how\b\W+big\b\W+is\b\W+that\b\W+dick\b', message.content, re.IGNORECASE):
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('small, leave me alone <:disappoint:469615738915913743>')

        # If it's a command I don't know, say so
        elif re.search(r'^lua\b\W+\w+', message.content, re.IGNORECASE):
            await message.channel.send('o que? idk how to do that')

        # If it's just my name, say hello
        else:
            async with message.channel.typing():
                await asyncio.sleep(0.75)
            await message.channel.send('e aí')

    # Check if message otherwise mentions me (case-insensitive and ignoring punctuation)
    elif re.search(r'\blua\b', message.content, re.IGNORECASE):
        # Stare if it's been more than 5 minutes since I was last mentioned
        if last_stare_time is None or (datetime.datetime.now() - last_stare_time).total_seconds() > 300:
            await message.channel.send('<:dogstare:1099020377004453990>')
    
    # Update the last stare time
    if re.search(r'\blua\b', message.content, re.IGNORECASE):
        last_stare_time = datetime.datetime.now()


client.run(
    token=token,
    log_handler=handler,
    log_level=logging.DEBUG,
)
