"""
===========================================================
Unit 1 DISCUSSION: Python OOP, Namespaces, and Copying
===========================================================

INSTRUCTIONS:
In this assignment, you will build and explore object-oriented programming (OOP) concepts in Python.
You are provided with starter code containing TODO sections. Your task is to complete, modify, and
analyze the code to demonstrate understanding of inheritance, namespaces, and object copying.

SCENARIO:
This program models dedicated game servers. GameServer is a general server that tracks
players, and PalworldServer is a specialized server that adds a world name and
Palworld-specific settings (EXP rate, pal spawn rate, and so on).
"""


from copy import copy, deepcopy


# TODO 1:
# Create a parent class.
#
# Requirements:
# - Include at least one class variable.
# - Include at least two instance variables.
# - Include a constructor (__init__).
# - Include a method that returns or displays information about the object.
#
# Replace the pass statement with your implementation.

class GameServer:
    """A general dedicated game server that players can join."""

    # Class variables: stored once on the class and shared by every server.
    server_count = 0
    host_platform = "TrueNAS home server"

    def __init__(self, name, max_players):
        # Instance variables: each server object gets its own copy.
        self.name = name
        self.max_players = max_players
        self.players = []  # mutable list, used later in the copy demonstration

        # Update the shared counter through the class, not self, so every
        # object sees the same total.
        GameServer.server_count += 1

    def status(self):
        """Return a one-line summary of the server."""
        return f"[{self.name}] {len(self.players)}/{self.max_players} players online"

    def add_player(self, player):
        """Add a player, rejecting blank names, duplicates, and full servers."""
        if not player or not player.strip():
            raise ValueError("Player name cannot be empty.")
        if player in self.players:
            raise ValueError(f"{player} is already on {self.name}.")
        if len(self.players) >= self.max_players:
            raise ValueError(f"{self.name} is full ({self.max_players} players max).")
        self.players.append(player)


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.
#
# Replace the pass statement with your implementation.

class PalworldServer(GameServer):
    """A Palworld dedicated server: a GameServer plus a world and game settings."""

    # New class variables that only Palworld servers have.
    game = "Palworld"
    default_port = 8211

    def __init__(self, name, max_players, world_name):
        # Let the parent set up name, max_players, players, and the counter.
        super().__init__(name, max_players)

        # New instance variables.
        self.world_name = world_name
        self.settings = {          # nested mutable data (dict)
            "exp_rate": 1.0,
            "pal_spawn_rate": 1.0,
            "death_penalty": "items",
        }

    def update_setting(self, key, value):
        """New method: change a world setting, only allowing known settings."""
        if key not in self.settings:
            raise KeyError(f"Unknown setting '{key}'. Valid settings: {list(self.settings)}")
        if isinstance(self.settings[key], float) and value <= 0:
            raise ValueError(f"{key} must be greater than 0.")
        self.settings[key] = value

    def status(self):
        """Override: reuse the parent's summary, then add Palworld details."""
        base = super().status()
        return (f"{base} | {self.game} world '{self.world_name}' on port {self.default_port} | "
                f"EXP x{self.settings['exp_rate']}, spawns x{self.settings['pal_spawn_rate']}")

    # ----- Student-created extension -----
    def kick_player(self, player):
        """Remove a player, raising an error if they are not on the server."""
        if player not in self.players:
            raise ValueError(f"Can't kick {player}: not on {self.name}.")
        self.players.remove(player)


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.
#
# Your function should:
# - Create at least two objects of the child class.
# - Access a class variable through the class itself.
# - Access the same class variable through an object.
# - Add a new attribute to only one object after it is created.
# - Display each object's namespace using __dict__.
# - Display information about the class namespace.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")

    base_camp = PalworldServer("Base Camp", 16, "Palpagos Islands")
    friends = PalworldServer("Friends Only", 4, "Sakurajima")

    # The same class variable, reached two ways. Python finds 'game' on the
    # object by checking the instance namespace first, then the class.
    print(f"Through the class:   PalworldServer.game = {PalworldServer.game}")
    print(f"Through an object:   base_camp.game      = {base_camp.game}")

    # Add an attribute to ONE object after creation. It lives only in that
    # object's __dict__, so the other server does not have it.
    base_camp.motd = "Welcome! No griefing bases."
    print(f"\nAdded base_camp.motd -> friends has motd? {hasattr(friends, 'motd')}")

    print(f"\nbase_camp.__dict__: {base_camp.__dict__}")
    print(f"friends.__dict__:   {friends.__dict__}")

    # Class namespace: names defined directly on each class (skipping dunders).
    child_names = [n for n in vars(PalworldServer) if not n.startswith("__")]
    parent_names = [n for n in vars(GameServer) if not n.startswith("__")]
    print(f"\nPalworldServer class namespace: {child_names}")
    print(f"GameServer class namespace:     {parent_names}")
    print(f"'add_player' is inherited, not copied: "
          f"{'add_player' in vars(PalworldServer)} in child, {'add_player' in vars(GameServer)} in parent")

    # Shadowing: assigning through an object creates a NEW instance variable
    # that hides the class variable for that object only.
    friends.game = "Palworld (modded)"
    print(f"\nAfter friends.game = 'Palworld (modded)':")
    print(f"  friends.game = {friends.game}  (instance variable)")
    print(f"  base_camp.game = {base_camp.game}  (still the class variable)")
    print(f"  PalworldServer.game = {PalworldServer.game}  (class unchanged)")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.
#
# Requirements:
# - Create an object that contains nested mutable data.
# - Create a shallow copy.
# - Create a deep copy.
# - Modify the original object's nested data.
# - Display the original object, shallow copy, and deep copy.
# - Use comments to explain the difference between shallow and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")

    original = PalworldServer("Main World", 8, "Palpagos Islands")
    original.add_player("DragonBones")

    # Shallow copy: a new PalworldServer object, but its attributes point to the
    # SAME list and dict objects as the original. Nested data is shared.
    shallow = copy(original)

    # Deep copy: a new object AND new copies of everything nested inside it.
    # Nothing is shared with the original.
    deep = deepcopy(original)

    # Change the original's nested data (the players list and settings dict)...
    original.add_player("Zoe")
    original.update_setting("exp_rate", 3.0)
    # ...and reassign a top-level attribute.
    original.name = "Main World (renamed)"

    for label, server in (("Original", original), ("Shallow copy", shallow), ("Deep copy", deep)):
        print(f"{label:13} name={server.name!r:24} players={server.players}  "
              f"exp_rate={server.settings['exp_rate']}")

    # The shallow copy sees Zoe and the 3.0 EXP rate because it shares the
    # original's list and dict. It keeps the old name because reassigning
    # original.name only changed the original's own reference.
    # The deep copy is fully independent and shows none of the changes.
    print(f"\nShallow shares the players list?  {shallow.players is original.players}")
    print(f"Deep shares the players list?     {deep.players is original.players}")


# TODO 5:
# Complete the main function.
#
# Requirements:
# - Create at least one object from the parent class.
# - Create at least one object from the child class.
# - Demonstrate inheritance by calling methods.
# - Call your namespace demonstration function.
# - Call your copy demonstration function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    print("\n--- Parent object: GameServer ---")
    generic = GameServer("Generic Survival", 10)
    generic.add_player("Alex")
    print(generic.status())

    print("\n--- Child object: PalworldServer ---")
    palworld = PalworldServer("Pal Paradise", 2, "Palpagos Islands")
    palworld.add_player("DragonBones")       # inherited from GameServer
    palworld.update_setting("pal_spawn_rate", 2.0)  # new child method
    print(palworld.status())                 # overridden method
    print(f"Hosted on: {palworld.host_platform}")   # inherited class variable

    print("\n--- Edge case tests ---")
    edge_cases = [
        ("Add a blank player name", lambda: palworld.add_player("   ")),
        ("Add a duplicate player", lambda: palworld.add_player("DragonBones")),
        ("Join a full server", lambda: (palworld.add_player("Zoe"), palworld.add_player("Sam"))),
        ("Kick a player who isn't online", lambda: palworld.kick_player("Ghost")),
        ("Change an unknown setting", lambda: palworld.update_setting("day_length", 2)),
        ("Set a zero EXP rate", lambda: palworld.update_setting("exp_rate", 0)),
    ]
    for description, action in edge_cases:
        try:
            action()
            print(f"{description}: allowed")
        except (ValueError, KeyError) as error:
            # error.args[0] avoids the extra quotes KeyError adds when printed
            print(f"{description}: rejected -> {error.args[0]}")

    palworld.kick_player("Zoe")
    print(f"After kicking Zoe: {palworld.status()}")

    demonstrate_namespaces()
    demonstrate_copying()

    # Copies made with copy()/deepcopy() skip __init__, so they don't count.
    print(f"\nTotal servers created with the constructor: {GameServer.server_count}")


if __name__ == "__main__":
    main()
