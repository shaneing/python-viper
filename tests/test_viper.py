import base64
import json
import os
import tempfile
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

JSON_CONFIG = b'''
{
  "hello": {
    "name": "foo"
  }
}
'''

YAML_CONFIG = b'''
hello:
  name: foo
'''


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

    def test_yaml(self):
        with tempfile.NamedTemporaryFile(suffix='.yaml') as temp:
            temp.write(YAML_CONFIG)
            temp.seek(0)
            viper.set_config_path(temp.name)
            viper.read_config()
            assert viper.get('hello.name') == 'foo'

    def test_json(self):
        with tempfile.NamedTemporaryFile(suffix='.json') as temp:
            temp.write(JSON_CONFIG)
            temp.seek(0)
            viper.set_config_path(temp.name)
            viper.read_config()
            assert viper.get('hello.name') == 'foo'

    @mock.patch.object(requests.Session, 'get')
    def test_remote_config(self, mock_get):
        mock_get.return_value = mock.Mock(text=json.dumps([TEST_DATA]), headers={'X-Consul-Index': 0}, status_code=200)
        viper.set_config_type('yml')
        viper.set_remote_provider('consul', '127.0.0.1', 8500, 'hello')
        viper.read_remote_config()
        self.assertEqual('foo', viper.get('hello.name'))
