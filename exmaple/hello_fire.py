import fire
import viper


@viper.bind_flags(flags=[
    viper.Flag(name='name', value='foo', usage='Indicate name'),
])
def hello():
    return "Hello %s!" % viper.get('name')


if __name__ == '__main__':
    fire.Fire(hello)
