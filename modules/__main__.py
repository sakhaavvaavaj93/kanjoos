import asyncio
from pyrogram import Client, idle
from modules.clientbot import run as run_client
from modules.config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Bot with modern in_memory flag
bot = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="plugins")
)

async def main():
    # Start the primary bot
    await bot.start()
    print("Bot started!")

    # Start your additional module logic
    # If run_client() is async, use: await run_client()
    # If it starts its own client, ensure they don't conflict
    await run_client() 

    # Keep the script alive and listen for signals (SIGINT, SIGTERM)
    await idle()
    
    # Graceful shutdown
    await bot.stop()

if __name__ == "__main__":
    # Use the [standard asyncio entry point](https://docs.python.org)
    asyncio.run(main())
