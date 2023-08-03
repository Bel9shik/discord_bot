import discord
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.members = False
intents.message_content = True
intents.voice_states = True
discord.Intents.voice_states = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='?', intents=intents)


@client.event
async def on_ready():
    print('Bot is ready')


temporary_channels = []
@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return


    if not before.channel:
        print(f'{member.name} joined {after.channel.name}')
    elif before.channel and not after.channel:
        print(f"{member.name} left channel")
    elif before.channel and after.channel:
        if before.channel.id != after.channel.id:
            print(f"{member.name} switched voice channels")
        else:
            if member.voice.self_stream:
                print(f'{member.name} started streaming')
            elif member.voice.self_mute:
                print(f'{member.name} muted')
            elif member.voice.self_deaf:
                print(f'{member.name} deafened')
            else:
                print("Something else happened")

    possible_channel_name = f"\U0001F449 {member.name}'s \U0001F448"

    if after.channel is not None:
        if after.channel.id == 1136750172697788456:
            temp_channel = await after.channel.clone(name=possible_channel_name)
            await member.move_to(temp_channel)
            temporary_channels.append(temp_channel.id)
            print(temporary_channels)

    if before.channel is not None:
        if before.channel.id in temporary_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                temporary_channels.remove(before.channel.id)


client.run(BOT_TOKEN)
