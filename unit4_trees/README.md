# Unit 4 Discussion: Binary Search Trees

## Overview

This assignment introduces Binary Search Trees (BSTs) and recursive tree operations.

## Learning Objectives

- Build a BST
- Insert values recursively
- Search recursively
- Perform in-order traversal
- Understand BST organization

## Requirements

1. Build a BST.
2. Insert multiple values.
3. Demonstrate in-order traversal.
4. Test searching.
5. Demonstrate edge cases.
6. Create a real-world BST example.

## Implementation

### Scenario

I used Pals from my Palworld server again. Each Pal was stored in the tree by its Paldeck number, with the Pal's name kept on the same node. The real-world scenario was a Paldeck lookup: given a number, find the Pal by walking down the tree instead of scanning a list.

### How to Run

From the repository root:

```
python unit4_trees/unit4_discussion.py
```

### Design

| Method | What it did | Cost |
|---|---|---|
| `insert(value, name)` / `_insert_recursive` | Compared the value at each node and went left if smaller, right if larger, then created a node at the first empty spot. Returned `True` if added, `False` for a duplicate. | O(log n) balanced, O(n) worst case |
| `search(value)` / `_search_recursive` | Followed the same left/right rule and returned `True` or `False`. Each comparison skipped a whole subtree. | O(log n) balanced, O(n) worst case |
| `inorder()` / `_inorder_recursive` | Visited left subtree, node, right subtree, which returned the values in sorted order. | O(n) |

- **Node data:** `Node` stored the key (`value`), an optional `name`, and `left`/`right` references. The name was optional, so the tree still worked with plain numbers.
- **Duplicates:** Paldeck numbers are unique, so inserting a value that was already in the tree did nothing. I tracked `size` so `insert()` could report whether anything was added.
- **Student-added helpers:** `search_path()` returned every node a search compared against, which showed how many steps a search took. `height()` counted the levels. `show()` printed the tree with each child indented under its parent. `get_name()` returned the Pal stored with a number.
- **Insert order:** I inserted the middle Paldeck number first (33, Mossanda), then the middle of each half, so the 12 Pals formed a tree only 4 levels tall.

### Search Tests

| Search | Result | Path | Comparisons |
|---|---|---|---|
| 10 | Found (Pengullet) | 33, 5, 17, 10 | 4 |
| 69 | Found (Lovander) | 33, 100, 55, 69 | 4 |
| 40 | Not found | 33, 100, 55 | 3 |
| 150 | Not found | 33, 100, 103, 111 | 4 |

No search took more than 4 comparisons, which is the tree's height. A linear search through the same 12 Pals could have taken 12.

### Edge Cases Tested

| Test | Result |
|---|---|
| Empty tree | `inorder()` returned `[]`, `search()` returned `False`, height was 0 |
| One-node tree | The root was the only node; searching for it returned `True`, anything else `False` |
| Duplicate insert (55) | Ignored; `insert()` returned `False` and the size stayed 12 |
| Same 12 Pals inserted in sorted order | Every node went to the right, so the tree became a 12-level chain. Finding 111 took 12 comparisons instead of 4. |
| 1,500 numbers inserted in sorted order | The recursive insert raised `RecursionError` after 997 values, because each level of the chain was another recursive call and Python's default limit is about 1,000. |

### Real-World Scenario

- **Lookup by number:** `get_name()` found Lovander (No. 69) and Cattiva (No. 2) in 4 comparisons each, and ruled out No. 42 in 3.
- **Range listing:** Because in-order traversal was already sorted, listing Pals No. 1 through 30 was just the front of the in-order result. No separate sort was needed.

### Observations

- A BST was fast because every comparison removed a whole subtree from the search. With a balanced tree, doubling the number of Pals only added about one more level.
- A BST was only as good as its shape. The tree did not balance itself, so the same data inserted in sorted order made it no better than a linked list. Self-balancing trees (AVL or red-black) fix this by rotating nodes after inserts.
- Compared with a sorted Python list, a BST had the same O(log n) search but could insert without shifting elements. Compared with an unsorted list, it kept the data in order at all times.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain BST behavior and compare to how ordering works to create efficiency as compared to other data structures.