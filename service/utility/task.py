import enum
import uuid


class TaskType(enum.Enum):
    Txt2Img = 1
    Img2Img = 2
    LoadModel = 3


class Task:
    def __init__(self, task_type: TaskType, task_data: dict, task_id: str = None):
        self.task_type = task_type
        self.task_data = task_data
        self.task_id = task_id if task_id is not None else str(uuid.uuid4())
