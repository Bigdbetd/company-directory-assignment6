"""A company directory stored in a custom binary tree.

Run the menu with: python3 tree_builder.py
Employee names must be unique, nonempty strings. Matching is case-sensitive.
"""


class EmployeeNode:
    """One employee, with up to two direct reports."""

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Employee name must be a nonempty string.")
        self.name = name.strip()
        self.left = None
        self.right = None


class TeamTree:
    """A reporting hierarchy built from linked EmployeeNode objects."""

    def __init__(self):
        self.root = None

    def _find(self, node, name):
        """Recursively check for an existing employee without a list or dict."""
        if node is None:
            return None
        if node.name == name:
            return node
        return self._find(node.left, name) or self._find(node.right, name)

    def insert(self, manager_name, employee_name, side, current_node=None):
        """Search recursively and attach a new report to an available side.

        True means inserted, False means rejected, and internal None means
        the manager was not found in this particular subtree.
        """
        first_call = current_node is None
        if first_call:
            if self.root is None:
                print("Error: Add a team lead before adding employees.")
                return False
            if not isinstance(manager_name, str) or not manager_name.strip():
                print("Error: Manager name cannot be blank.")
                return False
            if not isinstance(employee_name, str) or not employee_name.strip():
                print("Error: Employee name cannot be blank.")
                return False
            manager_name = manager_name.strip()
            employee_name = employee_name.strip()
            if not isinstance(side, str) or side.strip().lower() not in ("left", "right"):
                print("Error: Side must be left or right.")
                return False
            side = side.strip().lower()
            if self._find(self.root, employee_name) is not None:
                print(f"Error: Employee '{employee_name}' already exists.")
                return False
            current_node = self.root

        if current_node.name == manager_name:
            # Never replace an existing report or its descendants.
            if getattr(current_node, side) is not None:
                print(f"Error: The {side} report of '{manager_name}' is occupied.")
                return False
            setattr(current_node, side, EmployeeNode(employee_name))
            print(f"Success: {employee_name} added to the {side.upper()} of {manager_name}.")
            return True

        # Only recurse into real nodes; passing None would restart at root.
        if current_node.left is not None:
            result = self.insert(manager_name, employee_name, side, current_node.left)
            if result is not None:
                return result
        if current_node.right is not None:
            result = self.insert(manager_name, employee_name, side, current_node.right)
            if result is not None:
                return result

        if first_call:
            print(f"Error: Manager '{manager_name}' does not exist.")
            return False
        return None

    def print_tree(self, node=None, level=0):
        """Print a preorder traversal with indentation for reporting depth."""
        if node is None:
            if level == 0:
                node = self.root
                if node is None:
                    print("The team structure is empty.")
                    return
            else:
                return
        print("    " * level + "- " + node.name)
        self.print_tree(node.left, level + 1)
        self.print_tree(node.right, level + 1)


# Starter menu retained with input validation and a runnable entry point.
def company_directory():
    tree = TeamTree()
    while True:
        print("\nTeam Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            if tree.root is not None:
                print("Error: Team lead already exists.")
            else:
                name = input("Enter team lead's name: ").strip()
                try:
                    tree.root = EmployeeNode(name)
                except ValueError as error:
                    print(f"Error: {error}")
                else:
                    print(f"Success: {name} added as the team lead.")
        elif choice == "2":
            manager = input("Enter the manager's name: ")
            employee = input("Enter the new employee's name: ")
            side = input("Should this employee be on the LEFT or RIGHT of the manager? ")
            tree.insert(manager, employee, side)
        elif choice == "3":
            print("\nCurrent Team Structure:")
            tree.print_tree()
        elif choice == "4":
            print("Good Bye!")
            break
        else:
            print("Error: Invalid option. Try again.")


if __name__ == "__main__":
    company_directory()


"""
Design Memo

The directory uses an EmployeeNode for each person and a TeamTree to manage
the root. Each node stores a name and two references, left and right. These
references represent direct reports instead of alphabetical ordering. The
directory itself does not use a list or dictionary to store employees.

Recursive insertion starts at the root and compares the current employee's
name with the requested manager. If they match, it checks the selected side
before creating a new node. Otherwise, it searches the left subtree and then
the right subtree. Each recursive call handles a smaller part of the same
search. Returning a result stops the search after the manager is found.

The main implementation challenge was distinguishing an unsuccessful subtree
search from a rejected insertion. A manager might be absent from the left
branch but present in the right branch. Reporting an error immediately would
therefore be incorrect. The implementation returns None for an unsuccessful
internal search and prints the missing-manager message only after the full
search finishes. It also avoids passing empty children into insert, because
the default None argument means to start at the root. Occupied positions,
invalid sides, blank names, and duplicate names are rejected without changing
the existing hierarchy.

Trees are useful when relationships matter, such as reporting structures,
folders, and nested document elements. A subtree naturally groups a manager
with that manager's reports. This tree is not a binary search tree, so finding
a name can require O(n) time. Recursive searches use O(h) stack space, where
h is tree height. A long reporting chain can reach Python's recursion limit.
"""
