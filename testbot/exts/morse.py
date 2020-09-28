"""
Morse Code extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import discord.ext.commands as commands

import testbot.common as cmn
from testbot.resources import morse


class MorseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="morse", aliases=["cw"], category=cmn.cat.ref)
    async def _morse(self, ctx: commands.Context, *, msg: str):
        """Converts ASCII to international morse code."""
        result = ""
        for char in msg.upper():
            try:
                result += morse.morse[char]
            except KeyError:
                result += "<?>"
            result += " "
        embed = embeds.embed_factory(ctx)
        embed.title = f"Morse Code for {msg}"
        embed.description = "**" + result + "**"
        embed.colour = misc.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="unmorse", aliases=["demorse", "uncw", "decw"], category=cmn.cat.ref)
    async def _unmorse(self, ctx: commands.Context, *, msg: str):
        """Converts international morse code to ASCII."""
        result = ""
        msg0 = msg
        msg = msg.split("/")
        msg = [m.split() for m in msg]
        for word in msg:
            for char in word:
                try:
                    result += morse.ascii[char]
                except KeyError:
                    result += "<?>"
            result += " "
        embed = embeds.embed_factory(ctx)
        embed.title = f"ASCII for {msg0}"
        embed.description = result
        embed.colour = misc.colours.good
        await ctx.send(embed=embed)

    @commands.command(name="cwweight", aliases=["weight", "cww"], category=cmn.cat.ref)
    async def _weight(self, ctx: commands.Context, *, msg: str):
        """Calculates the CW weight of a callsign or message."""
        embed = embeds.embed_factory(ctx)
        msg = msg.upper()
        weight = 0
        for char in msg:
            try:
                cw_char = morse.morse[char].replace("-", "==")
                weight += len(cw_char) * 2 + 2
            except KeyError:
                embed.title = "Error in calculation of CW weight"
                embed.description = f"Unknown character `{char}` in message"
                embed.colour = misc.colours.bad
                await ctx.send(embed=embed)
                return
        embed.title = f"CW Weight of {msg}"
        embed.description = f"The CW weight is **{weight}**"
        embed.colour = misc.colours.good
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(MorseCog(bot))
