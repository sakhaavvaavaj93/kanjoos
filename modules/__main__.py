import asyncio
import os
import threading
from flask import Flask
from pyrogram import Client, idle
from modules.clientbot import run as run_client
from modules.config import API_ID, API_HASH, BOT_TOKEN, get_session, aiohttpsession

# 1. Flask setup for Health Checks
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    # Use PORT from environment (default 10000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Pyrogram Client setup
bot = Client(
    ":memory:", 
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():
    try:
        # Start Flask in a background thread
        threading.Thread(target=run_flask, daemon=True).start()
        print("Flask Health Check started!")

        # Initialize the aiohttp session
        await get_session() 
        print("Aiohttp session initialized!")

        # Start the primary bot
        await bot.start()
        print("Bot is online!")

        # Start additional module logic (PyTgCalls, etc.)
        await run_client() 

        # Keep the script alive
        await idle()

    except Exception as e:
        print(f"Startup failed: {e}")

    finally:
        # 5. Graceful shutdown
        from modules import config
        if config.aiohttpsession:
            await config.aiohttpsession.close()
            print("Aiohttp session closed.")
        
        await bot.stop()
        print("Bot stopped.")

if __name__ == "__main__":
    # Standard asyncio entry point
    asyncio.run(main())
