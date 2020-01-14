import tempfile
import viper

yaml_example = b'''
hello:
  name: foo
'''

if __name__ == '__main__':
    with tempfile.NamedTemporaryFile(suffix='.yaml') as temp:
        temp.write(yaml_example)
        temp.seek(0)
        viper.set_config_path(temp.name)
        viper.read_config()
        assert viper.get('hello.name') == 'foo'
