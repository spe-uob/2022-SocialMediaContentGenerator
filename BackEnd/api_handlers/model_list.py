from typing import Optional, Awaitable

import tornado.web


class ModelList(tornado.web.RequestHandler):
    router = r"/model_list"

    def __init__(self, application, request, **kwargs):
        self.model_list = []
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, model_list):
        self.model_list = model_list

    def get(self):
        self.write({"mode_list": self.model_list})
