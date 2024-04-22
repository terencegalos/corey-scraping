from telegram import Bot
from telegram.error import TelegramError
import asyncio

TELEGRAM_BOT_TOKEN = '7124421907:AAH-o9xnZiP7mF8dF0xRm0eVHzde0jqO3cw'
CHAT_ID = "6540845789" #6540845789 -4053668750

async def send_telegram_message(message):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await  bot.send_message(chat_id=CHAT_ID,text=message)
        print("Telegram notification sent successfully.")
    except TelegramError as e:
        print(f"Error sending Telegram message: {e}")

async def main():
    message = "This is a test sent by a Telegram Bot."
    await send_telegram_message(message)


if __name__ == "__main__":
    asyncio.run(main())


