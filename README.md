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
viper.set_config_path(_absolute_path('test.yml'))
viper.read_config()
self.assertEqual('foo', viper.get('hello.name'))
```

## TODO

- [ ] Read remote config