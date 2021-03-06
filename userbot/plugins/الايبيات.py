import bs4
import requests
import json
import asyncio
import base64
import re
import urllib
import io
import os
import moviepy.editor as m
import asyncio
import io
import logging
import time
import fitz
from datetime import datetime
from io import BytesIO
from covid import Covid
from pathlib import Path
from ShazamAPI import Shazam
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from shutil import copyfile
from pymediainfo import MediaInfo
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest
from telethon.utils import get_attributes
from search_engine_parser import BingSearch, GoogleSearch, YahooSearch
from html_telegraph_poster.upload_images import upload_image
from search_engine_parser.core.exceptions import NoResultsOrTrafficError
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url
from userbot import iqthon
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, progress, thumb_from_audio
from ..helpers.functions import name_dl, song_dl, video_dl, yt_search, deEmojify, convert_toimage, convert_tosticker, invert_frames, l_frames, r_frames, spin_frames, ud_frames, vid_to_gif
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id, _cattools, _format, parse_pre
from ..sql_helper.globals import gvarstatus
from . import BOTLOG, BOTLOG_CHATID, ALIVE_NAME, covidindia, make_gif
LOGS = logging.getLogger(__name__)
SONG_SEARCH_STRING = "⌔︙جاري البحث عن الاغنية إنتظر رجاءًا  🎧"
SONG_NOT_FOUND = "⌔︙لم أستطع إيجاد هذه الأغنية  ⚠️"
SONG_SENDING_STRING = "⌔︙قم بإلغاء حظر البوت  🚫"
opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
opener.addheaders = [("User-agent", useragent)]
async def phss(uplded, user_input, name):
    web = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={uplded}&text={user_input}&username={name}"
    ).json()
    alf = web.get("message")
    uri = url(alf)
    if not uri:
        return "check syntax once more"
    with open("alf.png", "wb") as f:
        f.write(requests.get(alf).content)
    img = Image.open("alf.png").convert("RGB")
    img.save("alf.webp", "webp")
    return "alf.webp"

async def purge():
    try:
        os.system("rm *.png *.webp")
    except OSError:
        pass

if not os.path.isdir("./temp"):
    os.makedirs("./temp")


LOGS = logging.getLogger(__name__)
PATH = os.path.join("./temp", "temp_vid.mp4")

thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
    return user_obj

async def ParseSauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results

async def scam(results, lim):
    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")
    imglinks = []
    counter = 0
    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)
    for imglink in oboi:
        counter += 1
        if counter <= int(lim):
            imglinks.append(imglink)
        else:
            break
    return imglinks

async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)
@iqthon.on(admin_cmd(pattern=r"رابط تطبيق ([\s\S]*)"))
async def app_search(event):
    app_name = event.pattern_match.group(1)
    event = await edit_or_reply(event, "⌔︙جـاري البحـث ↯")
    try:
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>⌔︙المطـور :</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>⌔︙التقييـم :</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>⌔︙المميـزات :</code> <a href='"
            + app_link
            + "'>⌔︙مشاهدتـه في سـوق بلـي 🝧</a>"
        )
        app_details += f"\n\n===> {ALIVE_NAME} <==="
        await event.edit(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await event.edit("**⌔︙لم يتـم العثـور على نتيجـة، الرجـاء إدخـال إسـم تطبيـق صالـح ⚠️**")
    except Exception as err:
        await event.edit("⌔︙حـدث استثنـاء ⌭ :" + str(err))
@iqthon.on(admin_cmd(pattern=r"الاذان(?: |$)(.*)"))
async def get_adzan(adzan):
    LOKASI = adzan.pattern_match.group(1)
    url = f"https://api.pray.zone/v2/times/today.json?city={LOKASI}"
    request = requests.get(url)
    if request.status_code != 200:
        await edit_delete(
            adzan, f"**⌔︙لم يـتم العثور على معلومات لـهذه المدينه ⚠️ {LOKASI}\n يرجى كتابة اسم محافظتك وباللغه الانكليزي **", 5
        ) 
        return
    result = json.loads(request.text)
    iqthonresult = f"<b>اوقـات صـلاه المـسلمين 👳‍♂️ </b>\
            \n\n<b>المـدينة  Ⓜ️  : </b><i>{result['results']['location']['city']}</i>\
            \n<b>الـدولة  🏳️ : </b><i>{result['results']['location']['country']}</i>\
            \n<b>التـاريخ  🔢  : </b><i>{result['results']['datetime'][0]['date']['gregorian']}</i>\
            \n<b>الهـجري  ⏳  : </b><i>{result['results']['datetime'][0]['date']['hijri']}</i>\
            \n\n<b>الامـساك  🕒  : </b><i>{result['results']['datetime'][0]['times']['Imsak']}</i>\
            \n<b>شـروق الشمس  🌝 : </b><i>{result['results']['datetime'][0]['times']['Sunrise']}</i>\
            \n<b>الـفجر  🌔   : </b><i>{result['results']['datetime'][0]['times']['Fajr']}</i>\
            \n<b>الضـهر 🌞   : </b><i>{result['results']['datetime'][0]['times']['Dhuhr']}</i>\
            \n<b>العـصر  🌥    : </b><i>{result['results']['datetime'][0]['times']['Asr']}</i>\
            \n<b>غـروب الشمس  🌘 : </b><i>{result['results']['datetime'][0]['times']['Sunset']}</i>\
            \n<b>المـغرب 🌑 : </b><i>{result['results']['datetime'][0]['times']['Maghrib']}</i>\
            \n<b>العشـاء  🌚   : </b><i>{result['results']['datetime'][0]['times']['Isha']}</i>\
            \n<b>منتـصف الليل 🕛 : </b><i>{result['results']['datetime'][0]['times']['Midnight']}</i>\
    "
    await edit_or_reply(adzan, iqthonresult, "html")
@iqthon.on(admin_cmd(pattern=r"كورونا(?:\s|$)([\s\S]*)"))
async def corona(event):
    input_str = event.pattern_match.group(1)
    country = (input_str).title() if input_str else "العالم"
    catevent = await edit_or_reply(event, "**⌔︙يتـم جلـب معلومـات فـايروس كـورونا فـي البلـد المحـدد 🔎**")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⌔︙ الاصابات المؤكده 😟 : <code>{hmm1}</code>"
        data += f"\n⌔︙ الاصابات المشبوهه 🥺 : <code>{country_data['active']}</code>"
        data += f"\n⌔︙ الوفيات ⚰️ : <code>{hmm2}</code>"
        data += f"\n⌔︙ الحرجه 😔 : <code>{country_data['critical']}</code>"
        data += f"\n⌔︙ حالات الشفاء 😊 : <code>{country_data['recovered']}</code>"
        data += f"\n⌔︙ اجمالي الاختبارات 📊 : <code>{country_data['total_tests']}</code>"
        data += f"\n⌔︙ الاصابات الجديده 🥺 : <code>{country_data['new_cases']}</code>"
        data += f"\n⌔︙ الوفيات الجديده ⚰️ : <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>⌔︙ معلومـات فـايروس كـورونا. 💉 لـ {}:{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n⌔︙ الاصابات المؤكده 😟 : <code>{data['new_positive']}</code>\
                \n⌔︙ الاصابات المشبوهه 🥺 : <code>{data['new_active']}</code>\
                \n⌔︙ الوفيات ⚰️ : <code>{data['new_death']}</code>\
                \n⌔︙ حالات الشفاء 😊 : <code>{data['new_cured']}</code>\
                \n⌔︙ اجمالي الاختبارات 📊  : <code>{cat1}</code>\
                \n⌔︙ الاصابات الجديده 🥺 : <code>{cat2}</code>\
                \n⌔︙ الوفيات الجديده ⚰️ : <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(catevent, "**⌔︙ معلومـات فـايروس كـورونا. 💉  \n  فـي بـلد  - {} غـير مـوجودة ❌**".format(country),
                5,
            )
@iqthon.on(admin_cmd(pattern=r"تحميل(320)?(?: |$)(.*)"))
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        return await edit_or_reply(event, "**⌔︙ما الذي تريد أن أبحث عنه  ⁉️**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**⌔︙جاري تحميل الأغنية إنتظر قليلا  ⏳**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**⌔︙عـذرًا لم أستطع إيجاد الأغنية أو الفيديو لـ  ❌** `{query}`"
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
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    catname = os.path.splitext(catname)[0]
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{catname}.mp3")
    if not os.path.exists(song_file):
        return await catevent.edit(
            f"**⌔︙عـذرًا لم أستطع إيجاد الأغنية أو الفيديو لـ  ❌** `{query}`"
        )
    await catevent.edit("**⌔︙لقد وجدت الاغنية إنتظر قليلا  ⏱**")
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
@iqthon.on(admin_cmd(pattern=r"بحث فيديو(?: |$)(.*)"))
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        return await edit_or_reply(event, "**⌔︙قم بوضع الأمر وبجانبه إسم الأغنية  🖇**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**⌔︙لقد وجدت الفيديو المطلوب إنتظر قليلا  ⏱ ...**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**⌔︙ عـذرًا لم أستطع إيجاد أي فيديو او صوت متعلق بـ ❌** `{query}`"
        )
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _catutils.runcmd(video_cmd))[1]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**⌔︙ خـطأ  ⚠️ :** `{stderr}`")
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    catname = os.path.splitext(catname)[0]
    vsong_file = Path(f"{catname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"**⌔︙ عـذرًا لم أستطع إيجاد أي فيديو او صوت متعلق بـ ❌** `{query}`"
        )
    await catevent.edit("**⌔︙لقد وجدت الفديو المطلوب انتظر قليلا  ⏳**")
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
@iqthon.on(admin_cmd(pattern=r"معلومات الاغنيه(?: |$)(.*)"))
async def shazamcmd(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "**⌔︙قم بالرد على الرسالة الصوتية لعكس البحث عن هذه الأغنية  ♻️**"
        )
    catevent = await edit_or_reply(event, "**⌔︙جاري تحميل المقطع الصوتي  📲**")
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
            catevent, f"**⌔︙هناك خطأ عند محاولة عكس الأغنية  ⚠️ :**\n__{str(e)}__"
        )
    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**⌔︙ الأغنية 🎧 :** `{song}`", reply_to=reply
    )
    await catevent.delete()
@iqthon.on(admin_cmd(pattern=r"كوكل بحث ([\s\S]*)"))
async def gsearch(q_event):
    "Google search command."
    catevent = await edit_or_reply(q_event, "**⌔︙جـاري البحـث ↯**")
    match = q_event.pattern_match.group(1)
    page = re.findall(r"-p\d+", match)
    lim = re.findall(r"-l\d+", match)
    try:
        page = page[0]
        page = page.replace("-p", "")
        match = match.replace("-p" + page, "")
    except IndexError:
        page = 1
    try:
        lim = lim[0]
        lim = lim.replace("-l", "")
        match = match.replace("-l" + lim, "")
        lim = int(lim)
        if lim <= 0:
            lim = int(5)
    except IndexError:
        lim = 5
    #     smatch = urllib.parse.quote_plus(match)
    smatch = match.replace(" ", "+")
    search_args = (str(smatch), int(page))
    gsearch = GoogleSearch()
    bsearch = BingSearch()
    ysearch = YahooSearch()
    try:
        gresults = await gsearch.async_search(*search_args)
    except NoResultsOrTrafficError:
        try:
            gresults = await bsearch.async_search(*search_args)
        except NoResultsOrTrafficError:
            try:
                gresults = await ysearch.async_search(*search_args)
            except Exception as e:
                return await edit_delete(catevent, f"**⌔︙خطـأ ⚠️ :**\n`{str(e)}`", time=10)
    msg = ""
    for i in range(lim):
        if i > len(gresults["links"]):
            break
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await edit_or_reply(
        catevent,
        "**⌔︙إستعـلام البحـث 🝰 :**\n`" + match + "`\n\n**⌔︙النتائـج ⎙ :**\n" + msg,
        link_preview=False,
        aslink=True,
        linktext=f"**⌔︙نتائـج البحـث عـن الإستعـلام ⎙ ** `{match}` :",
    )
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "**⌔︙إستعـلام بحـث جـوجـل 🝰 **" + match + "**تم تنفيـذه بنجـاح ✓**",
        )
@iqthon.on(admin_cmd(pattern=r"البحث العام(?: |$)(.*)"))
async def _(event):
    start = datetime.now()
    OUTPUT_STR = "**⌔︙قم بالـرد على صـورة لإجـراء البحـث العڪـسي في گـوگـل ✦**"
    if event.reply_to_msg_id:
        catevent = await edit_or_reply(event, "**⌔︙وسائـط ما قبـل المعالجـة ␥**")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        BASE_URL = "http://www.google.com"
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (
                    downloaded_file_name,
                    open(downloaded_file_name, "rb"),
                ),
                "image_content": "",
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(
                SEARCH_URL, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await catevent.edit("**⌔︙تم العثـور على نتيجـة بحـث جـوجـل ✓**")
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
            prs_anchor_element = prs_div.find("a")
            prs_url = BASE_URL + prs_anchor_element.get("href")
            prs_text = prs_anchor_element.text
            # document.getElementById("jHnbRc")
            img_size_div = soup.find(id="jHnbRc")
            img_size = img_size_div.find_all("div")
        except Exception:
            return await edit_delete(
                catevent, "**⌔︙غيـر قـادر على إيجـاد صـور مشابـهه !**"
            )
        end = datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """{img_size}
<b>⌔︙بحـث ممڪـن ذو صلـة 🜉  : </b> <a href="{prs_url}">{prs_text}</a> 
<b>⌔︙مزيـد من المعلومـات 🝰 : </b> إفتـح هـذا ␥ <a href="{the_location}">Link</a> 
<i>⌔︙تم الجلـب في {ms} ثانيـة ⏱</i>""".format(
            **locals()
        )
    else:
        catevent = event
    await edit_or_reply(catevent, OUTPUT_STR, parse_mode="HTML", link_preview=False)
@iqthon.on(admin_cmd(pattern=r"البحث اونلاين(?:\s|$)([\s\S]*)"))
async def google_search(event):
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not input_str:
        return await edit_delete(
            event, "**⌔︙ما الذي يجـب أن أبحـث عنـه؟ يرجـىٰ إعطـاء معلومـات عن البحـث ⚠️**"
        )
    input_str = deEmojify(input_str).strip()
    if len(input_str) > 195 or len(input_str) < 1:
        return await edit_delete(
            event,
            "**⌔︙لقـد تجـاوز إستعـلام البحـث 200 حـرف أو أن إستعـلام البحـث فـارغ ⚠️**",
        )
    query = "#12" + input_str
    results = await event.client.inline_query("@StickerizerBot", query)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()
@iqthon.on(admin_cmd(pattern="تخزين الصوت(?: |$)(.*)"))
async def iq(event):
    ureply = await event.get_reply_message()
    if not (ureply and ("audio" in ureply.document.mime_type)):
        await event.edit("**قم برد على الصوت بشرط ان يكون الامتداد mp3 وليس بصمه**")
        return
    await event.edit("**جاري تخزين الصوت**")
    d = os.path.join("SQL/extras", "iq.mp3")
    await event.edit("**جارٍ التنزيل ... الملفات الكبيرة تستغرق وقتًا ..**")
    await event.client.download_media(ureply, d)
    await event.edit("**تم .. الآن قم بالرد على الفيديو او المتحركه الذي تريد إضافة هذا الصوت فيه بالأمر :** `.اضف الصوت`")
@iqthon.on(admin_cmd(pattern="اضف الصوت(?: |$)(.*)"))
async def iq(event):
    ureply = await event.get_reply_message()
    if not (ureply and ("video" in ureply.document.mime_type)):
        await event.edit("**قم بالرد على متحركه او فيديو الذي تريد إضافة الصوت فيه.**")
        return
    xx = await event.edit("**  جاري اضافه الصوت انتضر قليلا \n ملاحضه لاتنسى تطابق وقت الفيديو او المتحركه مع وقت الصوت **")
    ultt = await ureply.download_media()
    ls = os.listdir("SQL/extras")
    z = "iq.mp3"
    x = "SQL/extras/iq.mp3"
    if z not in ls:
        await event.edit("**قم بالرد أولاً بصوت بامتداد mp3 فقط**")
        return
    video = m.VideoFileClip(ultt)
    audio = m.AudioFileClip(x)
    out = video.set_audio(audio)
    out.write_videofile("L5.mp4", fps=30)
    await event.client.send_file(
        event.chat_id,
        file="L5.mp4",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    os.remove("L5.mp4")
    os.remove(x)
    os.remove(ultt)
    await xx.delete()
@iqthon.on(admin_cmd(pattern="بورن هوب(?: |$)(.*)"))
async def phcomment(event):
    try:
        await event.edit("جاري الصنع")
        text = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        if reply:
            user = await get_user_from_event(event)
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            if text:
                text = text
            else:
                text = str(reply.message)
        elif text:
            user = await bot.get_me()
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            text = text
        else:
            return await event.edit("جاري الصنع")
        try:
            photo = await event.client.download_profile_photo(
                user.id,
                str(user.id) + ".png",
                download_big=False,
            )
            uplded = upload_image(photo)
        except BaseException:
            uplded = "https://telegra.ph/file/7d110cd944d54f72bcc84.jpg"
    except BaseException as e:
        await purge()
        return await event.edit(f"خطا : {e}")
    img = await phss(uplded, text, name)
    try:
        await event.client.send_file(
            event.chat_id,
            img,
            reply_to=event.reply_to_msg_id,
        )
    except BaseException:
        await purge()
        return await event.edit("قم برد على الرساله")
    await event.delete()
    await purge()
@iqthon.on(admin_cmd(pattern="تحويل صوره(?: |$)(.*)"))
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event, "**⌔︙ يجـب عليـك الرد عـلى الملصق لتحويـله الـى صورة ⚠️**"
        )
    output = await _cattools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "**⌔︙ غـير قـادر على تحويل الملصق إلى صورة من هـذا الـرد ⚠️**"
        )
    meme_file = convert_toimage(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()
@iqthon.on(admin_cmd(pattern="تحويل ملصق(?: |$)(.*)"))
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event, "**⌔︙ يجـب عليـك الرد عـلى الصـورة لتحويـلها الـى مـلصق ⚠️**"
        )
    output = await _cattools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "**⌔︙ غـير قـادر على استـخراج الـملصق من هـذا الـرد ⚠️**"
        )
    meme_file = convert_tosticker(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()
@iqthon.on(admin_cmd(pattern="تحويل (صوت|بصمه)(?: |$)(.*)"))
async def _(event):
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "**⌔︙ يـجب الـرد على اي مـلف اولا ⚠️**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "**⌔︙ يـجب الـرد على اي مـلف اولا ⚠️**")
        return
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "**⌔︙ يتـم التـحويل انتـظر قليـلا ⏱**")
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "**⌔︙ التحـميل الى `{}`  في {} من الثواني ⏱**".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "بصمه":
            new_required_file_caption = "voice_" + str(round(time.time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "صوت":
            new_required_file_caption = "mp3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("**⌔︙ غـير مدعوم ❕**")
            os.remove(downloaded_file_name)
            return
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()
@iqthon.on(admin_cmd(pattern="تحويل متحركة ?([0-9.]+)?$"))
async def _(event):
    reply = await event.get_reply_message()
    mediatype = media_type(event)
    if mediatype and mediatype != "video":
        return await edit_delete(event, "**⌔︙ يجـب عليك الـرد على فيديو اولا لتحـويله ⚠️**")
    args = event.pattern_match.group(1)
    if not args:
        args = 2.0
    else:
        try:
            args = float(args)
        except ValueError:
            args = 2.0
    catevent = await edit_or_reply(event, "**⌔︙ يتـم التحويل الى متـحركه انتـظر ⏱**")
    inputfile = await reply.download_media()
    outputfile = os.path.join(Config.TEMP_DIR, "vidtogif.gif")
    result = await vid_to_gif(inputfile, outputfile, speed=args)
    if result is None:
        return await edit_delete(event, "**⌔︙ عـذرا لا يمكـنني تحويل هذا الى متـحركة ⚠️**")
    jasme = await event.client.send_file(event.chat_id, result, reply_to=reply)
    await _catutils.unsavegif(event, jasme)
    await catevent.delete()
    for i in [inputfile, outputfile]:
        if os.path.exists(i):
            os.remove(i)
@iqthon.on(admin_cmd(pattern="تحويل فديو دائري(?: |$)((-)?(s)?)$"))
async def pic_gifcmd(event):  # sourcery no-metrics
    args = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "**⌔︙قـم بالـرد على وسائـط مدعومـة !**")
    media_type(reply)
    catevent = await edit_or_reply(event, "**⌔︙جـاري تحويل الملصق الى فيديو مرئي دائـري ⌯**")
    output = await _cattools.media_to_pic(event, reply, noedits=True)
    if output[1] is None:
        return await edit_delete(
            output[0], "**⌔︙تعـذّر إستخـراج الصـورة من الرسالـة التي تـم الـرّد عليهـا ✕**"
        )
    meme_file = convert_toimage(output[1])
    image = Image.open(meme_file)
    w, h = image.size
    outframes = []
    try:
        outframes = await spin_frames(image, w, h, outframes)
    except Exception as e:
        return await edit_delete(output[0], f"**⌔︙خطـأ ⚠️ :**\n__{str(e)}__")
    output = io.BytesIO()
    output.name = "Output.gif"
    outframes[0].save(output, save_all=True, append_images=outframes[1:], duration=1)
    output.seek(0)
    with open("Output.gif", "wb") as outfile:
        outfile.write(output.getbuffer())
    final = os.path.join(Config.TEMP_DIR, "output.gif")
    output = await vid_to_gif("Output.gif", final)
    if output is None:
        return await edit_delete(catevent, "**⌔︙تعـذّر صنـع صـورة متحرڪـة دوارة ✕**")
    media_info = MediaInfo.parse(final)
    aspect_ratio = 1
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    PATH = os.path.join(Config.TEMP_DIR, "round.gif")
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        await _catutils.runcmd(
            f'ffmpeg -i {final} -vf "crop={crop_by}:{crop_by}" {PATH}'
        )
    else:
        copyfile(final, PATH)
    time.time()
    ul = io.open(PATH, "rb")
    uploaded = await event.client.fast_upload_file(
        file=ul,
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type="video/mp4",
        attributes=[
            types.DocumentAttributeVideo(
                duration=0,
                w=1,
                h=1,
                round_message=True,
                supports_streaming=True,
            )
        ],
        force_file=False,
        thumb=await event.client.upload_file(meme_file),
    )
    sandy = await event.client.send_file(
        event.chat_id,
        media,
        reply_to=reply,
        video_note=True,
        supports_streaming=True,
    )
    if not args:
        await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for i in [final, "Output.gif", meme_file, PATH, final]:
        if os.path.exists(i):
            os.remove(i)
@iqthon.on(admin_cmd(pattern="تحويل ملصق دائري ?((-)?s)?$"))
async def video_catfile(event):  # sourcery no-metrics
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    catid = await reply_id(event)
    if not reply or not reply.media:
        return await edit_delete(event, "**⌔︙قـم بالـرد على وسائـط مدعومـة !**")
    mediatype = media_type(reply)
    if mediatype == "Round Video":
        return await edit_delete(
            event,
            "⌔︙الوسائـط التي تم الـرد عليهـا هـي بالفعـل في شڪـل دائـري، أعـد التحـقق !",
        )
    if mediatype not in ["Photo", "Audio", "Voice", "Gif", "Sticker", "Video"]:
        return await edit_delete(event, "**⌔︙لم يتـم العثـور على وسائـط مدعومـة !**")
    flag = True
    catevent = await edit_or_reply(event, "**⌔︙جـاري التحويـل إلى شڪـل دائـري ⌯**")
    catfile = await reply.download_media(file="./temp/")
    if mediatype in ["Gif", "Video", "Sticker"]:
        if not catfile.endswith((".webp")):
            if catfile.endswith((".tgs")):
                hmm = await make_gif(catevent, catfile)
                os.rename(hmm, "./temp/circle.mp4")
                catfile = "./temp/circle.mp4"
            media_info = MediaInfo.parse(catfile)
            aspect_ratio = 1
            for track in media_info.tracks:
                if track.track_type == "Video":
                    aspect_ratio = track.display_aspect_ratio
                    height = track.height
                    width = track.width
            if aspect_ratio != 1:
                crop_by = width if (height > width) else height
                await _catutils.runcmd(
                    f'ffmpeg -i {catfile} -vf "crop={crop_by}:{crop_by}" {PATH}'
                )
            else:
                copyfile(catfile, PATH)
            if str(catfile) != str(PATH):
                os.remove(catfile)
            try:
                catthumb = await reply.download_media(thumb=-1)
            except Exception as e:
                LOGS.error(f"circle - {str(e)}")
    elif mediatype in ["Voice", "Audio"]:
        catthumb = None
        try:
            catthumb = await reply.download_media(thumb=-1)
        except Exception:
            catthumb = os.path.join("./temp", "thumb.jpg")
            await thumb_from_audio(catfile, catthumb)
        if catthumb is not None and not os.path.exists(catthumb):
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if (
            catthumb is not None
            and not os.path.exists(catthumb)
            and os.path.exists(thumb_loc)
        ):
            flag = False
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if catthumb is not None and os.path.exists(catthumb):
            await _catutils.runcmd(
                f"""ffmpeg -loop 1 -i {catthumb} -i {catfile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -vf \"scale=\'iw-mod (iw,2)\':\'ih-mod(ih,2)\',format=yuv420p\" -shortest -movflags +faststart {PATH}"""
            )
            os.remove(catfile)
        else:
            os.remove(catfile)
            return await edit_delete(
                catevent, "**لا يوجـد ما يصلـح لجعلـه ملاحظـة فيديـو ⚠️**", 5
            )
    if (
        mediatype
        in [
            "Voice",
            "Audio",
            "Gif",
            "Video",
            "Sticker",
        ]
        and not catfile.endswith((".webp"))
    ):
        if os.path.exists(PATH):
            c_time = time.time()
            attributes, mime_type = get_attributes(PATH)
            ul = io.open(PATH, "rb")
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "**⌔︙قـم بالـرد على وسائـط مدعومـة !**")
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type="video/mp4",
                attributes=[
                    types.DocumentAttributeVideo(
                        duration=0,
                        w=1,
                        h=1,
                        round_message=True,
                        supports_streaming=True,
                    )
                ],
                force_file=False,
                thumb=await event.client.upload_file(catthumb) if catthumb else None,
            )
            sandy = await event.client.send_file(
                event.chat_id,
                media,
                reply_to=catid,
                video_note=True,
                supports_streaming=True,
            )

            if not args:
                await _catutils.unsavegif(event, sandy)
            os.remove(PATH)
            if flag:
                os.remove(catthumb)
        await catevent.delete()
        return
    data = reply.photo or reply.media.document
    img = io.BytesIO()
    await event.client.download_file(data, img)
    im = Image.open(img)
    w, h = im.size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste(im, (0, 0))
    m = min(w, h)
    img = img.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, w - 10, h - 10), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    img = ImageOps.fit(img, (w, h))
    img.putalpha(mask)
    im = io.BytesIO()
    im.name = "cat.webp"
    img.save(im)
    im.seek(0)
    await event.client.send_file(event.chat_id, im, reply_to=catid)
    await catevent.delete()
@iqthon.on(admin_cmd(pattern="تحويل ملف ([\s\S]*)"))
async def get(event):
    name = event.text[5:]
    if name is None:
        await edit_or_reply(event, "**⌔︙قم بالـرد على الرسالـة لتحويلها الى ملف**")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await edit_or_reply(event, "**⌔︙قم بالـرد على الرسالـة لتحويلها الى ملف**")

@iqthon.on(admin_cmd(pattern="تحويل رساله(?: |$)(.*)"))
async def get(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if mediatype != "Document":
        return await edit_delete(
            event, "**⌔︙يبـدو أن هـذا الملـف غـير قابـل للڪتابـة،  يرجـى الـرد على ملـف قابـل للكتابـة !**"
        )
    file_loc = await reply.download_media()
    file_content = ""
    try:
        with open(file_loc) as f:
            file_content = f.read().rstrip("\n")
    except UnicodeDecodeError:
        pass
    except Exception as e:
        LOGS.info(e)
    if file_content == "":
        try:
            with fitz.open(file_loc) as doc:
                for page in doc:
                    file_content += page.getText()
        except Exception as e:
            if os.path.exists(file_loc):
                os.remove(file_loc)
            return await edit_delete(event, f"**⌔︙خطـأ ⚠️**\n__{str(e)}__")
    await edit_or_reply(
        event,
        file_content,
        parse_mode=parse_pre,
        aslink=True,
        noformat=True,
        linktext="**⌔︙يسمـح تليڪرام فقـط بـ 4096 حرفًـا في الرسالـة الواحـدة، ولڪن الملـف الـذي قمـت بالـرد عليـه يحتـوي على أڪثـر مـن ذلـك بڪثيـر، لذلـك (( لصقها على رابط لصق )) غيرها انت)) !**",
    )
    if os.path.exists(file_loc):
        os.remove(file_loc)
@iqthon.on(admin_cmd(pattern="تحويل ملف صوره(?: |$)(.*)"))
async def on_file_to_photo(event):
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return await edit_delete(event, "**⌔︙هـذه ليسـت صـورة !**")
    if not image.mime_type.startswith("image/"):
        return await edit_delete(event, "**⌔︙هـذه ليسـت صـورة !**")
    if image.mime_type == "image/webp":
        return await edit_delete(event, "**⌔︙لتحويـل الملصـق إلى صـورة إستخـدم الأمـر  ⩥ :**  `.تحويل ملف صوره`")
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    catt = await edit_or_reply(event, "**⌔︙جـاري التحويـل  ↯**")
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await catt.delete()
@iqthon.on(admin_cmd(pattern="تحويل ملصق متحرك(?:\s|$)([\s\S]*)"))
async def _(event):  # sourcery no-metrics
    input_str = event.pattern_match.group(1)
    if not input_str:
        quality = None
        fps = None
    else:
        loc = input_str.split(";")
        if len(loc) > 2:
            return await edit_delete(
                event,
                "**⌔︙بنـاء جملـة خاطـئ !**",
            )
        if len(loc) == 2:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "**⌔︙إستخـدم جـودة النطـاق مـن 0 إلى 721 ✦**")
            if 0 < loc[1] < 20:
                quality = loc[1].strip()
            else:
                return await edit_delete(event, "**⌔︙إستخـدم جـودة النطـاق مـن 0 إلى 20 ✦**")
        if len(loc) == 1:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "**⌔︙إستخـدم جـودة النطـاق مـن 0 إلى 721 ✦**")
    catreply = await event.get_reply_message()
    cat_event = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not catreply or not catreply.media or not catreply.media.document:
        return await edit_or_reply(event, "**⌔︙هـذا ليـس ملصـق متحرك   !**")
    if catreply.media.document.mime_type != "application/x-tgsticker":
        return await edit_or_reply(event, "**⌔︙هـذا ليـس ملصـق متحرك  !**")
    catevent = await edit_or_reply(
        event,
        "⌔︙جـاري تحويـل هـذا الملصـق إلى صـورة متحرڪـة، قـد يستغـرق هـذا بضـع دقائـق ✦",
        parse_mode=_format.parse_pre,
    )
    try:
        cat_event = Get(cat_event)
        await event.client(cat_event)
    except BaseException:
        pass
    reply_to_id = await reply_id(event)
    catfile = await event.client.download_media(catreply)
    catgif = await make_gif(event, catfile, quality, fps)
    sandy = await event.client.send_file(
        event.chat_id,
        catgif,
        support_streaming=True,
        force_document=False,
        reply_to=reply_to_id,
    )
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for files in (catgif, catfile):
        if files and os.path.exists(files):
            os.remove(files)
@iqthon.on(admin_cmd(pattern="تحويل متحركه(?: |$)((-)?(r|l|u|d|s|i)?)$"))
async def pic_gifcmd(event):  # sourcery no-metrics
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(event, "**⌔︙قم بالـرد على صـورة أو ملصـق لجعلهـا صـورة متحرڪـة **")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edit_delete(
            event,
            "**⌔︙قم بالـرد على صـورة أو ملصـق لجعلهـا صـورة متحرڪـة، الملصقـات المتحرڪـة غيـر مدعومـة !**",
        )
    args = event.pattern_match.group(1)
    args = "i" if not args else args.replace("-", "")
    catevent = await edit_or_reply(event, "**⌔︙جـاري صنـع صـورة متحرڪـة من الوسائـط التي قمـت بالـرد عليهـا ↯**")
    imag = await _cattools.media_to_pic(event, reply, noedits=True)
    if imag[1] is None:
        return await edit_delete(
            imag[0], "**⌔︙تعـذّر إستخـراج الصـورة من الرسالـة التي تـم الـرّد عليهـا ✕**"
        )
    image = Image.open(imag[1])
    w, h = image.size
    outframes = []
    try:
        if args == "r":
            outframes = await r_frames(image, w, h, outframes)
        elif args == "l":
            outframes = await l_frames(image, w, h, outframes)
        elif args == "u":
            outframes = await ud_frames(image, w, h, outframes)
        elif args == "d":
            outframes = await ud_frames(image, w, h, outframes, flip=True)
        elif args == "s":
            outframes = await spin_frames(image, w, h, outframes)
        elif args == "i":
            outframes = await invert_frames(image, w, h, outframes)
    except Exception as e:
        return await edit_delete(catevent, f"**⌔︙خطـأ ⚠️**\n__{str(e)}__")
    output = io.BytesIO()
    output.name = "Output.gif"
    outframes[0].save(output, save_all=True, append_images=outframes[1:], duration=0.7)
    output.seek(0)
    with open("Output.gif", "wb") as outfile:
        outfile.write(output.getbuffer())
    final = os.path.join(Config.TEMP_DIR, "output.gif")
    output = await vid_to_gif("Output.gif", final)
    if output is None:
        await edit_delete(
            catevent, "**⌔︙حـدث خطـأ مـا في الوسائـط، لا أستطيـع تحويلهـا إلى صـورة متحرڪـة !**"
        )
        for i in [final, "Output.gif", imag[1]]:
            if os.path.exists(i):
                os.remove(i)
        return
    sandy = await event.client.send_file(event.chat_id, output, reply_to=reply)
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for i in [final, "Output.gif", imag[1]]:
        if os.path.exists(i):
            os.remove(i)
@iqthon.on(admin_cmd(pattern="تحويل فديو متحركه ?([0-9.]+)?$"))
async def _(event):
    reply = await event.get_reply_message()
    mediatype = media_type(event)
    if mediatype and mediatype != "video":
        return await edit_delete(event, "**⌔︙حـدث خطـأ مـا في الوسائـط، لا أستطيـع تحويلهـا إلى صـورة متحرڪـة !**")
    args = event.pattern_match.group(1)
    if not args:
        args = 2.0
    else:
        try:
            args = float(args)
        except ValueError:
            args = 2.0
    catevent = await edit_or_reply(event, "**⌔︙جـاري التحويـل إلى صـورة متحرڪة انتضر دقائق  ↯**")
    inputfile = await reply.download_media()
    outputfile = os.path.join(Config.TEMP_DIR, "vidtogif.gif")
    result = await vid_to_gif(inputfile, outputfile, speed=args)
    if result is None:
        return await edit_delete(event, "**⌔︙غيـر قـادر على تحويلهـا إلى صـورة متحرڪة !**")
    sandy = await event.client.send_file(event.chat_id, result, reply_to=reply)
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for i in [inputfile, outputfile]:
        if os.path.exists(i):
            os.remove(i)
