import unittest
from unittest.mock import Mock, patch
from ...services.error_log_data import AlertMessage

class TestAlertMessage(unittest.TestCase):
    def setUp(self):
        self.envelope = {
            "message": {
                "data": "eyJpbnNlcnRJZCI6IjAxODc2bWlsN2h2OXJqbG8iLCJqc29uUGF5bG9hZCI6eyJpbnN0YW50Ijp7ImVwb2NoU2Vjb25kIjoxNjUyNjM3NjExLCJuYW5vT2ZTZWNvbmQiOjQzNjkzOTAwMH0sImxldmVsIjoiRVJST1IiLCJtZXNzYWdlIjoiRXJyb3IuICh1c2VyPTAwMDAwIHZpbmVldGt1bWFyMTIzNDUsIHVybD1HRVQgL2dzL3YxL21hdGNoZXMvbXksIGVycm9yQ29kZT1FWFRFUk5BTF9BUElfRVJST1IpIiwidGhyZWFkIjoiaHR0cC1uaW8tODA4MC1leGVjLTMiLCJ0aHJlYWRQcmlvcml0eSI6NSwidGhyb3duIjp7Im5hbWUiOiJjb20uY2xvdWRsYXRpdHVkZS5nYW1lc2VydmVyLm1hdGNoLnF1ZXJ5LmFkYXB0ZXIubXkuR2V0TXlNYXRjaGVzUmVwb3NpdG9yeUV4Y2VwdGlvbiIsImV4dGVuZGVkU3RhY2tUcmFjZSI6W10sIm1lc3NhZ2UiOiJjb20uY2xvdWRsYXRpdHVkZS5zaGFyZWQuZXh0ZXJuYWwuVGhpcmRQYXJ0eUFwaUV4Y2VwdGlvbjogRXJyb3Igd2hlbiBjYWxsaW5nOiB0ZXN0IiwiY29tbW9uRWxlbWVudENvdW50IjowLCJsb2NhbGl6ZWRNZXNzYWdlIjoiY29tLmNsb3VkbGF0aXR1ZGUuc2hhcmVkLmV4dGVybmFsLlRoaXJkUGFydHlBcGlFeGNlcHRpb246IEVycm9yIHdoZW4gY2FsbGluZzogdGVzdCIsImNhdXNlIjp7ImNhdXNlIjp7ImNvbW1vbkVsZW1lbnRDb3VudCI6OTIsIm1lc3NhZ2UiOiI1MDAgSW50ZXJuYWwgU2VydmVyIEVycm9yOiBbbm8gYm9keV0iLCJuYW1lIjoib3JnLnNwcmluZ2ZyYW1ld29yay53ZWIuY2xpZW50Lkh0dHBTZXJ2ZXJFcnJvckV4Y2VwdGlvbiRJbnRlcm5hbFNlcnZlckVycm9yIiwiZXh0ZW5kZWRTdGFja1RyYWNlIjpbXSwibG9jYWxpemVkTWVzc2FnZSI6IjUwMCBJbnRlcm5hbCBTZXJ2ZXIgRXJyb3I6IFtubyBib2R5XSJ9LCJsb2NhbGl6ZWRNZXNzYWdlIjoiRXJyb3Igd2hlbiBjYWxsaW5nOiB0ZXN0IiwiY29tbW9uRWxlbWVudENvdW50Ijo5MiwibmFtZSI6ImNvbS5jbG91ZGxhdGl0dWRlLnNoYXJlZC5leHRlcm5hbC5UaGlyZFBhcnR5QXBpRXhjZXB0aW9uIiwibWVzc2FnZSI6IkVycm9yIHdoZW4gY2FsbGluZzogdGVzdCIsImV4dGVuZGVkU3RhY2tUcmFjZSI6W119fSwibG9nZ2VyRnFjbiI6Im9yZy5hcGFjaGUubG9nZ2luZyIsImxvZ2dlck5hbWUiOiJjb20uY2xvdWRsYXRpdHVkZS5nYW1lc2VydmVyLmNvbW1vbi5FeGNlcHRpb25BZHZpY2UiLCJ0aHJlYWRJZCI6NTd9LCJyZXNvdXJjZSI6eyJ0eXBlIjoiazhzX2NvbnRhaW5lciIsImxhYmVscyI6eyJwb2RfbmFtZSI6ImdhbWUtYXAtYjRjYzliYzY3LXpnMndrIiwibmFtZXNwYWNlX25hbWUiOiJsZWdlbmQtZmFudGFzeSIsImNvbnRhaW5lcl9uYW1lIjoiZ2FtZS1hcCIsImNsdXN0ZXJfbmFtZSI6InByb2QtYXNpYS0wMSIsImxvY2F0aW9uIjoiYXNpYS1zb3V0aGVhc3QxIiwicHJvamVjdF9pZCI6ImF2aWQtc3Vuc2V0LTMxMDYwOCJ9fSwidGltZXN0YW1wIjoiMjAyMi0wNS0xNVQxODowMDoxMS40MzkzNjM2OTdaIiwic2V2ZXJpdHkiOiJFUlJPUiIsImxhYmVscyI6eyJjb21wdXRlLmdvb2dsZWFwaXMuY29tL3Jlc291cmNlX25hbWUiOiJna2UtdGVzdC1hc2lhLTAxLXRlc3QtcG9vbC0wMS1jMzM5Y2Q0Zi0wcDkxIiwiazhzLXBvZC9wb2QtdGVtcGxhdGUtaGFzaCI6ImI0Y2M5YmM2NyIsIms4cy1wb2QvYXBwIjoiZ2FtZSJ9LCJsb2dOYW1lIjoicHJvamVjdHMvYXZpZC1zdW5zZXQtdGVzdC9sb2dzL3N0ZG91dCIsInJlY2VpdmVUaW1lc3RhbXAiOiIyMDIyLTA1LTE1VDE4OjAwOjE1LjcyMDI2MzE3N1oifQ==",
                "messageId": "4517634831393975",
                "message_id": "4517634831393975",
                "publishTime": "2022-05-04T08:18:18.154Z",
                "publish_time": "2022-05-04T08:18:18.154Z"
            },
            "subscription": "projects/avid-sunset-310608/subscriptions/myRunSubscription"
        }
        self.alert_message = AlertMessage(self.envelope)

    def test_get_error_log_url(self):
        expected_url = 'https://console.cloud.google.com/logs/query;query=%28resource.type%3D%22test_type%22%0Aresource.labels.container_name%3D%22test_container_name%22%0Aresource.labels.cluster_name%3D%22test_cluster_name%22%29%0AOR%0A%28resource.type%3D%22http_load_balancer%22%0Aresource.labels.backend_service_name%3D~%22%5E.*%28test_namespace_name%29-%28test_container_name%29.%2A%24%22%29%3BtimeRange%3D2022-04-06T23%3A50%3A00.000000Z%2F2022-04-07T00%3A10%3A00.000000Z%3BsummaryFields%3D%3Afalse%3A32%3Abeginning%3Afalse%3BcursorTimestamp%3D2022-04-07T00%3A00%3A00.000Z?authuser=0&project=test_project_id'
        with patch('pandas.to_datetime') as mock_to_datetime:
            mock_to_datetime.return_value = '2022-04-07T00:00:00.000Z'
            self.alert_message.get_error_log_url()
        self.assertEqual(self.alert_message.url, expected_url)

if __name__ == '__main__':
    unittest.main()