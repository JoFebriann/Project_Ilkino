import os
import time
from ilkinoapps.studio import Studio
from ilkinoapps.giftlist import GiftList
from ilkinoapps.gift import Gift
from ilkinoapps.seat import Seat, SpecialSeat
from ilkinoapps.hourlog import HourLog


class Ilkino:
    def __init__(self, _argv):
        self.__studio = Studio()
        self.__gift_list = GiftList(_argv)
        self.__hour_log = HourLog()

    def setup(self):
        index_special_seats_left = self.__gift_list.randomly_assign_left(self.__studio.get_studio_capacity())
        index_special_seats_right = self.__gift_list.randomly_assign_right(self.__studio.get_studio_capacity())

        # print(f"[DEBUG] Gifts di sisi kiri: {[i + 1 for i in index_special_seats_left]}")
        # print(f"[DEBUG] Gifts di sisi kanan: {[i + 1 for i in index_special_seats_right]}")

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
            print("\n▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝")
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
            print("2. Find by Name")
            print("3. Report")
            print("4. Exit")
            print("Enter your choice 1-4?:")

            user_input = None
            while user_input is None or user_input not in ("1", "2", "3", "4"):
                user_input = input()

                if user_input == "1":
                    self.booking("", "", False)
                elif user_input == "2":
                    self.search("")
                elif user_input == "3":
                    self.report()
                elif user_input == "4":
                    print("-ᣁ Thank you! ᣂ-")
                    exit = True
                else:
                    print("Incorrect input detected!")

    def booking(self, _seat_numbers: str, _name: str, _test: bool):  # Brian
        if self.__studio.get_filled_seats() == self.__studio.get_studio_capacity():
            print(f"Oh no, the cinema is full! :(")
            return "full"

        print("1. Seat Booking")
        if _seat_numbers == "":
            _seat_numbers = input(f"Enter seat number: ")

        seat_numbers_list = _seat_numbers.split(",")  # split dan ubah jadi list
        seat_numbers_list: list  # type hint

        for i in range(len(seat_numbers_list)):
            # validasi input: kursi harus bernomor 1-36
            if not seat_numbers_list[i].isnumeric() or int(seat_numbers_list[i]) < 1 or int(seat_numbers_list[i]) > self.__studio.get_studio_capacity():
                print(f"Seat input format should be 'Enter Seat Number: [1-36],[1-36 (optional)],...'! Please try again.")
                return "unknown"
            seat_numbers_list[i] = int(seat_numbers_list[i])

            # validasi input: kursi harus belum dipesan
            if self.__studio.get_seat_from_index(seat_numbers_list[i] - 1).get_name() is not None:
                print(f"You've attempted to book a seat that has already been booked! Please try again.")
                return "booked"

        if _name == "":
            _name = input(f"Enter name: ")

        _name = _name.lower()

        lucky_person = False
        seats_booked_by_person = []
        for seat_index in seat_numbers_list:
            seat = self.__studio.get_seat_from_index(seat_index - 1)
            seat.set_name(_name)  # modifikasi nama pemesan seat
            lucky_person = True if isinstance(seat, SpecialSeat) else lucky_person
            seats_booked_by_person.append(seat.get_number())

        if self.__studio.get_seat_log().get(_name) is not None:
            self.__studio.get_seat_log()[
                _name] += seats_booked_by_person  # tambah ke catatan yang sudah ada di booking log
        else:
            self.__studio.set_seat_log(_name, seats_booked_by_person)  # catat baru di booking log

        the_time = time.localtime(time.time())
        self.__hour_log.set_book_per_hour(the_time.tm_hour, seat_numbers_list)

        print(f"Seat {_seat_numbers} booked by {_name}.")
        self.receipt(_name, seat_numbers_list, lucky_person) if _test is False else None
        self.__studio.set_filled_seats(len(seat_numbers_list))

        return ("unbooked", seat_numbers_list) if lucky_person is False else ("unbooked_gift", seat_numbers_list)

    def receipt(self, _name: str, _seat_numbers_list: list, lucky_person: bool):
        name_txt = f'{_name}_{"_".join([str(i) for i in _seat_numbers_list])}'
        receipt_txt = open(os.path.split(os.path.abspath(__file__))[0] + f"\\ticket_receipt" + f"\\{name_txt}.txt", "w")
        receipt_txt.write("===============================================")
        receipt_txt.write("\n               IL Kino Receipt                 ")
        receipt_txt.write("\n===============================================")
        receipt_txt.write(f"\nName\t\t: {_name}")
        receipt_txt.write(f"\nSeat numbers\t: {','.join([str(i) for i in _seat_numbers_list])}")
        receipt_txt.write("\nPlease check below your seat to get your gift.") if lucky_person is True else None
        receipt_txt.write("\n       Please arrive 15 minutes before.       ")
        receipt_txt.close()
        print(f"Receipt {name_txt}.txt is printed. Don't lose your ticket.")

    def search(self, _name: str):  # Gracia
        seat_log = self.__studio.get_seat_log()

        print("2. Find by Name")
        if _name == "":
            _name = input("Enter your name: ")

        _name = _name.lower()

        if _name not in seat_log:
            print("Sorry, the name is not in the booking log, please try again.")
            return None
        else:
            seat_numbers_string = ", ".join([str(i) for i in seat_log[_name]])
            print("Here is what we found:")
            print(f"Name: {_name}\nSeat number: {seat_numbers_string}")
            return _name, seat_log[_name]

    def report(self):  # Steven
        print("===================================")
        print("IL Kino Bioskop Studio Report")
        print("===================================")
        print()
        booking_log_per_hour = self.__hour_log.get_book_per_hour()
        if not booking_log_per_hour:
            print("No bookings have been made.")
        else:
            print("Hour\tNumber of booking")
            for i in booking_log_per_hour:
                if 0 <= i < 10:
                    print(f"0{i}.00\t{booking_log_per_hour[i]}")
                else:
                    print(f"{i}.00\t{booking_log_per_hour[i]}")
        print()

        gift_seats = self.__studio.get_seats_with_gifts()
        if gift_seats:
            print("All distributed SeatNumber-Gift:")
            for gift_seat in gift_seats:
                print(f"{gift_seat[0]}-{gift_seat[1]}")

    def get_all_distributed_gifts(self):
        seats_with_gifts = self.__studio.get_seats_with_gifts()
        temp_list = []

        for i in seats_with_gifts:
            temp_list.append([i[0], i[1]])

        return temp_list

    def get_gift_list(self):
        return self.__gift_list

    def get_studio(self):
        return self.__studio

    def get_book_by_hour(self, hour: int):
        return self.__hour_log.get_book_per_hour()[hour]