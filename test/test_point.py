from math import pi
from unittest import TestCase
from datatypes.geometry.vector import Vector2D
from datatypes.geometry.point import Point2D


class TestPoint2D(TestCase):
    def test_init(self):
        p = Point2D(2, 3)
        self.assertEqual([type(p), p.x, p.y], [Point2D, 2, 3])

    def test_eq(self):
        p = Point2D(2, 3)
        q = Point2D(2, 3)
        r = Point2D(0, -2)
        self.assertEqual(p == q, True)
        self.assertEqual(p == r, False)

    def test_neg(self):
        p = Point2D(2, 3)
        self.assertEqual(-p, Point2D(-2, -3))

    def test_add(self):
        p = Point2D(2, 3)
        q = Point2D(0, -2)
        self.assertEqual(p + q, Point2D(2, 1))
        v = Vector2D(4, -3)
        w = Vector2D(r=3, t=pi/2)
        self.assertEqual(p + v, Point2D(6, 0))
        self.assertEqual(v + p, Point2D(6, 0))
        self.assertEqual(p + w, Point2D(2, 6))
        self.assertEqual(w + p, Point2D(2, 6))

    def test_sub(self):
        p = Point2D(2, 3)
        q = Point2D(4, -2)
        self.assertEqual(p - q, Vector2D(-2, 5))
        self.assertEqual(q - p, Vector2D(2, -5))
        v = Vector2D(4, -3)
        w = Vector2D(r=2, t=pi/2)
        self.assertEqual(p - v, Point2D(-2, 6))
        self.assertAlmostEqual((p - w - Point2D(2, 1)).length(), 0)

    def test_mul(self):
        p = Point2D(2, 3)
        self.assertEqual(p*3, Point2D(x=6, y=9))
        self.assertEqual(p*1, Point2D(x=2, y=3))
        self.assertEqual(p*0.4, Point2D(x=2*0.4, y=3*0.4))
        self.assertEqual(p*0, Point2D(x=0, y=0))

    def test_div(self):
        p = Point2D(x=2, y=3)
        self.assertEqual(p/3, Point2D(x=2/3, y=1))
        self.assertEqual(p/1, Point2D(x=2, y=3))
        self.assertEqual(p/0.4, Point2D(x=2/0.4, y=3/0.4))

    def test_to_list(self):
        p = Point2D(x=2, y=3)
        self.assertEqual(p.to_list(), [p.x, p.y])