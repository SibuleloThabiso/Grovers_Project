import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.classical_search import linear_search


def test_found_first():
    assert linear_search([5, 1, 2], 5) == (0, 1)


def test_found_last_worst_case():
    space = list(range(16))
    idx, comps = linear_search(space, 15)
    assert idx == 15
    assert comps == 16


def test_not_found():
    _, comps = linear_search([1, 2, 3], 99)
    assert comps == 3