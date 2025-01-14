from telegram.ext import ApplicationBuilder
import asyncio
import logging
from dotenv import load_dotenv
import os

load_dotenv()

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        # Load token and chat ID
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise ValueError("Telegram bot token and chat ID must be provided.")

        self.application = ApplicationBuilder().token(self.token).build()

    async def async_send_message(self, text, parse_mode="Markdown"):
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text=text, parse_mode=parse_mode)
            logging.info("✅ Message sent successfully via Telegram.")
        except Exception as e:
            logging.error(f"❌ Failed to send message: {e}")
        finally:
            await self.application.shutdown()

    def send_message(self, text, parse_mode="Markdown"):
        try:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self.async_send_message(text, parse_mode))
            else:
                asyncio.run(self.async_send_message(text, parse_mode))
        except RuntimeError as e:
            logging.error(f"❌ Runtime error during message send: {e}")
        except Exception as e:
            logging.error(f"❌ Unexpected error during Telegram message send: {e}")

    @staticmethod
    def format_signals(data):
        """
        Format stock signals for messaging.
        :param data: DataFrame containing stock symbols and their signal dates.
        :return: Formatted string message for Telegram.
        """
        if data.empty:
            return "🚨 *No stock signals generated in the past 3 days.* 🚨"

        # Build the message header
        message = "🚨 *Stock Signals from the Last 3 Days* 🚨\n\n"

        # Iterate through the data and format each signal
        for _, row in data.iterrows():
            message += f"🔹 `{row['Stock Symbol']}`: {row['Last Signal Date']}\n"

        return message
