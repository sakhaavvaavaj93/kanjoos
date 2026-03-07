import asyncio
from pyrogram import Client, idle
from modules.clientbot import run as run_client
from modules.config import API_ID, API_HASH, BOT_TOKEN, get_session # 1. Import get_session

# ... (Client initialization remains the same)

async def main():
    # 2. Initialize the aiohttp session FIRST
    # This sets config.aiohttpsession globally while the loop is active
    await get_session() 
    print("Aiohttp session initialized!")

    # 3. Start the primary bot
    await bot.start()
    print("Bot started!")

    # Start your additional module logic
    await run_client() 

    # Keep the script alive
    await idle()
    
    # 4. Graceful shutdown: Close the session when done
    from modules import config
    if config.aiohttpsession:
        await config.aiohttpsession.close()
        print("Aiohttp session closed.")

    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
