from asyncio import sleep

import requests
import random
from userbot import iqthon

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
    pattern="افتارات عيال",
    command=("افتارات عيال", plugin_category),
    info={
        "header": "Searches the given query in Google and shows you the link of that query.",
        "usage": "{tr}افتارات عيال<Query>",
    },
)
async def _(event):
    "افتارات عيال"
    ran = random.randint(1,200)
    photo = f"https://t.me/aftaraatt/{ran}"
    done = await client.download_media(photo,"/d.png")
    await event.client.send_file(event.chat_id,"/d.png")


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

