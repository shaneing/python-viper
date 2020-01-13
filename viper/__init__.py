import inspect
from functools import wraps

from .viper import Viper
from .flag import Flag

_viper = Viper()
_kind = inspect.Parameter.KEYWORD_ONLY


def bind_flags(flags: [Flag]):
    def decorate(func):
        params = []
        for f in flags:
            func.__doc__ = '\n'.join([f.doc() for f in flags])
            params.append(inspect.Parameter(name=f.name, default=f.value, kind=_kind))
            _viper.set_flag(f.name, f.value)

        func.__signature__ = inspect.Signature(params)

        @wraps(func)
        def wrapper(*args, **kwargs):
            for k, v in kwargs.items():
                _viper.set_flag(k, v)

            try:
                result = func()
            finally:
                _viper.clear_flag()

            return result

        return wrapper

    return decorate


def get(key: str):
    return _viper.get(key)


def set_config_path(p: str):
    _viper.set_config_path(p)


def read_config():
    _viper.read_config()
