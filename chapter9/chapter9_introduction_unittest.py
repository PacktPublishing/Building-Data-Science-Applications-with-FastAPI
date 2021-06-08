import unittest

from chapter9.chapter9_introduction import add


class TestChapter9Introduction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
