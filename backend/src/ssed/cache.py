from collections import OrderedDict

from typing import Any


class SimpleCache(OrderedDict[str, Any]):

    def __init__(self, *args: Any, maxsize: int = 5000, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.maxsize = maxsize

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)
        while len(self) > self.maxsize:
            self.popitem(
                last=False
            )
