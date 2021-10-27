from asyncio import sleep

import requests
import random
from userbot import iqthon
from telethon.tl.types import InputMessagesFilterPhotos
import re
from bs4 import BeautifulSoup
import bs4
import time
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@iqthon.iq_cmd(
    pattern="بحوثات كوكل ([\s\S]*)",
    command=("بحوثات كوكل", plugin_category),
    info={
        "header": "Searches the given query in Google and shows you the link of that query.",
        "usage": "{tr}بحوثات كوكل <Query>",
    },
)
async def _(event):
    "بحوثات كوكل"
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=http://google.com/search?q={}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "⌔︙جـاري البحـث ↯")
    await sleep(2)
    if response_api:
        await event.edit(
            "**⌔︙دعنـي أبحـث عن هـذا في جـوجل ↯**\n👉 [{}]({})".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "**⌔︙حـدث خطـأ مـا، الرجـاء تڪرار المحاولـة ⚠️**", 5)


@iqthon.iq_cmd(
    pattern="انمي",
    command=("انمي", plugin_category),
    info={
        "header": "Searches the given query in Google and shows you the link of that query.",
        "usage": "{tr}انمي <Query>",
    },
)
async def _(event):
    def geturl(name):
        r = requests.get(f"https://ww.anime4up.com/?search_param=animes&s={name}")
        soup = BeautifulSoup(r.content, 'html.parser')
        u = soup.find("a", {'class': 'overlay'})
        # u2 = soup.findAll("div",attrs={'class':'hover ehover6'})[1]
        url = "".join(re.findall("href=\"(.*?)\"></a>", str(u)))
        return url

    def getespodie(number, url):
        try:
            g = requests.get(url)
            soup44 = BeautifulSoup(g.content, 'html.parser')
            all = '\n'.join(re.findall("<h3><a href=\"(.*?)\"", str(soup44)))
            x = all.splitlines()
            se = x[int(number)]
            return se
        except:
            return "error"

    def done_all(url):
        try:
            dod = requests.get(url).text
            st = "".join(re.findall("\"https://www.solidfiles.com/v/(.*?)\">", str(dod)))
            GetLasts = requests.get('https://www.solidfiles.com/v/' + st).text
            Dlink = "".join(re.findall("jpg\",\"streamUrl\":\"(.*?)\",", str(GetLasts)))
            return Dlink
        except:
            return "error"

    def for_laksis(url):
        try:
            r = requests.get(url).content
            soup = BeautifulSoup(r, 'html.parser')
            url2 = "\n".join(re.findall("file: '(.*?)'", str(soup))).splitlines()[0]
            return url2
        except:
            return "error"

    def sherd(url):
        get = requests.get(url)
        soup = bs4.BeautifulSoup(get.content, "html.parser")
        try:
            shr = "\n".join(re.findall("<a data-ep-url=\"(.*?)\" id=\"4shared", str(soup)))
            return shr
        except:
            try:
                shr2 = "\n".join(re.findall("data-ep-url=\"(.*?)\">4sha", str(soup)))
                return shr2
            except:
                return None

    def fuck_jasim(url):
        get = requests.get(url)
        soup = bs4.BeautifulSoup(get.content, "html.parser")
        shr = "\n".join(re.findall("www\.4shared\.com/video/(.*?)\.html", str(soup)))
        all_thing = f"https://www.4shared.com/video/{shr}.html"
        r = requests.get(all_thing).content
        soup = BeautifulSoup(r, 'html.parser')
        try:
            url2 = "\n".join(re.findall("file: '(.*?)'", str(soup))).splitlines()[0]
        except:
            return None
        return url2

    try:
        "انمي"
        reply = await event.get_reply_message()
        reply_re = "".join(re.findall(", message='(.*?)',", str(reply)))
        name = "".join(re.findall("انمي(.*?)الحلقه", str(reply_re)))
        number = reply_re.split("الحلقه")[1]
        url_base = geturl(name)
        ass = getespodie(number, url_base)
        sososos = fuck_jasim(ass)
        await edit_or_reply(event, f"[- رابط مباشر للحلقة .]({sososos})"
                                   f"\n"
                                   f"- #Coding By : Laksis .")
    except Exception as er:
        print(er)


@iqthon.iq_cmd(
    pattern="بحوثات يوتيوب ([\s\S]*)",
    command=("بحوثات يوتيوب", plugin_category),
    info={
        "header": "Searches the given query in youtube and shows you the link of that query.",
        "usage": "{tr}بحوثات يوتيوب <Query>",
    },
)
async def _(event):
    "Searches the given query in youtube and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = (
        "https://da.gd/s?url=https://www.youtube.com/results?search_query={}".format(
            input_str.replace(" ", "+")
        )
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "**⌔︙جـاري البحـث ↯**")
    await sleep(2)
    if response_api:
        await event.edit(
            "**⌔︙دعنـي أبحـث عن هـذا في يوتيـوب ↯:**\n👉 [{}]({})".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "**⌔︙حـدث خطـأ مـا، الرجـاء تڪرار المحاولـة ⚠️**", 5)

