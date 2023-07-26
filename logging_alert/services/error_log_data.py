import urllib.parse
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from ..services.init_data import InitData


# set env variables
env_path = str(Path(__file__).parents[2] / '.env')
load_dotenv(dotenv_path = env_path)


class AlertMessage(InitData):
    def __init__(self, envelope):
        super().__init__(envelope)
        self.url = ""

    def get_error_log_url(self):
        resource_data = self._message_data.get('resource')

        search_query = '(resource.type="' + resource_data.get('type') + '"\n' + \
            'resource.labels.container_name="' + resource_data.get('labels').get('container_name') + '"\n' + \
            'resource.labels.cluster_name="' + resource_data.get('labels').get('cluster_name') + '")\n' + \
            'OR\n' + \
            '(resource.type="http_load_balancer"\n' + \
            'resource.labels.backend_service_name=~"^.*(' + resource_data.get('labels').get('namespace_name') + ')-(' + resource_data.get('labels').get('container_name') + ').*$")'

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
        self.get_error_log_url()
        
        self.add_data('url', self.url)

        return self.alert_message_data
