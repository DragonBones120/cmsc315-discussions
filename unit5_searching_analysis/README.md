# Unit 5 Discussion: Search Algorithms

## Overview

This assignment compares linear search and binary search.

## Learning Objectives

- Implement linear search
- Implement binary search
- Compare performance
- Analyze algorithm efficiency

## Requirements

1. Test both algorithms on a small dataset.
2. Test both algorithms on a large dataset.
3. Demonstrate edge cases.
4. Analyze performance.
5. Create a real-world search scenario.

## Implementation

### Scenario

I kept the Palworld theme from Units 3 and 4. The small dataset was the same 12 Pals from my server, stored as a list sorted by Paldeck number. The real-world scenario was a Paldeck lookup: players asked either "what is No. 103?" (a number, which the list was sorted by) or "what number is Chillet?" (a name, which the list was not sorted by).

### How to Run

From the repository root:

```
python unit5_searching_analysis/unit5_discussion.py
```

### Design

| Function | What it did | Cost |
|---|---|---|
| `linear_search(lst, target)` | Checked each index from 0 to the end and returned the first match, or -1. Worked on any list, sorted or not. | O(n) worst case, O(1) best case |
| `binary_search(lst, target)` | Kept `low` and `high` bounds, checked the middle, and threw away the half that could not hold the target. Returned -1 once `low` passed `high`. Required a sorted list. | O(log n) worst case |

- **Comparison counting:** I added an optional `trace` list parameter to both functions. When a list was passed in, each index the search compared against was appended to it, so `main()` could count comparisons without changing what the functions returned.
- **Helpers:** `run_both()` ran both searches on the same input and printed each result with its comparison count. `time_search()` averaged the time of repeated calls with `time.perf_counter()`.
- **Agreement check:** On the sorted Paldeck list, I ran both searches for every number from 0 to 119 and confirmed they always returned the same index.

### Small Dataset (12 Pals)

| Search | Linear | Binary |
|---|---|---|
| No. 69 (Lovander, exists) | index 8, 9 comparisons | index 8, 2 comparisons |
| No. 40 (missing) | -1, 12 comparisons | -1, 4 comparisons |

With only 12 items, the difference was small and both searches were instant.

### Large Dataset (1,000,000 sorted IDs)

I used the even numbers from 0 to 1,999,998, so any odd number was guaranteed to be missing. Times are from one run on my machine and will vary.

| Target | Linear comparisons | Binary comparisons | Linear time | Binary time |
|---|---|---|---|---|
| 0 (first) | 1 | 19 | 0.00 ms | 0.87 µs |
| 1,000,000 (middle) | 500,001 | 19 | 9.32 ms | 1.09 µs |
| 1,999,998 (last) | 1,000,000 | 20 | 19.56 ms | 1.14 µs |
| 1,234,567 (missing) | 1,000,000 | 20 | 19.50 ms | 1.21 µs |

The program also printed the worst case as n grew by 10 each step. Linear search went from 10 to 1,000,000 comparisons, while binary search went from 4 to 20. Binary search only needed one more comparison each time the list doubled in size.

### Edge Cases Tested

| Test | Result |
|---|---|
| Empty list | Both returned -1 after 0 comparisons. Binary search started with `high = -1`, so its loop never ran and nothing was indexed. |
| Single-element list `[33]` | Finding 33 returned index 0, and finding 69 returned -1. Both took 1 comparison. |
| First position (No. 1) | Linear search's best case: 1 comparison. Binary took 3. |
| Last position (No. 111) | Linear search's worst case for a found value: 12 comparisons. Binary took 4. |
| Below / above range (0 and 150) | Linear checked all 12. Binary ran off one end and stopped after 3 or 4. |
| Duplicates `[5, 10, 10, 10, 10, 10, 17]` | Linear returned index 1 (the first 10). Binary returned index 3, because it landed on a middle copy first. Both were "correct," but only linear guaranteed the first match. |
| Unsorted input | I sorted the same Pals by name, which put the numbers out of order. Binary search went the wrong direction and reported No. 69 as missing even though it was in the list. Linear search still found it at index 9. |

### Real-World Scenario

- **Lookup by number:** Binary search found No. 103 (Grizzbolt) in 3 comparisons and ruled out No. 42 in 4.
- **Lookup by name:** The list was sorted by number, not name, so binary search could not be used on names. Linear search found Chillet (No. 55) in 8 comparisons and reported Cremis (a Pal I hadn't caught) as missing after checking all 12.
- **Tradeoff:** Sorting by name first would have allowed binary search on names, but sorting costs O(n log n). For a one-time lookup, a single O(n) linear scan was cheaper than sorting first.

### Observations

- Binary search was fast because every comparison removed half of the remaining list. A million items took at most 20 comparisons.
- Binary search depended completely on the list being sorted by the value being searched. The unsorted test showed it doesn't crash when that rule is broken. It just returns the wrong answer, which is harder to catch.
- Linear search was still the right tool for small lists, unsorted data, one-time searches, and searching by a field the list wasn't sorted by.
- The first-position test was the one case where linear search beat binary search, and only because the target happened to be at the front.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain when to use linear versus binary search, including tradeoffs in real-world scenarios.
