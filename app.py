from balethon import Client
from balethon.objects import Message
import os

token = "458869954:0gnj0LISkmMk7xR34tTXlnsH21F7Wmd0g"
client = Client(token=token)

@client.on_message()
async def handle_message(message: Message):
    await message.reply("✅ ربات آنلاین است!")

if __name__ == "__main__":
    print("✅ ربات در حال اجراست...")
    client.run()