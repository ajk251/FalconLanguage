
from enum import Enum

from hypothesis import given
from hypothesis.strategies import integers

# from domains.domains import domain
# from predicates.predicates import predicate, onfail_false


# this is for Hypothesis and PyTest =======================

Triangle = Enum('Triangle', 'equilateral, isosceles, scalene, not_triangle')


class TriangleError(Exception):
    pass


def classify(a: int, b: int, c: int) -> Triangle:

    is_triangle = lambda a,b,c: (a < b+c) and (b < a+c) and (c < a+b)
    integers    = lambda a,b,c: isinstance(a, int) and isinstance(b, int) and isinstance(c, int)
    is_valid    = lambda a,b,c: (a > 0) and (b > 0) and (c > 0)

    assert integers(a, b, c), "All values must be integers"

    if not is_triangle(a, b, c): # and not is_valid(a, b, c):
        # print('sides too short ', end='')
        return Triangle.not_triangle
    elif not is_valid(a, b, c):
        # print('not a valid triangle ', end='')
        return Triangle.not_triangle
    elif a == b and b == c:
        return Triangle.equilateral
    elif a != b and b != c and c != a:
        return Triangle.scalene
    elif a == b or b == c or a == c:
        return Triangle.isosceles

    raise TriangleError(f'Could not classify input a ￫ {a}, b ￫ {b}, c ￫ {c}')


# Hypothesis tests -----------------------------------

@given(side_a=integers(), side_b=integers(), side_c=integers())
def test_classify(side_a: int, side_b: int, side_c: int):

    is_triangle = lambda a,b,c: (a < b+c) and (b < a+c) and (c < a+b)
    integers    = lambda a,b,c: isinstance(a, int) and isinstance(b, int) and isinstance(c, int)
    is_valid    = lambda a,b,c: (a > 0) and (b > 0) and (c > 0)

    sides = frozenset((side_a, side_b, side_c))             # a set only holds unquie items

    all_equal = lambda sides_: len(sides_) == 1
    two_equal = lambda sides_: len(sides_) == 2
    all_diff  = lambda sides_: len(sides_) == 3

    kind = classify(side_a, side_b, side_c)

    if (not is_triangle(side_a, side_b, side_c)) or (not is_valid(side_a, side_b, side_c)) or (not integers(side_a, side_b, side_c)):
        assert kind == Triangle.not_triangle
    elif all_equal(sides):
        assert kind == Triangle.equilateral
    elif all_diff(sides):
        assert kind == Triangle.scalene
    elif two_equal(sides):
        assert kind == Triangle.isosceles

    print(side_a, side_b, side_c)

# generate n triangle, then test all the properties
if kind == '':
    all_

if __name__ == "__main__":
    test_classify()