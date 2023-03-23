import enum
import uuid
import numpy as np


class TaskType(enum.Enum):
    Txt2Img = "Text to Image"
    Img2Img = "Image to Image"
    LoadModel = "Load Model"


class TaskStatus(enum.Enum):
    Pending = 1
    Running = 2
    Finished = 3
    Failed = 4


class Task:
    def __init__(self, task_type: TaskType, function_args: dict, func=None, total_progress=1, task_id: str = None):
        self.task_type = task_type
        self.function_args = function_args
        self.func = func
        self.task_id = task_id if task_id is not None else str(uuid.uuid4())
        self.task_status = TaskStatus.Pending
        self.total_progress = np.array(total_progress)
        self.progress = np.zeros(self.total_progress.shape)
        self.result = None
        self.progress_task = None

    def run(self):
        return self.func(**self.function_args)

    def get_progress(self):
        return self.progress / self.total_progress

    def update_progress(self, progress):
        self.progress += progress
        if self.progress_task is not None:
            self.progress_task.update(advance=progress[0])
        return self.get_progress()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "task_status": self.task_status.value,
            "progress": self.get_progress().tolist(),
            # "result": self.result,
        }

    def task_info(self):
        keys = ["progress", "length", "n_iter", "batch_size", "width", "height", "step", "sampler", "prompt", "negative_prompt", "cfg"]
        result = {key: self.function_args[key] for key in keys if key in self.function_args}
        result["uuid"] = self.task_id
        result["progress"] = self.get_progress()[0]
        return result
