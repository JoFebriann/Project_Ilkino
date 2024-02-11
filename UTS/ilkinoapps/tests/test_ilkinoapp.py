import random
import time
from ilkinoapps.ilkino import Ilkino


def test_book_unbooked_seat():
    random.seed(1)
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "unbooked", [1]  # seat no. 1 doesn't come with a gift
    current = ilkinoapps.booking("1", "Sanga", True)
    assert current == expected


def test_book_unbooked_seats():
    random.seed(1)
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "unbooked", [6, 10, 12, 13]  # seat no. 6, 10, 12, and 13 don't come with a gift
    current = ilkinoapps.booking("6,10,12,13", "Sanga", True)
    assert current == expected


def test_book_unknown_seat():
    random.seed(1)
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "unknown"
    current = ilkinoapps.booking("50", "Sanga", True)
    assert current == expected


def test_book_booked_seat():
    random.seed(1)
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "booked"
    ilkinoapps.booking("1", "Sanga", True)
    current = ilkinoapps.booking("1", "Sanga", True)
    assert current == expected


def test_book_seat_with_gift():
    random.seed(1)
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "unbooked_gift", [9]  # seat no. 9 comes with a gift
    current = ilkinoapps.booking("9", "Sanga", True)
    assert current == expected


def test_book_seats_with_gift():
    random.seed(1)
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "unbooked_gift", [26, 34, 8]  # seat no. 26, 34, and 8 come with a gift
    current = ilkinoapps.booking("26,34,8", "Sanga", True)
    assert current == expected


def test_search_booked_name_one_seat():
    teater = Ilkino(None)
    teater.setup()
    teater.booking("1", "Gracia", True)
    expected = "gracia", [1]
    current = teater.search("Gracia")
    assert current == expected


def test_search_booked_name_multiple_seats():
    teater = Ilkino(None)
    teater.setup()
    teater.booking("1,6,8", "Gracia", True)
    expected = "gracia", [1, 6, 8]
    current = teater.search("Gracia")
    assert current == expected


def test_search_unbooked_name():
    teater = Ilkino(None)
    teater.setup()
    teater.booking("8", "Yozef", True)
    expected = None
    current = teater.search("Erin")
    assert expected == current


def test_get_book_by_hour():
    teater = Ilkino(None)
    teater.setup()
    teater.booking("1", "Gracia", True)
    teater.booking("2", "Erin", True)
    the_time = time.localtime(time.time())
    expected = 2
    current = teater.get_book_by_hour(the_time.tm_hour)
    assert expected == current


def test_get_book_per_hour():
    teater = Ilkino(None)
    teater.setup()
    current_hour = time.localtime(time.time()).tm_hour

    teater.booking("9", "Orang1", True)
    teater.booking("5", "Orang2", True)
    teater.booking("17", "Orang3", True)
    teater.booking("3", "Orang4", True)
    teater.booking("15", "Orang5", True)
    expected = 5
    current = teater.get_book_by_hour(current_hour)
    assert expected == current


def test_get_all_distributed_gifts():
    random.seed(1)
    teater = Ilkino(None)
    teater.setup()

    # distributed gift on left
    teater.booking("9", "Orang1", True)
    teater.booking("5", "Orang2", True)
    teater.booking("17", "Orang3", True)
    teater.booking("3", "Orang4", True)
    teater.booking("15", "Orang5", True)

    # distributed gift on right
    teater.booking("30", "Orang1", True)
    teater.booking("32", "Orang2", True)
    teater.booking("26", "Orang3", True)
    teater.booking("34", "Orang4", True)
    teater.booking("8", "Orang5", True)

    current = teater.get_all_distributed_gifts()
    expected = [[3, 'placeholder1'], [5, 'placeholder5'], [8, 'placeholder1'], [9, 'placeholder3'], [15, 'placeholder4'], [17, 'placeholder2'], [26, 'placeholder5'], [30, 'placeholder3'], [32, 'placeholder2'], [34, 'placeholder4']]
    assert expected == current


def test_gift_randomly_assigned_left():
    random.seed(13)
    teater = Ilkino(None)
    teater.setup()
    expected = [16, 28, 26, 4, 24]
    current = teater.get_gift_list().randomly_assign_left(teater.get_studio().get_studio_capacity())
    assert expected == current


def test_gift_randomly_assigned_right():
    random.seed(13)
    teater = Ilkino(None)
    teater.setup()
    expected = [17, 29, 27, 5, 25]
    current = teater.get_gift_list().randomly_assign_right(teater.get_studio().get_studio_capacity())
    assert expected == current


def test_cinema_is_full():
    ilkinoapps = Ilkino(None)
    ilkinoapps.setup()
    expected = "full"
    for i in range(1, 37):
        ilkinoapps.booking(str(i), "Timothy", True)
    current = ilkinoapps.booking("", "", True)
    assert expected == current