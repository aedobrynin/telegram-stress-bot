from random import sample
from typing import Set


def get_word_id(ids: Set[int]) -> int:
    """Picks random word id from the set. The Id is removed from the set."""
    picked_id = sample(ids, 1)[0]
    ids.remove(picked_id)
    return picked_id
