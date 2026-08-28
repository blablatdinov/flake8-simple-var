# SPDX-FileCopyrightText: Copyright (c) 2025-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

"""Tests for flake8-simple-var plugin."""

import ast

from flake8_simple_var.entry import Plugin, VariableNameVisitor


class TestVariableNameVisitor:
    """Test VariableNameVisitor class."""

    def test_single_word_names_are_valid(self) -> None:
        """Test that single word names are valid."""
        code = '\n'.join(
            [
                'x = 1',
                "name = 'test'",
                'value = 42',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_camel_case_names_are_invalid(self) -> None:
        """Test that camelCase names are invalid."""
        code = '\n'.join(
            [
                'textLength = 10',
                "userName = 'john'",
                'currentValue = 42',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 3
        assert any('textLength' in str(error) for error in visitor.errors)
        assert any('userName' in str(error) for error in visitor.errors)
        assert any('currentValue' in str(error) for error in visitor.errors)

    def test_snake_case_names_are_invalid(self) -> None:
        """Test that snake_case names are invalid."""
        code = '\n'.join(
            [
                "table_name = 'users'",
                "current_user_email = 'test@example.com'",
                "file_path = '/tmp/file.txt'",
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 3
        assert any('table_name' in str(error) for error in visitor.errors)
        assert any('current_user_email' in str(error) for error in visitor.errors)
        assert any('file_path' in str(error) for error in visitor.errors)

    def test_private_variables_are_ignored(self) -> None:
        """Test that private variables (starting with _) are ignored."""
        code = '\n'.join(
            [
                '_private_var = 1',
                '__very_private = 2',
                '_ = 3',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_function_arguments_are_checked(self) -> None:
        """Test that function arguments are checked."""
        code = '\n'.join(
            [
                'def process_data(user_name, file_path):',
                '    return user_name + file_path',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 2
        assert any('SVN200' in str(error) for error in visitor.errors)
        assert any('user_name' in str(error) for error in visitor.errors)
        assert any('file_path' in str(error) for error in visitor.errors)

    def test_for_loop_variables_are_checked(self) -> None:
        """Test that for loop variables are checked."""
        code = '\n'.join(
            [
                'for item_name in items:',
                '    print(item_name)',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN200' in str(error) for error in visitor.errors)
        assert any('item_name' in str(error) for error in visitor.errors)

    def test_comprehension_variables_are_checked(self) -> None:
        """Test that comprehension variables are checked."""
        code = '\n'.join(
            [
                'result = [x * 2 for x in numbers]',
                'filtered = [item_name for item_name in items if item_name]',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN200' in str(error) for error in visitor.errors)
        assert any('item_name' in str(error) for error in visitor.errors)

    def test_exception_handler_variables_are_checked(self) -> None:
        """Test that exception handler variables are checked."""
        code = '\n'.join(
            [
                'try:',
                '    pass',
                'except ValueError as error_message:',
                '    print(error_message)',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN300' in str(error) for error in visitor.errors)
        assert any('error_message' in str(error) for error in visitor.errors)

    def test_with_statement_variables_are_checked(self) -> None:
        """Test that with statement variables are checked."""
        code = '\n'.join(
            [
                "with open('file.txt') as file_handle:",
                '    content = file_handle.read()',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN400' in str(error) for error in visitor.errors)
        assert any('file_handle' in str(error) for error in visitor.errors)

    def test_annotated_assignments_are_checked(self) -> None:
        """Test that annotated assignments are checked."""
        code = '\n'.join(
            [
                "user_name: str = 'john'",
                'count: int = 42',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN100' in str(error) for error in visitor.errors)
        assert any('user_name' in str(error) for error in visitor.errors)

    def test_empty_name_is_ignored(self) -> None:
        """Test that empty names are ignored."""
        code = '\n'.join(
            [
                'try:',
                '    pass',
                'except ValueError:',
                '    pass',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_with_statement_without_variable_is_ignored(self) -> None:
        """Test that with statement without variable is ignored."""
        code = '\n'.join(
            [
                "with open('file.txt'):",
                '    pass',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_multiple_assignments_are_checked(self) -> None:
        """Test that multiple assignments are checked."""
        code = '\n'.join(
            [
                'a, b, c = 1, 2, 3',
                'x, y, z = get_values()',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_upper_case_names_are_invalid(self) -> None:
        """Test that UPPER_CASE names are invalid."""
        code = '\n'.join(
            [
                "USER_NAME = 'john'",
                "FILE_PATH = '/tmp/file.txt'",
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 2
        assert any('USER_NAME' in str(error) for error in visitor.errors)
        assert any('FILE_PATH' in str(error) for error in visitor.errors)

    def test_mixed_case_names_are_invalid(self) -> None:
        """Test that mixed case names are invalid."""
        code = '\n'.join(
            [
                "userName = 'john'",
                "filePath = '/tmp/file.txt'",
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 2
        assert any('userName' in str(error) for error in visitor.errors)
        assert any('filePath' in str(error) for error in visitor.errors)

    def test_annotated_assignments_with_non_name_targets(self) -> None:
        """Test that annotated assignments with non-Name targets are handled."""
        code = '\n'.join(
            [
                'class MyClass:',
                '    pass',
                'obj: MyClass = MyClass()',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_assignments_with_non_name_targets(self) -> None:
        """Test that assignments with non-Name targets are handled."""
        code = '\n'.join(
            [
                'a, b = 1, 2',
                '(a, b) = (3, 4)',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_for_loops_with_non_name_targets(self) -> None:
        """Test that for loops with non-Name targets are handled."""
        code = '\n'.join(
            [
                'for a, b in [(1, 2), (3, 4)]:',
                '    print(a, b)',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_comprehensions_with_non_name_targets(self) -> None:
        """Test that comprehensions with non-Name targets are handled."""
        code = '\n'.join(
            [
                'result = [(a, b) for a, b in [(1, 2), (3, 4)]]',
            ],
        )
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 0

    def test_global_variables_code(self) -> None:
        code = """
user_name = "john"
"""
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN100' in str(error) for error in visitor.errors)
        assert any('user_name' in str(error) for error in visitor.errors)

    def test_local_variables_in_function(self) -> None:
        """Test that local variables in functions use SVN100."""
        code = """
def test_function():
    local_var = 42
    return local_var
"""
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN100' in str(error) for error in visitor.errors)
        assert any('local_var' in str(error) for error in visitor.errors)

    def test_local_variables_in_class(self) -> None:
        """Test that local variables in classes use SVN100."""
        code = """
class TestClass:
    def __init__(self):
        instance_var = 42
        self.value = instance_var
"""
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        assert len(visitor.errors) == 1
        assert any('SVN100' in str(error) for error in visitor.errors)
        assert any('instance_var' in str(error) for error in visitor.errors)

    def test_mixed_global_and_local_variables(self) -> None:
        """Test that global and local variables use different error codes."""
        code = """
global_var = "global"
user_name = "global_user"

def test_function():
    local_var = "local"
    user_name = "local_user"
    return local_var + user_name
"""
        tree = ast.parse(code)
        visitor = VariableNameVisitor()
        visitor.visit(tree)

        # Should have 4 errors: 2 global (SVN500) + 2 local (SVN100)
        assert len(visitor.errors) == 4
        
        # Check global variables
        global_errors = [e for e in visitor.errors if 'SVN500' in str(e)]
        assert len(global_errors) == 2
        assert any('global_var' in str(error) for error in global_errors)
        assert any('user_name' in str(error) for error in global_errors)
        
        # Check local variables
        local_errors = [e for e in visitor.errors if 'SVN100' in str(e)]
        assert len(local_errors) == 2
        assert any('local_var' in str(error) for error in local_errors)
        assert any('user_name' in str(error) for error in local_errors)


class TestPlugin:
    """Test Plugin class."""

    def test_plugin_returns_errors(self) -> None:
        """Test that plugin returns errors for invalid variable names."""
        code = '\n'.join(
            [
                'textLength = 10',
                "table_name = 'users'",
            ],
        )
        tree = ast.parse(code)
        plugin = Plugin(tree)
        errors = list(plugin.run())

        assert len(errors) == 2
        assert any('SVN100' in str(error) for error in errors)

    def test_plugin_returns_no_errors_for_valid_names(self) -> None:
        """Test that plugin returns no errors for valid variable names."""
        code = '\n'.join(
            [
                'x = 1',
                "name = 'test'",
                'value = 42',
            ],
        )
        tree = ast.parse(code)
        plugin = Plugin(tree)
        errors = list(plugin.run())

        assert len(errors) == 0

    def test_plugin_metadata(self) -> None:
        """Test plugin metadata."""
        tree = ast.parse('x = 1')
        plugin = Plugin(tree)

        assert plugin.name == 'flake8-simple-var'
        assert plugin.version == '0.1.0'

    def test_plugin_with_complex_code(self) -> None:
        """Test plugin with complex code containing various variable types."""
        code = '\n'.join(
            [
                'def process_user_data(user_name, file_path):',
                '    with open(file_path) as file_handle:',
                '        content = file_handle.read()',
                '',
                '    for line in content.splitlines():',
                '        if line.strip():',
                '            processed_line = line.strip()',
                '            yield processed_line',
                '',
                'try:',
                "    result = process_user_data('john', 'data.txt')",
                'except ValueError as error_message:',
                '    print(error_message)',
            ],
        )
        tree = ast.parse(code)
        plugin = Plugin(tree)
        errors = list(plugin.run())

        assert len(errors) == 5
        assert any('SVN100' in str(error) for error in errors)
        assert any('SVN200' in str(error) for error in errors)
        assert any('SVN300' in str(error) for error in errors)
        assert any('SVN400' in str(error) for error in errors)
