import datetime
import random
import sys


DEBUG = True


class Ilkino:
    def __init__(self):
        self.__studio = Studio()
        self.__gift_list = GiftList()
        self.__booking_log = BookingLog()
        # self.__options = {
        #     "1": self.booking,
        #     "2": self.search,
        #     "3": self.report
        # }

    def setup(self):
        index_special_seats_left = self.__gift_list.randomly_assign_left(self.__studio.get_studio_capacity())
        index_special_seats_right = self.__gift_list.randomly_assign_right(self.__studio.get_studio_capacity())

        print(f"[DEBUG] Gifts di sisi kiri: {[i + 1 for i in index_special_seats_left]}") if DEBUG is True else None
        print(f"[DEBUG] Gifts di sisi kanan: {[i + 1 for i in index_special_seats_right]}") if DEBUG is True else None

        for i in range(self.__studio.get_studio_capacity()):
            if i in index_special_seats_left:  # jika kursi kiri terpilih menjadi special seat
                self.__studio.set_seat(i, Gift(self.__gift_list.place_random_gift_left()))  # hadiahi kursi kiri
            elif i in index_special_seats_right:  # jika kursi kanan terpilih menjadi special seat
                self.__studio.set_seat(i, Gift(self.__gift_list.place_random_gift_right()))  # hadiahi kursi kanan
            else:  # jika kursi adalah seat biasa
                self.__studio.set_seat(i, None)  # taruh hadiah di kursi

    def run(self):
        exit = False
        while not exit:
            print("▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝")
            print("IL Kino".center(27))
            print("Nansentrasse 22,".center(27))
            print("12047 Berlin".center(27))
            print("╭⋟────────────────────────╮".center(30))
            print("SCREEN".center(27))
            print("╰────────────────────────⋞╯".center(30))
            print()
            print(self.__studio)
            print()
            print("1. Seat Booking")
            print("2. Find by Booking")
            print("3. Report")
            print("4. Exit")

            user_input = None
            while user_input is None or user_input not in ("1", "2", "3", "4"):
                user_input = input()

                if user_input == "1":
                    self.booking("", "")
                elif user_input == "2":
                    self.search()
                elif user_input == "3":
                    self.report()
                elif user_input == "4":
                    print("-ᣁ Thank you! ᣂ-")
                    exit = True
                else:
                    print("Incorrect input detected!")

            # user_input = input("Enter your choice 1–4?: ")
            # print()
            # try:
            #     if user_input == "4":
            #         print("-ᣁ Thank you! ᣂ-")
            #         exit = True
            #     else:
            #         self.__choose[user_input]()
            # except KeyError:
            #     print("Incorrect input was detected, please try again!")
            # print()

    def booking(self, _seat_numbers: str, _name: str):  # Brian
        print("1. Seat Booking")
        if _seat_numbers == "":
            _seat_numbers = input(f"Enter seat number: ")

        seat_numbers_list = _seat_numbers.split(",")  # split dan ubah jadi list
        seat_numbers_list: list  # type hint

        for i in range(len(seat_numbers_list)):
            # validasi input: kursi harus bernomor 1-36
            if not seat_numbers_list[i].isnumeric() or int(seat_numbers_list[i]) < 1 or int(seat_numbers_list[i]) > 36:
                print(f"Seat input format should be 'Enter Seat Number: [1-36],[1-36 (optional)],...'! Please try again.")
                return
            seat_numbers_list[i] = int(seat_numbers_list[i])

            # validasi input: kursi harus belum dipesan
            if self.__studio.get_seat_from_index(seat_numbers_list[i] - 1).get_name() is not None:
                print(f"You've attempted to book a seat that has already been booked! Please try again.")
                return

        if _name == "":
            _name = input(f"Enter name: ").lower()

        for seat_index in seat_numbers_list:
            seat = self.__studio.get_seat_from_index(seat_index - 1)
            seat.set_name(_name)  # modifikasi nama pemesan seat
            self.__studio.set_booking_log(_name, seat)  # catat di booking log

        print(f"Seat {_seat_numbers} booked by {_name}.")
        self.receipt(_name,_seat_numbers)

    def receipt(self, _name, _seat_numbers_list):
        name_txt = f'{_name}_{_seat_numbers_list}'
        receipt_txt = open(f"{name_txt}.txt", "w")
        receipt_txt.write("\n===============================================")
        receipt_txt.write("\n               IL Kino Receipt                 ")
        receipt_txt.write("\n===============================================")
        receipt_txt.write(f"\nName      : {_name}")
        receipt_txt.write(f"\nName      : {_seat_numbers_list}")
        receipt_txt.write("\nPlease check below your seat to get your gift.")
        receipt_txt.write("\n       Please arrive 15 minutes before.       ")
        receipt_txt.close()
        print(f"Receipt {receipt_txt}.txt is printed. Don't loose your ticket.")

    def search(self):  # Gracia
        exit = False
        book_log = self.__studio.get_booking_log()

        while not exit:
            try:
                print("2. Find by Name")
                name = input("Enter your name: ")

                print("Here is what we found:")
                print(f"Name: {name}\nSeat number: {book_log[name]}")

                yes_no = input("Find the name? (y/n)")

                if yes_no == "n" or yes_no == "N":
                    break

            except KeyError:
                print("Sorry, the name is not in the booking log, please try again")
                break

    def report(self):  # Steven
        print("===================================")
        print("IL Kino Bioskop Studio Report")
        print("===================================")
        print(f"Total Seats in Studio: {self.__studio.get_studio_capacity()}")
        print(f"Total Special Seats: {self.__gift_list.get_max_gift_count()}")
        print(f"Seats Booked: {len(self.__studio.get_booking_log())}")
        print(f"Available Seats: {self.__studio.get_studio_capacity() - len(self.__studio.get_booking_log())}")
        print("===================================")
        print("Booking Report:")
        booking_log = self.__studio.get_booking_log()
        if not booking_log:
            print("No bookings have been made.")
        else:
            for customer_name, seat_index in booking_log.items():
                seat_number = seat_index + 1
                print(f"Seat {seat_number}: {customer_name}")
        print("===================================")


class Studio:  # Objek tambahan
    def __init__(self):
        self.__studio_capacity = 36
        self.__seating = []  # akses dengan index seatnya, index 0 adalah seat 1, dst
        self.__booking_log = {}  # FORMAT: {"nama_customer": "indeks_kursi"}, buat di display output

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

    def set_booking_log(self, customer_name, seat_index):
        self.__booking_log[customer_name] = seat_index

    def get_seat_from_index(self, index):
        if 0 <= index <= 35:
            return self.__seating[index]
        return None

    def get_booking_log(self):
        return self.__booking_log

    def get_studio_capacity(self):
        return self.__studio_capacity

    def set_seat(self, _index: int, _gift):
        if _gift is not None:
            self.__seating.append(SpecialSeat(_index + 1, _gift))
        else:
            self.__seating.append(Seat(_index + 1))


class BookingLog:
    pass


class GiftList:  # Objek tambahan
    def __init__(self):
        self.__gifts_for_left_seats = self.set_gifts()
        self.__gifts_for_right_seats = self.__gifts_for_left_seats.copy()
        self.__max_gift_count = len(self.__gifts_for_left_seats)

    def get_max_gift_count(self):
        return self.__max_gift_count

    def set_gifts(self):
        if len(sys.argv) > 1 and sys.argv[-1][:6] == "-gift=":
            a = sys.argv[-1][6:].split(",")
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


class Gift:
    def __init__(self, _name: str):
        self.__name = _name

    def get_name(self):
        return self.__name


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


if __name__ == "__main__":
    ilkino = Ilkino()
    ilkino.setup()
    ilkino.run()
