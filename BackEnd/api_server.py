import asyncio

import tornado.web


class Application:
    def __init__(self, port, host="0.0.0.0"):
        self.components = []
        self.port = port
        self.host = host

    def register_handler(self, router, handler, params: dict):
        self.components.append({"class": handler, "params": params, "router": router})

    def build_app(self):
        return tornado.web.Application(
            [
                (component["router"],
                 component["class"],
                 component["params"]) for component in self.components
            ])

    async def run(self):
        app = self.build_app()
        app.listen(8888)
        await asyncio.Event().wait()
