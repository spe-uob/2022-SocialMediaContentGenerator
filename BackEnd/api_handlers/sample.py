import base64
import json
from typing import Optional, Awaitable

import cv2
import numpy as np
import tornado.web

from stable_diffusion.core import Core


class Sample(tornado.web.RequestHandler):
    router = r"/load_model"

    def __init__(self, application, request, **kwargs):
        self.core: Core = None
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

    def options(self):
        pass

    def post(self):
        post_data = self.request.body.decode('utf-8')
        try:
            data = json.loads(post_data)
            result = self.core.exec_sample(
                prompt=data.get('prompt', ""),
                negative_prompt=data.get('negative_prompt', ""),
                sample=data.get('sample', "dpm"),
                batch_size=data.get('batch_size', 1),
                step=data.get('step', 20),
                cfg=data.get('cfg', 7.5),
                width=data.get('width', 512),
                height=data.get('height', 512),
            )
            response = {"status": 0, "images": []}
            for image in result:
                retval, buffer = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                pic_str = base64.b64encode(buffer)
                pic_str = pic_str.decode()
                response["images"].append(f"data:image/jpg;base64,{pic_str}")
            self.write(response)
        except Exception as e:
            self.write({"error": str(e)})
