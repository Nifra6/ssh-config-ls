"""Provide completions for words in an SSH config."""

import re

from ssh_config_ls.lexer import Keyword

# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def get_completion(line: str, position: int) -> list[str]:
    """Get all completions for a word.

    Args:
        line: A line from an SSH config.
        position: Position of the cursor.

    Returns:
        All possible completions for the current word.
    """
    word = re.search(r"\S+", line)
    if word and word.start() <= position <= word.end():
        return _get_possible_keywords(word.group())
    return []


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _get_possible_keywords(word: str) -> list[str]:
    """Return all keywords that contains the given subword."""
    return [kw.name for kw in Keyword if word.lower() in kw.lower()]
