# Microsoft Unit Test Generator

A CLI tool that generates Python unit tests for a given function using an LLM.

## Project Structure

```
├── main.py             # CLI entry point
├── config.py           # Environment variables, model settings, system prompt
├── validator.py        # AST-based input validation
├── sanitizer.py        # Comment/docstring stripping & prompt injection prevention
├── generator.py        # LLM API call & output cleaning
├── requirements.txt
├── .env                # API key (not committed)
└── examples/
    ├── sample_function.py
    ├── factorial.py
    └── palindrome.py
```

## Setup

1. **Clone and install:**

   ```bash
   git clone https://github.com/Eyad-27/Microsoft-unit-test-generator.git
   cd Microsoft-unit-test-generator
   pip install -r requirements.txt
   ```

2. **Add your GitHub token:**

   Create a `.env` file:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```
   You can generate a token at [github.com/settings/tokens](https://github.com/settings/tokens).
   The token must have access to [GitHub Models](https://github.com/marketplace/models).

## Usage

```bash
# From a file
python main.py --file examples/factorial.py

# Inline code
python main.py --code "def add(a, b): return a + b"

# From stdin
cat examples/palindrome.py | python main.py --stdin

# Save to file
python main.py --file examples/factorial.py --output test_factorial.py
```

## Example

**Input:**
```python
def add(a, b):
    return a + b
```

**Output:**
```python
import unittest
from source import add

class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)

    def test_add_mixed(self):
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
```

## Error Handling

| Scenario | Output |
|----------|--------|
| No function in input | `Error: This tool only generates unit tests for functions.` |
| Invalid Python syntax | `Error: This tool only generates unit tests for functions.` |
| Natural language input | `Error: This tool only generates unit tests for functions.` |
| Missing API key | `Error: GITHUB_TOKEN not set. Add it to your .env file.` |
| File not found | `Error: File 'path' not found.` |

## How It Works

1. **Parse** — reads input from `--file`, `--code`, or `--stdin`.
2. **Validate** — uses `ast.parse()` to check for valid Python containing at least one function definition.
3. **Sanitize** — strips comments, docstrings, and prompt injection patterns before sending to the LLM.
4. **Generate** — sends the cleaned code to GPT-4o-mini via GitHub Models with a strict system prompt (temperature = 0).
5. **Clean** — removes any markdown fences or prose from the response, returning only valid Python test code.

```
Input → [Parser] → [Validator] → [Sanitizer] → [LLM] → [Cleaner] → Output
```

## Security

- Comments and docstrings are stripped via AST before code reaches the LLM.
- Regex-based detection removes common prompt injection phrases.
- The API key is loaded from `.env` and never printed or included in output.

## License

MIT — see [LICENSE](LICENSE).
