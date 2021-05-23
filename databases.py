from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///./databases/words.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    bad_variant = Column(String, nullable=False)
    success_count = Column(Integer, server_default=text('0'), nullable=False)
    total_count = Column(Integer, server_default=text('0'), nullable=False)

    def __init__(self, id: int, word: str, success_count: int,
                 total_count: int) -> None:
        self.id = id
        self.word = word
        self.bad_variant = bad_variant
        self.success_count = success_count
        self.total_count = total_count

    def __repr__(self):
        return f"<Word({self.id}, {self.word}, {self.bad_variant}, {self.success_count}, {self.total_count})>"


Base.metadata.create_all(engine)
