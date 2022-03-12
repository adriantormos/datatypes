from math import pi, tau, sqrt
from unittest import TestCase

import numpy as np

from types.geometry.vector import Vector2D, Vector2DCartesian, Vector2DPolar


class TestVector2D(TestCase):
    def test_init(self):
        v = Vector2D(2, 3)
        w = Vector2D(x=2, y=3)
        z = Vector2D(r=2, t=3)
        u = Vector2D(r=0, t=3)
        self.assertEqual([type(v), v.x, v.y], [Vector2DCartesian, 2, 3])
        self.assertEqual([type(w), w.x, w.y], [Vector2DCartesian, 2, 3])
        self.assertEqual([type(z), z.r, z.t], [Vector2DPolar, 2, 3])
        self.assertEqual([type(u), u.r, u.t], [Vector2DPolar, 0, 0])

    def test_eq(self):
        v = Vector2D(x=2, y=3)
        w = Vector2D(x=2, y=3)
        z = Vector2D(r=2, t=3)
        self.assertEqual(v == w, True)
        self.assertEqual(v == z, False)

    def test_length(self):
        v = Vector2D(x=2, y=3)
        w = Vector2D(x=3, y=4)
        z = Vector2D(r=2, t=3)
        self.assertEqual(v.length(), sqrt(13))
        self.assertEqual(w.length(), 5)
        self.assertEqual(z.length(), 2)

    def test_to_cartesian(self):
        v = Vector2D(x=2, y=3)
        self.assertEqual(v.to_cartesian(), Vector2D(x=2, y=3))
        self.assertEqual(v.to_cartesian(), v)
        w = Vector2D(r=2, t=3)
        self.assertEqual(w.to_cartesian(), Vector2D(x=2*np.cos(3), y=2*np.sin(3)))

    def test_to_polar(self):
        v = Vector2D(x=2, y=3)
        self.assertEqual(v.to_polar(), Vector2D(r=v.length(), t=np.arctan2(3, 2)))
        w = Vector2D(r=2, t=3)
        self.assertEqual(w.to_polar(), Vector2D(r=2, t=3))
        self.assertEqual(w.to_polar(), w)

    def test_neg(self):
        v = Vector2D(x=2, y=3)
        w = Vector2D(r=2, t=3)
        self.assertEqual(-v, Vector2D(x=-2, y=-3))
        self.assertEqual(-w, Vector2D(r=2, t=(3+pi) % tau))

    def test_add(self):
        v = Vector2D(x=2, y=3)
        w = Vector2D(x=4, y=2)
        self.assertEqual(v+w, Vector2D(x=6, y=5))
        z = Vector2D(r=2, t=3)
        t = Vector2D(r=5, t=3)
        self.assertEqual(z+t, Vector2D(r=7, t=3))
        w = Vector2D(r=2, t=pi)
        self.assertAlmostEqual((v+w-Vector2D(x=0, y=3)).length(), 0)

    def test_sub(self):
        v = Vector2D(x=2, y=3)
        w = Vector2D(x=4, y=2)
        self.assertEqual(v-w, Vector2D(x=-2, y=1))
        z = Vector2D(r=2, t=3)
        t = Vector2D(r=5, t=3)
        self.assertEqual(z-t, Vector2D(r=3, t=(3+pi) % tau))
        v = Vector2D(x=2, y=3)
        w = Vector2D(r=2, t=pi)
        self.assertAlmostEqual((v-w-Vector2D(x=4, y=3)).length(), 0)

    def test_mul(self):
        v = Vector2D(x=2, y=3)
        self.assertEqual(v*3, Vector2D(x=6, y=9))
        self.assertEqual(v*1, Vector2D(x=2, y=3))
        self.assertEqual(v*0.4, Vector2D(x=2*0.4, y=3*0.4))
        self.assertEqual(v*0, Vector2D(x=0, y=0))
        w = Vector2D(r=2, t=pi)
        self.assertEqual(w*3, Vector2D(r=6, t=pi))
        self.assertEqual(w*1, Vector2D(r=2, t=pi))
        self.assertEqual(w*0.4, Vector2D(r=0.8, t=pi))
        self.assertEqual(w*0, Vector2D(r=0, t=0))

    def test_div(self):
        v = Vector2D(x=2, y=3)
        self.assertEqual(v/3, Vector2D(x=2/3, y=1))
        self.assertEqual(v/1, Vector2D(x=2, y=3))
        self.assertEqual(v/0.4, Vector2D(x=2/0.4, y=3/0.4))
        w = Vector2D(r=2, t=pi)
        self.assertEqual(w/3, Vector2D(r=2/3, t=pi))
        self.assertEqual(w/1, Vector2D(r=2, t=pi))
        self.assertEqual(w/0.4, Vector2D(r=2/0.4, t=pi))

    def test_angle_with(self):
        v = Vector2D(x=2, y=2)
        w = Vector2D(r=2, t=pi)
        self.assertEqual(v.angle_with(w), 0.75*pi)
        self.assertEqual(w.angle_with(v), 0.75*pi)
        z = Vector2D(r=2, t=pi+2)
        u = Vector2D(r=2, t=3.5*pi)
        self.assertEqual(w.angle_with(z), 2)
        self.assertEqual(z.angle_with(w), 2)
        self.assertEqual(w.angle_with(u), 0.5*pi)

    def test_unit(self):
        v = Vector2D(x=3, y=3)
        o = Vector2D(x=0, y=0)
        self.assertAlmostEqual((v.unit()-Vector2D(x=1/np.sqrt(2), y=1/np.sqrt(2))).length(), 0)
        self.assertEqual(o.unit(),  Vector2D(x=0, y=0))
        w = Vector2D(r=6, t=pi/2)
        o = Vector2D(r=0, t=0)
        self.assertEqual(w.unit(),  Vector2D(r=1, t=pi/2))
        self.assertEqual(o.unit(),  Vector2D(r=1, t=0))

    def test_rotate(self):
        v = Vector2D(x=3, y=4)
        self.assertEqual(v.rotate(0), Vector2D(x=3, y=4))
        self.assertEqual(v.rotate(pi/2), Vector2D(x=-4, y=3))
        self.assertEqual(v.rotate(pi), Vector2D(x=-3, y=-4))
        self.assertEqual(v.rotate(3*pi/2), Vector2D(x=4, y=-3))
        self.assertAlmostEqual((v.rotate(pi/4)-Vector2D(r=v.length(), t=(pi/4+np.arctan2(4, 3)) % tau)).length(), 0)
        w = Vector2D(r=3, t=pi)
        self.assertEqual(w.rotate(0),  Vector2D(r=3, t=pi))
        self.assertEqual(w.rotate(3),  Vector2D(r=3, t=(pi+3) % tau))


