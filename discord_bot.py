"""Module responsible for creating and running a Discord bot"""

import asyncio
import discord
from discord.ext import commands

bot = commands.Bot('/', intents=discord.Intents.all())


async def call(id_queue, guild_id):
    """ async  main function for calling to phone"""
    async def get_user(ds_tag, guild):
        for _ in range(10):
            for channel in guild.voice_channels:
                for member_channel in channel.members:
                    if ds_tag == member_channel.name:
                        return member_channel
            await asyncio.sleep(2)
        return None

    async def calling(member_channel, guild):
        can_call = True
        str_roll = discord.utils.get(guild.roles, name="Стример").members
        str_member = next(member for member in str_roll)
        await str_member.edit(mute=True)
        while True:
            if can_call:
                can_call = False
                v_channel = next(ch for ch in guild.voice_channels
                                 if ch.name == "RedPhoneChannel")
                await member_channel.move_to(v_channel)

    guild = bot.get_guild(guild_id)
    in_call = False

    while True:
        if not id_queue.empty() and not in_call:
            ds_tag = id_queue.get()
            member_channel = await get_user(ds_tag, guild)
            if member_channel:
                await calling(member_channel, guild)
        await asyncio.sleep(5)
