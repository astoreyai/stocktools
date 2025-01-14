from telegram.ext import ApplicationBuilder
import asyncio
import logging
from dotenv import load_dotenv
import os

class TelegramNotifier:
    def __init__(self, token, chat_id):
        """
        Initialize the Telegram notifier using the ApplicationBuilder.

        :param token: Telegram bot token
        :param chat_id: Telegram chat ID where messages will be sent
        """
        if not token or not chat_id:
            raise ValueError("Token and Chat ID must be provided.")
        
        self.application = ApplicationBuilder().token(token).build()
        self.chat_id = chat_id

    async def async_send_message(self, text, parse_mode="Markdown"):
        """
        Send a message asynchronously via Telegram bot.

        :param text: Message to send
        :param parse_mode: Formatting style (Markdown or HTML)
        """
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text=text, parse_mode=parse_mode)
            logging.info("✅ Message sent successfully via Telegram.")
        except Exception as e:
            logging.error(f"❌ Failed to send message: {e}")
        finally:
            await self.application.shutdown()

    def send_message(self, text, parse_mode="Markdown"):
        """
        Wrapper for sending Telegram messages.

        Automatically detects whether the event loop is already running.

        :param text: Message to send
        :param parse_mode: Formatting style (Markdown or HTML)
        """
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
    def format_signals(strategies_dict):
        """
        Format the signals from different strategies for sending via Telegram.

        :param strategies_dict: Dictionary of strategies and their corresponding stock signals.
                               Example: {
                                   "Strategy A": [("AAPL", "10:30 AM"), ("MSFT", "11:00 AM")],
                                   "Strategy B": [("GOOG", "12:00 PM")]
                               }
        :return: Formatted message as a string
        """
        if not strategies_dict or all(not stocks for stocks in strategies_dict.values()):
            return "🚨 *No valid stock signals were generated in the past day.* 🚨"

        # Build the message header
        message = "🚨 *Stock Signals* 🚨\n\n"

        # Iterate through strategies and append formatted signals
        for strategy, stocks in strategies_dict.items():
            if stocks:
                stock_list = ', '.join(
                    f"{stock} (at {timestamp})" for stock, timestamp in stocks
                )
                message += f"🔹 *{strategy}*: {stock_list}\n"
            else:
                message += f"🔹 *{strategy}*: No signals generated.\n"

        return message


# Example Usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load environment variables from .env file
    load_dotenv()

    # Get the token and chat ID from environment variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Validate token and chat ID
    if not token or not chat_id:
        raise ValueError("Please provide TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the .env file.")

    notifier = TelegramNotifier(token, chat_id)

    # Example stock signals
    signals = {
        "Strategy A": [("AAPL", "10:30 AM"), ("MSFT", "11:00 AM")],
        "Strategy B": [("GOOG", "12:00 PM")],
        "Strategy C": []
    }

    # Uncomment the line below to test the notifier
    # formatted_message = notifier.format_signals(signals)
    # notifier.send_message(formatted_message)

    # Test Function
    def test_telegram_notifier():
        """
        Test the TelegramNotifier class with a mock signals dictionary.
        """
        print("Running test for TelegramNotifier...")

        # Test data
        test_signals = {
            "Strategy X": [("TSLA", "9:00 AM"), ("NFLX", "10:15 AM")],
            "Strategy Y": [],
        }

        # Format the signals
        formatted_message = notifier.format_signals(test_signals)

        # Output the formatted message
        print("Formatted Message:")
        print(formatted_message)

        # Mock sending the message (Comment out to avoid actual message sending during tests)
        notifier.send_message(formatted_message)

    # Uncomment the line below to run the test function
    test_telegram_notifier()