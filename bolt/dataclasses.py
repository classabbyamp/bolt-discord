"""
Dataclasses for Bolt
---

Copyright (c) 2020 classabbyamp, 0x5c
Released under the BSD 3-Clause License.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


def default_status_list():
    return [""]


def default_time_list():
    return [("", (00, 00), (00, 00))]


class StatusMode(Enum):
    """Represents the type of status."""
    static = "STATIC"
    random = "RANDOM"
    time = "TIME"
    disabled = "NOMESSAGE"


@dataclass
class BoltStatus:
    """
    Represents a Bolt status.

    [INSERT DOCS]

    For StatusType.static, the first item of status_list is used.
    """
    mode: StatusMode
    status_list: List[str] = field(default_factory=default_status_list)
    time_tz: str = "US/Eastern"
    time_list: List[Tuple[str, Tuple[int, int], Tuple[int, int]]] = field(default_factory=default_time_list)
    show_help: bool = False
