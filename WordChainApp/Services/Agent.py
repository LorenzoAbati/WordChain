import json
import logging


class Agent:

    TIMEOUT = 120  # seconds

    def __init__(self, app, words_location):
        self._app = app

        self._current_words = {int: str}  # {game_id: last_word}
        self._banned_words = {int: [str]}  # {game_id: list_of_already_used_words}

        try:
            with open(words_location + '/words.json', 'r') as f:
                self._words_list = json.load(f)
        except Exception as e:
            logging.exception(e)

    def start_game(self, user_email):
        game_id = self._app.database.create_new_history(player=user_email)
        return game_id

    async def game(self, game_id, word):

        if not game_id or not word:
            return {'error': 'Missing game_id or word parameter', 'status': 200}

        # checking that the word is an actual word
        if word not in self._words_list:
            return {'error': 'This is not a word'}

        # check if this is the first word
        if game_id in self._current_words:
            # get the last word played in the game
            last_word = self._current_words[game_id]

            # check if the user's word starts with the last letter of the last word played
            if last_word and last_word[-1].lower() != word.lower()[0]:
                return {'error': f'Invalid word, must start with the last letter of the previous word {last_word}', 'status': 200}
        else:
            self._current_words[game_id] = word

        # check if the users word is in banned words
        if game_id in self._banned_words:
            if word in self._banned_words[game_id]:
                return {'error': 'Invalid word, already used', 'status': 200}
        else:
            self._banned_words[game_id] = []

        # all the checks are passed the user can receive a point, updating score in db
        self._app.database.add_point(game_id=game_id, word=word)

        # add users word to banned words
        self._banned_words[game_id].append(word)

        # get a new word that starts with the last letter of the user's word
        new_word = self.get_word(word)

        # add servers word to banned words
        self._banned_words[game_id].append(new_word)

        # add the new word to the hashmap
        self._current_words[game_id] = new_word

        return {'word': new_word, 'status': 200}

    def get_word(self, word):
        last_letter = word[-1].lower()
        for w in self._words_list:
            if w in self._banned_words:
                continue
            if w[0].lower() == last_letter:
                return w
        else:
            return {"you won"}

    async def stop_game(self):
        return {"message": "game ended"}
