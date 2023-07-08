from unittest import TestCase
from mapperr import to_dict, to_obj


class A:
    a1: str
    a2: int
    recursive: "A"


class TestRecursiveObjects(TestCase):
    def setUp(self) -> None:
        self.a_inner = A()
        self.a_inner.a1, self.a_inner.a2, self.recursive = "text_inner", 2, None

        self.a = A()
        self.a.a1, self.a.a2, self.a.recursive = "text", 1, self.a_inner
        self.ad = {"a1": "text", "a2": 1, "recursive": {"a1": "text_inner", "a2": 2, "recursive": None}}

    def test__to_dict__when_recursive_classes(self):
        actual = to_dict(self.a)
        expected = self.ad
        self.assertEqual(actual, expected)

    def test__to_obj__when_recursive_classes(self):
        actual = to_dict(to_obj(self.ad, A))
        expected = self.ad
        self.assertEqual(actual, expected)
