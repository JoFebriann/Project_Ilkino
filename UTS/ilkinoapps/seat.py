class Seat:  # Brian , dibikin setiap kali booking
    def __init__(self, _number: int):
        self.__seat_number = _number
        self.__booker_name = None

    def __str__(self):
        if self.__booker_name is not None:
            return "[X ]"  # kembalikan [X] bila kursi telah di-book
        return f"[{self.__seat_number}]" if self.__seat_number > 9 else f"[{self.__seat_number} ]"  # kembalikan [no. kursi] bila kursi belum di-book

    def set_name(self, _name):
        self.__booker_name = _name

    def get_name(self):
        return self.__booker_name

    def get_number(self):
        return self.__seat_number


class SpecialSeat(Seat):  # Brian
    def __init__(self, _number: int, _gift: str):
        super().__init__(_number)
        self.__gift = _gift

    def __str__(self):
        if self.get_name() is not None:
            return "[G ]"  # kembalikan [G ] bila kursi telah di-book
        return f"[{self.get_number()}]" if self.get_number() > 9 else f"[{self.get_number()} ]"  # kembalikan [no. kursi] bila kursi belum di-book

    def get_gift(self):
        return self.__gift