from unittest import TestCase
from mapperr import to_obj

class A:
    a1: float
    a2: str
    op_required : list = ["a2"]

class B:
    a1: float
    a2: str
    op_required : list = ["a3"]

class TestOpRequired(TestCase):
    def setUp(self) -> None:
        self.a = A()
        self.a.a1, self.a.a2 = 1.0, "a"
        self.ad = {"a1": 1.0}

        self.b = A()
        self.b.a1, self.b.a2 = 1.0, "a"
        self.bd = {"a1": 1.0}

    def test__to_obj__throwsError_whenRequiredListNotProvided(self):
        self.assertRaises(AttributeError, to_obj, self.ad, A)

    def test__to_obj__throwsError_whenRequiredListContainsNonExistingElement(self):
        self.assertRaises(TypeError, to_obj, self.bd, B)