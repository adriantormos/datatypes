from __future__ import annotations

from typing import Union
import numpy as np

from datatypes.geometry import Vector2D, Vector2DPolar


class Point2D:
    """
    A 2-dimensional point.

    A point in a 2-dimensional space, expressed in cartesian coordinates.

    Args:
        x: The x coordinate of the point.
        y: The y coordinate of the point.
    """

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        assert x is not None
        assert y is not None
        assert np.isreal(x)
        assert np.isreal(y)
        object.__setattr__(self, 'x', x)
        object.__setattr__(self, 'y', y)

    def __eq__(self, other) -> bool:
        """
        Compares equality in two 2-dimensional points.

        Returns True if the attributes of `self` and `other` are the same.

        Args:
            other: A `Point2D` to compare with.

        Returns:
            A `bool` value expressing equality between the points.
        """
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> Point2D:
        """
        Negates `self`.

        Negates the two components of `self` and returns it.

        Returns:
            A negated `Point2D`.
        """
        return Point2D(-self.x, -self.y)

    def __add__(self, other) -> Point2D:
        """
        Adds `self` to a 2D vector or another point.

        If `other` is a `Point2D`, returns the sum with `self`, a `Point2D`. If `other` is a `Vector2D`, returns
        the displacement of `self` by it, a `Point2D`.

        Args:
            other: A `Point2D` or `Vector2D` to be added to `self`.

        Returns:
            Either the sum of `self` and `other` or the displacement of `self` by `other`.

        Raises:
            TypeError: If `other` is not a `Point2D` or `Vector2D`.
        """
        if not isinstance(other, Point2D) \
                and not isinstance(other, Vector2D):
            raise TypeError('Point2D can only be added by a Point2D or another Vector2D.')
        if isinstance(other, Vector2DPolar):
            other = other.to_cartesian()
        return Point2D(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other) -> Union[Point2D, Vector2D]:
        """
        Creates a vector from `self` and `other` or displaces `self` by `other`.

        If `other` is a `Point2D`, returns the `Vector2D` from `other` to `self`. If `other` is a `Vector2D`, returns
        the displacement of `self` by the negation of `other`.

        Args:
            other: A `Point2D` or `Vector2D` to be substracted to `self`.

        Returns:
            Either the vector from `other` to `self` or the displacement of `self` by `-other`.

        Raises:
            TypeError: If `other` is not a `Point2D` or `Vector2D`.

        """
        if not isinstance(other, Point2D) \
                and not isinstance(other, Vector2D):
            raise TypeError('Point2D can only be substracted by a Point2D or another Vector2D.')
        if isinstance(other, Point2D):
            return Vector2D(x=self.x - other.x, y=self.y - other.y)
        if isinstance(other, Vector2DPolar):
            other = other.to_cartesian()
        return Point2D(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other) -> Point2D:
        """
        Multiplies `self` by a scalar.

        Args:
            other: A scalar to multiply `self` by.

        Returns:
            A `Point2D` with the components of `self` multiplied by `other`.

        Raises:
            TypeError: If `other` is not a scalar.
        """
        if not np.isreal(other):
            raise TypeError('Point2D can only be multiplied by a scalar.')
        if other == 0:
            return Point2D(x=0, y=0)
        return Point2D(self.x*other, self.y*other)

    def __rmul__(self, other) -> Point2D:
        return self * other

    def __truediv__(self, other) -> Point2D:
        """
        Divides `self` by a scalar.

        Args:
            other: A scalar to divide `self` by.

        Returns:
            A `Point2D` with the components of `self` divided by `other`.

        Raises:
            TypeError: If `other` is not a scalar.
            ZeroDivisionError: If `other` is equal to 0.
        """
        if not np.isreal(other):
            raise TypeError('Point2D can only be divided by a scalar.')
        if other == 0:
            raise ZeroDivisionError
        return Point2D(self.x/other, self.y/other)

    def __setattr__(self, key, value):
        raise RuntimeError('Point2D object is immutable.')

    def to_list(self) -> list:
        """
        Passes `self` to a list format.

        Returns the x and y components of `self` contatenated into a list.

        Returns:
            The list `[self.x, self.y]`.
        """
        return [self.x, self.y]

    def __str__(self):
        return f'({round(self.x, 2)},{round(self.y, 2)})'

    def __repr__(self):
        return self.__str__()