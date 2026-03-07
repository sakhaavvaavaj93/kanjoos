import asyncio
import os
import threading
from flask import Flask
from pyrogram import Client, idle
from modules.clientbot import run as run_client
import modules.config as config 

# 1. Flask setup with multi-method support for Render health checks
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    # host='0.0.0.0' is mandatory for Render/Koyeb/Heroku
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# 2. Pyrogram Client setup
bot = Client(
    "kanjoos_bot", # Changed from ":memory:" to a string
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():
    try:
        # Start Flask in a background thread
        threading.Thread(target=run_flask, daemon=True).start()
        print("Flask Health Check started!")
        
        # Give the port a moment to bind
        await asyncio.sleep(1)

        # Initialize the aiohttp session safely within the loop
        await config.get_session() 
        print("Aiohttp session initialized!")

        # Start the bot client with Time Sync retry logic
        try:
            await bot.start()
        except Exception as e:
            if "[16]" in str(e) or "msg_id too low" in str(e).lower():
                print("Time sync error detected. Waiting 5 seconds to retry...")
                await asyncio.sleep(5)
                await bot.start() # Second attempt
            else:
                raise e

        print("Bot is online!")

        # Start your additional module logic (PyTgCalls, etc.)
        await run_client() 
        print("ClientBot logic running!")

        # Keep the script alive
        await idle()

    except Exception as e:
        print(f"CRITICAL ERROR during startup: {e}")

    finally:
        # Graceful cleanup
        if hasattr(config, 'aiohttpsession') and config.aiohttpsession:
            await config.aiohttpsession.close()
            print("Aiohttp session closed.")
        
        if bot.is_connected:
            await bot.stop()
            print("Bot disconnected gracefully.")

if __name__ == "__main__":
    # Manual loop management to satisfy PyTgCalls cleanup requirements
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    finally:
        # Handle lingering tasks (like pytgcalls cleanup) before closing loop
        try:
            pending = asyncio.all_tasks(loop)
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass
        
        # We wrap loop.close() in a try-block because pytgcalls often 
        # tries to use the loop during an 'atexit' call.
        try:
            loop.close()
            print("Loop closed.")
        except:
            pass
