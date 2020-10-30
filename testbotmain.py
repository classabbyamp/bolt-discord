#!/usr/bin/env python3
"""
qrm, a bot for Discord
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import asyncio
from types import SimpleNamespace

import bolt
import discord
from discord.ext import commands

import testbot.info as info
import testbot.common as cmn
import testbot.utils.connector as conn
from bolt.utils import embeds, misc

import testbot.data.keys as keys
import testbot.data.options as opt


# --- Settings ---

exit_code = 1  # The default exit code. ?shutdown and ?restart will change it accordingly (fail-safe)

ext_dir = "testbot.exts"  # The name of the directory where extensions are located.

debug_mode = opt.debug  # Separate assignement in-case we define an override (ternary operator goes here)

status = bolt.BoltStatus(mode=bolt.StatusMode(opt.status_mode),
                         status_list=opt.statuses,
                         time_tz=opt.status_tz,
                         time_list=opt.time_statuses,
                         show_help=opt.show_help)

# --- Bot setup ---

# Loop/aiohttp stuff
loop = asyncio.get_event_loop()
connector = loop.run_until_complete(conn.new_connector())

bot = bolt.Bolt(opt.prefix,
                display_prefix=opt.display_prefix,
                prefix_error_exclude=["?", "!"],
                bolt_status=status,
                auto_reacts=opt.msg_reacts,
                case_insensitive=True,
                description=info.description,
                help_command=commands.MinimalHelpCommand(),
                loop=loop,
                connector=connector)

# Simple way to access bot-wide stuff in extensions.
bot.qrm = SimpleNamespace()

# Let's store stuff here.
bot.qrm.connector = connector
bot.qrm.debug_mode = debug_mode  # TODO: NUKE


# --- Commands ---

@bot.command(name="restart", aliases=["rs"], category=cmn.cat.admin)
@commands.check(cmn.check_if_owner)
async def _restart_bot(ctx: commands.Context):
    """Restarts the bot."""
    global exit_code
    await misc.add_react(ctx.message, misc.emojis.check_mark)
    print(f"[**] Restarting! Requested by {ctx.author}.")
    exit_code = 42  # Signals to the wrapper script that the bot needs to be restarted.
    await bot.logout()


@bot.command(name="shutdown", aliases=["shut"], category=cmn.cat.admin)
@commands.check(cmn.check_if_owner)
async def _shutdown_bot(ctx: commands.Context):
    """Shuts down the bot."""
    global exit_code
    await misc.add_react(ctx.message, misc.emojis.check_mark)
    print(f"[**] Shutting down! Requested by {ctx.author}.")
    exit_code = 0  # Signals to the wrapper script that the bot should not be restarted.
    await bot.logout()


@bot.group(name="extctl", aliases=["ex"], case_insensitive=True, category=cmn.cat.admin)
@commands.check(cmn.check_if_owner)
async def _extctl(ctx: commands.Context):
    """Extension control commands.
    Defaults to `list` if no subcommand specified"""
    if ctx.invoked_subcommand is None:
        cmd = bot.get_command("extctl list")
        await ctx.invoke(cmd)


@_extctl.command(name="list", aliases=["ls"])
async def _extctl_list(ctx: commands.Context):
    """Lists loaded extensions."""
    embed = embeds.embed_factory(ctx)
    embed.title = "Loaded Extensions"
    embed.description = "\n".join(["‣ " + x.split(".")[1] for x in bot.extensions.keys()])
    await ctx.send(embed=embed)


@_extctl.command(name="load", aliases=["ld"])
async def _extctl_load(ctx: commands.Context, extension: str):
    """Loads an extension."""
    bot.load_extension(ext_dir + "." + extension)
    await misc.add_react(ctx.message, misc.emojis.check_mark)


@_extctl.command(name="reload", aliases=["rl", "r", "relaod"])
async def _extctl_reload(ctx: commands.Context, extension: str):
    """Reloads an extension."""
    if ctx.invoked_with == "relaod":
        pika = bot.get_emoji(opt.pika)
        if pika:
            await misc.add_react(ctx.message, pika)
    bot.reload_extension(ext_dir + "." + extension)
    await misc.add_react(ctx.message, misc.emojis.check_mark)


@_extctl.command(name="unload", aliases=["ul"])
async def _extctl_unload(ctx: commands.Context, extension: str):
    """Unloads an extension."""
    bot.unload_extension(ext_dir + "." + extension)
    await misc.add_react(ctx.message, misc.emojis.check_mark)


# --- Run ---

for ext in opt.exts:
    bot.load_extension(ext_dir + "." + ext)


try:
    bot.run(keys.discord_token)

except discord.LoginFailure as ex:
    # Miscellaneous authentications errors: borked token and co
    if bot.qrm.debug_mode:
        raise
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:
    # When the connection to the gateway (websocket) is closed
    if bot.qrm.debug_mode:
        raise
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    if bot.qrm.debug_mode:
        raise
    raise SystemExit("ConnectionResetError: {}".format(ex))


# --- Exit ---
# Codes for the wrapper shell script:
# 0 - Clean exit, don't restart
# 1 - Error exit, [restarting is up to the shell script]
# 42 - Clean exit, do restart

raise SystemExit(exit_code)
