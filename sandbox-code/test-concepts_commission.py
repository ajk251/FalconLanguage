
from collections import defaultdict, namedtuple
from itertools import product
from operator import eq, ne
from random import randint

# -----------------------------------------------------------------------------
# This project comes from Software Testing: A craftsman's approach. It is the lock, 
# stock, and barrels problem. I assume the the calculation isn't trival for the 
# purposes of testing it, ie calculate(x,y,z) == test_caclulation(x,y,z) isn't
# feasible.

# The challenge with this is how to test it. It returns a float. Either test by 
# enumerating assertions or over a domain and analyse the results.

# -----------------------------------------------------------------------------
# right from the problem
# should this return sales too? (100, 10), (7800, 1420)

def commission(nlocks: int, nstocks: int, nbarrels: int) -> float:

    inner = lambda xs,ys: sum(x*y for x,y in zip(xs,ys))

    assert nlocks <= 70,   'Exceeded lock sales inventory'
    assert nstocks <= 80,  'Exceeded stock sales inventory'
    assert nbarrels <= 90, 'Exceeded barrels sales inventory'

    assert nlocks >= 1,   'Must sell more than 1 lock'
    assert nstocks >= 1,  'Must sell more than 1 stock'
    assert nbarrels >= 1, 'Must sell more than 1 barrel'
    
    # the costs
    lock   = 45
    stock  = 30
    barrel = 25

    # sales = lock * nlocks + stocks * nstocks + nbarrels * barrel
    sales = inner([lock, stock, barrel], [nlocks, nstocks, nbarrels])

    if sales > 1800:
        commission = inner([.1, .15, .2], [1_000, 800, (sales-1_800)])
    elif sales > 1000:
        commission = inner([.1, .15], [1_000, (sales-1_000)])
    else:
        commission = 0.1 * sales

    return commission

# -----------------------------------------------------------------------------

TestCase = namedtuple('TestCase', 'predicate, test_value, test_solution')

# for the groupby
TestValue = namedtuple('TestValue', 'label, test_fn, rvalue')                    # ie < 4, Test(lt, 4) is  lt(_, 4) ⇔ _<4, implicitly True
TestPredicate = namedtuple('TestPredicate', 'label, predicate, test_fn')

#-----------------------

def satisfies_predicate(predicate, value):
    return predicate(*value) == True

def doesnt_satisfy_predicate(predicate, value):
    return predicate(*value) == False

def raises_error(fn, args, error_kind):
    
    try:
        _ = fn(*args)
    except error_kind as e:
        return True
    except Exception as e:
        return False
    
    return False

def is_all(sequence, predicate, test_value):

    if isinstance(predicate, str):
        predicate = Predicates[predicate]

    # ⊤ ∀ v ∈ S
    return all(predicate(value, test_value) for value in sequence)

def is_all_over(sequence, predicate, test_fn):

    if isinstance(predicate, str):
        predicate = Predicates[predicate]

    return all(predicate(test_fn, args) for args in sequence)

# to use symbols rather than functions
Predicates = {'=': eq,
              '==': lambda v,t: isinstance(v, type(t)) and eq(v, t),                # assert type and value
              '≠': ne,
              '!': raises_error,
              '⊧': 'satisfies_predicate', # invoke call
              '⊤': True,
              '⊥': False}

#-----------------------

# test by enumeration
def test(function, cases):

    strong_equality = lambda v,t: isinstance(v, type(t)) and eq(v, t)

    for case in cases:
        
        # this is what the tests would look like
        print(f'assert {function.__name__}{case.test_value} {case.predicate} {case.test_solution}', end='')

        # actual tests & handle special cases
        if case.predicate == '!':
            raises_error(function, case.test_value, case.test_solution)
            # continue
        else:
            assert Predicates[case.predicate](function(*case.test_value), case.test_solution), f'Assertion case {case.test_value} failed'
        
        # print('== : ', strong_equality(function(*case.test_value), case.test_solution))
        # print('  ', function(*case.test_value), case.test_solution)
        
        print('\t[PASSED]')


    print()

TestSatisfies = namedtuple('TestSatisfies', 'label, predicate')

def satisfies(fn, domain, test_cases):

    groups = {case.label: [] for case in test_cases}

    for args in domain:

        try:
            result = fn(*args)
        except Exception as e:
            result = e
        
        for case in test_cases:
            
            # this is ugly, but it can't test the predicate without raising an error for fail cases
            try:
                if case.predicate(result):
                    groups[case.label].append((result, args))
            except Exception as e:
                continue

            # need way to count how many 'result' belongs too

    # for case, result in groups.items():
    #     print(case, result)
    # print('Error: ', groups['error-too-few'])
    # print('Error: ', groups['error-too-many'])


# =============================================================================


# method 1
# Test commission (locks ⨯ stocks ⨯ barrels):
#   | <1,1,1>    == 10.0
#   | <70,80,90> == 1420.0

test(commission, [TestCase('=',  (1,1,1), 10),                               # type & value --> it fails too!
                  TestCase('==', (1,1,2), 12.5),                             # value, ie 3=3.0
                  TestCase('==', (70,80,90), 1420.0),
                  TestCase('!',  (100, 100, 100), AssertionError),
                  TestCase('!',  (1,1,0), AssertionError)])

# ------------------------------------------

locks   = [0, 1, 5, 10, 50, 70, 71] + [randint(0, 100) for _ in range(25)]
stocks  = [0, 1, 5, 10, 50, 80, 81] + [randint(0, 100) for _ in range(25)]
barrels = [0, 1, 5, 10, 50, 90, 91] + [randint(0, 100) for _ in range(25)]

strong_equality     = lambda v,t: isinstance(v, type(t)) and eq(v, t)
is_float            = lambda v: isinstance(v, float)
is_gt0              = lambda v: v > 0
is_too_many_error   = lambda e: isinstance(e, AssertionError) and e.args[0].startswith('Exceeded')
is_too_few_error    = lambda e: isinstance(e, AssertionError) and e.args[0].startswith('Must')


# Satisfies commission (locks ⨯ stocks ⨯ barrels):
#   | is-float    is_float
#   | is-gt-0     is_gt0
#   | is-too-few  is_too_few_error
#   | is-too-many is_too_many_error

satisfies(commission, product(locks, stocks, barrels), [TestSatisfies('is-float', is_float),
                                                        TestSatisfies('is-gt0', is_gt0),
                                                        TestSatisfies('error-too-few', is_too_few_error),
                                                        TestSatisfies('error-too-many', is_too_many_error)])


try:
    c = commission(0, 10, 100)
except Exception as e:
    print(is_too_many_error(e), e.args[0], e.args[0].startswith('Exceeded'))

try:
    c = commission(0, 10, 10)
except Exception as e:
    print('is too many: ', is_too_many_error(e))
    print('is too few:  ', is_too_few_error(e))