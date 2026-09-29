MAX_INPUT_CHARS = 12000
MAX_LINES = 1000

def sort_lines(text: str, reverse: bool = False):
    if not text or not text.strip():
        raise ValueError("Please send some text to sort.")
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError(
            f"Your text is too long. Please keep it under {MAX_INPUT_CHARS:,} characters."
        )

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("I couldn't find any non-empty lines to sort.")
    if len(lines) > MAX_LINES:
        raise ValueError(
            f"Please send no more than {MAX_LINES:,} non-empty lines at a time."
        )

    sorted_lines = sorted(lines, key=str.casefold, reverse=reverse)
    return "\n".join(sorted_lines), len(lines)
