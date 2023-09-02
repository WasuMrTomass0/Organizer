from typing import Any


class FrontData:

    def __init__(self, exceptions: bool = False) -> None:
        self._data = {}
        self._exceptions = exceptions

    def clear(self, key: str) -> None:
        self._data[key] = None

    def clear_keys(self, keys: "list[str]") -> None:
        for k in keys:
            self.clear(k)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str) -> Any:
        if key not in self._data and not self._exceptions:
            return None
        return self._data[key]

    def __getattr__(self, key: str) -> Any:
        if key not in self._data and not self._exceptions:
            return None
        return self._data[key]
