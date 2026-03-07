import os
from os import getenv
from dotenv import load_dotenv
import aiohttp
import asyncio

_session = None

async def get_session():
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session
    
load_dotenv()
que = {}
admins = {}

# Initialize as None instead of calling ClientSession()
aiohttpsession = None

async def get_session():
    global aiohttpsession
    # Create the session only if it doesn't exist or was closed
    if aiohttpsession is None or aiohttpsession.closed:
        aiohttpsession = aiohttp.ClientSession()
    return aiohttpsession
    
API_ID = int(getenv("API_ID", "1755145"))
API_HASH = getenv("API_HASH", "f1933c5fb9c5c7b4fc1240ae36c809df")
BOT_TOKEN = getenv("BOT_TOKEN", "8233014670:AAG5_XGjwq2yAo28v8nGz54GT5yqpetPQuU")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "1200"))
STRING_SESSION = getenv("STRING_SESSION", "BQAayAkALwhzWzgK02ZKzJ4nzQh3zIeaprf5ja3FjOq4GotUCkpl4CdGfvCbmswYXbanpNEqi2Twxt-3GXTuU754rLRn-Q9XSqov4edAhhv0shBnU9wuQrPkjBN1qX8oUmXIMgapzSAEHw28qY63N4L5WAjurK6YJfHGne9jVnLS8vgPVMklGKuNUvVEqwb9WkbZOMHc0SA7x9ymRmD3a-1RS2f_vYztMi8ATSbiohQc72PuFZrRftkEmylmC_R3yMjhbhebADSSvlVIUw0vNAkP_IpccPtok8j6skLLquSIee3ovxeRdwxGVLT_L6WvpEtIuxMbeVjT3BKjjeos_zudM7OhyQAAAAHmxfTeAA")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1254508607").split()))
aiohttpsession = aiohttp.ClientSession()
