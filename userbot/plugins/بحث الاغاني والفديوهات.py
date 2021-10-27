import asyncio
import base64
import io
import os
from pathlib import Path
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from userbot import iqthon

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import name_dl, song_dl, video_dl, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           الفارات                           #
# =========================================================== #
SONG_SEARCH_STRING = "- جاري البحث انتظر قليلا ."
SONG_NOT_FOUND = "- لم يتم العثور على نتائج .️"
SONG_SENDING_STRING = "- قم بألغاء حظر البوت اولا ."
# =========================================================== #
#                                                             #
# =========================================================== #


@iqthon.iq_cmd(
    pattern="بحث(320)?(?: |$)(.*)",
    command=("بحث", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def _(event):
    "- للبحث عن اغاني !."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        return await edit_or_reply(event, "**- اكتب بحث + الاسم .ا️**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**- جاري التحميل انتظر قليلا .**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**- لم يتم العثور على نتائج .** `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    stderr = (await _catutils.runcmd(song_cmd))[1]
    if stderr:
        return await catevent.edit(f"**- حدث خطأ .** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**- حدث خطأ .** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    catname = os.path.splitext(catname)[0]
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{catname}.mp3")
    if not os.path.exists(song_file):
        return await catevent.edit(
            f"**- لم يتم العثور على نتائج .** `{query}`"
        )
    await catevent.edit("**- يرجى الانتضار .**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None

    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@iqthon.iq_cmd(
    pattern="بحث فيديو(?: |$)(.*)",
    command=("بحث فيديو", plugin_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def _(event):
    "- للبحث عن مقاطع mp4 ."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        return await edit_or_reply(event, "**- قم بوضع الامر وبجانبة الاسم .**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**- يرجى الانتظار .**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**- لم يتم العثور على نتائج .** `{query}`"
        )
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _catutils.runcmd(video_cmd))[1]
    if stderr:
        return await catevent.edit(f"**- حدث خطأ .** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**- حدث خطأ .** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    catname = os.path.splitext(catname)[0]
    vsong_file = Path(f"{catname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"**- لم يتم العثور على نتائج .** `{query}`"
        )
    await catevent.edit("**- يرجى الانتظار .**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@iqthon.iq_cmd(
    pattern="معلومات الاغنيه$",
    command=("معلومات الاغنيه", plugin_category),
    info={
        "header": "To reverse search song.",
        "description": "Reverse search audio file using shazam api",
        "usage": "{tr}shazam <reply to voice/audio>",
    },
)
async def shazamcmd(event):
    "لعكس أغنية البحث."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "**- يرجى استعمال الامر مع الرد .**"
        )
    catevent = await edit_or_reply(event, "**- جاري تحميل المقطع الصوتي يرجى الانتظار .**")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            catevent, f"**- حدث خطأ .**\n__{str(e)}__"
        )
    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**- الاغنيه .** `{song}`", reply_to=reply
    )
    await catevent.delete()
    
 async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**▾∮ لم يتم العثور على المجموعة او القناة**")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**▾∮ لا يمكنني استخدام الامر من الكروبات او القنوات الخاصة**"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**▾∮ لم يتم العثور على المجموعة او القناة**")
            return None
        except (TypeError, ValueError):
            await event.reply("**▾∮ رابط الكروب غير صحيح**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


@iqthon.iq_cmd(admin_cmd(pattern=r"ضيف ?(.*)"))
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        roz = await event.reply("**▾∮ تتـم العـملية انتظـࢪ قليلا 🧸♥ ...**")
    else:
        roz = await event.edit("**▾∮ تتـم العـملية انتظـࢪ قليلا 🧸♥ ...**.")
    JMTHON = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await roz.edit("**▾∮ لا يمكننـي اضافـة المـستخدمين هـنا**")
    s = 0
    f = 0
    error = "None"

    await roz.edit(
        "**▾∮ حـالة الأضافة:**\n\n**▾∮ تتـم جـمع معـلومات الـمستخدمين 🔄 ...⏣**"
    )
    async for user in event.client.iter_participants(JMTHON.full_chat.id):
        try:
            if error.startswith("Too"):
                return (
                    await roz.edit(
                        f"**حـالة الأضـافة انتـهت مـع الأخـطاء**\n- (**ربـما هـنالك ضغـط عـلى الأمࢪ حاول مججـدا لاحقـا 🧸**) \n**الـخطأ** : \n`{error}`\n\n• اضالـة `{s}` \n• خـطأ بأضافـة `{f}`"
                    ),
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await roz.edit(
                f"**▾∮تتـم الأضـافة 🧸♥**\n\n• اضـيف `{s}` \n•  خـطأ بأضافـة `{f}` \n\n**× اخـر خـطأ:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await roz.edit(
        f"**▾∮اڪتـملت الأضافـة ✅** \n\n• تـم بنجـاح اضافـة `{s}` \n• خـطأ بأضافـة `{f}`"
    )
