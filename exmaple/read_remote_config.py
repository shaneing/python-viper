import viper

yaml_example = b'''
hello:
  name: foo
'''

if __name__ == '__main__':
    viper.set_config_type('yml')
    viper.set_remote_provider('consul', '127.0.0.1', 8500, 'hello')
    viper.read_remote_config()
    assert viper.get('hello.name') == 'foo'
