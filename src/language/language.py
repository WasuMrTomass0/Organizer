import json
import os

from config import DIR_LANGUAGE
from logger import warning


class Language:

    def __init__(self, language: str = None) -> None:
        self._language = language if language else 'english'
        path = os.path.join(DIR_LANGUAGE, f'data_{self._language}.json')
        self._data = {}
        self._load_data(path=path)

    def _load_data(self, path):
        with open(path, 'r') as f:
            self._data = json.load(f)

    def __getattr__(self, name) -> str:
        if name in self._data:
            return self._data[name]
        warning(msg=f'Unrecognized word key: "{name}"', delta=1)
        return name


lang = Language()
