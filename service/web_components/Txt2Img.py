import base64

import cv2
import numpy as np
from flask import request

from utility import TaskStatus
from . import *


class Txt2Img(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/sample', 'Txt2Img', ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        prompt = data['prompts']
        negative_prompt = data['negative_prompt']
        sampler = data['sample']
        step = data['step']
        width = data['width']
        height = data['height']
        n_iter = data['n_iter']
        batch_size = data['batch_size']
        cfg = data['cfg']
        task_uuid = self.env.scheduler.add_task_txt2img(prompt, negative_prompt, sampler, step, width, height, n_iter, batch_size, cfg)
        return {"status": 0, "uuid": task_uuid, "length": n_iter * batch_size}


class Txt2ImgResult(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/get_sample_result', 'Txt2ImgResult', ['GET'])
        self.env = env

    def view(self):
        uuid_str = request.args.get('uuid')
        length = int(request.args.get('length'))
        loaded = int(request.args.get('loaded'))
        task = self.env.scheduler.get_task(uuid_str)
        if task is None:
            return {"status": 1}
        if task.task_status == TaskStatus.Pending:
            return {"status": 0, "images": []}
        result = task.result
        response = {"status": 0, "images": []}
        for image, seed in result[loaded:len(result)]:
            retval, buffer = cv2.imencode('.jpg', cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            pic_str = base64.b64encode(buffer)
            pic_str = pic_str.decode()
            response['images'].append(f"data:image/jpg;base64,{pic_str}")
        return response
