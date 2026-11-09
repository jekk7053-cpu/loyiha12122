
import logging
import random
import os
import asyncio

from aiohttp import web

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# Render Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

if not TOKEN:
    raise RuntimeError("BOT_TOKEN Environment Variable topilmadi!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

samimiy = [
    "<b>💗 MARJONA, BILASANMI?</b>\n\n"
    "Sen dunyodagi eng zo'r do'stsan! 🥹 "
    "Shu paytgacha uchratgan do'stlarim orasida "
    "eng zo'risan. Sen juda chiroyli, samimiy va "
    "go'zal qizsan. Hamma tomondan ideal qizsan! 🌸\n\n"
    "Doim shunday ajoyib bo'lib yur! 🦋❤️",

    "<b>🌷 SEN HAQIQATAN HAM AJOYIBSAN!</b>\n\n"
    "Sening kulishing, samimiyliging va fe'l-atvoring "
    "juda ham yoqimli. Sen bilan do'st bo'lish "
    "haqiqiy omad! 💕 Hech qachon o'zingni "
    "boshqalar bilan solishtirma, sen o'zingcha zo'rsan! 👑",

    "<b>🥹 MARJONA, SEN BETAKRORSAN!</b>\n\n"
    "Senga o'xshagan samimiy va chiroyli insonlar "
    "juda kam uchraydi. Kulganingda yanada chiroyli "
    "bo'lib ketasan! 😍 Doim kulib yur, senga "
    "tabassum juda yarashadi! 💗"
]

tilaklar = [
    "<b>🌸 MARJONA, SENGA TILAGIM...</b>\n\n"
    "Har bir kuning quvonch bilan boshlangan bo'lsin. "
    "Orzularing birin-ketin amalga oshsin. "
    "Ko'zlaring faqat baxtdan porlasin, yuzingdan "
    "tabassum hech qachon arimasin. 🥰\n\n"
    "Hayoting go'zal xotiralar va yaxshi insonlarga "
    "to'la bo'lsin! 💗🦋",

    "<b>💐 ENG CHIROYLI TILAKLARIM SENGA!</b>\n\n"
    "Doimo sog'-salomat, baxtli va omadli bo'l. "
    "Hech qachon xafa bo'lma, barcha niyatlaring "
    "amalga oshsin. Har bir yangi kun senga "
    "yangi quvonch olib kelsin! ❤️✨",

    "<b>🦋 MARJONA, DOIM SHUNDAY KULIB YUR!</b>\n\n"
    "Senga cheksiz baxt, omad, xotirjamlik va "
    "eng go'zal kunlarni tilayman. Atrofingda "
    "doimo seni qadrlaydigan insonlar bo'lsin. "
    "Hayoting doim gullab-yashnasin! 🌷💗"
]

marjona_haqida = [
    "<b>👑 MARJONA — TAKRORLANMAS INSON!</b>\n\n"
    "💎 Go'zallik — o'ziga yarashgan!\n"
    "🌸 Samimiylik — o'ziga xos!\n"
    "🦋 Xarakter — betakror!\n"
    "💗 Tabassum — juda chiroyli!\n"
    "✨ Do'stlik — bebaho!\n\n"
    "<b>Marjona, sen haqiqatan ham o'zgachasan!</b> 🥹",

    "<b>💖 MARJONA HAQIDA 7 TA FAKT</b>\n\n"
    "1. 👑 Takrorlanmas qiz!\n"
    "2. 🌷 Juda chiroyli!\n"
    "3. 💎 Samimiy va mehribon!\n"
    "4. 🦋 O'ziga xos xarakter egasi!\n"
    "5. 😍 Kulishi juda yoqimli!\n"
    "6. 💗 Ajoyib do'st!\n"
    "7. ✨ O'zicha ideal inson!",

    "<b>🥰 MARJONA — ALOHIDA BIR OLAM!</b>\n\n"
    "Sen dunyodagi hamma qizlardan farq qilasan. "
    "Sening o'ziga xosliging, samimiyliging va "
    "go'zalliging seni yanada betakror qiladi.\n\n"
    "<b>Sen kabi inson boshqa takrorlanmaydi!</b> 👑💗"
]


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💗 Samimiy so'zlar", callback_data="samimiy")],
        [InlineKeyboardButton("🌸 Tilak", callback_data="tilak")],
        [InlineKeyboardButton("👑 Marjona haqida", callback_data="about")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>🌸 ASSALOMU ALAYKUM, MARJONA! 🌸</b>\n\n"
        "💗 Senga atab kichkina sovg'a tayyorlandi.\n\n"
        "Bu yerda seni kutayotgan samimiy so'zlar, "
        "go'zal tilaklar va sen haqingdagi "
        "ajoyib fikrlar bor! 🥹🦋\n\n"
        "<b>O'zingga yoqqan bo'limni tanla:</b> 👇",
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "samimiy":
        text = random.choice(samimiy)
    elif query.data == "tilak":
        text = random.choice(tilaklar)
    elif query.data == "about":
        text = random.choice(marjona_haqida)
    else:
        return

    await query.message.reply_text(
        text,
        reply_markup=menu(),
        parse_mode=ParseMode.HTML
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>💗 MARJONA BOT</b>\n\n"
        "/start — Botni boshlash 🌸\n"
        "/help — Yordam 🦋",
        parse_mode=ParseMode.HTML
    )


# WEB SERVER
async def home(request):
    return web.Response(
        text="💗 MARJONA BOT ISH JARAYONIDA!",
        content_type="text/plain"
    )


async def health(request):
    return web.Response(
        text="OK",
        status=200
    )


async def main():
    # Telegram bot
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(buttons))

    # Web server
    web_app = web.Application()
    web_app.router.add_get("/", home)
    web_app.router.add_get("/health", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=PORT
    )

    await site.start()

    print(f"🌐 WEB SERVER ISHLADI: PORT {PORT}")

    try:
        # Botni ishga tushirish
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

        print("💗 MARJONA BOT ISHLAYAPTI!")

        # Ikkala xizmatni bir vaqtda ishlatish
        await asyncio.Event().wait()

    finally:
        if app.updater.running:
            await app.updater.stop()

        if app.running:
            await app.stop()

        await app.shutdown()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
