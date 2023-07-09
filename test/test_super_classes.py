from unittest import TestCase
from mapperr import to_dict, to_obj
from typing import Dict

class A:
    a1: str

class B(A):
    b1: str

class C(A):
    a1: int

class D(A):
    d1: str
    d2: 'D'

class E(D):
    e1: str

class TestSuperClasses(TestCase):
    def setUp(self) -> None:
        self.b = B()
        self.b.a1, self.b.b1 = "texta1", "textb1"
        self.bd = {"a1": "texta1", "b1": "textb1"}

        self.c = C()
        self.c.a1 = 1
        self.cd = {"a1": 1}

        self.d_inner = D()
        self.d_inner.a1 = "texta1_inner"
        self.d_inner.d1 = "textd1_inner"

        self.d = D()
        self.d.a1 = "texta1"
        self.d.d1 = "textd1"
        self.d.d2 = self.d_inner

        self.d_dict = {
            "a1": "texta1",
            "d1": "textd1",
            "d2": {
                "a1": "texta1_inner",
                "d1": "textd1_inner",
                "d2": None
            }
        }

        self.e = E()
        self.e.a1, self.e.e1, self.e.d1, self.e.d2 = "texta1", "texte1", "textd1", self.d_inner
        self.ed = {
            "a1": "texta1",
            "e1": "texte1",
            "d1": "textd1",
            "d2": {
                "a1": "texta1_inner",
                "d1": "textd1_inner",
                "d2": None
            }
        }

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

    def test__to_obj__to_dict__when_classHasRecursiveAttribute(self):
        actual = to_dict(to_obj(self.d_dict, D))
        expected = to_dict(self.d)
        self.assertEqual(actual, expected)

    def test__to_obj__when_superClassHasRecursiveAttribute(self):
        actual = to_dict(to_obj(self.ed, E))
        expected = to_dict(self.e)
        self.assertEqual(actual, expected)