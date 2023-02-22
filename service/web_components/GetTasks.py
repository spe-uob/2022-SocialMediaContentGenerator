from flask import jsonify

from utility import TaskType
from . import *


class GetTasks(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/get_task_info', 'GetTasks', ['GET'])
        self.env = env

    def view(self):
        queue_copy = list(self.env.scheduler.tasks.queue)
        if self.env.scheduler.current_task is not None:
            queue_copy.append(self.env.scheduler.current_task)
        return jsonify([task.to_dict() for task in queue_copy])


class GetTxt2ImgTasks(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/get_txt2img_task_info', 'Txt2Img', ['GET'])
        self.env = env

    def view(self):
        queue_copy = list(self.env.scheduler.tasks.queue)
        if self.env.scheduler.current_task is not None:
            queue_copy.append(self.env.scheduler.current_task)
        queue_copy = [task for task in queue_copy if task.task_type == TaskType.Txt2Img]
        length = len(queue_copy)
        return {"status": 0, "queue_length": length,
                "tasks": [
                    {
                        "uuid": task.task_id,
                        "progress": task.get_progress()[0],
                        "length": task.function_args["n_iter"] * task.function_args["batch_size"],
                        "n_iter": task.function_args["n_iter"],
                        "batch_size": task.function_args["batch_size"],
                        "width": task.function_args["width"],
                        "height": task.function_args["height"],
                        "step": task.function_args["step"],
                        "sampler": task.function_args["sampler"],
                        "prompt": task.function_args["prompt"],
                        "negative_prompt": task.function_args["negative_prompt"],
                        "cfg": task.function_args["cfg"]
                    } for task in queue_copy]}
