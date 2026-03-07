from pyrogram import Client
# Ensure this path matches where you saved your filter function
from modules.helpers.filters import commandpro 

@Client.on_message(commandpro("ping"))
async def direct_ping(client: Client, message):
    # This will trigger when someone types "ping" without a / or !
    await message.reply("Pong!")
