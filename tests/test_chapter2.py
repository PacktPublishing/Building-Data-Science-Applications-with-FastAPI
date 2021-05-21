import asyncio
import runpy


def test_chapter2_basics_02():
    from chapter2.chapter2_basics_02 import even

    assert even == [2, 4, 6, 8, 10]


def test_chapter2_basics_03():
    from chapter2.chapter2_basics_03 import t, q, r

    assert t[0] == 1
    assert t[1] == 1

    assert q == 10
    assert r == 2


def test_chapter2_basics_04():
    from chapter2.chapter2_basics_04 import forward_order_status

    assert forward_order_status({"status": "NEW"}) == {"status": "IN_PROGRESS"}
    assert forward_order_status({"status": "IN_PROGRESS"}) == {"status": "SHIPPED"}
    assert forward_order_status({"status": "SHIPPED"}) == {"status": "DONE"}


def test_chapter2_basics_05():
    from chapter2.chapter2_basics_05 import items

    assert items == ["A", "B", "C", "A", "B", "C", "A", "B", "C"]


def test_chapter2_classes_objects_01():
    from chapter2.chapter2_classes_objects_01 import c

    assert c.greet("John") == "Hello, John"


def test_chapter2_classes_objects_02():
    from chapter2.chapter2_classes_objects_02 import c

    assert c.default_name == "Alan"
    assert c.greet() == "Hello, Alan"
    assert c.greet("John") == "Hello, John"


def test_chapter2_classes_objects_03():
    from chapter2.chapter2_classes_objects_03 import t

    assert repr(t) == "Temperature(25, 'C')"
    assert str(t) == "Temperature is 25 °C"


def test_chapter2_classes_objects_04():
    from chapter2.chapter2_classes_objects_04 import tc, tf, tf2

    assert tc == tf
    assert tc < tf2


def test_chapter2_classes_objects_05():
    from chapter2.chapter2_classes_objects_05 import Counter

    c = Counter()
    assert c.counter == 0
    c()
    assert c.counter == 1
    c(10)
    assert c.counter == 11


def test_chapter2_classes_objects_06():
    from chapter2.chapter2_classes_objects_06 import c

    assert c.f() == "A"


def test_chapter2_classes_objects_07():
    from chapter2.chapter2_classes_objects_07 import c

    assert c.f() == "Child A"


def test_chapter2_classes_objects_08():
    from chapter2.chapter2_classes_objects_08 import c

    assert c.f() == "A"
    assert c.g() == "B"


def test_chapter2_classes_objects_09():
    from chapter2.chapter2_classes_objects_09 import c

    assert c.f() == "A"


def test_chapter2_list_comprehensions_01():
    from chapter2.chapter2_list_comprehensions_01 import even

    assert even == [2, 4, 6, 8, 10]


def test_chapter2_list_comprehensions_02():
    from chapter2.chapter2_list_comprehensions_02 import random_elements

    assert random_elements == [10, 1, 7, 8, 10]


def test_chapter2_list_comprehensions_03():
    from chapter2.chapter2_list_comprehensions_03 import random_unique_elements

    assert random_unique_elements == {8, 1, 10, 7}


def test_chapter2_list_comprehensions_04():
    from chapter2.chapter2_list_comprehensions_04 import random_dictionary

    assert random_dictionary == {0: 10, 1: 1, 2: 7, 3: 8, 4: 10}


def test_chapter2_list_comprehensions_05():
    from chapter2.chapter2_list_comprehensions_05 import even, even_bis

    assert even == [2, 4, 6, 8, 10]
    assert even_bis == []


def test_chapter2_list_comprehensions_06():
    from chapter2.chapter2_list_comprehensions_06 import even

    assert even == [2, 4, 6, 8, 10]


def test_chapter2_list_comprehensions_07():
    from chapter2.chapter2_list_comprehensions_07 import even

    assert even == [2, 4, 6, 8, 10]


def test_chapter2_type_hints_01():
    from chapter2.chapter2_type_hints_01 import greeting

    assert greeting("John") == "Hello, John"


def test_chapter2_type_hints_04():
    from chapter2.chapter2_type_hints_04 import greeting

    assert greeting() == "Hello, Anonymous"


def test_chapter2_type_hints_05():
    from chapter2.chapter2_type_hints_05 import greeting

    assert greeting() == "Hello, Anonymous"


def test_chapter2_non_assertive(event_loop):
    asyncio.set_event_loop(event_loop)

    runpy.run_module("chapter2.chapter2_asyncio_01")
    runpy.run_module("chapter2.chapter2_asyncio_02")
    runpy.run_module("chapter2.chapter2_asyncio_03")

    runpy.run_module("chapter2.chapter2_basics_01")
    runpy.run_module("chapter2.chapter2_basics_module")

    runpy.run_module("chapter2.chapter2_type_hints_02")
    runpy.run_module("chapter2.chapter2_type_hints_03")
    runpy.run_module("chapter2.chapter2_type_hints_06")
    runpy.run_module("chapter2.chapter2_type_hints_07")
    runpy.run_module("chapter2.chapter2_type_hints_08")
    runpy.run_module("chapter2.chapter2_type_hints_09")
    runpy.run_module("chapter2.chapter2_type_hints_10")
