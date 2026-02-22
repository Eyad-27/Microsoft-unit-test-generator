import argparse
import sys

from config import ERROR_MSG, check_api_key
from validator import validate_source
from sanitizer import sanitize
from generator import generate_tests


def read_input(args):
    """Read source code from the chosen input method."""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        except IOError as e:
            print(f"Error: Could not read file '{args.file}': {e}")
            sys.exit(1)

    if args.code:
        return args.code

    if args.stdin:
        if sys.stdin.isatty():
            print("Error: No input piped to stdin.")
            sys.exit(1)
        return sys.stdin.read()

    return None


def build_parser():
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="unit-test-generator",
        description="Generate Python unit tests for a given function using an LLM.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to a Python source file.")
    group.add_argument("--code", type=str, help="Inline Python source code string.")
    group.add_argument("--stdin", action="store_true", help="Read from standard input.")
    parser.add_argument("--output", "-o", type=str, help="Save generated tests to a file.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    check_api_key()

    source_code = read_input(args)
    if source_code is None:
        print(ERROR_MSG)
        sys.exit(1)

    is_valid, result = validate_source(source_code)
    if not is_valid:
        print(result)
        sys.exit(1)

    sanitized = sanitize(source_code)

    try:
        tests = generate_tests(sanitized)
    except Exception as e:
        print(f"Error: Failed to generate tests — {e}")
        sys.exit(1)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(tests)
            print(f"Tests written to {args.output}")
        except IOError as e:
            print(f"Error: Could not write to '{args.output}': {e}")
            sys.exit(1)
    else:
        print(tests)


if __name__ == "__main__":
    main()
