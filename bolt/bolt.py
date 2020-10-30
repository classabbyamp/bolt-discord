"""
Bolt Class
---
The main class for Bolt.

Copyright (c) 2020 classabbyamp, 0x5c
Released under the BSD 3-Clause License.
"""


import traceback
import sys
import random
from datetime import datetime, time
from typing import Optional, Dict, Tuple, List, Union, Iterable, Callable

import pytz

import discord
from discord.ext import commands, tasks

from .utils import misc, embeds
from .dataclasses import BoltStatus, StatusMode


class Bolt(commands.Bot):
    def __init__(self,
                 command_prefix: Union[str, Iterable[str], Callable],
                 debug_mode: bool = False,
                 display_prefix: str = None,
                 prefix_error_exclude: Optional[List[str]] = None,
                 bolt_status: Optional[BoltStatus] = None,
                 auto_reacts: Optional[Dict[int, Tuple[str]]] = None,
                 *args, **kwargs) -> None:
        super().__init__(command_prefix, *args, **kwargs)
        self.display_prefix = display_prefix
        self.debug_mode = debug_mode
        self.prefix_error_exclude = prefix_error_exclude
        self.bolt_status = bolt_status
        self.auto_reacts = auto_reacts
        if isinstance(command_prefix, str):
            self.display_prefix = command_prefix
        else:
            if display_prefix is None:
                raise ValueError("You must pass 'display_prefix' if you don't pass a string as 'command_prefix'.")

    # --- Event handlers ---
    async def on_message(self, message: discord.Message):
        msg = message.content.lower()
        if self.auto_reacts is not None:
            for emoji, keywords in self.auto_reacts.items():
                if any([keyword in msg for keyword in keywords]):
                    try:
                        if e := discord.utils.find(lambda x: x.id == emoji, self.emojis):
                            await message.add_reaction(e)
                        else:
                            print(f"Error: Invalid or inaccessible emoji in config: {emoji}")
                    except discord.Forbidden:
                        print(f"Error: Missing Permissions to add reactions in {message.channel.id}")
        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, err: commands.CommandError):
        if isinstance(err, commands.UserInputError):
            await misc.add_react(ctx.message, misc.emojis.warning)
            await ctx.send_help(ctx.command)
        elif isinstance(err, commands.CommandNotFound):
            if self.prefix_error_exclude:
                if ctx.invoked_with.startswith(self.prefix_error_exclude):
                    return
            await misc.add_react(ctx.message, misc.emojis.question)
        elif isinstance(err, commands.CheckFailure):
            # Add handling of other subclasses of CheckFailure as needed.
            if isinstance(err, commands.NotOwner):
                await misc.add_react(ctx.message, misc.emojis.no_entry)
            else:
                await misc.add_react(ctx.message, misc.emojis.x)
        elif isinstance(err, commands.DisabledCommand):
            await misc.add_react(ctx.message, misc.emojis.bangbang)
        elif isinstance(err, (commands.CommandInvokeError, commands.ConversionError)):
            # Emulating discord.py's default beaviour.
            print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)
            embed = embeds.error_embed_factory(ctx, err.original, self.debug_mode)
            embed.description += f"\n`{type(err).__name__}`"  # type: ignore   # impossible type mismatch
            await misc.add_react(ctx.message, misc.emojis.warning)
            await ctx.send(embed=embed)
        else:
            # Emulating discord.py's default beaviour. (safest bet)
            print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)
            await misc.add_react(ctx.message, misc.emojis.warning)

    async def on_ready(self):
        print(f"Logged in as: {self.user} - {self.user.id}")
        print("------")
        if self.bolt_status:
            if self.bolt_status.mode == StatusMode.time:
                self._ensure_activity_time.start()
            elif self.bolt_status.mode == StatusMode.random:
                self._ensure_activity_random.start()
            elif self.bolt_status.mode == StatusMode.static:
                self._ensure_activity_fixed.start()

    # --- Background loops ---
    @tasks.loop(minutes=5)
    async def _ensure_activity_time(self):
        settings = self.bolt_status
        status = settings.status_list[0]
        try:
            tz = pytz.timezone(settings.time_tz)
        except pytz.exceptions.UnknownTimeZoneError:
            status = "with invalid timezones"
            if settings.show_help:
                status += f" | {self.display_prefix}help"
            await self.change_presence(activity=discord.Game(name=status))
            return
        now = datetime.now(tz=tz).time()
        for sts in settings.time_list:
            start_time = time(hour=sts[1][0], minute=sts[1][1], tzinfo=tz)
            end_time = time(hour=sts[2][0], minute=sts[2][1], tzinfo=tz)
            if start_time < now <= end_time:
                status = sts[0]
                if settings.show_help:
                    status += f" | {self.display_prefix}help"
        await self.change_presence(activity=discord.Game(name=status))

    @tasks.loop(minutes=5)
    async def _ensure_activity_random(self):
        settings = self.bolt_status
        status = random.choice(settings.status_list)
        if settings.show_help:
            status += f" | {self.display_prefix}help"
        await self.change_presence(activity=discord.Game(name=status))

    @tasks.loop(minutes=5)
    async def _ensure_activity_fixed(self):
        settings = self.bolt_status
        status = settings.status_list[0]
        if settings.show_help:
            status += f" | {self.display_prefix}help"
        await self.change_presence(activity=discord.Game(name=status))
