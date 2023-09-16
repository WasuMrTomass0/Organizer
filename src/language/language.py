class Language:

    def __init__(self, language: str = None) -> None:
        self._language = language if language else 'english'
        self._data = {}
        # TODO: Load data from file

    def __getattribute__(self, name):
        if name in self._data:
            return self._data[name]
        return name

    pass


lang = Language()
