from unittest import TestCase
from typing import List
from mapperr import to_dict, to_obj

class A:
    a1: str
    a2: int

class B:
    b1: str
    b2: int
    b3: A

class C:
    c1: str
    c2: int
    c3: List[B]
    c4: List[int]
    c5: dict
    c6: list
    c7: float


class TestNestedObjects(TestCase):
    def setUp(self) -> None:
        self.a = A()
        self.a.a1, self.a.a2 = "text", 1
        self.ad = {"a1": "text", "a2": 1}

        self.a2 = A()
        self.a2.a1, self.a2.a2 = "text2", 1

        self.b = B()
        self.b.b1, self.b.b2, self.b.b3 = "text", 1, self.a
        self.bd = {'b1': 'text', 'b2': 1, 'b3': {'a1': 'text', 'a2': 1}}

        self.b2 = B()
        self.b2.b1, self.b2.b2, self.b2.b3 = "text2", 1, self.a2

        self.c = C()
        self.c.c1, self.c.c2, self.c.c3, self.c.c4, self.c.c5, self.c.c6 = "text", 1, [self.b, self.b2], [1,2], {"msg": "hello"}, ["x", "y", "z"]
        self.c.c7 = 3.14
        self.cd = {'c1': 'text', 'c2': 1, 'c3': [{'b1': 'text', 'b2': 1, 'b3': {'a1': 'text', 'a2': 1}}, {'b1': 'text2', 'b2': 1, 'b3': {'a1': 'text2', 'a2': 1}}], 'c4': [1, 2], 'c5': {'msg': 'hello'}, 'c6': ['x', 'y', 'z'], 'c7' : 3.14}

    def test_todict_level1(self):
        self.assertEqual(to_dict(self.a), self.ad)

    def test_todict_level2(self):
        self.assertEqual(to_dict(self.b), self.bd)

    def test_todict_level3(self):
        self.assertEqual(to_dict(self.c), self.cd)

    def test_toobj_level1(self):
        self.assertEqual(to_dict( to_obj(self.ad, A) ), self.ad)

    def test_toobj_level2(self):
        self.assertEqual(to_dict( to_obj(self.bd, B) ), self.bd)

    def test_toobj_level3(self):
        self.assertEqual(to_dict( to_obj(self.cd, C) ), self.cd)