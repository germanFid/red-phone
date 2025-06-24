"""Main module of discord_bot.py"""
import web_server
import discord_bot
from data import guild_id, bot_token


@discord_bot.bot.event
async def on_ready():
    """async main loop function"""
    received_ids = web_server.Queue()

    discord_bot.bot.loop.create_task(web_server.start_webserver(received_ids))
    discord_bot.bot.loop.create_task(discord_bot.call(received_ids, guild_id))

if __name__ == "__main__":
    discord_bot.bot.run(bot_token)
