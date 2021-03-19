from typing import Optional


def greeting(name: Optional[str] = None) -> str:
    return f"Hello, {name if name else 'Anonymous'}"


assert greeting() == "Hello, Anonymous"
