import json
import re
import ollama
from prompts import SYSTEM_PROMPT

MODEL = "qwen2.5-coder:3b"


def _extract_json(text: str) -> str:
    """Extract a JSON object from raw model output by locating the outermost braces."""
    start = text.find("{")
    end   = text.rfind("}")
    if start == -1 or end == -1:
        return text
    return text[start : end + 1]


def _regex_fallback(text: str) -> dict | None:
    """
    Fallback parser if json.loads fails.
    Extracts hint fields even if there are unescaped characters or formatting flaws.
    """
    hints = {}
    for i in range(1, 5):
        # Look for "hint_X": "..." with non-greedy match
        match = re.search(rf'"hint_{i}"\s*:\s*"(.*?)(?="\s*,\s*"hint_{i+1}"|"\s*\}})', text, re.DOTALL)
        if match:
            val = match.group(1).replace("\\n", "\n").replace('\\"', '"')
            hints[f"hint_{i}"] = val
        else:
            return None
    return hints


def generate_hints(problem: str, user_approach: str, language: str = "Python") -> dict:
    """
    Send the problem and user's approach to the local model.
    Returns a dict with keys: hint_1, hint_2, hint_3, hint_4.
    """
    user_message = f"""
Problem Statement:
{problem}

User's Current Approach:
{user_approach.strip() if user_approach.strip() else "The user has not started yet."}

Preferred Programming Language for Hint 4: {language}

Generate the 4-level hint ladder now. Ensure all quotes inside JSON strings are properly escaped.
"""

    try:
        # format="json" forces Ollama to constrain generation to valid JSON
        response = ollama.chat(
            model=MODEL,
            format="json",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
        )

        raw_text   = response.message.content
        clean_text = _extract_json(raw_text)

        # strict=False allows literal newlines and control characters inside string values
        try:
            return json.loads(clean_text, strict=False)
        except json.JSONDecodeError:
            fallback = _regex_fallback(clean_text)
            if fallback:
                return fallback
            raise

    except json.JSONDecodeError:
        return _error_hints("The model returned an unexpected format. Please try again.")

    except Exception as e:
        return _error_hints(f"Could not connect to Ollama: {e}. Make sure Ollama is running.")


def _error_hints(message: str) -> dict:
    return {f"hint_{i}": message for i in range(1, 5)}
