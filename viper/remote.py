import collections
import consul


class Backend:
    def get(self, key: str):
        pass


class ConsulBackend(Backend):
    def __init__(self, host, port):
        self._client = consul.Consul(host=host, port=port)

    def get(self, key: str):
        _, data = self._client.kv.get(key)
        return data.get('Value', None)


RemoteProvider = collections.namedtuple('RemoteProvider', ['path', 'host', 'port', 'provider'])


def get_remote_config(rp: RemoteProvider):
    config = None
    if rp.provider == 'consul':
        backend = ConsulBackend(host=rp.host, port=rp.port)
        config = backend.get(rp.path)

    return config






