"""
Common tools for the bot.
---
Copyright (C) 2019-2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import collections
import json
from types import SimpleNamespace
from pathlib import Path

import discord.ext.commands as commands

from .data import options as opt


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

class ImageMetadata:
    """Represents the metadata of a single image."""
    def __init__(self, metadata: list):
        self.filename: str = metadata[0]
        self.name: str = metadata[1]
        self.long_name: str = metadata[2]
        self.description: str = metadata[3]
        self.source: str = metadata[4]
        self.emoji: str = metadata[5]


class ImagesGroup(collections.abc.Mapping):
    """Represents a group of images, loaded from a meta.json file."""
    def __init__(self, file_path):
        self._images = {}
        self.path = file_path

        with open(file_path, "r") as file:
            images: dict = json.load(file)
        for key, imgdata in images.items():
            self._images[key] = ImageMetadata(imgdata)

    # Wrappers to implement dict-like functionality
    def __len__(self):
        return len(self._images)

    def __getitem__(self, key: str):
        return self._images[key]

    def __iter__(self):
        return iter(self._images)

    # str(): Simply return what it would be for the underlaying dict
    def __str__(self):
        return str(self._images)


# TODO in qrm: this should be in the ext that needs it
class CallsignInfoData:
    """Represents a country's callsign info"""
    def __init__(self, data: list):
        self.title: str = data[0]
        self.desc: str = data[1]
        self.calls: str = data[2]
        self.emoji: str = data[3]


# --- Checks ---

async def check_if_owner(ctx: commands.Context):
    # TODO needs rework (opt.owner_uids)
    if ctx.author.id in opt.owners_uids:
        return True
    raise commands.NotOwner
