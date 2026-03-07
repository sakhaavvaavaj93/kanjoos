import asyncio
from pyrogram import Client, idle
from modules.clientbot import run as run_client
from modules.config import API_ID, API_HASH, BOT_TOKEN, get_session

bot = Client(
    "my_bot",       # Pass the name as the first positional argument
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="plugins")
)

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
