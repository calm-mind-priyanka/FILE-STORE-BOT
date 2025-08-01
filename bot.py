from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# === Hardcoded Bot Config ===
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
MONGO_DB_URI = "your_mongodb_uri"
DB_NAME = "filestore"

# === MongoDB Setup ===
mongo = MongoClient(MONGO_DB_URI)
db = mongo[DB_NAME]
collection = db["files"]

# === Pyrogram Bot ===
app = Client("filestore-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# === Start Command ===
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user = message.from_user.first_name
    await message.reply(
        f"ʜᴇʟʟᴏ, {user} ℡ ️️ᯤ̸\n\n"
        "ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴀɢᴇ ʙᴏᴛ. 📁\n\n"
        "ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴅᴏᴄᴜᴍᴇɴᴛ, ᴠɪᴅᴇᴏ, ᴀᴜᴅɪᴏ ᴏʀ ᴀɴɪᴍᴀᴛɪᴏɴ, "
        "ᴀɴᴅ ɪ ᴡɪʟʟ ꜱᴛᴏʀᴇ ɪᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ, "
        "ꜱʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ 🔗 ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴛʜᴀᴛ ꜰɪʟᴇ ᴀɴʏᴛɪᴍᴇ!\n\n"
        "‼️ ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ɢᴇᴛ ꜰᴜʟʟ ᴅᴇᴛᴀɪʟꜱ ᴏꜰ ᴀʟʟ ᴍʏ ꜰᴇᴀᴛᴜʀᴇꜱ.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("HELP", callback_data="help"),
             InlineKeyboardButton("ABOUT", callback_data="about")],
            [InlineKeyboardButton("UPDATE CHANNEL", url="https://t.me/YourChannel")],
            [InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/YourSupport")],
            [InlineKeyboardButton("DEVELOPER", url="https://t.me/YourUsername")]
        ])
    )

# === File Handler ===
@app.on_message(filters.document | filters.video | filters.audio | filters.animation)
async def save_file(client, message: Message):
    file_id = message.document or message.video or message.audio or message.animation
    if file_id:
        file_info = {
            "file_id": file_id.file_id,
            "file_name": file_id.file_name,
            "file_unique_id": file_id.file_unique_id,
            "user_id": message.from_user.id
        }
        collection.insert_one(file_info)
        share_link = f"https://t.me/{(await client.get_me()).username}?start={file_id.file_unique_id}"
        await message.reply(f"✅ File saved!\n🔗 Shareable Link: {share_link}")

# === Callback Handlers ===
@app.on_callback_query()
async def cb_handler(client, callback_query):
    data = callback_query.data
    if data == "help":
        await callback_query.message.edit_text("Send me any file and I will give you a permanent shareable link.")
    elif data == "about":
        await callback_query.message.edit_text("I'm a Pyrogram + MongoDB based file store bot.")

# === Run Bot ===
app.run()
