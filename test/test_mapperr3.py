from unittest import TestCase
from mapperr import to_dict, to_obj

class A:
    a1: float
    a2: str
    required : list = ["a2"]

class TestMapperr3(TestCase):
    def setUp(self) -> None:
        self.a = A()
        self.a.a1, self.a.a2 = 1.0, "a"
        self.ad = {"a1": 1.0}

    def test_toobj_level1(self):
        er = False
        try:
            to_obj(self.ad, A)
        except AttributeError:
            er = True
        
        self.assertEqual( er, True )