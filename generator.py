import re
import ast
from openai import OpenAI
from config import GITHUB_TOKEN, MODEL_NAME, API_BASE, TEMPERATURE, TOP_P, MAX_TOKENS, SYSTEM_PROMPT


def _clean_response(text):
    """Strip markdown fences and leading prose that the model might sneak in."""
    text = text.strip()
    text = re.sub(r"^```(?:python)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    # Skip any leading lines that aren't Python code
    lines = text.split("\n")
    code_starts = ("import ", "from ", "def ", "class ", "#", "@", "    ", "\t")
    for i, line in enumerate(lines):
        s = line.strip()
        if s == "" or any(s.startswith(p) for p in code_starts):
            text = "\n".join(lines[i:])
            break

    # Quick syntax check — if it fails, still return what we got
    try:
        ast.parse(text)
    except SyntaxError:
        pass

    return text


def generate_tests(sanitized_code):
    """Send the sanitized function to the LLM and return generated unit tests."""
    client = OpenAI(api_key=GITHUB_TOKEN, base_url=API_BASE)

    prompt = (
        "Generate comprehensive unit tests for the following Python function.\n"
        "Output ONLY valid Python unittest code. No markdown, no explanation.\n\n"
        + sanitized_code
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
    )

    return _clean_response(response.choices[0].message.content)
