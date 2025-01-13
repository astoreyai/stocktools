from telegram.ext import Application
import asyncio

class TelegramNotifier:
    def __init__(self, token, chat_id):
        """Initialize the Telegram notifier using the Application."""
        self.application = Application.builder().token(token).build()
        self.chat_id = chat_id

    async def async_send_message(self, text):
        """Send a message asynchronously via Telegram bot."""
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text=text)
            print("Message sent successfully via Telegram.")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def send_message(self, text):
        """Wrapper for sending Telegram messages."""
        try:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self.async_send_message(text))
            else:
                asyncio.run(self.async_send_message(text))
        except Exception as e:
            print(f"Error during Telegram message send: {e}")

    @staticmethod
    def format_signals(strategies_dict):
        """Format the signals from different strategies for sending via Telegram."""
        if not strategies_dict:
            return "🚨 No valid stock signals were generated in the past day. 🚨"

        message = "🚨 *Stock Signals* 🚨\n\n"
        for strategy, stocks in strategies_dict.items():
            if stocks:
                stock_list = ', '.join(
                    f"{stock} (at {timestamp})" for stock, timestamp in stocks
                )
                message += f"🔹 *{strategy}*: {stock_list}\n"
        return message