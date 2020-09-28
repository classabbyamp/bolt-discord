"""
misc utils for bolt-discord
---
Copyright (c) 2020 miaowware
Released under the BSD 3-Clause License.
"""

from types import SimpleNamespace

import discord


colours = SimpleNamespace(
    good=0x43B581,
    neutral=0x7289DA,
    bad=0xF04747,
)


emojis = SimpleNamespace(
    check_mark="✅",
    x="❌",
    warning="⚠️",
    question="❓",
    no_entry="⛔",
    bangbang="‼️",
    a="🇦",
    b="🇧",
    c="🇨",
    d="🇩",
)


async def add_react(msg: discord.Message, react: str):
    try:
        await msg.add_reaction(react)
    except discord.Forbidden:
        print(f"[!!] Missing permissions to add reaction in '{msg.channel.id}'!")
