from typing import Callable, List

ConditionFunction = Callable[[int], bool]


def filter_list(l: List[int], condition: ConditionFunction) -> List[int]:
    return [i for i in l if condition(i)]
