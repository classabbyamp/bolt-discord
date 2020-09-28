"""
Common tools for the bot.
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


from types import SimpleNamespace
from pathlib import Path


__all__ = ["cat", "paths"]


# --- Common values ---

# meow
cat = SimpleNamespace(
    lookup="Information Lookup",
    fun="Fun",
    maps="Mapping",
    ref="Reference",
    study="Exam Study",
    weather="Land and Space Weather",
    admin="Bot Control",
)

paths = SimpleNamespace(
    data=Path("./testbot/data/"),
    resources=Path("./testbot/resources/"),
    img=Path("./testbot/resources/img/"),
    bandcharts=Path("./testbot/resources/img/bandcharts/"),
    maps=Path("./testbot/resources/img/maps/"),
)


# --- Classes ---


# TODO in qrm: this should be in the ext that needs it
class CallsignInfoData:
    """Represents a country's callsign info"""
    def __init__(self, data: list):
        self.title: str = data[0]
        self.desc: str = data[1]
        self.calls: str = data[2]
        self.emoji: str = data[3]
