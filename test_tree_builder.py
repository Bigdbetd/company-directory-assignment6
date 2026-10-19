import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tree_builder import EmployeeNode, TeamTree, company_directory


class DirectoryTests(unittest.TestCase):
    def capture(self, function, *args):
        output = io.StringIO()
        with redirect_stdout(output):
            result = function(*args)
        return result, output.getvalue()

    def example(self):
        tree = TeamTree()
        tree.root = EmployeeNode("Jordan")
        for manager, employee, side in (
            ("Jordan", "Riley", "left"), ("Jordan", "Taylor", "right"),
            ("Riley", "Morgan", "left"), ("Riley", "Dana", "right"),
        ):
            self.assertTrue(self.capture(tree.insert, manager, employee, side)[0])
        return tree

    def test_node_and_empty_root(self):
        node = EmployeeNode("John")
        self.assertEqual(node.name, "John")
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertIsNone(TeamTree().root)

    def test_empty_operations(self):
        tree = TeamTree()
        self.assertIn("empty", self.capture(tree.print_tree)[1])
        result, message = self.capture(tree.insert, "Jordan", "Riley", "left")
        self.assertFalse(result)
        self.assertIn("team lead", message)

    def test_required_structure_and_print_order(self):
        tree = self.example()
        self.assertEqual(tree.root.left.right.name, "Dana")
        self.assertEqual(self.capture(tree.print_tree)[1],
                         "- Jordan\n    - Riley\n        - Morgan\n"
                         "        - Dana\n    - Taylor\n")

    def test_searches_right_branch_after_left_fails(self):
        tree = self.example()
        self.assertTrue(self.capture(tree.insert, "Taylor", "Sam", "right")[0])
        self.assertTrue(self.capture(tree.insert, "Sam", "Alex", "left")[0])
        self.assertEqual(tree.root.right.right.left.name, "Alex")

    def test_missing_manager_prints_one_error(self):
        tree = self.example()
        before = self.capture(tree.print_tree)[1]
        result, message = self.capture(tree.insert, "Missing", "Sam", "left")
        self.assertFalse(result)
        self.assertEqual(message.count("does not exist"), 1)
        self.assertEqual(before, self.capture(tree.print_tree)[1])

    def test_occupied_side_preserves_subtree(self):
        tree = self.example()
        original = tree.root.left
        result, message = self.capture(tree.insert, "Jordan", "Sam", "left")
        self.assertFalse(result)
        self.assertIn("occupied", message)
        self.assertIs(tree.root.left, original)
        self.assertEqual(original.left.name, "Morgan")

    def test_validation_and_duplicate_name(self):
        tree = self.example()
        for manager, employee, side in (
            ("Jordan", "Sam", "middle"), ("", "Sam", "left"),
            ("Jordan", "  ", "left"), ("Taylor", "Riley", "left"),
        ):
            with self.subTest(employee=employee, side=side):
                self.assertFalse(self.capture(tree.insert, manager, employee, side)[0])
        self.assertTrue(self.capture(tree.insert, " Taylor ", " Sam ", " LEFT ")[0])
        self.assertEqual(tree.root.right.left.name, "Sam")
        with self.assertRaises(ValueError):
            EmployeeNode(" ")

    def test_subtree_printing_and_leaf_base_case(self):
        tree = self.example()
        self.assertEqual(self.capture(tree.print_tree, tree.root.right)[1], "- Taylor\n")
        self.assertEqual(self.capture(tree.print_tree, None, 1)[1], "")

    def test_cli_full_flow(self):
        answers = ["3", "1", "Jordan", "1", "2", "Jordan", "Riley", "left",
                   "2", "Jordan", "Taylor", "right", "3", "4"]
        with patch("builtins.input", side_effect=answers):
            _, output = self.capture(company_directory)
        self.assertIn("Jordan added as the team lead", output)
        self.assertIn("Team lead already exists", output)
        self.assertIn("- Jordan\n    - Riley\n    - Taylor\n", output)
        self.assertIn("Good Bye!", output)

    def test_cli_invalid_choice_and_blank_lead(self):
        with patch("builtins.input", side_effect=["9", "1", " ", "1", "Jordan", "4"]):
            _, output = self.capture(company_directory)
        self.assertIn("Invalid option", output)
        self.assertIn("nonempty", output)
        self.assertIn("Jordan added as the team lead", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
