from telegram.ext import Application

# Replace with your actual bot token and chat ID
TOKEN = "7195903813:AAEB_3PUzafvjmqsqAUH0XbPrfb-0rsRdy4"
CHAT_ID = '6642709375'

async def test_bot():
    application = Application.builder().token(TOKEN).build()
    await application.bot.send_message(chat_id=CHAT_ID, text="Test message from TelegramNotifier!")

import asyncio
asyncio.run(test_bot())
