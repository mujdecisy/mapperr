from unittest import TestCase
from mapperr import to_dict, to_obj
from typing import Dict

class A:
    a1: float

# the type is float but
class TestIntToFloatTransformation(TestCase):
    def setUp(self) -> None:
        self.a = A()
        self.a.a1 = 1
        self.ad = {"a1": 1}

    def test__to_dict(self):
        actual = to_dict(self.a)
        expected = self.ad
        self.assertEqual(actual, expected)

    def test__to_obj(self):
        actual = to_dict(to_obj(self.ad, A))
        expected = self.ad
        self.assertEqual(actual, expected)