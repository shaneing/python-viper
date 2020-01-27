import base64
import json
import os
import unittest
import mock
import requests
import viper


def _absolute_path(p):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


TEST_DATA = {
    'LockIndex': 0,
    'Key': 'hello',
    'Flags': 0,
    'Value': base64.b64encode(b'hello:\n  name: foo').decode('utf-8'),
    'CreateIndex': 51,
    'ModifyIndex': 51
}


class TestViper(unittest.TestCase):
    def setUp(self) -> None:
        viper.reset()

    def test_bind_flags(self):
        @viper.bind_flags(flags=[
            viper.Flag(name='name', value='foo', usage='Indicate name'),
        ])
        def hello():
            return 'Hello {}!'.format(viper.get('name'))

        self.assertEqual('Hello foo!', hello())
        self.assertEqual('Hello bar!', hello(name='bar'))

    def test_read_config(self):
        viper.set_config_path(_absolute_path('test.yml'))
        viper.read_config()
        self.assertEqual('foo', viper.get('hello.name'))

    @patch('requests.get')
    def test_remote_config(self, mock_get):
        mock_get.return_value = mock.Mock(text=json.dumps([TEST_DATA]), headers={'X-Consul-Index': 0}, status_code=200)
        viper.set_config_type('yml')
        viper.set_remote_provider('consul', '127.0.0.1', 8500, 'hello')
        viper.read_remote_config()
        self.assertEqual('foo', viper.get('hello.name'))
