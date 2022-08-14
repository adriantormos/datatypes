from math import pi, tau, sqrt
from unittest import TestCase

import numpy as np

from datatypes.geometry import Segment2D, Point2D


class TestSegment2D(TestCase):
    def test_init(self):
        s = Segment2D(Point2D(0, 0), Point2D(4, 3))
        self.assertEqual([type(s), s.a, s.b], [Segment2D, Point2D(0, 0), Point2D(4, 3)])

    def test_eq(self):
        s = Segment2D(Point2D(0, 0), Point2D(4, 3))
        t = Segment2D(Point2D(0, 0), Point2D(4, 3))
        u = Segment2D(Point2D(-3, 0), Point2D(2, 3))
        self.assertEqual(s == t, True)
        self.assertEqual(s == u, False)

    def test_length(self):
        s = Segment2D(Point2D(0, 0), Point2D(4, 3))
        self.assertEqual(s.length(), 5)

    def test_intersects_with(self):
        s = Segment2D(Point2D(0, 0), Point2D(3, 3))
        t = Segment2D(Point2D(2, 0), Point2D(2, 3))
        u = Segment2D(Point2D(0, 0), Point2D(2, 3))
        v = Segment2D(Point2D(6, 0), Point2D(3, 3))
        w = Segment2D(Point2D(10, 10), Point2D(15, 15))
        self.assertEqual(s.intersects_with(t), True)
        self.assertEqual(s.intersects_with(u), True)
        self.assertEqual(s.intersects_with(v), True)
        self.assertEqual(s.intersects_with(w), False)

    def test_intersection(self):
        s = Segment2D(Point2D(0, 0), Point2D(3, 3))
        t = Segment2D(Point2D(2, 0), Point2D(2, 3))
        u = Segment2D(Point2D(0, 0), Point2D(2, 3))
        v = Segment2D(Point2D(6, 0), Point2D(3, 3))
        w = Segment2D(Point2D(10, 10), Point2D(15, 15))
        self.assertEqual(s.intersection(t), Point2D(2, 2))
        self.assertEqual(s.intersection(u), Point2D(0, 0))
        self.assertEqual(s.intersection(v), Point2D(3, 3))
        self.assertEqual(s.intersection(w), None)

