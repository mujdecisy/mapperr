from unittest import TestCase
from mapperr import to_dict, to_obj
import warnings

class A:
    a1: float
    a2: str

class TestMapperr2(TestCase):
    def setUp(self) -> None:
        self.a = A()
        self.a.a1, self.a.a2 = "text", 1
        self.ad = {"a1": "text", "a2": 1}

    def test_todict_level1(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            to_dict(self.a)
            self.assertEqual(len(w), 2)
            

    def test_toobj_level1(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            to_obj(self.ad, A)
            self.assertEqual(len(w), 2)