from enum import Enum

Triangle = Enum('Triangle', 'equilateral, isosceles, scalene, not_triangle')


class TriangleError(Exception):
    pass


def classify(a: int, b: int, c: int) -> Triangle:

    is_triangle = lambda a_,b_,c_: (a < b+c) and (b < a+c) and (c < a+b)
    integers    = lambda a_,b_,c_: isinstance(a_, int) and isinstance(b_, int) and isinstance(c_, int)
    is_valid    = lambda a_,b_,c_: (a_ > 0) and (b_ > 0) and (c_ > 0)

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