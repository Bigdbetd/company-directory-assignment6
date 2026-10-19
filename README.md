# Company Directory Assignment 6

A custom binary tree represents the company reporting structure. Employees are linked through `EmployeeNode.left` and `EmployeeNode.right`; the directory does not use a list or dictionary to store employees.

## Run the menu

Requires Python 3 and only the standard library.

```bash
python3 tree_builder.py
```

1. Choose **1** to add the team lead.
2. Choose **2** to enter an existing manager, a new employee, and `left` or `right`.
3. Choose **3** to print the hierarchy.
4. Choose **4** to exit.

Names must be unique and nonempty. Names are matched case-sensitively after trimming whitespace; sides are case-insensitive. Errors explain empty trees, missing managers, occupied positions, invalid sides, and duplicate names. Existing reports are never overwritten.

## Example

```python
from tree_builder import EmployeeNode, TeamTree

company_directory = TeamTree()
company_directory.root = EmployeeNode("Jordan")
company_directory.insert("Jordan", "Taylor", "right")
company_directory.insert("Jordan", "Riley", "left")
company_directory.insert("Riley", "Dana", "right")
company_directory.insert("Riley", "Morgan", "left")
company_directory.print_tree()
```

Tree output after the insertion success messages:

```text
- Jordan
    - Riley
        - Morgan
        - Dana
    - Taylor
```

## Tests

```bash
python3 -m unittest -v
```

All 10 tests passed locally. They cover constructors, empty trees, left/right insertion, deeper right-branch searches, missing managers, occupied slots, invalid inputs, duplicate names, exact traversal output, and the interactive menu.

`insert(manager_name, employee_name, side, current_node=None)` performs a recursive depth-first search. Normal calls return `True` on success and `False` on rejection. Internal recursive calls use `None` when a manager is absent from that subtree. `print_tree(node=None, level=0)` recursively prints root, left subtree, then right subtree.

## Design memo

The **263-word design memo** is included in a multiline comment at the bottom of `tree_builder.py`. It discusses recursive insertion, search challenges, applications of trees, search complexity, and recursion limits.

Starter template: https://github.com/RizeComputerScience/COMPSV-Assignment6
