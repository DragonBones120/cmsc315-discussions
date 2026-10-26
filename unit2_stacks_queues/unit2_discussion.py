"""
===========================================================
UNIT 2 DISCUSSION: STACKS AND QUEUES (PYTHON)
===========================================================

OVERVIEW:
This assignment introduces two fundamental data structures:
the Stack (LIFO) and the Queue (FIFO).

You will complete, modify, and extend the starter code while
explaining key concepts through comments and improved output.

SCENARIO:
The demos use my Palworld dedicated server. The real-world scenario
uses a Queue for players waiting to join a full server and a Stack
for undoing admin setting changes.
"""

from collections import deque


class Stack:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the stack.
        # Hint: A Python list can be used to store stack values.
        # The END of the list is the top of the stack. append() and pop()
        # both work on the end, so push and pop are O(1).
        self._items = []

    def push(self, value):
        # TODO (Student): Add value to the stack.
        # Add a short comment explaining why this operation supports LIFO behavior.
        # New values always go on top, so the newest value is the first one
        # pop() will reach. That is Last-In, First-Out.
        self._items.append(value)

    def pop(self):
        # TODO (Student): Remove and return the most recently added value.
        # Improve or explain empty-stack handling.
        # What should happen if the stack is empty?
        # An empty stack has nothing to return, so this raises an IndexError
        # with a clear message instead of failing silently or returning None
        # (None could be mistaken for a real value that was pushed).
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        # TODO (Student): Return the top value without removing it.
        # Add a comment explaining what peek does.
        # peek() lets you look at the next value pop() would return without
        # changing the stack. It raises the same error as pop() when empty.
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        # TODO (Student): Return True if the stack has no values.
        return len(self._items) == 0

    # ----- Student-added helpers -----
    def size(self):
        """Return how many values are on the stack."""
        return len(self._items)

    def __str__(self):
        # Show the stack bottom -> top so the output makes the order clear.
        return f"bottom -> {self._items} <- top"


class Queue:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the queue.
        # Hint: collections.deque is useful for efficient queue operations.
        # A deque removes from the front in O(1). A list would need pop(0),
        # which shifts every remaining item and is O(n).
        self._items = deque()

    def enqueue(self, value):
        # TODO (Student): Add value to the back of the queue.
        # Add a short comment explaining why this operation supports FIFO behavior.
        # New values join at the back and are removed from the front, so the
        # value that has waited longest leaves first. That is First-In, First-Out.
        self._items.append(value)

    def dequeue(self):
        # TODO (Student): Remove and return the value from the front of the queue.
        # Explain or improve empty-queue handling.
        # Like Stack.pop(), dequeuing from an empty queue raises an IndexError
        # with a clear message so the caller can catch it and keep running.
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def front(self):
        # TODO (Student): Return the front value without removing it.
        # Add a comment explaining what front returns.
        # front() returns the value that has waited the longest, which is the
        # next value dequeue() will remove. The queue is not changed.
        if self.is_empty():
            raise IndexError("front of an empty queue")
        return self._items[0]

    def is_empty(self):
        # TODO (Student): Return True if the queue has no values.
        return len(self._items) == 0

    # ----- Student-added helpers -----
    def size(self):
        """Return how many values are waiting in the queue."""
        return len(self._items)

    def __str__(self):
        # Show the queue front -> back so the output makes the order clear.
        return f"front -> {list(self._items)} <- back"


def try_operation(description, operation):
    """Run an operation that might fail on an empty structure and print the result."""
    try:
        result = operation()
        print(f"  {description}: returned {result!r}")
    except IndexError as error:
        print(f"  {description}: handled IndexError -> {error}")


# ----- Student-created real-world scenario -----
class PalworldServer:
    """A Palworld server with a join queue (FIFO) and an undo stack (LIFO)."""

    def __init__(self, name, max_players):
        self.name = name
        self.max_players = max_players
        self.players = []
        self.join_queue = Queue()   # players waiting for an open slot
        self.undo_stack = Stack()   # previous values of changed settings
        self.settings = {"exp_rate": 1.0, "pal_spawn_rate": 1.0, "day_length": 1.0}

    def request_join(self, player):
        # Join right away if there is room, otherwise wait in line.
        if len(self.players) < self.max_players:
            self.players.append(player)
            print(f"  {player} joined ({len(self.players)}/{self.max_players})")
        else:
            self.join_queue.enqueue(player)
            print(f"  Server full. {player} is #{self.join_queue.size()} in the join queue")

    def leave(self, player):
        # When someone leaves, the player who has waited longest gets the slot.
        self.players.remove(player)
        print(f"  {player} left")
        if not self.join_queue.is_empty():
            next_player = self.join_queue.dequeue()
            self.players.append(next_player)
            print(f"  {next_player} moved from the queue onto the server")

    def change_setting(self, key, value):
        # Save the old value on the stack before changing it, so it can be undone.
        self.undo_stack.push((key, self.settings[key]))
        self.settings[key] = value
        print(f"  Set {key} = {value}")

    def undo(self):
        # The most recent change is on top, so undo reverses changes newest-first.
        if self.undo_stack.is_empty():
            print("  Nothing to undo")
            return
        key, old_value = self.undo_stack.pop()
        self.settings[key] = old_value
        print(f"  Undo: {key} restored to {old_value}")


def main():
    print("=== UNIT 2: STACKS AND QUEUES ===")

    # ===============================
    # TODO (Student): STACK DEMO
    # ===============================
    # Requirements:
    # 1. Create a Stack object.
    # 2. Add at least 4 values to the stack.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate LIFO behavior.
    # 5. Show what happens when pop() is used on an empty stack.
    #
    # Edge Cases:
    # 6. Show what happens when peek() is used on an empty stack.
    # 7. Create a stack with only one item, remove it,
    #    and verify the stack is empty afterward.

    print("\n=== STACK DEMO ===")
    print("Values are admin console commands, pushed in the order they were run.")

    commands = Stack()
    for command in ["/save", "/broadcast Restart_in_5", "/kick Griefer", "/shutdown 300"]:
        commands.push(command)
        print(f"  {'push(' + repr(command) + ')':33} -> {commands}")

    print(f"\npeek() shows the top without removing it: {commands.peek()!r}")
    print(f"Size is still {commands.size()} after peeking.")

    # LIFO: pop() returns the commands in the reverse of the order they were pushed.
    print("\nPopping every command (LIFO = last pushed comes out first):")
    while not commands.is_empty():
        print(f"  pop() -> {commands.pop()!r}")

    print("\nEdge cases:")
    try_operation("pop() on an empty stack", commands.pop)
    try_operation("peek() on an empty stack", commands.peek)

    single = Stack()
    single.push("/save")
    print(f"  One-item stack: {single}")
    print(f"  pop() -> {single.pop()!r}; is_empty() = {single.is_empty()}")

    # ===============================
    # TODO (Student): QUEUE DEMO
    # ===============================
    # Requirements:
    # 1. Create a Queue object.
    # 2. Add at least 4 values to the queue.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate FIFO behavior.
    # 5. Show what happens when dequeue() is used on an empty queue.
    #
    # Edge Cases:
    # 6. Show what happens when front() is used on an empty queue.
    # 7. Create a queue with only one item, remove it,
    #    and verify the queue is empty afterward.

    print("\n=== QUEUE DEMO ===")
    print("Values are players lining up to join, enqueued in the order they arrived.")

    lobby = Queue()
    for player in ["DragonBones", "Zoe", "Sam", "Riley"]:
        lobby.enqueue(player)
        print(f"  {'enqueue(' + repr(player) + ')':23} -> {lobby}")

    print(f"\nfront() shows who is next without removing them: {lobby.front()!r}")
    print(f"Size is still {lobby.size()} after checking the front.")

    # FIFO: dequeue() returns players in the same order they were enqueued.
    print("\nDequeuing every player (FIFO = first in line goes first):")
    while not lobby.is_empty():
        print(f"  dequeue() -> {lobby.dequeue()!r}")

    print("\nEdge cases:")
    try_operation("dequeue() on an empty queue", lobby.dequeue)
    try_operation("front() on an empty queue", lobby.front)

    single_queue = Queue()
    single_queue.enqueue("DragonBones")
    print(f"  One-item queue: {single_queue}")
    print(f"  dequeue() -> {single_queue.dequeue()!r}; is_empty() = {single_queue.is_empty()}")

    # ===============================
    # Student-created real-world scenario
    # ===============================
    print("\n=== REAL-WORLD SCENARIO: PALWORLD SERVER ===")
    server = PalworldServer("Pal Paradise", 2)

    print("Join queue (Queue, FIFO):")
    for player in ["DragonBones", "Zoe", "Sam", "Riley"]:
        server.request_join(player)
    server.leave("Zoe")
    server.leave("DragonBones")
    print(f"  Online: {server.players} | Still waiting: {server.join_queue}")

    print("\nSetting changes with undo (Stack, LIFO):")
    server.change_setting("exp_rate", 2.0)
    server.change_setting("pal_spawn_rate", 1.5)
    server.change_setting("exp_rate", 5.0)
    print(f"  Current settings: {server.settings}")
    server.undo()   # undoes exp_rate 5.0 (the newest change)
    server.undo()   # undoes pal_spawn_rate 1.5
    server.undo()   # undoes exp_rate 2.0 (the oldest change)
    server.undo()   # edge case: empty undo stack
    print(f"  Settings after undo: {server.settings}")


if __name__ == "__main__":
    main()
