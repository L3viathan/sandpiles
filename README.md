# Sandpile arithmetics

This code implements sandpile arithmetics as seen in
[this Numberphile video](https://www.youtube.com/watch?v=1MtEUErz7Gg).

## Usage

Construct a sandpile:

    >>> from sandpiles import Sandpile, null3x3
    >>> Sandpile([9,9,9], [9,9,9], [9,9,9])
    Sandpile([1, 3, 1], [3, 1, 3], [1, 3, 1])

Get the order and inverse. For this, you'll need to have the identity
element, which is included for the 2x2, 3x3, or 4x4 grids.

    >>> Sandpile([9,9,9], [9,9,9], [9,9,9]).order(null3x3)
    16
    >>> Sandpile([9,9,9], [9,9,9], [9,9,9]).inverse(null3x3)
    Sandpile([3, 2, 3], [2, 3, 2], [3, 2, 3])

Test if an element is in S:

    >>> from sandpiles import S3x3
    >>> Sandpile([9,9,9], [9,9,9], [9,9,9]) in S
    True
    >>> Sandpile([0,0,0], [0,0,0], [0,0,0]) in S
    False

Inspect the toppling process:

    >>> s = Sandpile([1,2,3], [2,3,4], [4,3,2], topple=False)
    >>> s.topple()
    ┏━━━━━━━┓
    ┃ 1 2 3 ┃
    ┃ 2 3 4 ┃
    ┃ 4 3 2 ┃
    ┗━━━━━━━┛
    ┏━━━━━━━┓
    ┃ 1 2 4 ┃
    ┃ 3 5 1 ┃
    ┃ 1 1 0 ┃
    ┗━━━━━━━┛
    ┏━━━━━━━┓
    ┃ 1 4 0 ┃
    ┃ 4 1 3 ┃
    ┃ 1 2 0 ┃
    ┗━━━━━━━┛
    ┏━━━━━━━┓
    ┃ 3 0 1 ┃
    ┃ 0 3 3 ┃
    ┃ 2 2 0 ┃
    ┗━━━━━━━┛

Get order frequencies of all elements in S (uses `nested_loop` from
[toolib](https://github.com/L3viathan/toolib)):

    >>> from sandpiles import Sandpile, null3x3, S3x3
    >>> from collections import Counter
    >>> from toolib.tools import nested_loop
    >>> for a,b,c,d,e,f,g,h,i in nested_loop(9, 4):
    ...     x = Sandpile([a,b,c],[d,e,f],[g,h,i])
    ...     if x not in S3x3:
    ...         continue
    ...     o = x.order(null3x3)
    ...     orders[o] += 1
    >>> orders
    Counter({224: 49152, 112: 36864, 56: 9216, 28: 2688, 32: 1024, 16: 768, 14: 336, 8: 192, 4: 56, 7: 48, 2: 7, 1: 1})
