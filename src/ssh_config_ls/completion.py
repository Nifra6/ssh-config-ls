"""Provide completions for words in an SSH config."""

from ssh_config_ls.lexer import Keyword

# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def get_completion(line: str) -> list[str]:
    """Get all completions for a word.

    Args:
        line: A line from an SSH config.

    Returns:
        All possible completions for the current word.
    """
    words = line.split()
    if len(words) == 1:
        return _get_possible_keywords(words[0])
    return []


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _get_possible_keywords(word: str) -> list[str]:
    """Return all keywords that contains the given subword."""
    return [kw.name for kw in Keyword if word.lower() in kw.lower()]
