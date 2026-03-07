from typing import List
from pyrogram.types import Chat, User
import modules.cache.admins
from modules import config  # Import your config

async def get_administrators(chat: Chat) -> List[User]:
    get = modules.cache.admins.get(chat.id)

    if get:
        return get
    else:
        # 1. Fetch admins from Pyrogram
        administrators = await chat.get_members(filter="administrators")
        to_set = []

        # 2. Example: Using the session to check something externally
        # (e.g., checking if the admin is globally whitelisted)
        session = await config.get_session() 
        
        for administrator in administrators:
            if administrator.can_manage_voice_chats:
                # Example external API call using the session
                # async with session.get(f"https://api.yoursite.com{administrator.user.id}") as resp:
                #     is_valid = await resp.json()
                
                to_set.append(administrator.user.id)

        modules.cache.admins.set(chat.id, to_set)
        return await get_administrators(chat)
