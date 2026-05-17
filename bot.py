import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from twilio.rest import Client

TELEGRAM_BOT_TOKEN = "ВСТАВЬ_ТОКЕН_БОТА"
TWILIO_ACCOUNT_SID = "ВСТАВЬ_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "ВСТАВЬ_AUTH_TOKEN"
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

def handle_message(update, context):
    text = update.message.text
    phone = extract_phone(text)
    if not phone:
        return
    try:
        twilio_client.calls.create(
            to=phone,
            from_=TWILIO_FROM_NUMBER,
            twiml=f"<Response><Say>Please hold.</Say><Dial>{NEXFIELD_NUMBER}</Dial></Response>"
        )
        update.message.reply_text(f"Calling {phone}")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
