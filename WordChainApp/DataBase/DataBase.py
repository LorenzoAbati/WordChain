from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os
import json


Base = declarative_base()


class DataBase:

    def __init__(self, app, database_location):
        self.app = app

        self.location = os.path.abspath(database_location)

        self.engine = create_engine("sqlite:///" + self.location + "/storage.db")
        self.session = sessionmaker(bind=self.engine)()

        self._init_all_tables()

    def create_new_history(self, player):
        # create a new history record
        new_history = History(score=0, player=player)

        # add the new record to the session and commit
        self.session.add(new_history)
        self.session.commit()

        # retrieve the game_id of the new record
        return new_history.game_id

    def get_score(self, user):
        records = self.session.query(History).filter_by(player=user).all()
        score_list = [{"game_id": record.game_id, "score": record.score} for record in records]
        return json.dumps(score_list)

    def add_point(self, game_id, word):
        record = self.session.query(History).filter_by(game_id=game_id).first()
        consonants = sum(1 for c in word if c.isalpha() and c.lower() not in 'aeiou')
        vowels = sum(1 for c in word if c.isalpha() and c.lower() in 'aeiou')
        record.score += consonants + 2 * vowels
        self.session.commit()

    @staticmethod
    def _init_all_tables():
        User()
        History()


class User(Base):
    __tablename__ = 'user'
    email = Column(String, primary_key=True)


class History(Base):
    __tablename__ = 'history'
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer)
    player = Column(String)
