import warnings
from collections import namedtuple
from enum import Enum
from functools import wraps
from typing import Union

PREDICATES = dict()
SUPRESS_PREDICATE_WARN = False       # Don't show if it has been found already

# Value = namedtuple('Value', 'name,symbol,is_symbolic,is_error,is_group,only_values,doc_error,error_message')
Predicate = namedtuple('Predicate', 'name,symbol,is_symbolic,is_error,is_group,only_values,doc_error,error_message')
#     name: str              the name of the predicate
#     symbol: str            uses a binary symbol, x < y
#     is_symbolic: bool
#     is_group: bool          operates in an aggregate group
#     only_values: bool       I DON'T KNOW OR WHY IT IS THERE
#     doc_error: str          Use the doc string as an error message
#     error_message: str      the actual message


# help from: https://realpython.com/primer-on-python-decorators/
# TODO: add arg analysis to predicate, ie breakdown of args
#		if error, wrap and return ([Error|None], [True|False])

# TODO: change all the names & stuff to PredicateFn
#       change Value to Predicate

NullString = Union[None, str]

# note: is_error implies calls should be expanded, ie fn(f, args)
#       is_group implies tests should be in the aggregate
#       only_values implies ... something ...

# TODO: make is_error => make_callable

def predicate(_fn=None, *, alias=None, symbol: NullString = None, is_error: bool = False,
              is_group: bool = False, only_values=False, doc_error: bool = False):
    """Function decorator to define predicates for Falcon."""

    # @wraps()
    def function(func):

        is_symbolic = True if symbol is not None else False

        values = Predicate(func.__name__, symbol, is_symbolic, is_error, is_group, only_values, doc_error, func.__doc__)

        if isinstance(alias, (list, tuple)):
            for name in alias:

                if SUPRESS_PREDICATE_WARN and name in PREDICATES:
                    warnings.warn(f"Name {name} was previously defined. Replacing existing.")

                PREDICATES[name] = values

        elif alias:

            if SUPRESS_PREDICATE_WARN and alias in PREDICATES:
                    warnings.warn(f"Name {alias} was previously defined. Replacing existing.")

            PREDICATES[alias] = values

        PREDICATES[func.__name__] = values

        return func

    return function if _fn is None else function(_fn)

# -----------------------------------------------
# better name? no_fail, pure, bool_pure, pure_predicate ???


def on_fail_false(fn) -> bool:
    """Decorator to wrap a predicate, ensure that it *only* returns a Boolean, even in the case of failure."""

    @wraps(fn)
    def call_fn(*args, **kwargs):
        """Decorates a predicate. If the predicate fails, it returns False"""

        try:
            result = fn(*args, **kwargs)
        except Exception as error:
            result = False

        return result

    return call_fn


# -----------------------------------------------
# for future use. Rather than a predicate returning a boolean, it returns a tribool/trit

# Disposition = Enum('Disposition', 'true,false,failure')


# def disposition(fn) -> Disposition:
#     """Decorator to wrap a predicate, ensure that it *only* returns true, false, or failure."""
#
#     @wraps(fn)
#     def call_fn(*args, **kwargs):
#         """Decorates a predicate. If the predicate fails, it returns False"""
#
#         try:
#             outcome = fn(*args, **kwargs)
#             result = Disposition.true if outcome else Disposition.false
#         except:
#             result = Disposition.failure
#
#         return result
#     return call_fn
