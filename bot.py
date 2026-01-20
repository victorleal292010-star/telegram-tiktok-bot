import os
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "👋 Hola!\n\n"
        "Envíame un enlace de TikTok y te descargaré el video sin marca de agua.\n"
        "🎵 El MP3 es solo para usuarios PREMIUM."
    )

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text

    if "tiktok.com" not in text:
        await message.reply("❌ Envíame un enlace válido de TikTok.")
        return

    api_url = f"https://tikwm.com/api/?url={text}"
    r = requests.get(api_url).json()

    if not r.get("data"):
        await message.reply("❌ No pude descargar ese video.")
        return

    video_url = r["data"]["play"]
    await message.reply_video(video_url)

if __name__ == "__main__":
    print("🤖 Bot en ejecución...")
    executor.start_polling(dp, skip_updates=True)
