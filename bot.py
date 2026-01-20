import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola!\n\n"
        "Envíame un enlace de TikTok y te descargaré el video sin marca de agua.\n"
        "🎵 El MP3 es solo para usuarios PREMIUM."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "tiktok.com" not in text:
        await update.message.reply_text("❌ Envíame un enlace válido de TikTok.")
        return

    # API Tikwm
    api_url = f"https://tikwm.com/api/?url={text}"
    r = requests.get(api_url).json()

    if not r.get("data"):
        await update.message.reply_text("❌ No pude descargar ese video.")
        return

    video_url = r["data"]["play"]
    await update.message.reply_video(video_url)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot en ejecución...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
