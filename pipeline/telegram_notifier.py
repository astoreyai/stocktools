import asyncio
import telegram
from config import TOKEN, CHAT_ID

class TelegramNotifier:
    def __init__(self, token, chat_id):
        """Initialize the Telegram bot with token and chat ID."""
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    async def async_send_message(self, text):
        """Send a message asynchronously via Telegram bot."""
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text)
        except telegram.error.TelegramError as e:
            print(f"Failed to send message: {e}")

    def send_message(self, text):
        """Wrapper for sending Telegram messages."""
        # Check if there's an event loop running and use the correct approach
        try:
            if asyncio.get_event_loop().is_running():
                # If an event loop is already running, use create_task
                asyncio.create_task(self.async_send_message(text))
            else:
                # If no event loop is running, use asyncio.run
                asyncio.run(self.async_send_message(text))
        except Exception as e:
            print(f"Error during telegram message send: {e}")

    @staticmethod
    def format_signals(strategies_dict):
        """Format the signals from different strategies for sending via Telegram."""
        message = "🚨 Stock Signals 🚨\n\n"
        for strategy, stocks in strategies_dict.items():
            if stocks:
                message += f"🔹 *{strategy}*: {', '.join(stocks)}\n"
        return message


# Example usage
if __name__ == "__main__":
    notifier = TelegramNotifier(token=TOKEN, chat_id=CHAT_ID)
    
    # Example strategies_dict from process_signals.py
    strategies_dict = {
        'ITG Scalper + MACD': ['AAPL', 'GOOGL'],
        'Bollinger Bands + RSI': ['MSFT'],
        'RSI + Alligator': ['TSLA', 'AMZN']
    }

    # Format the message
    message = notifier.format_signals(strategies_dict)

    # Send the message
    notifier.send_message(message)
