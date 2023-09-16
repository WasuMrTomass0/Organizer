import json
import os

from config import DIR_LANGUAGE
from logger import warning, error, debug


class Language:

    def __init__(self) -> None:
        self._language = None
        self._path = None
        self._data = {}
        self.set_english()

    def _set_path(self, language) -> None:
        return os.path.join(DIR_LANGUAGE, f'{language}.json')

    def _is_language(self, language) -> bool:
        path = self._set_path(language=language)
        return os.path.isfile(path)

    def _load_data(self, path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            debug(f'Loaded language data from "{path}"')
        return data

    def _load_language(self, raise_err: bool = False) -> None:
        # Set file path based on selected language
        self._path = self._set_path(self._language)
        # Check if file exists
        if not self._is_language(self._language):
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
        self._data = self._load_data(path=self._path)

    def __getattr__(self, name) -> str:
        if name in self._data:
            return self._data[name]
        warning(msg=f'Unrecognized word key: "{name}"', delta=1)
        return name

    def set_english(self) -> None:
        self._language = 'english'
        self._load_language()

    def set_polish(self) -> None:
        self._language = 'polski'
        self._load_language()


lang = Language()
