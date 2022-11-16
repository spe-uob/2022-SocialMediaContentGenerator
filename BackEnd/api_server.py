import asyncio

import tornado.web


class Application:
    def __init__(self, port, host="0.0.0.0"):
        self.handlers = []
        self.port = port
        self.host = host

    def register_handler(self, handler):
        self.handlers.append(handler)

    def build_app(self):
        return tornado.web.Application([(r"/", handler) for handler in self.handlers])

    async def run(self):
        app = self.build_app()
        app.listen(8888)
        await asyncio.Event().wait()
