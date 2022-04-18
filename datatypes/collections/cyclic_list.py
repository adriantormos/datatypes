import math
from collections import UserList


class CyclicList(UserList):
    """
    A list that allows indices greater than its length by looping.

    A class that maintains the behavior of the base list while removing IndexError by looping the list when needed.
    When trying to access an index greater that the length of the list, it loops back to the start of the list
    analogously to negative indices.
    """
    def __init__(self, x):
        super().__init__(x)

    def __setitem__(self, key, value):
        """
        Sets `self[key]` to value.

        Sets the element `key` to `value`. If `key` is greater than `len(self)`, the element of the index modulo the
        length of the list (`key % len(self)`) is set to `value`. Otherwise (including slices as indices), it has the
        same behavior as a normal list.

        Args:
            key:
            value:

        """
        if isinstance(key, slice):
            self.data[key] = value
        elif key >= 0 and len(self) > 0:
            self.data[key % len(self)] = value
        else:
            self.data[key] = value

    def __getitem__(self, item):
        """
        Returns `self[item]`, accounting for looping.

        When `item` is an integer larger than the length of the list, it returns the element in position
        `item % len(self)`. For the rest of integers it has the same behavior as a regular list. When `item` is a
        slice, the start of the list will be concatenated after its end even resulting in a larger list than the
        original. The start and stops of the slice correspond to their value modulo `len(self)`.

        Args:
            item:

        Returns:
            A CyclicList, cycling if needed, if `item` is a slice. If `item` is an integer, it returns the
            corresponding element from the list.

        """
        if isinstance(item, slice):
            start = 0 if item.start is None else item.start
            stop = (len(self) if item.stop is None else item.stop) - 1
            if start > stop:
                return CyclicList([])
            list_for_start = math.floor(start / len(self))
            list_for_stop = math.floor(stop / len(self))
            if list_for_stop == list_for_start:
                return CyclicList(
                    (self.data[start % len(self):stop % len(self)] + [self.data[stop % len(self)]])[::item.step]
                )
            entire_lists = max(0, list_for_stop - list_for_start - 1)
            return CyclicList(
                (self.data[start % len(self):]
                 + entire_lists * self.data
                 + self.data[:stop % len(self)]
                 + [self.data[stop % len(self)]]
                 )[::item.step]
            )
        if item >= 0 and len(self) > 0:
            return self.data[item % len(self)]
        return self.data[item]

    def __delitem__(self, key):
        """
        Deletes `self[key]`.

        Removes the element in position `key` from the list. If `key` is an integer bigger than `len(self)`, the
        element `key % len(self)` is deleted. In any other case, it has the same behavior as a regular list.

        Args:
            key:

        """
        if isinstance(key, slice):
            del self.data[key]
        elif key >= 0 and len(self) > 0:
            del self.data[key % len(self)]
        else:
            del self.data[key]

    def __iter__(self):
        return self.data.__iter__()
