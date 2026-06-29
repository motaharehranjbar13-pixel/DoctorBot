from balethon import Client
from balethon.objects import Message
import os

client = Client(token="458869954:jMNBFOv_vG1I_wXzUA_eHAsV5f8YIZBEhk")

@client.on_message()
async def handle_message(message: Message):
    await message.reply("✅ ربات آنلاین است!")

if __name__ == "__main__":
    print("✅ ربات در حال اجراست...")
    client.run()