import base64
import json
from typing import Optional, Awaitable

import cv2
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
            result = self.core.exec_img2img(
                prompt=data['prompt'],
                sample=data['sample'],
                batch_size=data['batch_size'],
                step=data['step'],
                cfg=data['cfg'],
                width=data['width'],
                height=data['height'],
                image=data['image']
            )

            retval, buffer = cv2.imencode('.jpg', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
            pic_str = base64.b64encode(buffer)
            pic_str = pic_str.decode()
            self.write({"status": 0, "image": f"data:image/jpg;base64,{pic_str}"})
        except Exception as e:
            self.write({"error": str(e)})
