
from aiohttp import web

from WordChainApp.DataBase.DataBase import User

import logging


class Validator:

    def __init__(self, app):
        self._app = app

    @property
    def middlewares(self):
        """Return a list with all the middlewares"""
        return [self.authenticate]

    @web.middleware
    async def authenticate(self, request: web.Request, handler):
        """Check if the user has given the necessary credentials"""

        try:
            email = request.query.get('email')
            if email:
                user = self._app.database.session.query(User).filter_by(email=email).first()
                if not user:
                    return web.json_response({'error': 'Email does not exist in the database'}, status=400)
            else:
                return web.Response(text='You have to specify a valid email', status=500)

            # email ok
            return await handler(request)

        except Exception as e:
            logging.exception(e)
            return web.Response(text='Internal Server Error', status=500)

