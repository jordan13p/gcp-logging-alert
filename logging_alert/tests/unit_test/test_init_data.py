import unittest
from unittest.mock import patch, MagicMock
from ...services.init_data import InitData


class TestInitData(unittest.TestCase):
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
        self.init_data = InitData(self.envelope)

    def test_get_message_data_valid_data(self):
        self.init_data.get_message_data()
        self.assertEqual(self.init_data._message_data, {'insertId': '01876mil7hv9rjlo', 'jsonPayload': {'instant': {'epochSecond': 1652637611, 'nanoOfSecond': 436939000}, 'level': 'ERROR', 'message': 'Error. (user=00000 vineetkumar12345, url=GET /gs/v1/matches/my, errorCode=EXTERNAL_API_ERROR)', 'thread': 'http-nio-8080-exec-3', 'threadPriority': 5, 'thrown': {'name': 'com.cloudlatitude.gameserver.match.query.adapter.my.GetMyMatchesRepositoryException', 'extendedStackTrace': [], 'message': 'com.cloudlatitude.shared.external.ThirdPartyApiException: Error when calling: test', 'commonElementCount': 0, 'localizedMessage': 'com.cloudlatitude.shared.external.ThirdPartyApiException: Error when calling: test', 'cause': {'cause': {'commonElementCount': 92, 'message': '500 Internal Server Error: [no body]', 'name': 'org.springframework.web.client.HttpServerErrorException$InternalServerError', 'extendedStackTrace': [], 'localizedMessage': '500 Internal Server Error: [no body]'},
                         'localizedMessage': 'Error when calling: test', 'commonElementCount': 92, 'name': 'com.cloudlatitude.shared.external.ThirdPartyApiException', 'message': 'Error when calling: test', 'extendedStackTrace': []}}, 'loggerFqcn': 'org.apache.logging', 'loggerName': 'com.cloudlatitude.gameserver.common.ExceptionAdvice', 'threadId': 57}, 'resource': {'type': 'k8s_container', 'labels': {'pod_name': 'game-ap-b4cc9bc67-zg2wk', 'namespace_name': 'legend-fantasy', 'container_name': 'game-ap', 'cluster_name': 'prod-asia-01', 'location': 'asia-southeast1', 'project_id': 'avid-sunset-310608'}}, 'timestamp': '2022-05-15T18:00:11.439363697Z', 'severity': 'ERROR', 'labels': {'compute.googleapis.com/resource_name': 'gke-test-asia-01-test-pool-01-c339cd4f-0p91', 'k8s-pod/pod-template-hash': 'b4cc9bc67', 'k8s-pod/app': 'game'}, 'logName': 'projects/avid-sunset-test/logs/stdout', 'receiveTimestamp': '2022-05-15T18:00:15.720263177Z'})

    def test_get_message_data_invalid_data(self):
        envelope = {}
        init_data = InitData(envelope)
        with self.assertRaises(Exception):
            init_data.get_message_data()

    def test_get_alert_message_json_payload(self):
        init_data = InitData(self.envelope)
        init_data.get_message_data()
        init_data.get_alert_message()
        self.assertEqual(init_data.alert_message_data.get('message'), 'Error. (user=00000 vineetkumar12345, url=GET /gs/v1/matches/my, errorCode=EXTERNAL_API_ERROR)')
        self.assertEqual(init_data.alert_message_data.get('dtime'), '2022-05-15 18:00:11')
        self.assertEqual(init_data.alert_message_data.get('timestamp'), 1652637611.439)
        self.assertEqual(init_data.alert_message_data.get('cluster_name'), 'prod-asia-01')
        self.assertEqual(init_data.alert_message_data.get('namespace_name'), 'legend-fantasy')
        self.assertEqual(init_data.alert_message_data.get('container_name'), 'game-ap')

    def test_get_alert_message_text_payload(self):
        envelope = {
            "message": {
                "data": "eyJ0ZXh0UGF5bG9hZCI6IldBUk5JTkc6IFVzZSAtLWlsbGVnYWwtYWNjZXNzPXdhcm4gdG8gZW5hYmxlIHdhcm5pbmdzIG9mIGZ1cnRoZXIgaWxsZWdhbCByZWZsZWN0aXZlIGFjY2VzcyBvcGVyYXRpb25zIiwiaW5zZXJ0SWQiOiJkcG9kbTFxNXpqOTFvbjd1IiwicmVzb3VyY2UiOnsidHlwZSI6Ims4c19jb250YWluZXIiLCJsYWJlbHMiOnsiY2x1c3Rlcl9uYW1lIjoidGVtcC1jbHVzdGVyLTAxIiwicHJvamVjdF9pZCI6ImF2aWQtc3Vuc2V0LTMxMDYwOCIsImxvY2F0aW9uIjoiYXNpYS1lYXN0MSIsImNvbnRhaW5lcl9uYW1lIjoiZ2FtZS1hcCIsIm5hbWVzcGFjZV9uYW1lIjoidGVzdCIsInBvZF9uYW1lIjoiZ2FtZS1hcC02Njc1ZGI2NTc4LW1kcWxkIn19LCJ0aW1lc3RhbXAiOiIyMDIzLTA0LTA3VDA0OjEzOjU1LjcxMTIyMzU4MVoiLCJzZXZlcml0eSI6IkVSUk9SIiwibGFiZWxzIjp7Ims4cy1wb2QvZGF0ZSI6IjE2MTg1NjE5ODEiLCJrOHMtcG9kL3BvZC10ZW1wbGF0ZS1oYXNoIjoiNjY3NWRiNjU3OCIsImNvbXB1dGUuZ29vZ2xlYXBpcy5jb20vcmVzb3VyY2VfbmFtZSI6ImdrZS10ZW1wLWNsdXN0ZXItMDEtcG9vbC0wNC00ODBhMDEyNS14MmJtIiwiazhzLXBvZC9hcHAiOiJnYW1lLWFwIn0sImxvZ05hbWUiOiJwcm9qZWN0cy9hdmlkLXN1bnNldC0zMTA2MDgvbG9ncy9zdGRlcnIiLCJyZWNlaXZlVGltZXN0YW1wIjoiMjAyMy0wNC0wN1QwNDoxMzo1Ni43Nzk2ODk5MDdaIn0=",
                "messageId": "4517634831393975",
                "message_id": "4517634831393975",
                "publishTime": "2022-05-04T08:18:18.154Z",
                "publish_time": "2022-05-04T08:18:18.154Z"
            },
            "subscription": "projects/avid-sunset-310608/subscriptions/myRunSubscription"
        }

        init_data = InitData(envelope)
        init_data.get_message_data()
        init_data.get_alert_message()
        self.assertEqual(init_data.alert_message_data.get('message'), "WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations")
        self.assertEqual(init_data.alert_message_data.get('dtime'), '2023-04-07 04:13:56')
        self.assertEqual(init_data.alert_message_data.get('timestamp'), 1680840835.711)
        self.assertEqual(init_data.alert_message_data.get('cluster_name'), "temp-cluster-01")
        self.assertEqual(init_data.alert_message_data.get('namespace_name'), "test")
        self.assertEqual(init_data.alert_message_data.get('container_name'), "game-ap")


if __name__ == '__main__':
    unittest.main()
