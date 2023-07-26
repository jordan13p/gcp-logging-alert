import os
import telegram
from pathlib import Path
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook


class MessageSender:
    @staticmethod
    def send_tg_alert_message(alert_message):
        # set env variables
        env_path = str(Path(__file__).parents[2] / '.env')
        load_dotenv(dotenv_path=env_path)

        # send message to telegram bot
        bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
        bot.send_message(chat_id=os.getenv("TELEGRAM_USER_ID"), text=alert_message, parse_mode=telegram.ParseMode.HTML)

    @staticmethod
    def send_discord_alert_message(embed, discord_webhook_url):
        # send message to discord webhook
        webhook = DiscordWebhook(url=discord_webhook_url)

        # add embed object to webhook
        webhook.add_embed(embed)

        # execute send message
        webhook.execute()
