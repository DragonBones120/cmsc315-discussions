"""
=========================================================
UNIT 4 DISCUSSION: BINARY SEARCH TREES (BST)
=========================================================

INSTRUCTIONS:
This assignment focuses on understanding and implementing a
Binary Search Tree (BST).

You will complete and modify the provided code while explaining
key concepts in your own words using comments and output.

SCENARIO:
The demos use Pals from my Palworld server again. Each Pal is stored
by its Paldeck number (the key the tree is ordered by), with the Pal's
name kept alongside it. The real-world scenario is a Paldeck lookup:
given a Paldeck number, find the Pal without scanning the whole list.
"""


class Node:
    def __init__(self, value, name=None):
        # TODO (Student):
        # Store the node's value and initialize references
        # to the left and right child nodes.

        # value is the key the tree is ordered by (a Paldeck number).
        # name is extra data carried along with the key (the Pal's name).
        # It is optional so the class still works with plain numbers.
        self.value = value
        self.name = name
        # A new node starts as a leaf, so it has no children yet.
        self.left = None    # subtree of smaller values
        self.right = None   # subtree of larger values


class BST:
    def __init__(self):
        # TODO (Student):
        # Initialize an empty Binary Search Tree.

        # An empty tree is just a missing root. Every method checks for
        # None, so an empty tree is handled the same way as an empty subtree.
        self.root = None
        self.size = 0

    def insert(self, value, name=None):
        """
        TODO (Student):
        Insert a value into the BST.

        Requirements:
        - Use the recursive helper method.
        - Add comments explaining why insertion depends on
          whether a value is smaller or larger than the
          current node.
        """
        # Insertion has to follow the BST rule: everything in a node's left
        # subtree is smaller than the node, and everything in its right
        # subtree is larger. Comparing the new value to each node on the way
        # down decides which side it belongs on. If it went anywhere else,
        # search would later look on the wrong side and never find it.
        #
        # Returns True if the value was added and False if it was a
        # duplicate. Paldeck numbers are unique, so duplicates are ignored.
        size_before = self.size
        self.root = self._insert_recursive(self.root, value, name)
        return self.size > size_before

    def _insert_recursive(self, node, value, name=None):
        """
        TODO (Student):
        Implement recursive BST insertion.

        Requirements:
        - Create a new node when a position is found.
        - Insert smaller values into the left subtree.
        - Insert larger values into the right subtree.
        - Return the updated node reference.
        """
        # Base case: an empty spot. This is where the value belongs, so
        # create the node here and hand it back to the parent.
        if node is None:
            self.size += 1
            return Node(value, name)

        if value < node.value:
            # Smaller values go left. The returned reference is stored back
            # in node.left, which is how a new node gets attached.
            node.left = self._insert_recursive(node.left, value, name)
        elif value > node.value:
            # Larger values go right.
            node.right = self._insert_recursive(node.right, value, name)
        # Equal value: a duplicate. Nothing is added, and the tree is
        # returned unchanged.

        # Return this node so the parent keeps pointing at the same subtree.
        return node

    def search(self, value):
        """
        TODO (Student):
        Search for a value in the BST.

        Requirements:
        - Return True if found.
        - Return False if not found.
        - Add comments explaining why BST search is often
          more efficient than linear search.
        """
        # A linear search checks items one by one, so finding (or ruling
        # out) a value can take n comparisons. In a BST, each comparison
        # rules out an entire subtree: if the value is smaller than the
        # node, nothing on the right can match, so that whole half is
        # skipped. In a balanced tree this cuts the search space roughly in
        # half every step, so it takes about log2(n) comparisons, O(log n).
        # "Often" matters here: if the tree is lopsided, it can still be O(n).
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST search.
        """
        # Base case 1: fell off the tree, so the value is not here.
        if node is None:
            return False
        # Base case 2: found it.
        if value == node.value:
            return True
        # Otherwise, only one side can contain the value. Search that side
        # and skip the other one completely.
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def inorder(self):
        """
        TODO (Student):
        Return a list containing the values from an
        in-order traversal.
        """
        values = []
        self._inorder_recursive(self.root, values)
        return values

    def _inorder_recursive(self, node, values):
        """
        TODO (Student):
        Implement in-order traversal.

        Requirements:
        - Visit the left subtree.
        - Visit the current node.
        - Visit the right subtree.
        - Add comments explaining why this traversal
          produces sorted output in a BST.
        """
        # Why this comes out sorted: for any node, every value in its left
        # subtree is smaller and every value in its right subtree is larger.
        # Visiting left, then the node, then right means all the smaller
        # values are added before the node and all the larger ones after it.
        # Because that holds at every node, the whole list ends up in order.
        if node is None:
            return                                   # empty subtree: nothing to add
        self._inorder_recursive(node.left, values)   # 1. smaller values
        values.append(node.value)                    # 2. this node
        self._inorder_recursive(node.right, values)  # 3. larger values

    # ----- Student-added helpers -----
    def search_path(self, value):
        """
        Return the list of node values visited while searching for value.
        Uses a loop instead of recursion so it can show every step. The
        path length is the number of comparisons the search needed.
        """
        path = []
        node = self.root
        while node is not None:
            path.append(node.value)
            if value == node.value:
                break
            node = node.left if value < node.value else node.right
        return path

    def get_name(self, value):
        """Return the name stored with value, or None if it is not in the tree."""
        node = self.root
        while node is not None:
            if value == node.value:
                return node.name
            node = node.left if value < node.value else node.right
        return None

    def height(self):
        """Number of levels in the tree (0 for empty, 1 for one node)."""
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left),
                       self._height_recursive(node.right))

    def show(self, node="root", indent="", label="Root"):
        """Print the tree with each child indented under its parent (L = left, R = right)."""
        if node == "root":
            node = self.root
            if node is None:
                print("  (empty tree)")
                return
        if node is None:
            return
        name = f" {node.name}" if node.name else ""
        print(f"  {indent}{label}: {node.value}{name}")
        self.show(node.left, indent + "    ", "L")
        self.show(node.right, indent + "    ", "R")


# Paldeck numbers and names used in the demos.
PALS = {
    1: "Lamball", 2: "Cattiva", 5: "Foxparks", 10: "Pengullet",
    17: "Depresso", 26: "Direhowl", 33: "Mossanda", 55: "Chillet",
    69: "Lovander", 100: "Anubis", 103: "Grizzbolt", 111: "Jetragon",
}


def main():
    print("=== UNIT 4: BINARY SEARCH TREES ===")

    # ===============================
    # TODO (Student): BUILD A TREE
    # ===============================
    #
    # Requirements:
    # 1. Create a BST object.
    # 2. Insert at least 7 values.
    # 3. Include values that go into both left
    #    and right subtrees.
    # 4. Display the values inserted.
    # 5. Use comments to explain why a BST is efficient at reducing search space for each step.

    print("\n=== TREE CONSTRUCTION ===")
    paldeck = BST()

    # Insert order matters. The 12 Paldeck numbers sorted are
    # 1, 2, 5, 10, 17, 26, 33, 55, 69, 100, 103, 111. I inserted the middle
    # one first (33, Mossanda), so half the Pals end up on each side of the
    # root. Then I inserted the middle of each half (5 on the left, 100 on
    # the right), and so on. Each comparison on the way down sends a value
    # left or right, so it only travels through one branch at each level.
    #   - 33 becomes the root.
    #   - 5 < 33 goes left; 100 > 33 goes right.
    #   - 1 and 17 split the left half; 55 and 103 split the right half.
    #   - 2, 10, 26, 69, 111 fill the bottom level.
    # Because each step throws away one whole subtree, a search for any of
    # these 12 Pals takes at most 4 comparisons instead of up to 12 with a
    # list.
    insert_order = [33, 5, 100, 1, 17, 55, 103, 2, 10, 26, 69, 111]
    for number in insert_order:
        paldeck.insert(number, PALS[number])
    print(f"Inserted {len(insert_order)} Pals in this order: {insert_order}")
    print(f"Tree size: {paldeck.size}, height: {paldeck.height()} levels")
    paldeck.show()

    # ===============================
    # TODO (Student): IN-ORDER TRAVERSAL
    # ===============================
    #
    # Requirements:
    # 1. Perform an in-order traversal.
    # 2. Display the traversal results.
    # 3. Use comments to explain why the traversal produces
    #    sorted output in a BST.

    print("\n=== IN-ORDER TRAVERSAL ===")
    # The values were inserted out of order, but in-order traversal returns
    # them sorted. Left subtree (smaller), node, right subtree (larger) is
    # applied at every node, so smaller numbers always print first. No
    # sorting step was needed; the tree's shape already holds the order.
    ordered = paldeck.inorder()
    print(f"In-order result: {ordered}")
    print(f"Matches sorted(): {ordered == sorted(insert_order)}")
    print("As a Paldeck listing:")
    for number in ordered:
        print(f"  No. {number:>3}  {paldeck.get_name(number)}")

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for at least two values that exist.
    # 2. Search for at least two values that do not exist.
    # 3. Use comments to clearly explain the results.

    print("\n=== SEARCH TESTS ===")
    # search_path() shows which nodes were compared. The number of steps is
    # never more than the tree's height (4 levels), not the number of Pals.
    tests = [
        (10, "exists, bottom level on the left"),
        (69, "exists, bottom level on the right"),
        (40, "missing, falls between 33 and 55"),
        (150, "missing, larger than everything"),
    ]
    for value, note in tests:
        found = paldeck.search(value)
        path = paldeck.search_path(value)
        result = f"found ({paldeck.get_name(value)})" if found else "not found"
        print(f"Search {value:>3}: {result:<20} path {path}, "
              f"{len(path)} comparisons [{note}]")
    # Every search finished in 4 comparisons or fewer. The missing values
    # were ruled out as soon as the search reached an empty child, because
    # the BST rule means there was no other place in the tree they could be.

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least one edge case.
    #
    # Example ideas:
    # - Traverse an empty tree
    # - Search an empty tree
    # - Insert duplicate values
    # - Create a tree with only one node
    #
    # Use comments to explain what happens and why.

    print("\n=== EDGE CASES ===")

    # Edge case 1: empty tree. The root is None, so traversal returns an
    # empty list and search returns False right away without crashing.
    empty = BST()
    print(f"1. Empty tree: inorder() = {empty.inorder()}, "
          f"search(1) = {empty.search(1)}, height = {empty.height()}")

    # Edge case 2: one node. The root is also the only leaf, so a search
    # either matches it or falls off on the first comparison.
    single = BST()
    single.insert(1, "Lamball")
    print(f"2. One-node tree: inorder() = {single.inorder()}, "
          f"search(1) = {single.search(1)}, search(2) = {single.search(2)}, "
          f"height = {single.height()}")

    # Edge case 3: duplicate value. Paldeck numbers are unique, so a second
    # 55 is ignored instead of being stored twice.
    added = paldeck.insert(55, "Chillet")
    print(f"3. Insert duplicate 55: added = {added}, size still {paldeck.size}, "
          f"inorder count = {len(paldeck.inorder())}")

    # Edge case 4: sorted insert order. This is when a BST becomes
    # inefficient. If every new value is larger than the last, each one
    # goes to the right of the previous node, and the tree turns into a
    # chain (basically a linked list). Search is back to O(n).
    chain = BST()
    for number in sorted(insert_order):
        chain.insert(number, PALS[number])
    print(f"4. Same 12 Pals inserted in sorted order:")
    print(f"   height = {chain.height()} (balanced order gave {paldeck.height()})")
    print(f"   search 111 path: {chain.search_path(111)} "
          f"= {len(chain.search_path(111))} comparisons "
          f"(balanced tree: {len(paldeck.search_path(111))})")

    # Edge case 5: a very tall chain breaks the recursive methods. Python
    # stops recursion at about 1,000 calls by default, and each level of the
    # chain is one recursive call, so inserting 1,500 sorted numbers raises
    # RecursionError. A balanced tree with 1,500 values is only about 11
    # levels deep, so the same code would have no problem.
    tall = BST()
    try:
        for number in range(1, 1501):
            tall.insert(number)
        print(f"5. 1,500 sorted inserts: height {tall.height()}")
    except RecursionError:
        print(f"5. 1,500 sorted inserts: RecursionError after "
              f"{tall.size} values (the chain got deeper than Python's "
              f"recursion limit)")

    # ===============================
    # Student-added: REAL-WORLD SCENARIO
    # ===============================
    print("\n=== REAL-WORLD SCENARIO: PALDECK LOOKUP ===")
    # Players on my server ask things like "what's number 69?" The Paldeck
    # tree answers by walking down from the root instead of scanning every
    # Pal. Range questions also work well, because in-order traversal is
    # already sorted: "list every Pal from No. 1 to No. 30" is just the
    # front of the in-order result.
    for number in [69, 2, 42]:
        name = paldeck.get_name(number)
        steps = len(paldeck.search_path(number))
        if name:
            print(f"Lookup No. {number}: {name} ({steps} comparisons)")
        else:
            print(f"Lookup No. {number}: no Pal with that number on the server "
                  f"({steps} comparisons to rule it out)")
    early = [f"{n} {paldeck.get_name(n)}" for n in paldeck.inorder() if n <= 30]
    print(f"Pals No. 1-30 in order: {', '.join(early)}")


if __name__ == "__main__":
    main()
