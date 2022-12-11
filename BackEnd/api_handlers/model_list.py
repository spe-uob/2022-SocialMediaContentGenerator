from typing import Optional, Awaitable

import tornado.web

from stable_diffusion.model import Model


class ModelList(tornado.web.RequestHandler):
    router = r"/model_list"

    def __init__(self, application, request, **kwargs):
        self.model_list = []
        self.model_dir = ""
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, model_dir):
        self.model_dir = model_dir

    def get(self):
        self.model_list = Model.find_model(self.model_dir)
        self.write({"mode_list": self.model_list})
