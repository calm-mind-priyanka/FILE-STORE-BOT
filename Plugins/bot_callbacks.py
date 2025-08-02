from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto

# -- HELP CALLBACK
@Client.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_caption(
        caption=(
            "**⚠️ Help Info**\n\n"
            "• You will get to see all this in the settings command.\n"
            "• You can do on/off in file protection.\n"
            "• You can do on/off in permanent link.\n"
            "• You can set custom file caption.\n"
            "• You can add two tutorial video link.\n"
            "• You can add one shortlink for direct file link.\n"
            "• You can add two shortlink for each verify.\n"
            "• You can add user verified info log channel.\n"
            "• You can do on/off for 1st and 2nd verification.\n"
            "• You can add 2nd verification time.\n"
            "• You can add multiple force subscribe channel.\n"
            "• You can add post channel and tutorial and poster.\n"
            "✅ You can change all these settings according to your need."
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])
    )

# -- ABOUT CALLBACK (unchanged)
@Client.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_caption(
        caption=(
            "**╭────[ ᴍʏ ᴅᴇᴛᴀɪʟs ]───⍟**\n"
            "**├⍟ ᴍʏ ɴᴀᴍᴇ :** [ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ](https://t.me/File_Store_iBot)\n"
            "**├⍟ ᴏᴡɴᴇʀ :** [sɪʟɪᴄᴏɴ ᴏꜰꜰɪᴄɪᴀʟ](https://t.me/Silicon_Official)\n"
            "**├⍟ ʟɪʙʀᴀʀʏ :** ᴘʏʀᴏɢʀᴀᴍ\n"
            "**├⍟ ʟᴀɴɢᴜᴀɢᴇ :** ᴘʏᴛʜᴏɴ 𝟹\n"
            "**├⍟ ᴅᴀᴛᴀʙᴀꜱᴇ :** ᴍᴏɴɢᴏ ᴅʙ\n"
            "**├⍟ ꜱᴇʀᴠᴇʀ :** ʜᴇʀᴏᴋᴜ\n"
            "**├⍟ ꜱᴛᴀᴛᴜꜱ :** ᴠ𝟷.𝟶 [ ꜱᴛᴀʙʟᴇ ]\n"
            "**╰───────────────⍟**"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])
    )

# -- BACK CALLBACK TO START MENU
@Client.on_callback_query(filters.regex("back_to_start"))
async def back_to_start(client, callback_query: CallbackQuery):
    user = callback_query.from_user.first_name
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media="https://te.legra.ph/file/2d74c0aa6a2bb2174b128.jpg",  # Replace with your actual image link
            caption=(
                f"ʜᴇʟʟᴏ {user},\n\n"
                "̸ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ ꜱᴛᴏʀᴀɢᴇ ʙᴏᴛ. 📁\n"
                "ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴀɴᴅ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ.\n"
                "ɪ ᴄᴀɴ ʙᴇ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘꜱ ᴀꜱ ᴡᴇʟʟ."
            )
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 HELP", callback_data="help")],
            [InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")],
            [InlineKeyboardButton("🔔 UPDATE", url="https://t.me/YourChannel"),
             InlineKeyboardButton("👥 SUPPORT", url="https://t.me/YourSupport")],
            [InlineKeyboardButton("👨‍💻 DEVELOPER", url="https://t.me/YourUsername")]
        ])
    )
