import re
import json
import aiohttp
from pyrogram import Client, filters
import requests
import emoji
from config import *


# ##################################  droplink  #################################################################

@Client.on_message(filters.command('short'))
async def reply_text(c, m):

    text = await m.reply_text("`Processing...... May take some time`")

    if m.reply_to_message.reply_markup:
        msg = ""
        txt = m.reply_to_message.reply_markup
        print(txt)
        txt = json.loads(str(txt))
        for t in txt["inline_keyboard"]:
            for j in t:
                texts = j["text"]
                url = j["url"]
                urls = await get_shortlink(url)
                msg += f"**{texts} - [👉 Link 🔗]({urls})**\n\n"
                print(msg)
                print(urls)
        print(msg)
        await m.reply_text(msg)

    elif m.reply_to_message.text:
        txt = await bulk_shortener(m.reply_to_message.text)
        r = f"**{txt}**\n\n**{SUPPORT_CHANNEL}**"
        await m.reply_text(r)
    elif m.reply_to_message.media:
        txt = await bulk_shortener(m.reply_to_message.caption)
        id = m.reply_to_message.photo.file_id
        r = f"**{txt}**\n\n**{SUPPORT_CHANNEL}**"
        await m.reply_photo(id, caption=r)

    await text.delete()



async def bulk_shortener(message):
    emoji_text = message.split()

    for emojis in emoji_text:
        isEmoji = emoji.is_emoji(emojis)
        if isEmoji is True:
            message = message.replace(emojis, "")
        else:
            pass
    urls = re.findall(r'https?://[^\s]+', message)
    for url in urls:
        short_link = await get_shortlink(url)
        short_link = f"[👉 Link 🔗]({short_link})"
        if url in message:
            message = message.replace(url, short_link)

    return message


async def get_shortlink(link):
    url = f'https://{WEBSITE}/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            return data["shortenedUrl"]


# ##################################  Mdisk  #################################################################


@Client.on_message(filters.command('mdisk'))
async def mdisk(c, m):
    try:
        text = await m.reply_text("`Processing...... May take some time`")
        if m.reply_to_message.reply_markup:
            msg = ""
            txt = m.reply_to_message.reply_markup
            print(txt)
            txt = json.loads(str(txt))
            for t in txt["inline_keyboard"]:
                for j in t:
                    texts = j["text"]
                    url = j["url"]
                    urls = await get_mdisk(url)
                    msg += f"**{texts} - [👉 Link 🔗]({urls})**\n\n"
                    print(msg)
                    print(urls)
            print(msg)
            await m.reply_text(msg)

        elif m.reply_to_message.text:
            txt = await mdisk_bulk_shortener(m.reply_to_message.text)
            r = f"**{txt}**\n\n**{SUPPORT_CHANNEL}**"
            await m.reply_text(r)
        elif m.reply_to_message.media:
            txt = await mdisk_bulk_shortener(m.reply_to_message.caption)
            id = m.reply_to_message.photo.file_id
            r = f"**{txt}**\n\n**{SUPPORT_CHANNEL}**"
            await m.reply_photo(id, caption=r)
        await text.delete()
    except Exception as e:
        await text.delete()
        await m.reply_text(f"`Some Error Occurred, Reply only to MDisk links\n\n{e}`")


async def mdisk_bulk_shortener(message):
    urls = re.findall(r'https?://[^\s]+', message)
    for url in urls:
        mdisk_link = await get_mdisk(url)
        mdisk_link = f"[👉 Link 🔗]({mdisk_link})"
        if url in message:
            message = message.replace(url, mdisk_link)

    emoji_text = message.split()

    for emojis in emoji_text:
        isEmoji = emoji.is_emoji(emojis)
        if isEmoji is True:
            message = message.replace(emojis, "")
        else:
            pass

    return message


async def get_mdisk(link):
    url = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
    param = {'token':
                 MDISK_KEY, 'link': link
             }
    res = requests.post(url, json=param)
    shareLink = res.json()
    return shareLink["sharelink"]


########################################Mdisk and droplink#######################################################


@Client.on_message(filters.command('bulk'))
async def shorten(c, m):
    try:
        text = await m.reply_text("`Converting other MDisk links to your MDisk account... May take some time`")
        if m.reply_to_message.reply_markup:
            msg = ""
            txt = m.reply_to_message.reply_markup
            print(txt)
            txt = json.loads(str(txt))
            for t in txt["inline_keyboard"]:
                for j in t:
                    texts = j["text"]
                    url = j["url"]
                    mdisk_url = await get_mdisk(url)
                    urls = await get_shortlink(mdisk_url)
                    msg += f"**{texts} - [👉 Link 🔗]({urls})**\n\n"
                    print(msg)
                    print(urls)
            print(msg)
            await m.reply_text(msg)
        elif m.reply_to_message.text:
            txt = await mdisks_bulk_shortener(m.reply_to_message.text)
            await text.edit(
                "Converted all links to your MDisk account. Now converting all your MDisk links to droplink url.....")
            txt = await bulk_shortener(txt)
            r = f"**{txt}**\n\n**{SUPPORT_CHANNEL}**"
            await m.reply_text(r)

        elif m.reply_to_message.media:
            txt = await mdisks_bulk_shortener(m.reply_to_message.caption)
            txt = await bulk_shortener(txt)
            id = m.reply_to_message.photo.file_id
            r = f"**{txt}**\n\n**{SUPPORT_CHANNEL}**"
            await m.reply_photo(id, caption=r)

        await text.delete()
    except:
        await text.delete()
        await m.reply_text("`Some Error Occurred, Reply only to MDisk links`")


async def mdisks_bulk_shortener(message):
    urls = re.findall(r'https?://[^\s]+', message)
    for url in urls:
        mdisk_link = await get_mdisk(url)
        if url in message:
            message = message.replace(url, mdisk_link)

    emoji_text = message.split()

    for emojis in emoji_text:
        isEmoji = emoji.is_emoji(emojis)
        if isEmoji is True:
            message = message.replace(emojis, "")
        else:
            pass

    return message
