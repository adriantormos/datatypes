from __future__ import annotations
from abc import abstractmethod
from math import tau, pi, sqrt
from typing import Union

import numpy as np


def normalize_t(t): return t % tau


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


class Vector2D:
    """
    A 2-dimensional vector.

    A vector in a 2-dimensional space that can be expressed in cartesian or polar form. It can be instantiated with
    its x and y coordinates (cartesian form) or with its length and orientation (polar form).

    Args:
        x: The x coordinate of the vector (cartesian form).
        y: The y coordinate of the vector (cartesian form).
        r: The length of the vector (polar form).
        t: The orientation of the vector, in radians (polar form).
    """

    def __new__(cls, x=None, y=None, r=None, t=None):
        if cls is Vector2D:
            assert ((x is not None and y is not None) or (r is not None and t is not None))
            if x is not None and y is not None:
                return Vector2DCartesian(x, y)
            elif r is not None and t is not None:
                return Vector2DPolar(r, t)
        else:
            return object.__new__(cls)

    @abstractmethod
    def __eq__(self, other) -> bool:
        """
        Compares equality in two 2-dimensional vectors.

        Returns True if the attributes of `self` and `other` are the same when expressed in the current form of `self`.

        Args:
            other: A `Vector2D` to compare with.

        Returns:
            A `bool` value expressing equality between the vectors.
        """
        pass

    @abstractmethod
    def length(self) -> float:
        """
        Returns the magnitude of the vector.

        Returns:
            A `float` value corresponding to the magnitude of the vector.
        """
        pass

    @abstractmethod
    def __neg__(self) -> Vector2D:
        """
        Negates the vector.

        Returns the `Vector2D` of same length than `self` but of opposite direction.

        Returns:
            A `Vector2DCartesian` with both components negated or a `Vector2DPolar` with opposite direction and
        same magnitude.

        """
        pass

    @abstractmethod
    def __add__(self, other: Union[Vector2D, Point2D]) -> Union[Vector2D, Point2D]:
        """
        Adds a vector to a point or another one.

        If `other` is a `Vector2D`, returns the sum with `self`, a `Vector2D`. If `other` is a `Point2D`, returns its
        displacement point by `self`, a `Point2D`.

        Args:
            other: A `Point2D` or `Vector2D` to be added to `self`.

        Returns:
            Either the sum of `self` and `other` (`Vector2D`) or the displacement of `other` by `self` (`Point2D`).

        Raises:
            TypeError: If `other` is not a `Point2D` or `Vector2D`.
        """
        pass

    @abstractmethod
    def __sub__(self, other: Vector2D) -> Vector2D:
        """
        Substracts a vector to another one.

        Substracts `other`, a `Vector2D`, to `self`.

        Args:
            other: A `Vector2D` to be substracted to `self`.

        Returns:
            The substraction of `self` and `other`.

        Raises:
            TypeError: If `other` is not a `Vector2D`.

        """
        pass

    @abstractmethod
    def __mul__(self, other) -> Vector2D:
        """
        Multiplies a vector by a scalar.

        Multiplies the magnitude of the vector `self` by `other`, a scalar, while mantaining its original orientation.

        Args:
            other: A scalar to multiply `self` by.

        Returns:
            A `Vector2D` of same orientation than `self` but magnitude proportional to `other`.

        Raises:
            TypeError: If `other` is not a scalar.
        """
        pass

    @abstractmethod
    def __truediv__(self, other):
        """
        Divides the magnitude of the vector `self` by `other`, a scalar, while mantaining its original orientation.
        Args:
            other: A scalar to divide `self` by.

        Returns:
            A `Vector2D` of same orientation than `self` but magnitude divided to `other`.

        Raises:
            TypeError: If `other` is not a scalar.
        """
        pass

    def __radd__(self, other): return self + other

    def __rsub__(self, other): return (-self) + other

    def __rmul__(self, other): return self * other

    @abstractmethod
    def to_cartesian(self) -> Vector2DCartesian:
        """
        Changes the vector to cartesian form.

        Returns:
            An equivalent vector to `self` in cartesian form (`Vector2DCartesian`).
        """
        pass

    @abstractmethod
    def to_polar(self) -> Vector2DPolar:
        """
        Changes the vector to polar form.

        Returns:
            An equivalent vector to `self` in polar form (`Vector2DPolar`).
        """
        pass

    @abstractmethod
    def angle_with(self, other) -> float:
        """
        Computes the angle between `self` and `other`.

        Returns the value of the smallest angle formed by `self` and `other`, another `Vector2D`, in radians.

        Args:
            other: A `Vector2D` to compute the angle with.

        Returns:
            The value in radians of the smallest angle formed by `self` and `other`.

        Raises:
            TypeError: If `other` is not a `Vector2D`.
        """
        pass

    @abstractmethod
    def unit(self):
        """
        Returns the unit vector of same orientation as `self`.

        Returns the unit vector, a `Vector2D`, of same orientation as `self`. When `self` has magnitude 0 in cartesian
        form, it returns `self`.

        Returns:
            A `Vector2D` of same orientation as `self` but magnitude 1.
        """
        pass

    @abstractmethod
    def rotate(self, angle: float) -> Vector2D:
        """Rotates the vector by `angle` radians

        Returns a `Vector2D` of same magnitud than `self` but rotated counter-clockwise by `angle` radians.

        Returns:
            A `Vector2D` of same magnitude as `self` rotated counter-clockwise `angle` radians.
        """

    def __setattr__(self, key, value):
        raise TypeError('Vector2 object is immutable')

    @abstractmethod
    def __str__(self) -> str: pass
    @abstractmethod
    def __repr__(self) -> str: pass


class Vector2DCartesian(Vector2D):

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        super().__init__()
        assert np.isreal(x)
        assert np.isreal(y)
        object.__setattr__(self, 'x', x)
        object.__setattr__(self, 'y', y)

    def to_cartesian(self) -> Vector2DCartesian: return self

    def to_polar(self) -> Vector2DPolar: return Vector2DPolar(self.length(), np.arctan2(self.y, self.x))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2D):
            return False
        other = other.to_cartesian()
        return self.x == other.x and self.y == other.y

    def length(self) -> float: return sqrt(self.x*self.x + self.y*self.y)

    def __neg__(self): return Vector2DCartesian(-self.x, -self.y)

    def __add__(self, other: Union[Vector2D, Point2D]) -> Union[Vector2DCartesian, Point2D]:
        if isinstance(other, Point2D):
            return other + self
        if not isinstance(other, Vector2D):
            raise TypeError('Vector2D can only be added by a Point2D or another Vector2D.')
        if isinstance(other, Vector2DPolar):
            other = other.to_cartesian()
        return Vector2DCartesian(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        if not isinstance(other, Vector2D):
            raise TypeError('Vector2D can only be substracted by another Vector2D.')
        if isinstance(other, Vector2DPolar):
            other = other.to_cartesian()
        return Vector2DCartesian(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> Vector2DCartesian:
        if not np.isreal(other):
            raise TypeError('Vector2D can only be multiplied by a scalar.')
        if other == 0:
            return Vector2D(x=0, y=0)
        return Vector2DCartesian(self.x*other, self.y*other)

    def __truediv__(self, other) -> Vector2DCartesian:
        if not np.isreal(other):
            raise TypeError('Vector2D can only be divided by a scalar.')
        if other == 0:
            raise ZeroDivisionError
        return Vector2DCartesian(self.x/other, self.y/other)

    def angle_with(self, other):
        if not np.isreal(other):
            raise TypeError('Argument must be a Vector2D.')
        return self.to_polar().angle_with(other)

    def unit(self): return (self / self.length()) if self.length() != 0 else self

    def rotate(self, angle:float) -> Vector2D:
        if normalize_t(angle) == 0:
            return self
        if normalize_t(angle) == pi/2:
            return Vector2DCartesian(-self.y, self.x)
        if normalize_t(angle) == pi:
            return -self
        if normalize_t(angle) == 3*pi/2:
            return Vector2DCartesian(self.y, -self.x)
        return self.to_polar().rotate(angle)

    def __repr__(self): return f'<{self.x:.2f},{self.y:.2f}>'

    def __str__(self): return self.__repr__()


class Vector2DPolar(Vector2D):

    __slots__ = ['r', 't']

    def __init__(self, r, t):
        super().__init__()
        assert np.isreal(r)
        assert np.isreal(t)
        assert r >= 0
        object.__setattr__(self, 'r', r)
        object.__setattr__(self, 't', normalize_t(t) if r != 0 else 0)

    def to_cartesian(self) -> Vector2DCartesian:
        return Vector2DCartesian(self.r * np.cos(self.t), self.r * np.sin(self.t))

    def to_polar(self) -> Vector2DPolar: return self

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2D):
            return False
        other = other.to_polar()
        return self.r == other.r and self.t == other.t

    def length(self) -> float: return self.r

    def __neg__(self): return Vector2DPolar(self.r, normalize_t(self.t+pi))

    def __add__(self, other: Union[Vector2D, Point2D]) -> Union[Vector2D, Point2D]:
        if isinstance(other, Point2D):
            return other + self
        if not isinstance(other, Vector2D):
            raise TypeError('Vector2D can only be added by a Point2D or another Vector2D.')
        if isinstance(other, Vector2DPolar) and self.t == other.t:
            return Vector2DPolar(self.r + other.r, self.t)
        return self.to_cartesian() + other.to_cartesian()

    def __sub__(self, other: Vector2D) -> Vector2D:
        if not isinstance(other, Vector2D):
            raise TypeError('Vector2D can only be substracted by another Vector2D.')
        if isinstance(other, Vector2DPolar) and self.t == other.t:
            return Vector2DPolar(self.r - other.r, self.t) \
                if self.r >= other.r \
                else Vector2DPolar(other.r - self.r, normalize_t(self.t+pi))
        return self.to_cartesian() - other.to_cartesian()

    def __mul__(self, other) -> Vector2D:
        if not np.isreal(other):
            raise TypeError('Vector2D can only be multiplied by a scalar.')
        if other == 0:
            return Vector2D(x=0, y=0)
        return Vector2DPolar(self.r*other, self.t)

    def __truediv__(self, other) -> Vector2DPolar:
        if not np.isreal(other):
            raise TypeError('Vector2D can only be divided by a scalar.')
        if other == 0:
            raise ZeroDivisionError
        return Vector2DPolar(self.r/other, self.t)

    def angle_with(self, other):
        if not np.isreal(other):
            raise TypeError('Argument must be a Vector2D.')
        if isinstance(other, Vector2DCartesian):
            other = other.to_polar()
        return min(normalize_t(self.t-other.t), normalize_t(other.t-self.t))

    def unit(self): return Vector2DPolar(1, self.t)

    def rotate(self, angle: float): return Vector2DPolar(self.r, normalize_t(self.t + angle))

    def __repr__(self): return f'<{self.r:.2f}, {self.t:.2f} rad>'

    def __str__(self): return self.__repr__()