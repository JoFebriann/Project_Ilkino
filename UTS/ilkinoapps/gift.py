class Gift:
    def __init__(self, _name: str):
        self.__name = _name

    def __str__(self):
        return self.__name

    def get_name(self):
        return self.__name