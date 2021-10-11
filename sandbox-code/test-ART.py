

from math import inf, sqrt
from random import choice, randint, uniform


# distance measures------------------------------
def euclidean(X, Y):
    return sqrt(sum([(x-y)**2.0 for x,y in zip(X,Y)]))

# generate random values-------------------------

def rreals(lb: float, ub: float):
    
    while True:
        yield uniform(lb, ub)

def rnaturals(lb: int, ub: int):

    while True:
        yield randint(lb, ub)

def domain(*dms):
    while True:
        yield tuple(next(dm) for dm in dms)

# the problem------------------------------------

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

# -----------------------------------------------

# this isn't quite how it done. This only generates the test arguments, it doesn't do the testing like
#   in the paper.

# this produces a diversity of results, … what about a max_distance? precondition? postcondition?

def ART(case, fn, domain, n_cases=100, min_distance=5.0, distance=euclidean, max_num_candidates=1_000):

    # the stopping criterian, number of cases or too much effort
    stop = lambda i: False if (len(cases) <= n_cases) or (max_num_candidates <= ntests_generated) else True

    cases = [case]
        
    ntests_generated: int = 0

    while not stop(ntests_generated):

        cʹ = next(domain)
        ntests_generated += 1           

        if distance(case, cʹ) >= min_distance:
            cases.append(cʹ)
            case = cʹ                                       # this is what the paper does, improves diversity?

            # test the function
            try:
                print('[PASSED]\t', case, '\t', fn(*case))
            except AssertionError as e:
                print('[FAILED]\t', case, '\t', e)

    return cases

# =========================================================

D = domain(rnaturals(-1, 100), rnaturals(-1, 100), rnaturals(-1, 100))

c = ART((50, 50, 50),
        commission,
        D,
        100,
        5.0)

print('―'*25)