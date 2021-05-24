import json
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    bad_variant = Column(String, nullable=False)
    success_count = Column(Integer, server_default=text('0'), nullable=False)
    total_count = Column(Integer, server_default=text('0'), nullable=False)

    def __repr__(self) -> str:
        return f'<Word({self.id}, {self.word}, {self.bad_variant}, '\
                f'{self.success_count}, {self.total_count})>'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    total_games = Column(Integer, server_default=text('0'), nullable=False)
    best_score = Column(Integer, server_default=text('0'), nullable=False)
    stats_by_word_id_json =\
        Column(String, server_default=text("'{}'"), nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.total_games = 0
        self.best_score = 0
        self.stats_by_word_id_json = json.dumps(dict())

    def __repr__(self) -> str:
        return f'<User({self.id}, {self.total_games}, {self.best_score}, '\
                f'{self.lost_count_by_id_json})>'

    def update_best_score(self, score: int) -> None:
        self.best_score = max(self.best_score, score)

    def update_stats(self, word_id: int, win: bool) -> None:
        stats = json.loads(self.stats_by_word_id_json)

        if word_id not in stats:
            stats[word_id] = [0, 0]

        stats[word_id][1] += 1
        if win:
            stats[word_id][0] += 1

        self.stats_by_word_id_json = json.dumps(stats)


Base.metadata.create_all(engine)
