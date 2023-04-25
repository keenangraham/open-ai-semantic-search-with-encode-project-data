from collections import OrderedDict


class SimpleCache(OrderedDict):

    def __init__(self, *args, maxsize=5000, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxsize = maxsize

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        while len(self) > self.maxsize:
            self.popitem(
                last=False
            )
