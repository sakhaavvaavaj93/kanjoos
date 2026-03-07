import asyncio
from pyrogram import Client, idle
from modules.clientbot import run as run_client
from modules.config import API_ID, API_HASH, BOT_TOKEN, get_session

bot = Client(
    ":memory:", # Use this special name for an in-memory session
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def main():
    # 1. Initialize the aiohttp session FIRST (while loop is active)
    await get_session() 
    print("Aiohttp session initialized!")

    # 2. Start the primary bot
    await bot.start()
    print("Bot started!")

    # 3. Start your additional module logic
    await run_client() 

    # 4. Keep the script alive
    await idle()
    
    # 5. Graceful shutdown: Close session and stop bot
    from modules import config
    if config.aiohttpsession:
        await config.aiohttpsession.close()
        print("Aiohttp session closed.")

    await bot.stop()

if __name__ == "__main__":
    # This creates the event loop and runs main()
    asyncio.run(main())
