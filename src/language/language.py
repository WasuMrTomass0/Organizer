import json
import os

from config import DIR_LANGUAGE


class Language:

    def __init__(self, language: str = None) -> None:
        self._language = language if language else 'english'
        path = os.path.join(DIR_LANGUAGE, f'data_{self._language}.jsonc')
        self._data = {}
        self._load_data(path=path)

    def _load_data(self, path):
        with open(path, 'r') as f:
            self._data = json.load(f)

    def __getattr__(self, name) -> str:
        if name in self._data:
            return self._data[name]
        return name


lang = Language()
