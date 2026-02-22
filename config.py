import os
import sys
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 4096
API_BASE = "https://models.inference.ai.azure.com"

SYSTEM_PROMPT = (
    "You are a unit test generator. Your ONLY job is to produce Python unit tests.\n\n"
    "RULES:\n"
    "1. Output ONLY valid Python code using the unittest framework.\n"
    "2. Do NOT include any explanation, commentary, markdown fences, or extra text.\n"
    "3. Import the function under test assuming it lives in a module called `source`.\n"
    "4. Cover normal cases, edge cases (empty input, zero, None, negatives, "
    "boundary values, type errors) and expected exceptions.\n"
    "5. Each test method must have a descriptive name starting with test_.\n"
    "6. End with if __name__ == '__main__': unittest.main().\n"
    "7. Output raw Python code ONLY."
)

ERROR_MSG = "Error: This tool only generates unit tests for functions."


def check_api_key():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not set. Add it to your .env file.")
        sys.exit(1)
