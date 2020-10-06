"""
converters for bolt-discord
---
Copyright (c) 2020 miaowware
Released under the BSD 3-Clause License.
"""


import re

import discord
import discord.ext.commands as commands


class GlobalChannelConverter(commands.IDConverter):
    """Converter to get any bot-accessible channel by ID/mention (global), or name (in current guild only)."""
    async def convert(self, ctx: commands.Context, argument: str):
        bot = ctx.bot
        guild = ctx.guild
        match = self._get_id_match(argument) or re.match(r"<#([0-9]+)>$", argument)
        result = None
        if match is None:
            # not a mention/ID
            if guild:
                result = discord.utils.get(guild.text_channels, name=argument)
            else:
                raise commands.BadArgument(f"""Channel named "{argument}" not found in this guild.""")
        else:
            channel_id = int(match.group(1))
            result = bot.get_channel(channel_id)
        if not isinstance(result, (discord.TextChannel, discord.abc.PrivateChannel)):
            raise commands.BadArgument(f"""Channel "{argument}" not found.""")
        return result
