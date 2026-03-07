import asyncio
import os
import threading
from flask import Flask
from pyrogram import Client, idle
from modules.clientbot import run as run_client
# Ensure config is imported correctly for the session close logic
import modules.config as config 

# 1. Flask setup
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    # Render REQUIRES host='0.0.0.0'
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# 2. Pyrogram Client
bot = Client(
    ":memory:", 
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():
    try:
        # Start Flask FIRST
        threading.Thread(target=run_flask, daemon=True).start()
        print("Flask Health Check started!")
        
        # Give Flask 1 second to bind to the port (Helps Render status)
        await asyncio.sleep(1)

        # Initialize session
        await config.get_session() 
        print("Aiohttp session initialized!")

        # Start the bot
        await bot.start()
        print("Bot is online!")

        # Start PyTgCalls or ClientBot
        await run_client() 
        print("ClientBot logic running!")

        await idle()

    except Exception as e:
        print(f"CRITICAL ERROR during startup: {e}")

    finally:
        # Improved Cleanup
        if hasattr(config, 'aiohttpsession') and config.aiohttpsession:
            await config.aiohttpsession.close()
            print("Aiohttp session closed.")
        
        if bot.is_connected:
            await bot.stop()
            print("Bot disconnected gracefully.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    finally:
        # Clean up any lingering tasks from pytgcalls
        try:
            pending = asyncio.all_tasks(loop)
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass
        loop.close()
