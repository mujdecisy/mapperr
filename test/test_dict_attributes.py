from unittest import TestCase
from mapperr import to_dict, to_obj
from typing import Dict

class A:
    a1: Dict[str, int]

class TestDictAttributes(TestCase):
    def setUp(self) -> None:
        self.a = A()
        self.a.a1 = {"apple": 5, "banana": 6}
        self.ad = {"a1": {"apple": 5, "banana": 6}}

    def test__to_dict__when_dictAttrExist(self):
        actual = to_dict(self.a)
        expected = self.ad
        self.assertEqual(actual, expected)

    def test__to_obj__when_dictAttrExist(self):
        actual = to_dict(to_obj(self.ad, A))
        expected = self.ad
        self.assertEqual(actual, expected)