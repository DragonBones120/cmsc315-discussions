# Unit 2 Discussion: Stacks and Queues

## Overview

This assignment explores two fundamental linear data structures:

- Stack (LIFO)
- Queue (FIFO)

## Learning Objectives

- Implement stack operations
- Implement queue operations
- Understand LIFO and FIFO behavior
- Create edge cases

## Requirements

Complete all TODO sections:

1. Implement stack operations.
2. Implement queue operations.
3. Demonstrate LIFO behavior.
4. Demonstrate FIFO behavior.
5. Create and test edge cases.
6. Create a real-world scenario.

## Implementation

### Scenario

I used my Palworld dedicated server again. In the demos, the stack held admin console commands and the queue held players lining up to join. The real-world scenario combined both: a `PalworldServer` class used a Queue for players waiting for an open slot and a Stack for undoing setting changes.

### How to Run

From the repository root:

```
python unit2_stacks_queues/unit2_discussion.py
```

### Design

| Class | Internal storage | Operations | Why this storage |
|---|---|---|---|
| `Stack` | Python `list` (the end of the list is the top) | `push`, `pop`, `peek`, `is_empty`, `size` | `append()` and `pop()` both work on the end of a list, so every operation was O(1). |
| `Queue` | `collections.deque` | `enqueue`, `dequeue`, `front`, `is_empty`, `size` | `popleft()` is O(1). A list would need `pop(0)`, which shifts every remaining item and is O(n). |
| `PalworldServer` | a `Queue` and a `Stack` | `request_join`, `leave`, `change_setting`, `undo` | The join line needed FIFO fairness, and undo needed to reverse the newest change first (LIFO). |

- **Stack operations:** `push()` added to the top, and `pop()` removed from the top, so the last value pushed was always the first one out. `peek()` returned the top value without changing the stack.
- **Queue operations:** `enqueue()` added to the back, and `dequeue()` removed from the front, so the value that waited longest always left first. `front()` returned the next value without removing it.
- **Empty handling:** `pop()`, `peek()`, `dequeue()`, and `front()` raised an `IndexError` with a clear message when the structure was empty. I chose an error over returning `None` because `None` could be mistaken for a real value that had been added. A helper, `try_operation()`, caught the error and printed it so the program kept running.
- **LIFO demo:** I pushed four commands (`/save`, `/broadcast`, `/kick`, `/shutdown`) and popped them all. They came out in reverse order.
- **FIFO demo:** I enqueued four players and dequeued them all. They came out in the same order they arrived.
- **Readable output:** I added `__str__` methods that printed the stack bottom → top and the queue front → back, so each step showed exactly where the new value went.

### Edge Cases Tested

| Test | Result |
|---|---|
| `pop()` on an empty stack | Handled `IndexError`: pop from an empty stack |
| `peek()` on an empty stack | Handled `IndexError`: peek at an empty stack |
| One-item stack, then `pop()` | Returned the item; `is_empty()` was `True` |
| `dequeue()` on an empty queue | Handled `IndexError`: dequeue from an empty queue |
| `front()` on an empty queue | Handled `IndexError`: front of an empty queue |
| One-item queue, then `dequeue()` | Returned the item; `is_empty()` was `True` |
| `undo()` with no changes left | Printed "Nothing to undo" instead of crashing |

### Real-World Scenario

- **Join queue (FIFO):** The server held 2 players. DragonBones and Zoe joined, then Sam and Riley were queued as #1 and #2. When Zoe left, Sam (who had waited longest) took the slot, and when DragonBones left, Riley got in. A stack here would have been unfair, because the newest arrival would have skipped everyone else.
- **Undo stack (LIFO):** Before each setting change, the server pushed the setting's old value. I changed `exp_rate` to 2.0, `pal_spawn_rate` to 1.5, and `exp_rate` to 5.0. Three undos restored them newest-first (`exp_rate` 2.0, `pal_spawn_rate` 1.0, `exp_rate` 1.0), which returned every setting to its original value. Undoing in any other order would have restored `exp_rate` to the wrong value.

### Observations

- Both classes wrapped a built-in structure and exposed only the operations that matched their rules. Code using `Stack` could not reach into the middle of the list, which kept LIFO behavior guaranteed.
- `peek()` and `front()` were more useful than they first seemed. The server could check who was next or what undo would change without committing to it.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Explain the differences between stacks and queues as this relates to real-world applications.
