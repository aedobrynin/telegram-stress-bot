from random import sample
from typing import Set
from models import Word


def get_word(words: Set[Word]) -> Word:
    """Picks random word from set. Word is removed from the set."""
    picked_word = sample(words, 1)[0]
    words.remove(picked_word)
    return picked_word
