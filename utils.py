from random import sample


def get_word(words: set) -> dict:
    picked_word = sample(words, 1)[0]
    words.remove(picked_word)
    return picked_word
