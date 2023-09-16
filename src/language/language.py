import json
import os

from config import DIR_LANGUAGE
from logger import warning, error


class Language:

    def __init__(self, language: str = None) -> None:
        self._language = language if language else 'english'
        self._path = None
        self._data = {}
        self._load_language()

    def _set_path(self) -> None:
        self._path = os.path.join(DIR_LANGUAGE, f'{self._language}.json')

    def _is_language(self) -> bool:
        if self._path is None:
            return False
        return os.path.isfile(self._path)

    def _load_data(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def _load_language(self, raise_err: bool = False) -> None:
        # Set file path based on selected language
        self._set_path()
        # Check if file exists
        if not self._is_language():
            # Log error message
            msg = f'Language data file does not exist! "{self._path}"'
            error(msg)
            # If called again - raise error
            if raise_err:
                raise FileNotFoundError(msg)
            # Set default language
            self._language = 'english'
            return self._load_language(raise_err=True)
        # Load existing file
        self._load_data(path=self._path)

    def __getattr__(self, name) -> str:
        if name in self._data:
            return self._data[name]
        warning(msg=f'Unrecognized word key: "{name}"', delta=1)
        return name


lang = Language()
