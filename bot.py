from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask
import threading
import os

# === Bot Config ===
API_ID = 24222039
API_HASH = "6dd2dc70434b2f577f76a2e993135662"
BOT_TOKEN = "8248598058:AAHz70ltZ5hAkGcc0zGo1vGKnrn2FbA_fe8"
MONGO_DB_URI = "mongodb+srv://rpeditz:rpeditz@rpeditz.3vkebbh.mongodb.net/?retryWrites=true&w=majority&appName=rpeditz"
DB_NAME = "filestore"

# === MongoDB Setup ===
try:
    mongo = MongoClient(MONGO_DB_URI)
    db = mongo[DB_NAME]
    collection = db["files"]
    print("✅ MongoDB connected.")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")

# === Health Check Server ===
health_app = Flask(__name__)

@health_app.route('/')
def health():
    return 'Bot is running!', 200

def run_health_server():
    health_app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_health_server).start()

# === Pyrogram Bot ===
app = Client(
    "filestore-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

# === /start Command ===
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user = message.from_user.first_name
    args = message.text.split(" ", 1)

    if len(args) > 1:
        file_unique_id = args[1]
        file_data = collection.find_one({"file_unique_id": file_unique_id})
        if file_data:
            file_id = file_data["file_id"]
            file_name = file_data.get("file_name", "File")
            media_type = file_data.get("media_type", "document")

            try:
                if media_type == "video":
                    await message.reply_video(file_id, caption=file_name)
                elif media_type == "audio":
                    await message.reply_audio(file_id, caption=file_name)
                elif media_type == "photo":
                    await message.reply_photo(file_id, caption=file_name)
                elif media_type == "animation":
                    await message.reply_animation(file_id, caption=file_name)
                else:
                    await message.reply_document(file_id, caption=file_name)
            except Exception as e:
                await message.reply(f"❌ Error sending file: {e}")
        else:
            await message.reply("❌ File not found.")
        return

    await message.reply_photo(
        photo="https://graph.org/file/5cf384404bf0f1e5cdd30-cb1c81c282651396d9.jpg",
        caption=(
            f"ʜᴇʟʟᴏ {user},\n\n"
            "̸ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴀɢᴇ ʙᴏᴛ. 📁"
            "ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴅᴏᴄᴜᴍᴇɴᴛ, ᴠɪᴅᴇᴏ, ᴀᴜᴅɪᴏ ᴏʀ ᴀɴɪᴍᴀᴛɪᴏɴ, "
            "ᴀɴᴅ ɪ ᴡɪʟʟ ꜱᴛᴏʀᴇ ɪᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢɪᴠᴇ ʏᴏᴜ "
            "ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ, ꜱʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ 🔗 ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴛʜᴀᴛ ꜰɪʟᴇ ᴀɴʏᴛɪᴍᴇ!‼️\n\n"
            "ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ɢᴇᴛ ꜰᴜʟʟ ᴅᴇᴛᴀɪʟꜱ ᴏꜰ ᴀʟʟ ᴍʏ ꜰᴇᴀᴛᴜʀᴇꜱ."
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 HELP", callback_data="help")],
            [InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")],
            [InlineKeyboardButton("🔔 UPDATE", url="https://t.me/YourChannel"),
             InlineKeyboardButton("👥 SUPPORT", url="https://t.me/YourSupport")],
            [InlineKeyboardButton("👨‍💻 DEVELOPER", url="https://t.me/YourUsername")]
        ])
    )

# === Save All Media ===
@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.animation | filters.photo))
async def save_file(client, message: Message):
    media = (
        message.document
        or message.video
        or message.audio
        or message.animation
        or message.photo
    )
    if not media:
        await message.reply("❌ Unsupported file type.")
        return

    file_unique_id = getattr(media, "file_unique_id", None)
    file_id = getattr(media, "file_id", None)
    file_name = getattr(media, "file_name", "File")
    media_type = media.__class__.__name__.lower()

    file_info = {
        "file_id": file_id,
        "file_name": file_name,
        "file_unique_id": file_unique_id,
        "media_type": media_type,
        "user_id": message.from_user.id
    }

    if not collection.find_one({"file_unique_id": file_unique_id}):
        collection.insert_one(file_info)

    bot_username = (await client.get_me()).username
    share_link = f"https://t.me/{bot_username}?start={file_unique_id}"

    await message.reply(
        f"✅ File saved successfully!\n\n"
        f"🔗 **Shareable Link:**\n{share_link}"
    )

# === Run the Bot ===
app.run()
