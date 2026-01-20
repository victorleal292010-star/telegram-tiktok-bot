import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# El token se pondrá luego en Railway (NO aquí)
TOKEN = os.getenv("BOT_TOKEN")

# IDs premium (luego puedes agregar más)
PREMIUM_USERS = [
    123456789  # luego pondremos tu ID real
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu bot de TikTok\n\n"
        "📥 Envíame un link de TikTok\n"
        "🎬 Video sin marca GRATIS\n"
        "🔒 Audio MP3 solo PREMIUM"
    )

async def handle_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    link = update.message.text.strip()

    if "tiktok.com" not in link:
        await update.message.reply_text("❌ Ese no es un link válido de TikTok")
        return

    await update.message.reply_text("⏳ Procesando, espera un momento...")

    try:
        api_url = f"https://tikwm.com/api/?url={link}"
        response = requests.get(api_url, timeout=20)
        data = response.json()

        if "data" not in data:
            await update.message.reply_text("⚠️ No se pudo obtener el video")
            return

        video_url = data["data"].get("play")
        audio_url = data["data"].get("music")
        title = data["data"].get("title", "tiktok")

        # Enviar video (gratis)
        if video_url:
            await update.message.reply_video(video_url)

        # Enviar audio solo premium
        if user_id in PREMIUM_USERS:
            if audio_url:
                await update.message.reply_audio(audio_url, title=title)
        else:
            await update.message.reply_text(
                "🔒 El audio MP3 es PREMIUM\n"
                "💰 Escríbenos para activar el acceso"
            )

    except Exception as e:
        await update.message.reply_text("❌ Error al procesar el enlace")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tiktok))

print("🤖 Bot en ejecución")
app.run_polling()
