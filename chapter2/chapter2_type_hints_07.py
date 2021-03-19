from typing import List


class Post:
    def __init__(self, title: str) -> None:
        self.title = title

    def __str__(self) -> str:
        return self.title


posts: List[Post] = [Post("Post A"), Post("Post B")]
