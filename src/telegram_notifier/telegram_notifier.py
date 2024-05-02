from telegram import Bot
from telegram.error import TelegramError
# import asyncio

TELEGRAM_BOT_TOKEN = '7124421907:AAH-o9xnZiP7mF8dF0xRm0eVHzde0jqO3cw'
GROUP_CHAT = '-4053668750'
TEST_CHAT = '-4186476202'
BOT_CHAT = '6540845789'
CHAT_ID = GROUP_CHAT # Specify chat id here

async def send_telegram_message(message='This is a test message.'):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await  bot.send_message(chat_id=CHAT_ID,text=message)
        print("Telegram notification sent successfully.")
    except TelegramError as e:
        print(f"Error sending Telegram message: {e}")


# asyncio.run(send_telegram_message())