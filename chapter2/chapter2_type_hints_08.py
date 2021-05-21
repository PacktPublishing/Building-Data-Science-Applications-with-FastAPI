from typing import Callable, List

ConditionFunction = Callable[[int], bool]


def filter_list(l: List[int], condition: ConditionFunction) -> List[int]:
    return [i for i in l if condition(i)]


def is_even(i: int) -> bool:
    return i % 2 == 0


filter_list([1, 2, 3, 4, 5], is_even)
