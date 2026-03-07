import os
from os import getenv
from dotenv import load_dotenv
import aiohttp
from typing import List

load_dotenv()

# --- 1. Global Variables (Static) ---
API_ID = int(getenv("API_ID", "1755145"))
API_HASH = getenv("API_HASH", "f1933c5fb9c5c7b4fc1240ae36c809df")
BOT_TOKEN = getenv("BOT_TOKEN", "8233014670:AAG5_XGjwq2yAo28v8nGz54GT5yqpetPQuU")
STRING_SESSION = getenv("STRING_SESSION", "BQAayAk...") # Keep your full string here
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "1200"))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1254508607").split()))

# Add your specific hardcoded user if needed
if 1282754256 not in SUDO_USERS:
    SUDO_USERS.append(1282754256)

que = {}
admins = {}

# --- 2. Session Management (Lazy Initialization) ---
# We define it as None so it doesn't trigger the "no running event loop" error on import.
aiohttpsession = None

async def get_session():
    global aiohttpsession
    if aiohttpsession is None or aiohttpsession.closed:
        aiohttpsession = aiohttp.ClientSession()
    return aiohttpsession
