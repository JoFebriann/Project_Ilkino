import random


class GiftList:
    def __init__(self, _argv):
        self.__gifts_for_left_seats = self.set_gifts(_argv)
        self.__gifts_for_right_seats = self.__gifts_for_left_seats.copy()
        self.__max_gift_count = len(self.__gifts_for_left_seats)

    def get_max_gift_count(self):
        return self.__max_gift_count

    def set_gifts(self, _argv):
        if _argv is not None and len(_argv) > 1 and _argv[-1][:6] == "-gift=":
            a = _argv[-1][6:].split(",")
            return a
        else:
            print("[Warning] Command line parameter '-gift=' was not detected! \n")
            return ["placeholder1", "placeholder2", "placeholder3", "placeholder4", "placeholder5"]

    # def assign_gifts_to_seats(self, _studio_capacity):  # pilih 5 (jumlah hadiah) indeks acak dari semua kursi
    #     return random.sample(range(0, _studio_capacity), self.get_max_gift_count())

    def randomly_assign_left(self, _studio_capacity):  # pilih 5 indeks acak dari kursi sisi kiri
        return random.sample(range(0, _studio_capacity - 1, 2), self.get_max_gift_count())

    def randomly_assign_right(self, _studio_capacity):  # pilih 5 indeks acak dari kursi sisi kanan
        return random.sample(range(1, _studio_capacity, 2), self.get_max_gift_count())

    def place_random_gift_left(self):
        random_index = random.randint(0, len(self.__gifts_for_left_seats) - 1)  # pilih satu indeks hadiah secara acak
        random_gift = self.__gifts_for_left_seats.pop(random_index)  # ambil hadiah yang terpilih & coret dari daftar
        return random_gift  # kembalikan hadiah acak

    def place_random_gift_right(self):
        random_index = random.randint(0, len(self.__gifts_for_right_seats) - 1)  # pilih satu indeks hadiah secara acak
        random_gift = self.__gifts_for_right_seats.pop(random_index)  # ambil hadiah yang terpilih & coret dari daftar
        return random_gift  # kembalikan hadiah acak