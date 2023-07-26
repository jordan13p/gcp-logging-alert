import json
import pandas as pd
from base64 import b64decode
from ..utils.logger import StructuredLogger


class InitData:
    def __init__(self, envelope):
        self.envelope = envelope
        self._message_data = {}
        self.alert_message_data = {}

    def get_message_data(self):
        # check pub/sub message received
        if not self.envelope:
            msg = "no Pub/Sub message received"
            StructuredLogger.log_error(f"Bad Request: {msg}")

        # check pub/sub message json
        if not isinstance(self.envelope, dict) or "message" not in self.envelope:
            msg = "invalid Pub/Sub message format"
            StructuredLogger.log_error(f"Bad Request: {msg}")

        # get message json from envelope
        pubsub_message = self.envelope["message"]

        # check data in message json
        if isinstance(pubsub_message, dict) and "data" in pubsub_message:
            # base64 decode and get message_data from data json
            data = b64decode(pubsub_message["data"]).decode("utf-8")
            self._message_data = json.loads(data)

        else:
            msg = "Key 'data' does not exists in pubsub_message dict."
            StructuredLogger.log_error(f"Bad Request: {msg}")

    def get_alert_message(self):
        if "jsonPayload" in self._message_data:
            # ex. "2022-04-18T09:14:34.059312957Z" -> "2022-04-18 09:14:34"
            # ex. "2022-04-18T09:14:34.059312957Z" -> "1650273274.059"
            log_dtime = pd.Timestamp(self._message_data.get('timestamp')).tz_convert(None).round(freq = "S")
            log_timestamp = pd.Timestamp(self._message_data.get('timestamp')).tz_convert(None).round(freq = "L").timestamp()

            # new message data
            self.alert_message_data = {
                'message': self._message_data.get('jsonPayload').get('message'), 
                'dtime': str(log_dtime),
                'timestamp': log_timestamp
            }

        elif "textPayload" in self._message_data:
            # ex. "2022-04-18T09:14:34.059312957Z" -> "2022-04-18 09:14:34"
            # ex. "2022-04-18T09:14:34.059312957Z" -> "1650273274.059"
            log_dtime = pd.Timestamp(self._message_data.get('timestamp')).tz_convert(None).round(freq = "S")
            log_timestamp = pd.Timestamp(self._message_data.get('timestamp')).tz_convert(None).round(freq = "L").timestamp()

            # new message data
            self.alert_message_data = {
                'message': self._message_data.get('textPayload'), 
                'dtime': str(log_dtime),
                'timestamp': log_timestamp
            }
    
        else:
            msg = "Key 'data' does not have Payload message."
            StructuredLogger.log_error(f"Bad Request: {msg}")

        if len(self.alert_message_data['message']) > 1024:
            self.alert_message_data['message'] = "Attention: The logging alert message is too long. Please check the log in Cloud Logging."
    
        # new k8s message data
        k8s_message_data = self._message_data.get('resource').get('labels')

        # Python 3.9+, message data + k8s message data
        self.alert_message_data |= k8s_message_data
