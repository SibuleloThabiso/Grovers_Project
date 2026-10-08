"""
Classical linear search with comparison counting.

Corresponds to Section 2.1 of the proposal: worst-case O(N) comparisons.
"""


def linear_search(search_space, target):
    """
    Perform a classical linear search.

    Args:
        search_space: list of elements to search.
        target: element to find.

    Returns:
        (index, comparisons): index of target (-1 if not found)
                             and number of comparisons performed.
    """
    comparisons = 0
    for i, element in enumerate(search_space):
        comparisons += 1
        if element == target:
            return i, comparisons
    return -1, comparisons


def worst_case_comparisons(N):
    """
    For an N-element search space with the target at the last position,
    the worst-case number of comparisons is exactly N.
    """
    return N


if __name__ == "__main__":
    # Quick self-test
    space = list(range(16))
    target = 15  # worst case
    idx, comps = linear_search(space, target)
    print(f"Target {target} found at index {idx} after {comps} comparisons.")
    assert comps == 16
    print("Classical search OK.")