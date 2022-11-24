from typing import Optional, Awaitable

import tornado.web


class ModelList(tornado.web.RequestHandler):
    router = r"/load_model"

    def __init__(self, application, request, **kwargs):
        self.on_load_model = lambda model_name: None
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, on_load_model):
        self.on_load_model = on_load_model

    def get(self):
        model_name = self.get_argument('ModelName', None)
        try:
            self.on_load_model(model_name)
            self.write({"status": 0})
        except Exception as e:
            self.write({"error": str(e)})
