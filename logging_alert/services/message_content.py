from discord_webhook import DiscordEmbed


TG_ERROR_LOG_MESSAGE_TEMPLATE = """
\U0001F525 <b><a href='{url}'>{container_name} alert!!</a></b> \U0001F525
Click link to view log \U00002934

<b>Env:</b>  {cluster_name}

<b>Namespaces:</b>  {namespace_name}

<b>Time:</b>  {dtime}  UTC +0

<b>Message:</b>
{message}
"""

TG_COUNTS_MESSAGE_TEMPLATE = """
\U0001F525 <b><a href='{url}'>{container_name}: {error_code} !!</a></b> \U0001F525
Click link to view log \U00002934

<b>Counts:</b>  {counts}

<b>Namespaces:</b>  {namespace_name}

<b>Time:</b>  {dtime}  UTC +0

<b>Message:</b>
{container_name} has encountered "{error_code}" {limit_times} or more times in {time_range_convert}.
"""


class TelegramMessage:
    def __init__(self, alert_message_data):
        self.alert_message_data = alert_message_data
        self.tg_message = ""

    def create_error_log_message(self):
        self.tg_message = TG_ERROR_LOG_MESSAGE_TEMPLATE.format(**self.alert_message_data)

    def create_counts_message(self):
        self.tg_message = TG_COUNTS_MESSAGE_TEMPLATE.format(**self.alert_message_data)


class DiscordMessage:
    def __init__(self, alert_message_data):
        self.alert_message_data = alert_message_data
        self.discord_embed = None

    def create_error_log_embed(self):
        self.discord_embed = DiscordEmbed(
            title='\U0001F525 ' + self.alert_message_data.get('container_name') + ' alert!! \U0001F525',
            description='Click link to view log \U00002934 \n',
            color='f80365'
        )

        self.discord_embed.set_url(url=self.alert_message_data.get('url'))
        self.discord_embed.add_embed_field(name='Env', value=self.alert_message_data.get('cluster_name'))
        self.discord_embed.add_embed_field(name='Namespaces', value=self.alert_message_data.get('namespace_name'))
        self.discord_embed.add_embed_field(name='Time', value=self.alert_message_data.get('dtime') + '  UTC +0')
        self.discord_embed.add_embed_field(name='Message', value=self.alert_message_data.get('message'), inline=False)

    def create_counts_embed(self):
        self.discord_embed = DiscordEmbed(
            title='\U0001F525 '+ self.alert_message_data.get('container_name') + ": " + self.alert_message_data.get('error_code') +' !! \U0001F525',
            description='Click link to view log \U00002934 \n',
            color='f80365'
        )

        self.discord_embed.set_url(url=self.alert_message_data.get('url'))
        self.discord_embed.add_embed_field(name='Counts', value=self.alert_message_data.get('counts'))
        self.discord_embed.add_embed_field(name='Namespaces', value=self.alert_message_data.get('namespace_name'))
        self.discord_embed.add_embed_field(name='Time', value=self.alert_message_data.get('dtime') + '  UTC +0')
        self.discord_embed.add_embed_field(name='Message', value=self.alert_message_data.get('container_name') + ' has encountered "' + self.alert_message_data.get('error_code') + '" ' + str(self.alert_message_data.get('limit_times')) + ' or more times in '+ str(self.alert_message_data.get('time_range_convert')) + '.', inline=False)
