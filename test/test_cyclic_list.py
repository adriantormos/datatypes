from unittest import TestCase
from src.cyclic_list import CyclicList


class TestCyclicList(TestCase):
    def test_init(self):
        cl = CyclicList([1, 2, 3, 4, 5])
        self.assertEqual(type(cl), CyclicList)
        self.assertEqual(cl.data, [1, 2, 3, 4, 5])

    def test_set(self):
        cl = CyclicList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        cl[2] = '2'
        cl[-4] = '-4'
        cl[-4].__setitem__('-4')
        cl[23] = '23'
        self.assertEqual(cl, CyclicList([0, 1, '2', '23', 4, 5, '-4', 7, 8, 9]))
        cl[7:15] = '7'
        self.assertEqual(cl, CyclicList([0, 1, '2', '23', 4, 5, '-4', '7']))

    def test_get(self):
        cl = CyclicList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(cl[3], 3)
        self.assertEqual(cl[-1], 9)
        self.assertEqual(cl[15], 5)
        self.assertEqual(cl[:8], CyclicList([0, 1, 2, 3, 4, 5, 6, 7]))
        self.assertEqual(cl[2:], CyclicList([2, 3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(cl[2:8], CyclicList([2, 3, 4, 5, 6, 7]))
        self.assertEqual(cl[2:23], CyclicList([2, 3, 4, 5, 6, 7, 8, 9] + cl.data + [0, 1, 2]))
        self.assertEqual(cl[:23], CyclicList(2 * cl.data + [0, 1, 2]))
        self.assertEqual(cl[-12:23], CyclicList([8, 9] + 3 * cl.data + [0, 1, 2]))
        self.assertEqual(cl[-12:], CyclicList([8, 9] + 2 * cl.data))

    def test_del(self):
        cl = CyclicList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        del cl[16]
        del cl[2]
        self.assertEqual(cl, CyclicList([0, 1, 3, 4, 5, 7, 8, 9]))
        del cl[5:40]
        self.assertEqual(cl, CyclicList([0, 1, 3, 4, 5]))
