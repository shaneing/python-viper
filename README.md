# Python Viper

This project was inspired by [spf13/viper](https://github.com/spf13/viper).

## Installation

```
pip install py-viper
```

## Usage

### Using viper.bind_flags in fire

```python
import fire
import viper


@viper.bind_flags(flags=[
    viper.Flag(name='name', value='foo', usage='Indicate name'),
])
def hello():
    return "Hello %s!" % viper.get('name')


if __name__ == '__main__':
    fire.Fire(hello)
```

### Reading config by viper

```python
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

```

## TODO

- [ ] Read remote config