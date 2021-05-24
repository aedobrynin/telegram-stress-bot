import unittest
from models import Session, Word


class WordsTest(unittest.TestCase):
    def test_word_and_bad_variant_equality(self):
        session = Session()
        for word in session.query(Word).all():
            self.assertEqual(word.word.lower(), word.bad_variant.lower())
        session.close()

    def test_only_one_stress_in_word(self):
        session = Session()
        for word in session.query(Word).all():
            self.assertEqual(1, sum([char.isupper() for char in word.word]))
            self.assertEqual(
                1,
                sum([char.isupper() for char in word.bad_variant])
            )
        session.close()


if __name__ == "__main__":
    unittest.main()
