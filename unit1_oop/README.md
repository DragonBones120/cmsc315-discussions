# Unit 1 Discussion: Python OOP, Namespaces, and Copying

## Overview

This assignment explores object-oriented programming (OOP) concepts in Python, including inheritance, namespaces, and object copying.

## Learning Objectives

- Create parent and child classes
- Use inheritance to extend functionality
- Understand class and instance namespaces
- Demonstrate shallow and deep copying
- Apply object-oriented design principles

## Requirements

Complete all TODO sections in the source code:

1. Create a parent class.
2. Create a child class using inheritance.
3. Demonstrate class and instance namespaces.
4. Demonstrate shallow and deep copying.
5. Create and test objects in `main()`.
6. Add a student-created extension.

## Implementation

### Scenario

I modeled dedicated game servers, based on the Palworld server I host at home. A general `GameServer` tracked players, and a specialized `PalworldServer` added a world name and Palworld-specific settings. Game servers fit inheritance well because every server shares the same basics (a name, a player limit, a player list), while each game adds its own details on top.

### How to Run

From the repository root:

```
python unit1_oop/unit1_discussion.py
```

### Design

| Class | Class variables | Instance variables | Methods |
|---|---|---|---|
| `GameServer` (parent) | `server_count`, `host_platform` | `name`, `max_players`, `players` | `status()`, `add_player()` |
| `PalworldServer` (child) | `game`, `default_port` | `world_name`, `settings` (plus the inherited ones) | `update_setting()` (new), `status()` (overridden), `kick_player()` (extension) |

- **TODO 1 – Parent class:** I created `GameServer` with a constructor that set up the instance variables and incremented the shared `server_count` class variable through the class name, so every object saw the same total. `add_player()` validated input before changing the player list.
- **TODO 2 – Child class:** `PalworldServer` inherited from `GameServer` and called `super().__init__()` so the parent handled the shared setup. It added a `settings` dictionary and an `update_setting()` method that only accepted known settings. I overrode `status()` by calling the parent's version with `super().status()` and appending Palworld details, instead of rewriting the parent's logic.
- **TODO 3 – Namespaces:** I read the `game` class variable both through the class and through an object, added a `motd` attribute to only one server, and printed each object's `__dict__` to show the attribute existed only on that object. I also printed both class namespaces, which showed that `add_player` lived only in `GameServer` and was found through inheritance rather than copied into the child. Finally, I assigned `friends.game` to show shadowing: the assignment created a new instance variable that hid the class variable for that one object while the class and other objects were unchanged.
- **TODO 4 – Copying:** I created a server with a player list and a settings dictionary, then made a shallow copy and a deep copy. After I added a player, raised the EXP rate, and renamed the original, the shallow copy showed the new player and EXP rate because it shared the same list and dictionary objects. It kept the old name because reassigning `original.name` only changed the original's reference. The deep copy showed none of the changes because `deepcopy()` duplicated the nested data as well. I confirmed this with `is` checks on the player lists.
- **TODO 5 – main():** I created one object of each class and called inherited (`add_player`), new (`update_setting`), and overridden (`status`) methods.
- **TODO 6 – Extension:** I added `kick_player()` and a table of edge-case tests.

### Edge Cases Tested

Each case raised a `ValueError` or `KeyError` that `main()` caught and printed, so the program kept running instead of crashing:

| Test | Result |
|---|---|
| Adding a blank player name | Rejected: name cannot be empty |
| Adding a player who was already online | Rejected: duplicate player |
| Joining a server at its player limit | Rejected: server full |
| Kicking a player who was not online | Rejected: player not found |
| Changing a setting that did not exist | Rejected: lists the valid settings |
| Setting the EXP rate to 0 | Rejected: rate must be greater than 0 |

### Observations

- `server_count` ended at 5 even though 7 server objects existed, because `copy()` and `deepcopy()` did not call `__init__`. A counter in the constructor only counts objects that were actually constructed.
- The shallow copy result showed a real risk: copying a server config to make a "test" world and then editing its settings would silently change the live server too. A deep copy is the safe choice when objects contain lists or dictionaries.

### Real-World Use

Server hosting panels manage many game servers that share the same core features (start, stop, player limits, player lists) but have game-specific settings. Putting the shared behavior in a parent class means a new game only needs a small child class, and a fix to `add_player()` applies to every game at once.

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?
2. What challenges did you encounter, and how did you overcome them?
3. Compare OOP to procedural programming.
4. Discuss the benefits of maintainability and reusability and apply this managing overhead, practical application development, and future use.