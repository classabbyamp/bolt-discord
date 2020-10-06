"""
embed utils for bolt-discord
---
Copyright (c) 2020 miaowware
Released under the BSD 3-Clause License.
"""


from datetime import datetime
import traceback

import discord
import discord.ext.commands as commands

from .misc import colours, emojis


def embed_factory(ctx: commands.Context) -> discord.Embed:
    """Creates an embed with neutral colour and standard footer."""
    embed = discord.Embed(timestamp=datetime.utcnow(), colour=colours.neutral)
    embed.set_footer(text=ctx.author, icon_url=str(ctx.author.avatar_url))
    return embed


def error_embed_factory(ctx: commands.Context, exception: Exception, debug_mode: bool) -> discord.Embed:
    """Creates an Error embed."""
    if debug_mode:
        fmtd_ex = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    else:
        fmtd_ex = traceback.format_exception_only(exception.__class__, exception)
    embed = embed_factory(ctx)
    embed.title = f"{emojis.warning} Error"
    embed.description = "```\n" + "\n".join(fmtd_ex) + "```"
    embed.colour = colours.bad
    return embed
