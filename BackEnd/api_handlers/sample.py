import json
from typing import Optional, Awaitable

import tornado.web

from stable_diffusion.core import Core


class Sample(tornado.web.RequestHandler):
    router = r"/load_model"

    def __init__(self, application, request, **kwargs):
        self.core: Core = None
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, core: Core):
        self.core = core

    def post(self):
        post_data = self.request.body.decode('utf-8')
        try:
            data = json.loads(post_data)
            self.core.exec_sample(
                prompt=data['prompt'],
                sample=data['sample'],
                batch_size=data['batch_size'],
                step=data['step'],
                cfg=data['cfg'],
                width=data['width'],
                height=data['height']
            )
            self.write({"status": 0})
        except Exception as e:
            self.write({"error": str(e)})
