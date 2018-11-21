import unittest
import json
from webhook import create_app
from unittest.mock import call
from unittest.mock import patch


class TestRoadLocation(unittest.TestCase):

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

        requested_location = {'long': 4.8367074, 'lat': 51.321642499999996 }
        expected_result = {'snappedPoints':
                               [{'location': {'latitude': 51.32162537389561, 'longitude': 4.836712880479233},
                                 'originalIndex': 0, 'placeId': 'ChIJv2Ez8i2sxkcRgMoDzJ4ADy0'},
                                {'location': {'latitude': 51.32162537389561, 'longitude': 4.836712880479233},
                                 'originalIndex': 0, 'placeId': 'ChIJv2Ez8i2sxkcRgcoDzJ4ADy0'}]}

        with app.test_client() as client:
            rabbit_mock.channel.basic_publish.return_value = True
            request_mock.post.return_value.json.return_value = expected_result
            request_mock.post.return_value.status_code = 200

            rv = client.post('/demo/street?api_key={}'.format(app.config['API_KEY']),
                             data=json.dumps(requested_location),
                             content_type='application/json')

            self.assertEqual([call.channel.basic_publish(
                body=expected_result,
                exchange='webhook', routing_key='demo')], rabbit_mock.mock_calls)

            self.assertEqual({'success': True}, json.loads(rv.data))
