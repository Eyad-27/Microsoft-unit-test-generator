import ast
from config import ERROR_MSG


def validate_source(source_code):
    """Check that the input is valid Python containing at least one function."""
    if not source_code or not source_code.strip():
        return False, ERROR_MSG

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return False, ERROR_MSG

    has_function = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        for node in ast.walk(tree)
    )

    if not has_function:
        return False, ERROR_MSG

    return True, source_code
