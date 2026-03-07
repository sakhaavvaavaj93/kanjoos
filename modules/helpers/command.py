from typing import Union, List
from pyrogram import filters
from modules.config import COMMAND_PREFIXES

# 1. Standard Group Filters
other_filters = filters.group & ~ filters.edited & ~ filters.via_bot & ~ filters.forwarded

# 2. Standard Private Filters
other_filters2 = filters.private & ~ filters.edited & ~ filters.via_bot & ~ filters.forwarded

# 3. Standard Command (uses / or !)
def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)
