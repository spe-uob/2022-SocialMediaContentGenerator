from typing import Optional, Awaitable

import tornado.web


class LoadVAE(tornado.web.RequestHandler):
    router = r"/load_vae"

    def __init__(self, application, request, **kwargs):
        self.on_load_vae = lambda vae_name: None
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

    def initialize(self, on_load_vae):
        self.on_load_vae = on_load_vae

    def get(self):
        vae_name = self.get_argument('VaeName', None)
        try:
            self.on_load_vae(vae_name)
            self.write({"status": 0})
        except Exception as e:
            self.write({"error": str(e)})
