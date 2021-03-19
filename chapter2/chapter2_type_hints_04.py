from typing import Union


def greeting(name: Union[str, None] = None) -> str:
    return f"Hello, {name if name else 'Anonymous'}"


assert greeting() == "Hello, Anonymous"
