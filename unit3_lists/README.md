# Unit 3 Discussion: List Operations

## Overview

This assignment examines insertion, deletion, and searching in Python lists.

## Learning Objectives

- Insert values into a list
- Delete values from a list
- Search for values in a list
- Analyze list behavior and performance

## Requirements

1. Test insertion at the beginning, middle, and end.
2. Test deletion at the beginning, middle, and end.
3. Search for existing and missing values.
4. Demonstrate edge cases.
5. Create a real-world scenario.

## Implementation

### Scenario

I used Pals from my Palworld server again. The demos inserted, deleted, and searched a list of Pal names. The real-world scenario was a `PalParty` class: a party lineup holds up to 5 Pals in order, and the Pal in slot 1 fights first.

### How to Run

From the repository root:

```
python unit3_lists/unit3_discussion.py
```

### Design

| Function | List operation | Cost | Notes |
|---|---|---|---|
| `insert_at(lst, index, value)` | `lst.insert(index, value)` | O(1) at the end, O(n) at the front or middle | Every element from `index` onward shifted one position right. |
| `delete_at(lst, index)` | `lst.pop(index)` after a range check | O(1) at the end, O(n) at the front or middle | Returned `None` for any index outside `0` to `len(lst) - 1`. |
| `search_value(lst, value)` | a `for` loop over the indexes | O(1) best, O(n) worst | Returned the first matching index, or `-1` if nothing matched. |

- **Shifting:** A Python list stores its elements next to each other in memory, so inserting or deleting anywhere except the end moved every element after that spot. I added a `show()` helper that printed each value with its index, so the output showed exactly which Pals moved after each operation.
- **Safe deletion:** `delete_at()` checked the index before calling `pop()`. Without the check, a bad index raised an `IndexError` and stopped the program.
- **Rejecting negative indexes:** Python treats `-1` as "the last item." Since `search_value()` returned `-1` for "not found," passing that result straight to `pop()` would have deleted the last Pal by mistake. `delete_at()` only accepted non-negative indexes to prevent that.
- **Linear search:** The list was unsorted, so the search had to check each element in order. The search output reported how many items were checked, which showed the difference between a quick hit and a full scan.

### Edge Cases Tested

| Test | Result |
|---|---|
| Delete at index 10 (past the end) | Returned `None`; the list was unchanged |
| Delete at index -1 (the "not found" value) | Returned `None`; the last Pal was not removed |
| Insert into an empty list | The value became element `[0]` |
| Delete from an empty list | Returned `None` |
| Search an empty list | Returned `-1` right away |
| Search a list with duplicates | Returned the first match (index 0) only |
| Add a 6th Pal to a full party | Rejected and sent to the Pal Box |
| Remove a Pal that was not in the party | Printed a message; nothing was removed |

### Performance Check

I timed 1,000 inserts at the front and at the end of a 100,000-item list with `timeit`. Front inserts took about 17 ms, and end inserts took about 0.3 ms, so the front was roughly 59 times slower on my machine. Every front insert had to shift all 100,000+ elements, while an end insert shifted none.

### Real-World Scenario

- **Filling the party:** Four Pals were added to the end of the lineup, the cheap case with no shifting.
- **Changing the lead:** Adding Anubis to slot 1 was an insert at index 0. Every other Pal moved down one slot, and Anubis became the lead.
- **Party limit:** When the party was full, Jetragon was rejected instead of the list growing past 5.
- **Removing by name:** `remove()` searched for the Pal's index and then deleted it. When Cattiva was removed, the Pals behind it moved up to close the gap. Removing Lamball, who was not in the party, safely did nothing because `delete_at()` rejected the `-1`.

### Observations

- A list was a good fit for the party because the lineup was small, order mattered, and slots were looked up by position, which is O(1) for a list.
- A linked list would have been better if the program inserted or removed at the front of a very long list often, such as a feed where new items always go on top. A linked list only changes a couple of links instead of shifting every element. It would be worse for jumping to slot 3, because it has to walk the links from the start.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. How do list operations impact performance in real-world applications?
