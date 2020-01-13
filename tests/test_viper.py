import os
import unittest
import viper


def _absolute_path(p):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


class TestViper(unittest.TestCase):
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
