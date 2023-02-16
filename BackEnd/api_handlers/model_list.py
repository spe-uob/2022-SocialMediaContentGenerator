from typing import Optional, Awaitable

import tornado.web

from stable_diffusion.core import Core
from stable_diffusion.model import StableDiffusionModel


class ModelList(tornado.web.RequestHandler):
    router = r"/model_list"

    def __init__(self, application, request, **kwargs):
        self.core = None
        self.model_list = []
        self.model_dir = ""
        super().__init__(application, request, **kwargs)

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, core: Core):
        self.core = core

    def get(self):
        self.model_list = list(self.core.model_loader.checkpoints.keys())
        self.write({"mode_list": self.model_list})
