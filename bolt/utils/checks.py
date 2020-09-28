"""
checks for bolt-discord
---
Copyright (c) 2020 miaowware
Released under the BSD 3-Clause License.
"""


import discord.ext.commands as commands


async def check_if_owner(ctx: commands.Context):
    # TODO needs rework (opt.owner_uids)
    if ctx.author.id in opt.owners_uids:
        return True
    raise commands.NotOwner
