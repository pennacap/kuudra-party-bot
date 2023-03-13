import discord
from discord.ext import commands
import os

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')
"""
print(bot.tree)
@discord.app_commands.choices(type=[
    discord.app_commands.Choice(name='Burning', value=1),
    discord.app_commands.Choice(name='Fiery', value=2),
    discord.app_commands.Choice(name='Infernal', value=3),
])
@bot.tree.command()
async def lfg_msg(self: discord.Interaction, type: int, channel: discord.TextChannel):
    pass
"""
msg = None
@bot.event
async def on_raw_reaction_add(reaction):
    if not msg or not reaction.message_id == msg.id or reaction.user_id == bot.user.id or reaction.emoji.name not in ['⛰️', '🔥', '🧨']:
        return
    name = {
        '⛰️': 'infernal',
        '🔥': 'fiery',
        '🧨': 'burning'
    }[reaction.emoji.name]
    channels = [i for i in bot.get_channel(1084534415495004202).channels if name+'-team-' in i.name]
    print(name)
    for i in channels:
        if len(i.overwrites) < 5:
            await i.set_permissions(i.guild.get_member(reaction.user_id), read_messages=True)
            return
    count = 0 if not len(channels) else channels[-1].split('-')[-1]
    await bot.get_channel(1084534415495004202).create_text_channel(name+'-team-'+str(int(count)+1), overwrites={bot.guilds[0].default_role: discord.PermissionOverwrite(read_messages=False), bot.guilds[0].get_member(reaction.user_id): discord.PermissionOverwrite(read_messages=True)})

   # await (await bot.get_channel(reaction.channel_id).fetch_message(reaction.message_id)).remove_reaction(reaction.emoji,discord.Object(reaction.user_id))

@bot.event
async def on_raw_reaction_remove(reaction):
    if not msg or not reaction.message_id == msg.id or reaction.user_id == bot.user.id or reaction.emoji.name not in ['⛰️', '🔥', '🧨']:
        return
    name = {
        '⛰️': 'infernal',
        '🔥': 'fiery',
        '🧨': 'burning'
    }[reaction.emoji.name]
    channels = [i for i in bot.get_channel(1084534415495004202).channels if name+'-team-' in i.name]
    reaction.member = bot.guilds[0].get_member(reaction.user_id)
    for i in channels:
        if reaction.member in i.overwrites:
            await i.set_permissions(reaction.member, overwrite=None)
            if len(i.overwrites) == 1:
                await i.delete()
            return
 
@bot.event
async def on_ready():
    global msg
    channel = await bot.fetch_channel(1084878464450052177)
    print(channel)
    if not channel.last_message_id:
        msg = await channel.send("To join an **Infernal** Kuudra party, tap the :mountain: below\nTo join a **Fiery** Kuudra party, tap the :fire: below\nTo join a **Burning** Kuudra party, tap the :firecracker: below")
    else:
        try:
            msg= await channel.fetch_message(channel.last_message_id)
            if msg.author.id != bot.user.id:
                raise Exception
        except Exception:
            msg = await channel.send("To join an **Infernal** Kuudra party, tap the :mountain: below\nTo join a **Fiery** Kuudra party, tap the :fire: below\nTo join a **Burning** Kuudra party, tap the :firecracker: below")
    if not msg.reactions:
        await msg.add_reaction("⛰️")
        await msg.add_reaction("🔥")
        await msg.add_reaction("🧨")
        
        
    bot.tree.copy_global_to(guild=discord.Object(1082637489665224795))
    await bot.tree.sync(guild=discord.Object(1082637489665224795))


bot.run(os.getenv("TOKEN"))
