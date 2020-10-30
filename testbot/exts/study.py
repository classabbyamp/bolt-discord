"""
Study extension for qrm
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import random
import json
from datetime import datetime
import asyncio

import aiohttp

import discord.ext.commands as commands

import testbot.common as cmn
from testbot.resources import study
from bolt.utils import exceptions, embeds, misc


class StudyCog(commands.Cog):
    choices = {misc.emojis.a: "A", misc.emojis.b: "B", misc.emojis.c: "C", misc.emojis.d: "D"}

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastq = dict()
        self.source = "Data courtesy of [HamStudy.org](https://hamstudy.org/)"
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="hamstudy", aliases=["rq", "randomquestion", "randomq"], category=cmn.cat.study)
    async def _random_question(self, ctx: commands.Context, country: str = "", level: str = ""):
        """Gets a random question from [HamStudy's](https://hamstudy.org) question pools."""
        with ctx.typing():
            embed = embeds.embed_factory(ctx)

            country = country.lower()
            level = level.lower()

            if country in study.pool_names.keys():
                if level in study.pool_names[country].keys():
                    pool_name = study.pool_names[country][level]

                elif level in ("random", "r"):
                    # select a random level in that country
                    pool_name = random.choice(list(study.pool_names[country].values()))

                else:
                    # show list of possible pools
                    embed.title = "Pool Not Found!"
                    embed.description = "Possible arguments are:"
                    embed.colour = misc.colours.bad
                    for cty in study.pool_names:
                        levels = "`, `".join(study.pool_names[cty].keys())
                        embed.add_field(name=f"**Country: `{cty}` {study.pool_emojis[cty]}**",
                                        value=f"Levels: `{levels}`", inline=False)
                    embed.add_field(name="**Random**", value="To select a random pool or country, use `random` or `r`")
                    await ctx.send(embed=embed)
                    return

            elif country in ("random", "r"):
                # select a random country and level
                country = random.choice(list(study.pool_names.keys()))
                pool_name = random.choice(list(study.pool_names[country].values()))

            else:
                # show list of possible pools
                embed.title = "Pool Not Found!"
                embed.description = "Possible arguments are:"
                embed.colour = misc.colours.bad
                for cty in study.pool_names:
                    levels = "`, `".join(study.pool_names[cty].keys())
                    embed.add_field(name=f"**Country: `{cty}` {study.pool_emojis[cty]}**",
                                    value=f"Levels: `{levels}`", inline=False)
                embed.add_field(name="**Random**", value="To select a random pool or country, use `random` or `r`")
                await ctx.send(embed=embed)
                return

            pools = await self.hamstudy_get_pools()

            pool_matches = [p for p in pools.keys() if "_".join(p.split("_")[:-1]) == pool_name]

            if len(pool_matches) > 0:
                if len(pool_matches) == 1:
                    pool = pool_matches[0]
                else:
                    # look at valid_from and expires dates to find the correct one
                    for p in pool_matches:
                        valid_from = datetime.fromisoformat(pools[p]["valid_from"][:-1])
                        expires = datetime.fromisoformat(pools[p]["expires"][:-1])

                        if valid_from < datetime.utcnow() < expires:
                            pool = p
                            break
            else:
                # show list of possible pools
                embed.title = "Pool Not Found!"
                embed.description = "Possible arguments are:"
                embed.colour = misc.colours.bad
                for cty in study.pool_names:
                    levels = "`, `".join(study.pool_names[cty].keys())
                    embed.add_field(name=f"**Country: `{cty}` {study.pool_emojis[cty]}**",
                                    value=f"Levels: `{levels}`", inline=False)
                embed.add_field(name="**Random**", value="To select a random pool or country, use `random` or `r`")
                await ctx.send(embed=embed)
                return

            pool_meta = pools[pool]

            async with self.session.get(f"https://hamstudy.org/pools/{pool}") as resp:
                if resp.status != 200:
                    raise exceptions.BotHTTPError(resp)
                pool = json.loads(await resp.read())["pool"]

            # Select a question
            pool_section = random.choice(pool)["sections"]
            pool_questions = random.choice(pool_section)["questions"]
            question = random.choice(pool_questions)

            embed.title = f"{study.pool_emojis[country]} {pool_meta['class']} {question['id']}"
            embed.description = self.source
            embed.add_field(name="Question:", value=question["text"], inline=False)
            embed.add_field(name="Answers:",
                            value=(f"**{misc.emojis.a}** {question['answers']['A']}"
                                   f"\n**{misc.emojis.b}** {question['answers']['B']}"
                                   f"\n**{misc.emojis.c}** {question['answers']['C']}"
                                   f"\n**{misc.emojis.d}** {question['answers']['D']}"),
                            inline=False)
            embed.add_field(name="To Answer:",
                            value=("Answer with reactions below. If not answered within 10 minutes,"
                                   " the answer will be revealed."),
                            inline=False)
            if "image" in question:
                image_url = f"https://hamstudy.org/images/{pool_meta['year']}/{question['image']}"
                embed.set_image(url=image_url)

        q_msg = await ctx.send(embed=embed)

        await misc.add_react(q_msg, misc.emojis.a)
        await misc.add_react(q_msg, misc.emojis.b)
        await misc.add_react(q_msg, misc.emojis.c)
        await misc.add_react(q_msg, misc.emojis.d)

        def check(reaction, user):
            return (user.id != self.bot.user.id
                    and reaction.message.id == q_msg.id
                    and str(reaction.emoji) in self.choices.keys())

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=600.0, check=check)
        except asyncio.TimeoutError:
            embed.remove_field(2)
            embed.add_field(name="Answer:", value=f"Timed out! The correct answer was **{question['answer']}**.")
            await q_msg.edit(embed=embed)
        else:
            if self.choices[str(reaction.emoji)] == question["answer"]:
                embed.remove_field(2)
                embed.add_field(name="Answer:", value=f"Correct! The answer was **{question['answer']}**.")
                embed.colour = misc.colours.good
                await q_msg.edit(embed=embed)
            else:
                embed.remove_field(2)
                embed.add_field(name="Answer:", value=f"Incorrect! The correct answer was **{question['answer']}**.")
                embed.colour = misc.colours.bad
                await q_msg.edit(embed=embed)

    async def hamstudy_get_pools(self):
        async with self.session.get("https://hamstudy.org/pools/") as resp:
            if resp.status != 200:
                raise exceptions.BotHTTPError(resp)
            else:
                pools_dict = json.loads(await resp.read())

        pools = dict()
        for ls in pools_dict.values():
            for pool in ls:
                pools[pool["id"]] = pool

        return pools


def setup(bot: commands.Bot):
    bot.add_cog(StudyCog(bot))
