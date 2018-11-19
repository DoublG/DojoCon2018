import unittest
import json
from webhook import create_app
from unittest.mock import patch, call


class TestCellTowerLocation(unittest.TestCase):

    @patch('webhook.views.rabbit', spec=['channel'])
    @patch('webhook.views.requests', spec=['post'])
    def test_location(self, request_mock, rabbit_mock):
        app = create_app(test_config={
            'TESTING': True,
            'GOOGLE_KEY': 'dummy',
            'API_KEY': 'dummy',
            'RABBITMQ_USER': 'dummy',
            'RABBITMQ_PWD': 'dummy',
            'RABBITMQ_EXCHANGE': 'webhook'})

        requested_location = {
            "homeMobileCountryCode": 206,  # MCC
            "homeMobileNetworkCode": 1,  # MNC
            "considerIp": False,
            "carrier": "Proximus",
            "cellTowers": [
                {
                    "cellId": 66674698,  # CID
                    "locationAreaCode": 3024,  # LAC
                    "mobileCountryCode": 206,  # MCC
                    "mobileNetworkCode": 1,  # MNC
                },
                {
                    "cellId": 46190596,  # CID
                    "locationAreaCode": 3052,  # LAC
                    "mobileCountryCode": 206,  # MCC
                    "mobileNetworkCode": 1  # MNC
                },
                {
                    "cellId": 21409538,  # CID
                    "locationAreaCode": 3052,  # LAC
                    "mobileCountryCode": 206,  # MCC
                    "mobileNetworkCode": 1  # MNC
                }
            ]
        }
        expected_location = {'location': {'lat': 51.3216935, 'lng': 4.8364321}, 'accuracy': 1807.0}

        with app.test_client() as client:
            rabbit_mock.channel.basic_publish.return_value = True
            request_mock.post.return_value.json.return_value = expected_location

            rv = client.post('/demo/geo?api_key={}'.format(app.config['API_KEY']),
                             data=json.dumps(requested_location),
                             content_type='application/json')

            self.assertEqual([call.channel.basic_publish(
                body=expected_location,
                exchange='webhook', routing_key='demo')], rabbit_mock.mock_calls)

            self.assertEqual({'success': True}, json.loads(rv.data))
