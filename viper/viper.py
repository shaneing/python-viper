import collections
import json
import os

from yaml import Loader, load as yaml_load
from .remote import get_remote_config, RemoteProvider


supported_config_type = {'yaml', 'yml', 'json'}
supported_remote_providers = {'consul'}


class Viper(object):
    def __init__(self):
        self._flag = collections.defaultdict()
        self._config = collections.defaultdict()
        self._kv = collections.defaultdict()
        self._config_type = None
        self._config_path = None
        self._remote_provider: RemoteProvider = None

    def get(self, k: str):
        v = self._flag.get(k)
        if v is not None:
            return v

        p = k.split('.')
        v = self.find(p, self._config)
        if v is not None:
            return v

        return self.find(p, self._kv)

    def find(self, p: [str], d: collections.defaultdict):
        if d is None:
            return None

        if len(p) == 1:
            return d.get(p[0])

        return self.find(p[1:], d.get(p[0]))

    def set_flag(self, key, value):
        self._flag[key] = value

    def clear_flag(self):
        self._flag.clear()

    def set_config_path(self, p: str):
        self._config_path = p

    def set_remote_provider(self, provider: str, host: str, port: int, path: str):
        if provider not in supported_remote_providers:
            raise Exception('Unsupported remote provider: {}'.format(provider))

        self._remote_provider = RemoteProvider(provider=provider, host=host, port=port, path=path)

    def read_config(self):
        with open(self._config_path) as f:
            s = ''.join(f.readlines())
            self._load(s, self._config)

    def read_remote_config(self):
        s = get_remote_config(self._remote_provider)
        if s is None:
            return

        self._load(s, self._kv)

    def _load(self, s: str, d: dict):
        config_type = self._get_config_type()
        if config_type == 'yaml' or config_type == 'yml':
            d.update(yaml_load(s, Loader=Loader))
        elif config_type == 'json':
            d.update(json.loads(s, encoding='utf-8'))

    def _get_config_type(self):
        if self._config_type is not None:
            return self._config_type

        if self._config_path is None:
            return None

        _, ext = os.path.splitext(self._config_path)
        if len(ext) > 1:
            return ext[1:]

        return ''

    def set_config_type(self, config_type: str):
        if config_type not in supported_config_type:
            raise Exception('Unsupported config type: {}'.format(config_type))

        self._config_type = config_type

    def unmarshal(self, o: object):
        if self._remote_provider is not None:
            self._unmarshal_dict(self._kv, o)
        else:
            self._unmarshal_dict(self._config, o)

    def _unmarshal_dict(self, d: dict, cls: object):
        for (k, v) in d.items():
            if not hasattr(cls, k):
                continue

            attr = getattr(cls, k)
            if isinstance(attr, type):
                self._unmarshal_dict(d[k], attr)
            else:
                setattr(cls, k, v)
