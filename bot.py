import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URI = os.getenv("MONGO_DB_URI")
DB_NAME = os.getenv("DB_NAME", "filestore")

client = Client("filestore-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = MongoClient(DB_URI)[DB_NAME]
files_collection = db["files"]

START_TEXT = """ʜᴇʟʟᴏ, {} ℡ ️️ᯤ̸

ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴀɢᴇ ʙᴏᴛ. 📁

ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴀɴᴅ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ, ꜱʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ 🔗 ᴛᴏ ᴀᴄᴄᴇꜱꜱ ɪᴛ.
"""

BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("HELP", callback_data="help"), InlineKeyboardButton("ABOUT", callback_data="about")],
    [InlineKeyboardButton("UPDATE CHANNEL", url="https://t.me/yourchannel")],
    [InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/yourgroup")],
    [InlineKeyboardButton("DEVELOPER", url="https://t.me/yourusername")]
])

@client.on_message(filters.private & filters.command("start"))
def start_handler(bot, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        file = files_collection.find_one({"file_id": file_id})
        if file:
            bot.send_cached_media(
                chat_id=message.chat.id,
                file_id=file["file_unique_id"],
                caption="📁 Your requested file"
            )
        else:
            message.reply_text("❌ File not found or has been deleted.")
    else:
        name = message.from_user.mention
        message.reply_text(START_TEXT.format(name), reply_markup=BUTTONS)

@client.on_message(filters.private & filters.document | filters.video | filters.audio | filters.animation)
def save_file(bot, message):
    media = message.document or message.video or message.audio or message.animation
    file_id = media.file_id
    unique_id = media.file_unique_id[:10]

    files_collection.insert_one({
        "file_id": unique_id,
        "file_unique_id": file_id
    })

    link = f"https://t.me/{bot.me.username}?start={unique_id}"
    message.reply_text(f"✅ File saved!\n\n🔗 Here is your permanent link:\n{link}")

client.run()
