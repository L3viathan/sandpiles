"""
Sandpile arithmetics.

The Sandpile class is used to construct a sandpile grid.

S2x2, S3x3, S4x4 is a virtual set that elements can be checked to be contained in.
null2x2, null3x3, and null4x4 are the identity elements of the respective size.
"""
from itertools import zip_longest

__all__ = ['Sandpile', 'S2x2', 'S3x3', 'S4x4', 'null2x2', 'null3x3', 'null4x4']

class Sandpile(object):
    """A sandpile grid"""
    TL = '┏'
    V = '┃'
    TR = '┓'
    BL = '┗'
    BR = '┛'
    H = '━'
    null_cache = None
    def __init__(self, *args, topple=True):
        """
        Initializes a sandpile grid from its arguments.

        The values are automatically toppled, unless the keyword argument
        topple=False is provided.

        >>> Sandpile([9,9,9], [9,9,9], [9,9,9])
        Sandpile([1, 3, 1], [3, 1, 3], [1, 3, 1])

        >>> Sandpile([9,9,9], [9,9,9], [9,9,9], topple=False)
        Sandpile([9, 9, 9], [9, 9, 9], [9, 9, 9])

        """
        self.num_of_cols = None
        array = []
        for row in args:
            array.append([])
            for col in row:
                array[-1].append(col)
            if self.num_of_cols is None:
                self.num_of_cols = len(array[-1])
            elif self.num_of_cols != len(array[-1]):
                raise ValueError("All rows must have the same amount of values")
        self.data = array
        if topple:
            self.topple(verbose=False)

    def __str__(self):
        """Printing a sandpile grid leads to fancy display"""
        return '{tl}{h}{tr}\n{lines}\n{bl}{h}{br}'.format(
            tl=Sandpile.TL,
            tr=Sandpile.TR,
            bl=Sandpile.BL,
            br=Sandpile.BR,
            h=Sandpile.H*(2*self.num_of_cols+1),
            lines='\n'.join(
                '{v} {cols} {v}'.format(
                    v=Sandpile.V,
                    cols=' '.join(str(col) for col in row)
                )
                for row in self.data
            )
        )

    def __repr__(self):
        return "Sandpile({})".format(", ".join(map(repr, self.data)))

    def __add__(self, other):
        """Add two sandpiles or a sandpile to a list of int lists"""
        if not isinstance(other, Sandpile):
            if isinstance(other, list):
                other = Sandpile(*other)
            else:
                raise RuntimeError("Can't add sandpiles to other things.")
        elif len(self.data) != len(other.data) or self.num_of_cols != other.num_of_cols:
            raise RuntimeError("Can't add sandpiles with different dimensions.")
        def add(x, y):
            for xr, yr in zip(x, y):
                yield map((lambda X: X[0]+X[1]), zip(xr,yr))
        return Sandpile(*add(self.data, other.data))
    __radd__ = __add__

    def topple(self, verbose=True):
        """Topple a sandpile grid. By default, prints intermediary states."""
        if verbose:
            print(self)
        while True:
            changed=False
            for row in range(len(self.data)):
                for col in range(self.num_of_cols):
                    if self.data[row][col] > 3:
                        changed = True
                        self.data[row][col] -= 4
                        if row > 0:
                            self.data[row-1][col] += 1
                        if row < len(self.data)-1:
                            self.data[row+1][col] += 1
                        if col > 0:
                            self.data[row][col-1] += 1
                        if col < self.num_of_cols-1:
                            self.data[row][col+1] += 1
            if not changed:
                break
            if verbose:
                print(self)

    def __eq__(self, other):
        """
        Test for equality.

        A sandpile is equal to another sandpile if its values are equal.
        A sandpile is equal to a list l if it is equal to Sandpile(*l).
        """
        if not isinstance(other, Sandpile):
            if isinstance(other, list):
                other = Sandpile(*other)
            else:
                raise RuntimeError("Can't compare sandpiles to other things.")
        for xr, yr in zip_longest(self.data, other.data):
            for xc, yc in zip_longest(xr, yr):
                if xc != yc:
                    return False
        return True

    def order(self, identity):
        """
        Return the order of the sandpile grid, given the identity (null) element.

        This is the integer n such that self * n == identity.
        """
        x = self
        value = 1
        while True:
            if x == identity:
                return value
            value += 1
            x += self

    def inverse(self, identity):
        """
        Return the inverse of the sandpile grid, given the identity (null) element.

        This is the sandpile grid g such that g + self == identity.
        """
        x = self
        while True:
            y = x + self
            if y == identity:
                return x
            x = y

null4x4 = Sandpile([2,1,1,2], [1,0,0,1], [1,0,0,1], [2,1,1,2])
null3x3 = Sandpile([2,1,2], [1,0,1], [2,1,2])
null2x2 = Sandpile([2,2], [2,2])

class SandpileSetS(object):
    """
    For a given identity, construct an object that, given an element x,
    returns True iff x + identity == x, i.e. if it is in S.
    """
    def __init__(self, null):
        self.null = null
    def __contains__(self, other):
        return self.null + other == other

S4x4 = SandpileSetS(null4x4)
S3x3 = SandpileSetS(null3x3)
S2x2 = SandpileSetS(null2x2)
