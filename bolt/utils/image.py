"""
Image utils for bolt-discord
---
Copyright (c) 2020 miaowware
Released under the BSD 3-Clause License.
"""


import collections
import json


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
