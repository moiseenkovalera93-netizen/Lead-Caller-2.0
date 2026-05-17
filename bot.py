import re
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from twilio.rest import Client

TELEGRAM_BOT_TOKEN = "8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg"
TWILIO_ACCOUNT_SID = "AC93fa6ab5de0da1e3dd0de4714b6105cc"
TWILIO_AUTH_TOKEN = "90dcaf93695e27878f4c7542b5fb4d67"
TWILIO_FROM_NUMBER = "+19165716526"
NEXFIELD_NUMBER = "+19165071904"

logging.basicConfig(level=logging.INFO)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def extract_phone(text):
    patterns = [r'\+1\s?\d{10}', r'\+\d{11,12}', r'\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            digits = re.sub(r'[^\d]', '', match.group())
            if len(digits) == 10:
                return f"+1{digits}"
            elif len(digits) >= 11:
                return f"+{digits}"
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    phone = extract_phone(text)
    if not phone:
        return
        await asyncio.sleep(120)
    try:
        twilio_client.calls.create(
            to=phone,
            from_=TWILIO_FROM_NUMBER,
            twiml=f"<Response><Say>Please hold.</Say><Dial>{NEXFIELD_NUMBER}</Dial></Response>"
        )
        await update.message.reply_text(f"Calling {phone}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
