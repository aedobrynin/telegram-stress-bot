from random import sample
from typing import Set, Tuple, List
from sqlalchemy import Float, desc
from sqlalchemy.sql.expression import cast
from models import Session, Word, User


def get_word_id(ids: Set[int]) -> int:
    """Picks random word id from the set. The Id is removed from the set."""
    picked_id = sample(ids, 1)[0]
    ids.remove(picked_id)
    return picked_id


def get_top_five_globally_mistaken() -> List[Tuple[str, float, int]]:
    session = Session()
    query =\
        session.query(Word.word, Word.success_count, Word.total_count)\
        .filter(Word.total_count >= 1)\
        .order_by(cast(Word.success_count, Float) /
                  cast(Word.total_count, Float))\
        .order_by(desc(Word.total_count))\
        .limit(5)\
        .all()

    session.close()

    ret_val = []
    for (word, succ_cnt, tot_cnt) in query:
        ret_val.append((word, round(100 * succ_cnt / tot_cnt, 2), tot_cnt))
    return ret_val


def get_top_five_locally_mistaken(word_stats: dict)\
        -> List[Tuple[str, float, int]]:
    items =\
        list(item for item in word_stats.items() if item[1][0] != item[1][1])
    items.sort(key=lambda x: (1 - x[1][0] / x[1][1], x[1][1]), reverse=True)

    session = Session()

    ret_val = list()
    for i in range(min(len(items), 5)):
        word = session.query(Word).get(items[i][0]).word
        percent = round(100 * items[i][1][0] / items[i][1][1], 2)
        total_cnt = items[i][1][1]
        ret_val.append((word, percent, total_cnt))

    session.close()

    return ret_val


def get_best_players() -> List[Tuple[str, int]]:
    session = Session()
    players =\
        session.query(User.name, User.best_score)\
               .order_by(desc(User.best_score)).limit(3).all()
    session.close()
    return players


def get_total_players_cnt() -> int:
    session = Session()
    total_players = session.query(User).count()
    session.close()
    return total_players
