from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask
import threading

# === Bot Config ===
API_ID = 24222039
API_HASH = "6dd2dc70434b2f577f76a2e993135662"
BOT_TOKEN = "8248598058:AAHz70ltZ5hAkGcc0zGo1vGKnrn2FbA_fe8"
MONGO_DB_URI = "mongodb+srv://chatbot10:j@cluster0.9esnn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "filestore"

# === MongoDB Setup ===
mongo = MongoClient(MONGO_DB_URI)
db = mongo[DB_NAME]
collection = db["files"]

# === Health Check Server ===
health_app = Flask(__name__)

@health_app.route('/')
def health():
    return 'Bot is running!', 200

def run_health_server():
    health_app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_health_server).start()

# === Pyrogram Bot ===
app = Client("filestore-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# === Start Command (with File Retrieval) ===
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user = message.from_user.first_name
    args = message.text.split(" ", 1)

    if len(args) > 1:
        file_unique_id = args[1]
        file_data = collection.find_one({"file_unique_id": file_unique_id})
        if file_data:
            try:
                await message.reply_document(file_data["file_id"])
            except Exception as e:
                await message.reply("❌ Error sending file. Maybe it's too large or expired.")
        else:
            await message.reply("❌ File not found.")
        return

    await message.reply(
        f"Hello {user} 👋\n\n"
        "I am a powerful File Store Bot.\n"
        "📁 Send me any file and I will save it and give you a **permanent shareable link** 🔗\n\n"
        "Just click HELP to know more.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 HELP", callback_data="help"),
             InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")],
            [InlineKeyboardButton("🔔 UPDATES", url="https://t.me/YourChannel")],
            [InlineKeyboardButton("👥 SUPPORT", url="https://t.me/YourSupport")]
        ])
    )

# === File Save Handler ===
@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.animation))
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
        await message.reply(f"✅ File saved!\n\n🔗 **Shareable Link:**\n{share_link}")

# === Callback Buttons ===
@app.on_callback_query()
async def cb_handler(client, callback_query):
    data = callback_query.data
    if data == "help":
        await callback_query.message.edit_text(
            "📁 **How to Use:**\n\n"
            "1. Send me any file.\n"
            "2. I will store it in the database.\n"
            "3. You will get a permanent link to access it anytime.\n\n"
            "✅ You can share this link with anyone!"
        )
    elif data == "about":
        await callback_query.message.edit_text(
            "🤖 **FileStore Bot**\n"
            "Made with ❤️ using Pyrogram + MongoDB\n"
            "🔐 Store and share files up to 2GB.\n\n"
            "👨‍💻 Developer: @YourUsername"
        )

# === Run the Bot ===
app.run()
