import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import os

TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("Salom! Menga Terabox havolasini yuboring, men sizga yuklab olish linkini chiqarib beraman.")

def handle_link(update, context):
    url = update.message.text.strip()

    if "terabox" not in url and "shortlinkshare" not in url:
        update.message.reply_text("Bu Terabox havolasiga o‘xshamayapti.")
        return

    update.message.reply_text("Iltimos, kuting... Yuklab olish linki olinmoqda...")

    try:
        api_url = f"https://teraboxdownloader.com/api/download?url={url}"
        res = requests.get(api_url)
        data = res.json()

        if "downloadUrl" in data:
            dl_link = data["downloadUrl"]
            filename = data.get("file_name", "video")
            update.message.reply_text(f"✅ *{filename}*
⬇️ [Yuklab olish havolasi]({dl_link})", parse_mode='Markdown')
        else:
            update.message.reply_text("Linkni olishda muammo bo‘ldi yoki video yopiq.")

    except Exception as e:
        update.message.reply_text("Xatolik yuz berdi: " + str(e))

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_link))

updater.start_polling()
updater.idle()
