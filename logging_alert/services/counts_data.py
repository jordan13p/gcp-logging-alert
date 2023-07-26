import os, re
import urllib.parse
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from ..services.init_data import InitData
from ..utils.logger import StructuredLogger


# set env variables
env_path = str(Path(__file__).parents[2] / '.env')
load_dotenv(dotenv_path = env_path)


class CountsAlertMessage(InitData):
    def __init__(self, envelope):
        super().__init__(envelope)
        self.error_code = ""
        self.limit_times = 0
        self.time_range = 0
        self.time_range_convert = ""
        self.url = ""

    def get_error_code(self):
        # self.get_alert_message()
        try:
            # regex
            # "(?i:error)" case-insensitive "error"
            # ".?" 0 or 1 any characters
            # "(?i:code)" case-insensitive "code"
            # "\ *=\ *" 0 or numerous blank character before "=" or after "="
            # "([A-Z]+(?:_[A-Z]+)*)" get all capital and underscore from message, ex. "EXTERNAL_API_ERROR"
            # match = re.search(r'(?i:error)?.?(?i:code)\ *=\ *([A-Z]+(?:_[A-Z]+)*)', message)
            match = re.search(r'([A-Z]+(?:_[A-Z]+)+)', self.alert_message_data.get('message'))
            self.error_code = match.group(1)

        except Exception as err:
            msg = "(" + str(err) + ") Can not get error code from message."
            StructuredLogger.log_error(f"Bad Request: {msg}")
    
    def get_time_data(self):
        limit_times = os.getenv('LIMIT_TIMES_' + self.error_code, os.getenv('LIMIT_TIMES'))
        time_range = os.getenv('TIME_RANGES_' + self.error_code, os.getenv('TIME_RANGES'))

        self.limit_times = int(limit_times)
        self.time_range = int(time_range)
        self.time_range_convert = f"{self.time_range // 3600} Hours {self.time_range % 3600 // 60} Minutes"

    def get_counts_url(self):
        resource_data = self._message_data.get('resource')

        search_query = 'resource.type="' + resource_data.get('type') + '"\n' + \
            'resource.labels.container_name="' + resource_data.get('labels').get('container_name') + '"\n' + \
            'resource.labels.cluster_name="' + resource_data.get('labels').get('cluster_name') + '"\n' + \
            'jsonPayload.message=~"^.*(' + self.error_code + ').*$"'

        # url encode
        search_query_urlencode = urllib.parse.quote_plus(search_query) + ';'

        # time range
        datetime = pd.to_datetime(self._message_data.get('timestamp'))

        # 計算前後10分鐘的時間差
        start_datetime = datetime - pd.Timedelta(minutes=10)
        start_time = start_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        end_datetime = datetime + pd.Timedelta(minutes=10)
        end_time = end_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        time_range = 'timeRange=' + start_time + '%2F' + end_time + ';'

        # url data
        summary_fields = 'summaryFields=:false:32:beginning:false;'
        cursor_timestamp = 'cursorTimestamp=' + self._message_data.get('timestamp')
        others = '?authuser=0&project=' + resource_data.get('labels').get('project_id')

        self.url = 'https://console.cloud.google.com/logs/query;query=' + search_query_urlencode + time_range + summary_fields + cursor_timestamp + others

    def add_data(self, key, value):
        self.alert_message_data[key] = value

    def get_alert_message_data(self):
        self.get_message_data()
        self.get_alert_message()
        self.get_error_code()
        self.get_time_data()
        self.get_counts_url()

        self.add_data('error_code', self.error_code)
        self.add_data('limit_times', self.limit_times)
        self.add_data('time_range', self.time_range)
        self.add_data('time_range_convert', self.time_range_convert)
        self.add_data('url', self.url)

        return self.alert_message_data