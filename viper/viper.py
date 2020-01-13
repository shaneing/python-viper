import collections
import os

from yaml import Loader, load as yaml_load


class Viper(object):
    def __init__(self):
        self._flag = collections.defaultdict()
        self._config = collections.defaultdict()
        self._config_type = None
        self._config_path = None

    def get(self, k: str):
        v = self._flag.get(k)
        if v is not None:
            return v

        p = k.split('.')
        return self.find(p, self._config)

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

    def read_config(self):
        with open(self._config_path) as f:
            s = ''.join(f.readlines())
            self._load(s, self._config)

    def read_remote_config(self):
        pass

    def _load(self, s: str, d: dict):
        config_type = self._get_config_type()
        if config_type == 'yaml' or config_type == 'yml':
            d.update(yaml_load(s, Loader=Loader))

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
        self._config_type = config_type

