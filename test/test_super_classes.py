from unittest import TestCase
from mapperr import to_dict, to_obj
from typing import Dict

class A:
    a1: str

class B(A):
    b1: str

class C(A):
    a1: int

class TestSuperClasses(TestCase):
    def setUp(self) -> None:
        self.b = B()
        self.b.a1, self.b.b1 = "texta1", "textb1"
        self.bd = {"a1": "texta1", "b1": "textb1"}

        self.c = C()
        self.c.a1 = 1
        self.cd = {"a1": 1}

    def test__to_dict__when_superClassExists(self):
        actual = to_dict(self.b)
        expected = self.bd
        self.assertEqual(actual, expected)

    def test__to_obj__when_superClassExists(self):
        actual = to_dict(to_obj(self.bd, B))
        expected = self.bd
        self.assertEqual(actual, expected)

    def test__to_obj__when_classOverridesAttrOfSuperClass(self):
        actual = to_dict(to_obj(self.cd, C))
        expected = self.cd
        self.assertEqual(actual, expected)