"""
=====================================================
UNIT 5 DISCUSSION: SEARCH ALGORITHMS (LINEAR vs BINARY)
=====================================================

INSTRUCTIONS:
In this assignment, you will implement and analyze two
fundamental search algorithms: linear search and binary search.

You will demonstrate your understanding by modifying the
provided code, running experiments on different dataset sizes,
and clearly explaining your results through code comments
and program output.
"""

import time


def linear_search(lst, target, trace=None):
    """
    TODO (Student):
    Implement a linear search algorithm.

    Requirements:
    - Search the list from beginning to end.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining why linear search
      has O(n) time complexity.

    Student addition: if a list is passed as `trace`, every index the
    search compares against is appended to it. This lets main() count
    comparisons without changing the return value.
    """
    # Check each position in order, starting at index 0.
    # Linear search has no way to skip anything: an item it hasn't looked at
    # could be the target, so in the worst case (target is last or missing)
    # it compares against all n items. The work grows in direct proportion
    # to the size of the list, which is why it is O(n).
    # It also doesn't care whether the list is sorted.
    for index in range(len(lst)):
        if trace is not None:
            trace.append(index)
        if lst[index] == target:
            return index  # Found it; stop early (best case is O(1)).
    return -1  # Checked every item and never found the target.


def binary_search(lst, target, trace=None):
    """
    TODO (Student):
    Implement a binary search algorithm.

    Requirements:
    - Assume the list is already sorted.
    - Repeatedly reduce the search space by half.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining how each iteration
      reduces the search space.

    Student addition: `trace` works the same way as in linear_search,
    recording the middle index checked on each iteration.
    """
    # low and high mark the part of the list that could still hold the target.
    # At the start, that is the whole list.
    low = 0
    high = len(lst) - 1

    # An empty list makes high = -1, so the loop never runs and we return -1.
    while low <= high:
        mid = (low + high) // 2  # Middle of the remaining search space.
        if trace is not None:
            trace.append(mid)

        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            # The list is sorted, so everything at or left of mid is too small.
            # Throw away that whole left half and keep searching the right half.
            low = mid + 1
        else:
            # lst[mid] is too big, so everything at or right of mid is too big.
            # Throw away the right half and keep searching the left half.
            high = mid - 1

        # Each pass removes about half of what was left:
        # n -> n/2 -> n/4 -> ... -> 1. That takes about log2(n) passes,
        # which is why binary search is O(log n).

    # low passed high, so the search space is empty and the target isn't here.
    return -1


# ---------------------------------------------------------------------
# Student-added data and helpers
# ---------------------------------------------------------------------

# Same Pals from my Palworld server that I used in Units 3 and 4.
# Paldeck numbers are unique, and this list is sorted by number.
PALDECK = [
    (1, "Lamball"), (2, "Cattiva"), (5, "Foxparks"), (10, "Pengullet"),
    (17, "Depresso"), (26, "Direhowl"), (33, "Mossanda"), (55, "Chillet"),
    (69, "Lovander"), (100, "Anubis"), (103, "Grizzbolt"), (111, "Jetragon"),
]
PAL_NUMBERS = [number for number, _ in PALDECK]  # sorted keys for searching
PAL_NAMES = [name for _, name in PALDECK]        # NOT alphabetical


def run_both(lst, target, label=""):
    """Run both searches on the same list and print index + comparisons."""
    lin_trace, bin_trace = [], []
    lin = linear_search(lst, target, lin_trace)
    bin_ = binary_search(lst, target, bin_trace)
    label = label or repr(target)
    print(f"  {label:<28} linear -> index {lin:>3} in {len(lin_trace):>2} comparisons"
          f" | binary -> index {bin_:>3} in {len(bin_trace)} comparisons")
    return lin, bin_, len(lin_trace), len(bin_trace)


def time_search(search, lst, target, repeats):
    """Average time of one search call, in microseconds."""
    start = time.perf_counter()
    for _ in range(repeats):
        search(lst, target)
    return (time.perf_counter() - start) / repeats * 1_000_000


def main():
    print("=== UNIT 5: SEARCH ALGORITHMS ===")

    # ===============================
    # TODO (Student): SMALL DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a small sorted dataset.
    # 2. Test both linear search and binary search.
    # 3. Search for:
    #    - a value that exists
    #    - a value that does not exist
    # 4. Use comments to clearly explain the results.

    print("\n=== SMALL DATASET TEST ===")
    print(f"Paldeck numbers (sorted, n = {len(PAL_NUMBERS)}): {PAL_NUMBERS}")

    # A value that exists: Lovander is No. 69, at index 8.
    # Linear search walks indexes 0-8 (9 comparisons). Binary search checks
    # index 5 (26, too small), then 8 (69, found): 2 comparisons.
    index, _, _, _ = run_both(PAL_NUMBERS, 69, "No. 69 (exists)")
    print(f"    -> No. 69 is {PAL_NAMES[index]}")

    # A value that does not exist: No. 40 would sit between 33 and 55.
    # Linear search has to check all 12 numbers before giving up.
    # Binary search narrows to the gap between 33 and 55 and stops after 4.
    run_both(PAL_NUMBERS, 40, "No. 40 (missing)")

    # Sanity check: on a sorted list, both searches must agree for every value.
    agree = all(linear_search(PAL_NUMBERS, n) == binary_search(PAL_NUMBERS, n)
                for n in range(0, 120))
    print(f"  Both searches agree for every number 0-119: {agree}")

    # With only 12 items, the gap is small (12 vs 4 comparisons at worst).
    # On a list this size, either search is basically instant.

    # ===============================
    # TODO (Student): LARGE DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a much larger sorted dataset.
    # 2. Test both search algorithms.
    # 3. Compare the results.
    # 4. Use comments to explain why binary search becomes more
    #    efficient as datasets grow larger.

    print("\n=== LARGE DATASET TEST ===")
    # Scenario: a server-side log of 1,000,000 sorted event IDs.
    # Even numbers only, so any odd number is guaranteed to be missing.
    big = list(range(0, 2_000_000, 2))
    print(f"Sorted event IDs: n = {len(big):,} (0, 2, 4, ..., {big[-1]:,})")

    targets = [
        (0, "first ID"),
        (1_000_000, "middle ID"),
        (1_999_998, "last ID"),
        (1_234_567, "missing (odd)"),
    ]
    print(f"  {'target':<24}{'linear comps':>14}{'binary comps':>14}"
          f"{'linear time':>14}{'binary time':>14}")
    for target, label in targets:
        lin_trace, bin_trace = [], []
        lin = linear_search(big, target, lin_trace)
        bin_ = binary_search(big, target, bin_trace)
        assert lin == bin_  # same answer, very different amount of work
        lin_us = time_search(linear_search, big, target, repeats=3)
        bin_us = time_search(binary_search, big, target, repeats=2000)
        print(f"  {target:>9,} {label:<14}{len(lin_trace):>14,}{len(bin_trace):>14}"
              f"{lin_us / 1000:>11.2f} ms{bin_us:>11.2f} us")

    # Why binary search pulls ahead as the data grows:
    # - Linear search's worst case grows 1 comparison per item: 12 items -> 12,
    #   1,000,000 items -> 1,000,000.
    # - Binary search's worst case grows by 1 comparison each time the list
    #   DOUBLES: 12 items -> 4, 1,000,000 items -> 20 (2^20 is about 1 million).
    # - The first ID is linear search's best case (1 comparison). That is the
    #   one place it wins, and only because the target happens to be at the front.
    print("  Worst-case growth when n multiplies by 10:")
    for n in (10, 100, 1_000, 10_000, 100_000, 1_000_000):
        bin_worst = n.bit_length()  # floor(log2 n) + 1 passes at most
        print(f"    n = {n:>9,}: linear up to {n:>9,} comparisons, binary up to {bin_worst}")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Single-element list
    # - Value not present
    # - Value at the first position
    # - Value at the last position
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")

    # 1. Empty list: linear search's loop runs 0 times; binary search starts
    #    with low = 0, high = -1, so its while loop never runs. Both return -1
    #    without touching the list (no IndexError).
    run_both([], 69, "empty list")

    # 2. Single-element list: the only item is both the first and last index.
    run_both([33], 33, "[33], find 33")
    run_both([33], 69, "[33], find 69")

    # 3. First and last positions: linear search's best and worst cases.
    #    Binary search takes 3-4 comparisons either way.
    run_both(PAL_NUMBERS, 1, "first position (No. 1)")
    run_both(PAL_NUMBERS, 111, "last position (No. 111)")

    # 4. Missing values outside the range: smaller than everything and
    #    larger than everything. Binary search runs off one end and stops.
    run_both(PAL_NUMBERS, 0, "below range (No. 0)")
    run_both(PAL_NUMBERS, 150, "above range (No. 150)")

    # 5. Duplicates: Paldeck numbers are unique, but other data might not be.
    #    Linear search always returns the FIRST match. Binary search returns
    #    whichever match it lands on first, which may not be the first one.
    dupes = [5, 10, 10, 10, 10, 10, 17]
    run_both(dupes, 10, "duplicates of 10")

    # 6. Unsorted input breaks binary search. The same 12 Pals, sorted by NAME
    #    instead of number, are out of numeric order. Binary search goes the
    #    wrong direction and reports Lovander (69) as missing even though
    #    it is in the list. Linear search still finds it.
    by_name = sorted(PALDECK, key=lambda pal: pal[1])
    numbers_by_name = [number for number, _ in by_name]
    print(f"  Numbers in name order: {numbers_by_name}")
    run_both(numbers_by_name, 69, "No. 69 in name order")

    # ===============================
    # Student addition: REAL-WORLD SCENARIO
    # ===============================
    # Paldeck lookups on my server. Players ask two kinds of questions:
    #   "What is No. 103?"  -> the list is sorted by number, so binary search.
    #   "What number is Chillet?" -> the list is NOT sorted by name, so
    #   binary search can't be used on names; linear search is the only option
    #   unless I keep a second copy sorted by name.
    print("\n=== REAL-WORLD SCENARIO: PALDECK LOOKUP ===")
    for number in (103, 42):
        trace = []
        index = binary_search(PAL_NUMBERS, number, trace)
        result = PAL_NAMES[index] if index != -1 else "not in my Paldeck"
        print(f"  Lookup No. {number} (binary): {result} after {len(trace)} comparisons")

    for name in ("Chillet", "Cremis"):
        trace = []
        index = linear_search(PAL_NAMES, name, trace)
        result = f"No. {PAL_NUMBERS[index]}" if index != -1 else "not in my Paldeck"
        print(f"  Lookup {name!r} (linear, names unsorted): {result} after {len(trace)} comparisons")

    # Tradeoff: sorting once costs O(n log n). That pays off only if the list
    # is searched many times. For a one-time search of unsorted data,
    # linear search (O(n)) is cheaper than sorting first.
    print("  Sorting the 12 names first would allow binary search on names,")
    print("  but for a one-off lookup the O(n log n) sort costs more than one O(n) scan.")


if __name__ == "__main__":
    main()
