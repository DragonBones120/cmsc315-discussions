"""
==================================================
Unit 3 DISCUSSION: List Operations (Insert, Delete, Search)
==================================================

INSTRUCTIONS:
This assignment focuses on understanding how lists behave when elements
are inserted, removed, and searched. You will analyze how Python lists
shift elements in memory and how different operations impact performance.

SCENARIO:
The demos use Pals from my Palworld server. The real-world scenario is a
party lineup: a player carries up to 5 Pals in a fixed order, and the Pal
in slot 1 is the one that fights first.
"""

import timeit


def insert_at(lst, index, value):
    """
    TODO (Student):
    Insert a value into the list at the specified index.

    Requirements:
    - Use a list operation to insert the value.
    - Add comments explaining what happens to existing elements
      after an insertion occurs.
    - Use comments to explain how insertion performance may vary depending on
      where the insertion occurs.
    """
    # list.insert() puts the value at the given index. Every element from that
    # index to the end moves one position to the right to make room, so their
    # indexes all go up by 1.
    #
    # Performance depends on where the insert happens:
    # - At the end (index == len(lst)): nothing has to shift, so it is O(1),
    #   the same as append().
    # - In the middle: about half the elements shift, which is O(n).
    # - At the beginning (index 0): every element shifts, the worst case, O(n).
    #
    # Note: Python does not raise an error for an out-of-range index here.
    # A large index adds to the end and a very negative one adds to the front.
    lst.insert(index, value)


def delete_at(lst, index):
    """
    TODO (Student):
    Remove and return the value at the specified index.

    Requirements:
    - Validate that the index exists.
    - Return the removed value.
    - Return None if the index is invalid.
    - Add comments explaining why index validation and safe deletion are important.
    """
    # Validate first. Calling pop() with an index that does not exist raises
    # an IndexError and would crash the program. Checking the range lets the
    # caller get None back and decide what to do, so one bad request (like
    # "remove the Pal in slot 9") does not stop everything else.
    #
    # Only non-negative indexes are accepted. Python would treat -1 as "the
    # last item", which could silently delete the wrong value if -1 came
    # from a failed search (search_value returns -1 for "not found").
    if index < 0 or index >= len(lst):
        return None

    # pop(index) removes the value and returns it. Every element after it
    # shifts one position left to close the gap, so deleting from the front
    # is O(n) and deleting from the end is O(1).
    return lst.pop(index)


def search_value(lst, value):
    """
    TODO (Student):
    Search for a value within the list.

    Requirements:
    - Return the index if the value is found.
    - Return -1 if the value is not found.
    - Add comments explaining why this is a linear search and why it scans sequentially.
    """
    # This is a linear search. The list is not sorted and has no index by
    # value, so there is no way to jump to the right spot. The only option is
    # to check each element in order, starting at index 0, until a match is
    # found or the list runs out.
    #
    # Best case: the value is first, O(1). Worst case: the value is last or
    # missing, so all n elements are checked, O(n).
    for i in range(len(lst)):
        if lst[i] == value:
            return i   # found it, stop scanning
    return -1          # scanned everything without a match


# ----- Student-added helpers -----
def show(label, lst):
    """Print a list with each value's index so shifts are easy to see."""
    slots = ", ".join(f"[{i}] {v}" for i, v in enumerate(lst))
    print(f"{label:<28} {slots if slots else '(empty)'}")


class PalParty:
    """
    Real-world scenario: a player's party lineup (max 5 Pals).
    The order matters: slot 1 (index 0) fights first.
    """

    MAX_SIZE = 5

    def __init__(self, owner):
        self.owner = owner
        self.lineup = []

    def add(self, pal, slot=None):
        # A full party rejects the new Pal instead of growing past the limit.
        if len(self.lineup) >= PalParty.MAX_SIZE:
            print(f"  Party full ({PalParty.MAX_SIZE}/{PalParty.MAX_SIZE}). "
                  f"{pal} was sent to the Pal Box instead.")
            return False
        # No slot given means "add to the end", the cheap O(1) case.
        # Slots are 1-based for the player and converted to list indexes.
        index = len(self.lineup) if slot is None else slot - 1
        insert_at(self.lineup, index, pal)
        return True

    def remove(self, pal):
        # Search first, then delete by index. delete_at() rejects -1, so a
        # missing Pal cannot accidentally remove the last one.
        index = search_value(self.lineup, pal)
        removed = delete_at(self.lineup, index)
        if removed is None:
            print(f"  {pal} is not in the party. Nothing was removed.")
        return removed

    def lead(self):
        return self.lineup[0] if self.lineup else None

    def __str__(self):
        slots = ", ".join(f"{i + 1}. {p}" for i, p in enumerate(self.lineup))
        return f"{self.owner}'s party ({len(self.lineup)}/{PalParty.MAX_SIZE}): " \
               f"{slots if slots else '(empty)'}"


def main():
    print("=== UNIT 3: LIST OPERATIONS ===")

    # ===============================
    # TODO (Student): INSERTION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Create a list containing several values.
    # 2. Display the original list.
    # 3. Test insertion at:
    #    - the beginning
    #    - the middle
    #    - the end
    # 4. Display the list after each insertion.
    # 5. Use comments to explain each step in the implementation.

    print("\n=== INSERTION TESTS ===")
    # Step 1: start with four Pals. show() prints each index so we can watch
    # values shift after every insert.
    pals = ["Lamball", "Cattiva", "Foxparks", "Pengullet"]
    show("Original list:", pals)

    # Step 2: insert at the beginning. Every existing Pal shifts right by one
    # (Lamball moves from [0] to [1], and so on). This is the slowest case.
    insert_at(pals, 0, "Chikipi")
    show("Insert Chikipi at 0:", pals)

    # Step 3: insert in the middle. Only the Pals from index 2 onward shift.
    middle = len(pals) // 2
    insert_at(pals, middle, "Depresso")
    show(f"Insert Depresso at {middle}:", pals)

    # Step 4: insert at the end (index == length). Nothing shifts, so this
    # is the same O(1) work as append().
    insert_at(pals, len(pals), "Anubis")
    show("Insert Anubis at end:", pals)

    # ===============================
    # TODO (Student): DELETION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Delete an item from:
    #    - the beginning
    #    - the middle
    #    - the end
    # 2. Display the removed value.
    # 3. Display the updated list after each deletion.
    # 4. Use comments to clearly explain what is happening in the output.

    print("\n=== DELETION TESTS ===")
    show("Starting list:", pals)

    # Delete from the beginning: every remaining Pal shifts left by one,
    # so Lamball moves back from [1] to [0].
    removed = delete_at(pals, 0)
    print(f"Removed from beginning: {removed}")
    show("After deletion:", pals)

    # Delete from the middle: only the Pals after the gap shift left.
    middle = len(pals) // 2
    removed = delete_at(pals, middle)
    print(f"Removed from middle (index {middle}): {removed}")
    show("After deletion:", pals)

    # Delete from the end: nothing comes after it, so nothing shifts.
    removed = delete_at(pals, len(pals) - 1)
    print(f"Removed from end: {removed}")
    show("After deletion:", pals)

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for a value that exists.
    # 2. Search for a value that does not exist.
    # 3. Display the search results with clear explanations.
    # 4. Use comments to explain each step.

    print("\n=== SEARCH TESTS ===")
    show("Searching in:", pals)

    # Search for a Pal that is in the list. The scan stops as soon as it
    # finds a match, so it only checks indexes 0 through the match.
    index = search_value(pals, "Cattiva")
    print(f"Search for Cattiva: found at index {index} "
          f"(checked {index + 1} of {len(pals)} items)")

    # Search for a Pal that is not in the list. The scan has to check every
    # item before it can say "not found", which is the O(n) worst case.
    index = search_value(pals, "Jetragon")
    print(f"Search for Jetragon: returned {index} "
          f"(checked all {len(pals)} items, not found)")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Delete using an invalid index
    # - Search for a missing value
    # - Insert into an empty list
    # - Delete from an empty list
    # - Use comments to explain each edge case.

    print("\n=== EDGE CASES ===")

    # Edge case 1: delete using an index past the end. delete_at() returns
    # None instead of letting pop() raise an IndexError.
    print(f"1. Delete at index 10 from {pals}: {delete_at(pals, 10)}")

    # Edge case 2: delete using -1, the value a failed search returns.
    # Python's pop(-1) would remove the last Pal; delete_at() refuses it.
    print(f"2. Delete at index -1 from {pals}: {delete_at(pals, -1)} "
          f"(list unchanged: {pals})")

    # Edge case 3: insert into an empty list. Any index works, and the
    # value becomes element [0].
    empty = []
    insert_at(empty, 0, "Lamball")
    print(f"3. Insert into an empty list: {empty}")

    # Edge case 4: delete from an empty list. There is no valid index at all,
    # so even index 0 returns None.
    print(f"4. Delete at index 0 from []: {delete_at([], 0)}")

    # Edge case 5: search an empty list. The loop never runs, so it
    # returns -1 right away.
    print(f"5. Search an empty list for Lamball: {search_value([], 'Lamball')}")

    # Edge case 6: duplicates. Linear search returns the FIRST match only.
    dupes = ["Lamball", "Cattiva", "Lamball"]
    print(f"6. Search {dupes} for Lamball: index {search_value(dupes, 'Lamball')} "
          f"(the first match; the second Lamball at index 2 is not reported)")

    # ===============================
    # Student-added: PERFORMANCE CHECK
    # ===============================
    # Time 1,000 inserts at the front vs. the end of a 100,000-item list.
    # Front inserts shift every element each time; end inserts shift none.
    print("\n=== PERFORMANCE CHECK ===")
    setup = "lst = list(range(100_000))"
    front = timeit.timeit("lst.insert(0, -1)", setup=setup, number=1_000)
    end = timeit.timeit("lst.insert(len(lst), -1)", setup=setup, number=1_000)
    print(f"1,000 inserts at the front: {front * 1000:.2f} ms")
    print(f"1,000 inserts at the end:   {end * 1000:.2f} ms")
    print(f"Front inserts were about {front / end:.0f}x slower.")

    # ===============================
    # Student-added: REAL-WORLD SCENARIO
    # ===============================
    print("\n=== REAL-WORLD SCENARIO: PAL PARTY LINEUP ===")
    party = PalParty("DragonBones")

    # Fill the party by adding to the end (no shifting).
    for pal in ["Foxparks", "Pengullet", "Cattiva", "Depresso"]:
        party.add(pal)
    print(party)

    # Put a strong Pal in slot 1 so it fights first. Everyone else shifts
    # down a slot, which is an insert at index 0.
    party.add("Anubis", slot=1)
    print(f"Added Anubis to slot 1: {party}")
    print(f"Lead Pal is now: {party.lead()}")

    # The party is full, so the next Pal is rejected.
    party.add("Jetragon")

    # Remove a Pal by name: search for its index, then delete it.
    print(f"Removed {party.remove('Cattiva')}: {party}")

    # Try to remove a Pal that is not in the party.
    party.remove("Lamball")
    print(party)


if __name__ == "__main__":
    main()
