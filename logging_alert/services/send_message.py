import os
from time import sleep
from datetime import datetime
from random import randint
import multiprocessing
from pathlib import Path
from dotenv import load_dotenv
from ..utils.logger import StructuredLogger
from ..utils.messenger import MessageSender
from ..services.message_content import TelegramMessage, DiscordMessage
from ..services.counts_check import CountsAlertMessageCheck


# set env variables
env_path = str(Path(__file__).parents[2] / '.env')
load_dotenv(dotenv_path = env_path)

# add lock
lock = multiprocessing.RLock()


class AlertSender(TelegramMessage, DiscordMessage, MessageSender):
    def __init__(self, alert_message_data):
        TelegramMessage.__init__(self, alert_message_data)
        DiscordMessage.__init__(self, alert_message_data)
        self.cluster_name = self.alert_message_data.get('cluster_name')
        self.namespace_name = self.alert_message_data.get('namespace_name')
    
    def send_error_log_message(self):
        try:
            if self.cluster_name == "prod-asia-01":
                discord_webhook_url = os.getenv("PROD_DISCORD_WEBHOOK_URL")

                sleep(randint(50, 500) / 1000)
                self.create_error_log_message()
                self.send_tg_alert_message(self.tg_message)

            elif self.namespace_name == "pre-2b-power11":
                discord_webhook_url = os.getenv("PREPROD_DISCORD_WEBHOOK_URL")
            
            else:
                discord_webhook_url = os.getenv("DEV_DISCORD_WEBHOOK_URL")
                
            sleep(randint(50, 500) / 1000)
            self.create_error_log_embed()
            self.send_discord_alert_message(self.discord_embed, discord_webhook_url)

        except Exception as err:
            msg = "[ERROR] " + str(err) + " (Maybe, the bot will not be able to send more than 20 or 30 messages per minute to the same group.)"
            StructuredLogger.log_error(msg)

    def send_counts_log_message(self):
        with lock:
            limit_times = self.alert_message_data.get('limit_times')

            counts_check = CountsAlertMessageCheck(self.alert_message_data)
            counts_check.create_folder()
            time_list = counts_check.check_time_list()
            send_message_flag = counts_check.check_send_message_period()

             # 10 times or more times in 10 minutes
            if len(time_list) > limit_times - 1 and send_message_flag:
                # add counts data to alert_message_data
                self.alert_message_data['counts'] = len(time_list)
            
                try:
                    counts_check.write_send_message_time()

                    if self.cluster_name == "prod-asia-01":
                        discord_webhook_url = os.getenv("PROD_DISCORD_WEBHOOK_URL")

                        # telegram bot message limit: 20 messages / min
                        self.create_counts_message()
                        self.send_tg_alert_message(self.tg_message)

                    elif self.namespace_name == "pre-asia-01":
                        discord_webhook_url = os.getenv("PREPROD_DISCORD_WEBHOOK_URL")

                    else:
                        discord_webhook_url = os.getenv("DEV_DISCORD_WEBHOOK_URL")

                    # discord webhook message limit: 30 messages / min
                    self.create_counts_embed()
                    self.send_discord_alert_message(self.discord_embed, discord_webhook_url)

                except Exception as err:
                    msg = "[ERROR] " + str(err) + " (Maybe, the bot will not be able to send more than 20 or 30 messages per minute to the same group.)"
                    StructuredLogger.log_error(msg)
