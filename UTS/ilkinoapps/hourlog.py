class HourLog():  # objek tambahan
    def __init__(self):
        self.__hourlog = {}

    def get_book_per_hour(self):
        return self.__hourlog

    def set_book_per_hour(self, _time: int, _seat_nums: list):
        if _time not in self.__hourlog:  # jika jam belum tercatat
            self.__hourlog.update({_time: len(_seat_nums)})
        else:
            self.__hourlog[_time] += len(_seat_nums)