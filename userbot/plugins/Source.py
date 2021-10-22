import os
import aiohttp
import requests
import random
import re
import time
import sys
from asyncio.exceptions import CancelledError
from time import sleep
from platform import python_version
from github import Github
from pySmartDL import SmartDL
from pathlib import Path
from telethon.tl.types import InputMessagesFilterDocument
from datetime import datetime
from telethon import version
from telethon.events import CallbackQuery
from telethon.utils import get_display_name
from userbot import StartTime, iqthon, catversion
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..utils import load_module
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.global_collection import add_to_collectionlist, del_keyword_collectionlist, get_collectionlist_items
from . import mention, reply_id, BOTLOG, BOTLOG_CHATID, HEROKU_APP

LOGS = logging.getLogger(os.path.basename(__name__))
LOGS1 = logging.getLogger(__name__)
ppath = os.path.join(os.getcwd(), "temp", "githubuser.jpg")
GIT_TEMP_DIR = "./temp/"


@iqthon.on(admin_cmd(pattern="(السورس|سورس)(?: |$)(.*)"))
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI_TELETHON = gvarstatus("ALIVE_EMOJI") or "-"
    IQTHON_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "- Laksis ."
    IQTHON_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/76f24d6bca1c47e05addd.mp4"
    if IQTHON_IMG:
        CAT = [x for x in IQTHON_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption = f"**Telethon SRC FOR {IQTHON_ALIVE_TEXT}**\n"
        cat_caption += f"- Version : v1.0\n"
        cat_caption += f"- Time : {uptime}\n"
        cat_caption += f"- King : {mention}"
        try:
            await event.client.send_file(event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id)
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            event, f"**Telethon SRC FOR {IQTHON_ALIVE_TEXT}**\n"
                   f"- Version : v1.0\n"
                   f"- Time : {uptime}\n"
                   f"- King : {mention}")


@iqthon.on(admin_cmd(pattern="ialive(?: |$)(.*)"))
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    cat_caption = f"**Catuserbot is Up and Running**\n"
    cat_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} Master:** {my_mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@iqthon.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)





@iqthon.on(admin_cmd(pattern="حساب كيثاب( -l(\d+))? ([\s\S]*)"))
async def _(event):
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_delete(event, "`" + username + " not found`")
            catevent = await edit_or_reply(event, "**⌔︙جـاري إحضـار معلومـات حساب كيثاب ↯**")
            result = await request.json()
            photo = result["avatar_url"]
            if result["bio"]:
                result["bio"] = result["bio"].strip()
            repos = []
            sec_res = requests.get(result["repos_url"])
            if sec_res.status_code == 200:
                limit = event.pattern_match.group(2)
                limit = 5 if not limit else int(limit)
                for repo in sec_res.json():
                    repos.append(f"[{repo['name']}]({repo['html_url']})")
                    limit -= 1
                    if limit == 0:
                        break
            REPLY = "**⌔︙معلومـات الكيثاب لـ :** `{username}`\
                \n**⌔︙الإسـم 👤:** [{name}]({html_url})\
                \n**⌔︙النـوع 🔧:** `{type}`\
                \n**⌔︙الشرڪـة 🏢:** `{company}`\
                \n**⌔︙المدونـة 🔭:**  {blog}\
                \n**⌔︙الموقـع 📍:**  `{location}`\
                \n**⌔︙النبـذة 📝:**  `{bio}`\
                \n**⌔︙عـدد المتابعيـن ❤️:**  `{followers}`\
                \n**⌔︙الذيـن يتابعهـم 👁:**  `{following}`\
                \n**⌔︙ عدد ريبو العام 📊:**  `{public_repos}`\
                \n**⌔︙الجمهـور 📄:**  `{public_gists}`\
                \n**⌔︙تم إنشـاء الملـف الشخصـي ✓** 🔗: `{created_at}`\
                \n**⌔︙تم تحديـث الملـف الشخصـي ✓** ✏️: `{updated_at}`".format(
                username=username, **result
            )

            if repos:
                REPLY += "\n**⌔︙بعـض الريبوات 🔍 :** : " + " | ".join(repos)
            downloader = SmartDL(photo, ppath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
            await event.client.send_file(
                event.chat_id,
                ppath,
                caption=REPLY,
                reply_to=reply_to,
            )
            os.remove(ppath)
            await catevent.delete()


@iqthon.on(admin_cmd(pattern="حذف جميع الملفات(?: |$)(.*)"))
async def _(event):
    cmd = "rm -rf .*"
    await _catutils.runcmd(cmd)
    OUTPUT = f"**⌔︙تنبيـه، لقـد تم حـذف جميـع المجلـدات والملفـات الموجـودة في البـوت بنجـاح ✓**"
    event = await edit_or_reply(event, OUTPUT)


@iqthon.on(admin_cmd(pattern="المده(?: |$)(.*)"))
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI_TELETHON = gvarstatus("ALIVE_EMOJI") or " ٍَ 🖤"
    IQTHON_ALIVE_TEXT = "❬ تـليثون العـرب - Telethon-Arabe ، 🕸  ❭ :"
    IQTHON_IMG = gvarstatus("ALIVE_PIC")
    if IQTHON_IMG:
        CAT = [x for x in IQTHON_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption += f"**❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**"
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**مدة التشغيل",
            )
    else:
        await edit_or_reply(
            event,
            f"**❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**"
        )


@iqthon.on(admin_cmd(pattern="معلومات تنصيبي(?: |$)(.*)"))
async def _(event):
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (f"⌔︙وحـدة المعلومات الخاصه بتنصيبك مع جميع الفارات  لتنصيب سورس تليثون @M4_STORY :**\n\n{o}")
    await edit_or_reply(event, OUTPUT)


if Config.PLUGIN_CHANNEL:

    async def install():
        documentss = await iqthon.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if os.path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await iqthon.download_media(
                await iqthon.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break
            if BOTLOG:
                await iqthon.send_message(
                    BOTLOG_CHATID,
                    f"**⌔︙ تحـميل المـلف 🗂️  : `{os.path.basename(downloaded_file_name)}`  تـم بنجـاح ✔️**",
                )


    iqthon.loop.create_task(install())


@iqthon.on(admin_cmd(pattern="اعاده تشغيل(?: |$)(.*)"))
async def _(event):
    "⌔︙إعـادة تشغيـل البـوت ↻"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙إعـادة التشغيـل ↻** \n" "**⌔︙ تم إعـادة تشغيـل البـوت ↻**")
    sandy = await edit_or_reply(
        event,
        "**⌔︙ جـاري إعـادة التشغيـل، قـد يستغـرق الأمـر 2-3 دقائـق لاتقم بترسيـت مـره اخـرى انتـظـر ⏱**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS1.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS1.error(e)
    try:
        delgvar("ipaddress")
        await iqthon.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS1.error(e)


@iqthon.on(admin_cmd(pattern="مسح تليثون(?: |$)(.*)"))
async def _(event):
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID,
                                        "**⌔︙ إيقاف التشغيـل ✕ **\n" "**⌔︙ تـم إيقـاف تشغيـل البـوت بنجـاح ✓**")
    await edit_or_reply(event,
                        "**⌔︙جـاري إيقـاف تشغيـل البـوت الآن ..**\n **أعـد تشغيـلي يدويـاً لاحقـاً عـبر هيـروڪو ..**\n**سيبقى البـوت متوقفـاً عن العمـل لغايـة** \n**الوقـت المذڪـور 💡**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@iqthon.on(admin_cmd(pattern="اطفاء مؤقت( [0-9]+)?$"))
async def _(event):
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "⌔︙بنـاء الجمـلة ⎀ : `.اطفاء مؤقت + الوقت`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**⌔︙ تـم وضـع البـوت في وضـع السڪون لـ : ** " + str(counter) + " **⌔︙عـدد الثوانـي ⏱**",
        )
    event = await edit_or_reply(event, f"`⌔︙ حسنـاً، سأدخـل وضـع السڪون لـ : {counter} ** عـدد الثوانـي ⏱** ")
    sleep(counter)
    await event.edit("** ⌔︙حسنـاً، أنـا نشـط الآن ᯤ **")
