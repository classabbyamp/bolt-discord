"""
exceptions for bolt-discord
---
Copyright (c) 2020 miaowware
Released under the BSD 3-Clause License.
"""


import aiohttp


class BotHTTPError(Exception):
    """Raised whan a requests fails (status != 200) in a command."""
    def __init__(self, response: aiohttp.ClientResponse):
        msg = f"Request failed: {response.status} {response.reason}"
        super().__init__(msg)
        self.response = response
        self.status = response.status
        self.reason = response.reason
