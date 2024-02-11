from ilkinoapps.seat import Seat, SpecialSeat


class Studio:  # Objek tambahan
    def __init__(self):
        self.__studio_capacity = 36
        self.__filled_seats = 0
        self.__seating = []  # akses dengan index seatnya, index 0 adalah seat 1, dst
        # kenapa ga langsung dari seat log aja carinya, kenapa seating itu perlu?
        self.__seat_log = {}  # FORMAT: {"nama_customer": [indeks_kursi]}, buat di display output

    def __str__(self):
        count_rows = int(self.__studio_capacity / 6)  # banyak barisan (horizontal)
        count_columns = int(self.__studio_capacity / 12)  # banyak kolom (vertikal) pada satu sisi

        output = ""
        for index_row in range(count_rows):
            for index_column in range(count_columns):
                output += f"{self.__seating[count_rows * index_row + 2 * index_column]}"
            output += "\t"
            for index_column in range(3):
                output += f"{self.__seating[count_rows * index_row + 2 * index_column + 1]}"
            output += "\n" if (index_row < count_rows - 1) else ""
        return output

    def get_filled_seats(self):
        return self.__filled_seats

    def get_seat_log(self):
        return self.__seat_log

    def get_seat_from_index(self, index):
        if 0 <= index <= 35:
            return self.__seating[index]
        return None

    def get_seating(self):
        return self.__seating

    def get_studio_capacity(self):
        return self.__studio_capacity

    def get_seats_with_gifts(self):
        gift_seats = []

        for seat in self.__seating:
            if isinstance(seat, SpecialSeat) and seat.get_name() in self.__seat_log:
                gift_seats.append([seat.get_number(), seat.get_gift().get_name()])

        return gift_seats

    def set_filled_seats(self, _count: int):
        self.__filled_seats += _count

    def set_seat_log(self, customer_name, _seat_index):
        self.__seat_log[customer_name] = _seat_index

    def set_seat(self, _index: int, _gift):
        if _gift is not None:
            self.__seating.append(SpecialSeat(_index + 1, _gift))
        else:
            self.__seating.append(Seat(_index + 1))