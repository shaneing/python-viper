# Python Viper

This project was inspired by [spf13/viper](https://github.com/spf13/viper).

## Installation

```
pip install py-viper
```

## Usage

```python
import tempfile
import viper

yaml_example = b'''
hello:
  name: foo
'''


class Hello:
    name = ''


class Config:
    hello = Hello


if __name__ == '__main__':
    with tempfile.NamedTemporaryFile(suffix='.yaml') as temp:
        temp.write(yaml_example)
        temp.seek(0)
        viper.set_config_path(temp.name)
        viper.read_config()
        assert viper.get('hello.name') == 'foo'

        conf = Config()
        viper.unmarshal(conf)
        assert conf.hello.name == 'foo'
```

You also can using remote config instead of local config:

```python
viper.set_config_type('yml')
viper.set_remote_provider('consul', '127.0.0.1', 8500, 'hello')
viper.read_remote_config()
```

Note:

- The config type only support for *yaml* or *yml*.
- The remote config only support for *consul*.

## TODO

- [x] Read remote config
- [x] Unmarshal config