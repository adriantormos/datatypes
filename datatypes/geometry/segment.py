from typing import Optional

from datatypes.geometry import Point2D


class Segment2D:
    """
    A 2-dimensional line segment.

    A closed line segment that joins two Point2D.

    Args:
        a: The origin endpoint.
        b: The destination endpoint.
    """
    __slots__ = ['a', 'b']

    def __init__(self, a: Point2D, b: Point2D):
        self.a: Point2D
        self.b: Point2D
        assert isinstance(a, Point2D)
        assert isinstance(b, Point2D)
        object.__setattr__(self, 'a', a)
        object.__setattr__(self, 'b', b)

    def length(self) -> float:
        """
        Returns the distance between the two endpoints of the line segment.

        Returns:
            A `float` value corresponding to the distance between `self.a` and `self.b`.

        """
        return (self.b - self.a).length()

    def intersection(self, other) -> Optional[Point2D]:
        """
        Calculates the intersection between two line segments.

        Returns the intersection point if it exists, `None` otherwise.

        Args:
            other: A `Segment2D` to calculate the intersection with.

        Returns:
            The intersection `Point2D` between `self` and `other`, if it exists, and `None` otherwise.
        """
        if not isinstance(other, Segment2D):
            raise ValueError('Parameter must be a Segment.')
        v1, v2 = (self.b - self.a).to_cartesian(), (other.b - other.a).to_cartesian()
        denom: float = v1.y * v2.x - v1.x * v2.y
        if denom == 0:
            return None
        numer: float = v1.x * (other.a.y - self.a.y) - v1.y * (other.a.x - self.a.x)
        u: float = numer / denom
        t: float = (u * v2.x + other.a.x - self.a.x) / v1.x
        if 0 <= u <= 1 and 0 <= t <= 1:
            return other.a + u * v2
        return None

    def intersects_with(self, other) -> bool:
        """
        Checks whether the intersection between two line segments exists.

        Returns `True` if it exists, `False` otherwise.

        Args:
            other: A `Segment2D` to check the intersection with.

        Returns:
            A `bool` value expressing whether there exists an intersection point between `self` and `other`.
        """
        return self.intersection(other) is not None

    def __eq__(self, other):
        """
        Compares equality in two 2-dimensional line segments.

        Returns True if the attributes of `self` and `other` are the same.

        Args:
            other: A `Segment2D` to compare with.

        Returns:
            A `bool` value expressing equality between the line segments.
        """
        if not isinstance(other, Segment2D):
            return False
        return self.a == other.a and self.b == other.b

    def __setattr__(self, key, value):
        raise TypeError('Segment object is immutable.')

    def __repr__(self):
        return f'{self.a}->{self.b}'

    def __str__(self):
        return self.__repr__()