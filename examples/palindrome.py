def is_palindrome(s):
    """Check whether a string is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
