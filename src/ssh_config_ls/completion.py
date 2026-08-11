"""Provide completions for words in an SSH config."""


# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------

from ssh_config_ls.keywords import Keyword


def get_completion(line: str, position: int) -> list[str]:
    """Get keyword completions for the current word at the cursor position.

    Args:
        line: A line from an SSH config.
        position: Position of the cursor in the line.

    Returns:
        All keywords containing the current word as a substring,
        or an empty list if the cursor is not on the first word.
    """
    words = line[:position].split()
    if len(words) == 1:
        return _get_possible_keywords(words[0])
    return []


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _get_possible_keywords(word: str) -> list[str]:
    """Return all keywords containing the given string as a substring.

    Args:
        word: The partial word to match against keyword names.

    Returns:
        Canonical names of all matching keywords.
    """
    return [
        kw.value.canonical
        for kw in Keyword
        if word.lower() in kw.value.canonical.lower()
    ]
