from typing import Optional, Awaitable

import tornado.web



class VAEList(tornado.web.RequestHandler):
    router = r"/vae_list"

    def __init__(self, application, request, **kwargs):
        self.vae_list = []
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

    def initialize(self, model_dir):
        self.model_dir = model_dir

    def get(self):
        # self.vae_list = Model.find_vae(self.model_dir)
        self.write({"mode_list": self.vae_list})
