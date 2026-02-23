import ast
import re


class _DocstringStripper(ast.NodeTransformer):
    """Removes docstrings from all function, class, and module nodes."""

    def _strip(self, node):
        if (node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
            node.body = node.body[1:] or [ast.Pass()]
        return node

    def visit_Module(self, node):
        self.generic_visit(node)
        return self._strip(node)

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        return self._strip(node)

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        return self._strip(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        return self._strip(node)


# Patterns that look like prompt injection attempts
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?|rules?)",
    r"you\s+are\s+now",
    r"forget\s+(all\s+)?(previous|above|prior)",
    r"system\s*:\s*",
    r"assistant\s*:\s*",
    r"override\s+(instructions?|prompts?|rules?)",
]


def sanitize(source_code):
    """
    Strip comments and docstrings from source code to prevent prompt injection.
    Uses ast.parse + ast.unparse to rebuild clean code, then scrubs known
    injection patterns from any remaining string literals.
    """
    tree = ast.parse(source_code)
    tree = _DocstringStripper().visit(tree)
    ast.fix_missing_locations(tree)

    clean = ast.unparse(tree)

    for pattern in INJECTION_PATTERNS:
        clean = re.sub(pattern, "", clean, flags=re.IGNORECASE)

    return clean
