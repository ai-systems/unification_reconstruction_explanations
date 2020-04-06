from collections import defaultdict

import msgpack
from ailog import Loggable
from luigi import LocalTarget
from overrides import overrides

from regra.common.util import custom_deserialize, custom_serialize


class MsgPackTarget(LocalTarget):

    def __init__(self, **kwargs):
        self.transform = kwargs.pop('transform', None)
        super(MsgPackTarget, self).__init__(**kwargs)

    def load(self):
        with open(self.path, 'rb') as f:
            data = defaultdict(lambda: None, msgpack.load(
                f, raw=False, object_hook=custom_deserialize))
            if self.transform is not None:
                return self.transform(data)
            else:
                return data

    def dump(self, data):
        with open(self.path, 'wb+') as f:
            msgpack.dump(data, f,
                         default=custom_serialize, use_bin_type=True)
