from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# === Bot Config ===
API_ID = 24222039
API_HASH = "6dd2dc70434b2f577f76a2e993135662"
BOT_TOKEN = "your_bot_token"  # Replace with actual token
MONGO_DB_URI = "mongodb+srv://chatbot10:j@cluster0.9esnn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "filestore"

# === MongoDB Setup ===
mongo = MongoClient(MONGO_DB_URI)
db = mongo[DB_NAME]
collection = db["files"]

# === Pyrogram Bot ===
app = Client("filestore-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# === Start Command with File Retrieval ===
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user = message.from_user.first_name
    args = message.text.split(" ", 1)

    # If user clicked shareable link with file id
    if len(args) > 1:
        file_unique_id = args[1]
        file_data = collection.find_one({"file_unique_id": file_unique_id})
        if file_data:
            await message.reply_document(file_data["file_id"])
        else:
            await message.reply("❌ File not found.")
        return

    # Normal /start command
    await message.reply(
        f"ʜᴇʟʟᴏ, {user} ℡ ️️ᯤ̸\n\n"
        "ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴀɢᴇ ʙᴏᴛ. 📁\n\n"
        "ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴅᴏᴄᴜᴍᴇɴᴛ, ᴠɪᴅᴇᴏ, ᴀᴜᴅɪᴏ ᴏʀ ᴀɴɪᴍᴀᴛɪᴏɴ, "
        "ᴀɴᴅ ɪ ᴡɪʟʟ ꜱᴛᴏʀᴇ ɪᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ ᴀɴᴅ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ, "
        "ꜱʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ 🔗 ᴛᴏ ᴀᴄᴄᴇꜱꜱ ᴛʜᴀᴛ ꜰɪʟᴇ ᴀɴʏᴛɪᴍᴇ!\n\n"
        "‼️ ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ᴛᴏ ɢᴇᴛ ꜰᴜʟʟ ᴅᴇᴛᴀɪʟꜱ.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("HELP", callback_data="help"),
             InlineKeyboardButton("ABOUT", callback_data="about")],
            [InlineKeyboardButton("UPDATE CHANNEL", url="https://t.me/YourChannel")],
            [InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/YourSupport")],
            [InlineKeyboardButton("DEVELOPER", url="https://t.me/YourUsername")]
        ])
    )

# === File Save Handler ===
@app.on_message(filters.document | filters.video | filters.audio | filters.animation)
async def save_file(client, message: Message):
    file = message.document or message.video or message.audio or message.animation
    if file:
        file_info = {
            "file_id": file.file_id,
            "file_name": file.file_name,
            "file_unique_id": file.file_unique_id,
            "user_id": message.from_user.id
        }
        collection.insert_one(file_info)

        bot_username = (await client.get_me()).username
        share_link = f"https://t.me/{bot_username}?start={file.file_unique_id}"
        await message.reply(f"✅ File saved!\n🔗 Shareable Link:\n{share_link}")

# === Callback Buttons ===
@app.on_callback_query()
async def cb_handler(client, callback_query):
    data = callback_query.data
    if data == "help":
        await callback_query.message.edit_text("📁 Just send me a file and I will save it and give you a permanent shareable link.\nYou can share that link with anyone.")
    elif data == "about":
        await callback_query.message.edit_text("🤖 This bot is powered by Pyrogram + MongoDB.\nMade with ❤️ for file storage and retrieval.")

# === Run the Bot ===
app.run()
