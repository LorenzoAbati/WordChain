import logging

from aiohttp import web

import time

from WordChainApp.Services.Validator import Validator
from WordChainApp.DataBase.DataBase import DataBase
from WordChainApp.Services.Agent import Agent


class WordChainApp:

    TIMEOUT = 120  # seconds

    def __init__(self, storage_location):
        self.database = DataBase(app=self, database_location=storage_location)
        self.agent = Agent(app=self, words_location=storage_location)
        self.validator = Validator(app=self)

        self._web_app = web.Application(middlewares=list(self.validator.middlewares))

        self.last_request_timestamps = {}

        self._set_routes()
        self._start_web_app()

    def _set_routes(self):
        self._web_app.add_routes([
            web.get('/start/', self._start_game),
            web.get('/game/', self._game),
            web.get('/stop/', self._stop_game),
            web.get('/progress/', self._get_progress)
        ])

    def _start_web_app(self):
        web.run_app(self._web_app)

    async def _start_game(self, request=None):
        email = request.query.get('email')
        game_id = self.agent.start_game(email)

        return web.json_response({'game_id': game_id}, status=200)

    async def _game(self, request=None):
        session_id = request.query.get('session_id')
        game_id = request.query.get('game_id')
        word = request.query.get('word')
        email = request.query.get('email')

        # Check if this session ID has been seen before
        if session_id in self.last_request_timestamps:
            # Check if the previous request was more than two minutes ago
            last_request_time = self.last_request_timestamps[session_id]
            time_since_last_request = time.time() - last_request_time
            if time_since_last_request > WordChainApp.TIMEOUT:
                # Return a timeout error
                return web.Response(text=f"more than {WordChainApp.TIMEOUT} seconds have passed, you lost the match,"
                                         f"these are your scores: {self.database.get_score(email)}")

        # Record the timestamp of this request
        self.last_request_timestamps[session_id] = time.time()

        logging.info(f"received a new word: {word}")
        result = await self.agent.game(game_id, word)
        logging.info(f"sending result: {result}")

        return web.Response(text=f"{result}")

    async def _stop_game(self, request=None):
        return web.Response(text="game stopped", status=200)

    async def _get_progress(self, request=None):
        email = request.query.get('email')
        return web.Response(text=str(self.database.get_score(email)))
