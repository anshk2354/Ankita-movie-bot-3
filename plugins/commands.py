# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, IS_TUTORIAL, PREMIUM_USER
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial
from database.connections_mdb import active_connection
# from plugins.pm_filter import ENABLE_SHORTLINK
import re, asyncio, os, sys
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url="https://t.me/mxmoder")
                ],[
                    InlineKeyboardButton('✪ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url="https://t.me/mxmoder_support"),
                    InlineKeyboardButton('BOT OWNER ', url='https://telegram.me/mxmoder_bot')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
                    InlineKeyboardButton('Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url="https://t.me/mxmoder")
                ],[
                    InlineKeyboardButton('✪ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url="https://t.me/mxmoder_support"),
                    InlineKeyboardButton('BOT OWNER ', url='https://telegram.me/mxmoder_bot')
                 ]]
                    
        
        reply_markup = InlineKeyboardMarkup(buttons)

# Sticker ki jagah message send karna
m = await message.reply_text(
    "✅ Aapka message send ho gaya hai.\nPlease wait... Kuchh hi der mein aapko Mod APK mil jaega.\n\nYour message has been sent.\nYou will receive the mod app in a few minutes"
)

# 20 second wait karo fir message delete karo
await asyncio.sleep(20)
await m.delete()

# Uske baad image send karo with caption and buttons
await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton("❆ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ ❆", url=invite_link.invite_link)
                
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                btn.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", callback_data=f"checksub#{kk}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_photo(
            chat_id=message.from_user.id,
            photo="https://telegra.ph/file/20b4aaaddb8aba646e53c.jpg",
            caption="**You are not in our channel mentioned below, so you are not getting the Mod APK file...\n\nIf you want the Mod APK file, click on the '🍿 Join Our Back-Up Channel 🍿' button below and join our back-up channel.\n\nThen click on the '🔄 Try Again' button below...\n\nAfter that, you will get access to the Mod APK files...**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
                    InlineKeyboardButton('Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url="https://t.me/mxmoder")
                ],[
                    InlineKeyboardButton('✪ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url="https://t.me/mxmoder_support"),
                    InlineKeyboardButton('BOT OWNER ', url='https://telegram.me/mxmoder_bot')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)      
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("<b>Please wait...</b>")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                # Create the inline keyboard button with callback_data
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('✇ Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url="https://t.me/mxmoder"),
                                InlineKeyboardButton(' SUPPORT CHANNEL', url='https://t.me/mxmoder_support')
                            ],[
                                InlineKeyboardButton('🚀 Fast Download / Watch Online🖥️', callback_data=f'generate_stream_link:{file_id}') #Don't change anything without contacting me @LazyDeveloperr
                            ]
                        ]
                    )
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(
                        [
                         [
                          InlineKeyboardButton('✇ Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url="https://t.me/mxmoder"),
                                InlineKeyboardButton(' SUPPORT CHANNEL', url='https://t.me/mxmoder_support')
                       ],[ 
                          InlineKeyboardButton('🚀 Fast Download / Watch Online🖥️', callback_data=f'generate_stream_link:{file_id}') #Don't change anything without contacting me @LazyDeveloperr
                            ]
                        ]
                    )
                )
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1) 
        await sts.delete()
        return
    
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("<b>Please wait...</b>")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()
    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True if PROTECT_CONTENT else False
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all movies till today midnight.</b>",
                 protect_content=True if PROTECT_CONTENT else False
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True if PROTECT_CONTENT else False
            )
    if data.startswith("sendfiles"):
        chat_id = int("-" + file_id.split("-")[1])
        userid = message.from_user.id if message.from_user else None
        g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=allfiles_{file_id}")
        k = await client.send_message(chat_id=message.from_user.id,text=f"<b>Get All Files in a Single Click!!!\n\n📂 ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 5 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                    ],[
                        InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=await get_tutorial(chat_id))
                    ]
                ]
            )
        )
        await asyncio.sleep(300)
        await k.edit("<b>Your message is successfully deleted!!!</b>")
        return
        
    
    elif data.startswith("short"):
        user = message.from_user.id
        chat_id = temp.SHORT.get(user)
        files_ = await get_file_details(file_id)
        files = files_[0]
        g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
        k = await client.send_message(chat_id=user,text=f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}\n\n📂Fɪʟᴇ ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 20 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                    ], [
                        InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=await get_tutorial(chat_id))
                    ]
                ]
            )
        )
        await asyncio.sleep(1200)
        await k.edit("<b>Your message is successfully deleted!!!</b>")
        return
        
    elif data.startswith("all"):
        files = temp.GETALL.get(file_id)
        if not files:
            return await message.reply('<b><i>No such file exist.</b></i>')
        filesarr = []
        for file in files:
            file_id = file.file_id
            files_ = await get_file_details(file_id)
            files1 = files_[0]
            title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))
            size=get_size(files1.file_size)
            f_caption=files1.caption
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))}"
            if not await check_verification(client, message.from_user.id) and VERIFY == True:
                btn = [[
                    InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=")),
                    InlineKeyboardButton("⚡ ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғɪᴇᴅ ⚡",url='https://t.me/mxmoder_video_download/6')
                   ]]
                await message.reply_text(
                    text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴘʀᴇᴍɪᴜᴍ ᴍᴏᴅ ᴀᴘᴋs ᴜɴᴛɪʟ 24 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ!\n\nआप verified नहीं हैं ! \nकृपया जारी रखने के लिए verify करें ताकि आप अब से 24 घंटे तक unlimited ᴍᴏᴅ ᴀᴘᴋs प्राप्त कर सकें</b>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                caption=f_caption,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup(
                    [
                     [
                      InlineKeyboardButton('✇ Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇', url="https://t.me/mxmoder"),
                                InlineKeyboardButton(' SUPPORT CHANNEL', url='https://t.me/mxmoder_support')
                   ],[
                      InlineKeyboardButton('🚀 Fast Download / Watch Online🖥️', callback_data=f'generate_stream_link:{file_id}') #Don't change anything without contacting me @LazyDeveloperr

                     ]
                    ]
                )
            )
            filesarr.append(msg)
        # k = await client.send_message(chat_id = message.from_user.id, text=f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie Files/Videos will be deleted in <b><u>10 mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this ALL Files/Videos to your Saved Messages and Start Download there</i></b>")
        #await asyncio.sleep(600)
        #for x in filesarr:
         #   await x.delete()
        #await k.edit_text("<b>Your All Files/Videos is successfully deleted!!!</b>")
        return    
        
    elif data.startswith("files"):
        user = message.from_user.id
        if temp.SHORT.get(user)==None:
            await message.reply_text(text="<b>Please Search Again in Group</b>")
        else:
            chat_id = temp.SHORT.get(user)
        settings = await get_settings(chat_id)
        if settings['is_shortlink'] and user not in PREMIUM_USER:
            files_ = await get_file_details(file_id)
            files = files_[0]
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
            k = await client.send_message(chat_id=message.from_user.id,text=f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}\n\n📂Fɪʟᴇ ʟɪɴᴋ ➠ : {g}\n\n<i>Note: This message is deleted in 20 mins to avoid copyrights. Save the link to Somewhere else</i></b>", reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                        ], [
                            InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=await get_tutorial(chat_id))
                        ]
                    ]
                )
            )
            await asyncio.sleep(1200)
            await k.edit("<b>Your message is successfully deleted!!!</b>")
            return
    user = message.from_user.id
    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            if not await check_verification(client, message.from_user.id) and VERIFY == True:
                btn = [[
                    InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://te
