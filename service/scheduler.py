import queue
import threading

from loguru import logger

from core import Core
from utility import Environment
from rich.progress import Progress
from utility import Task, TaskType, TaskStatus


class Scheduler:
    def __init__(self, core: Core, environment: Environment):
        self.core = core
        self.environment = environment
        self.tasks = queue.Queue()
        self.current_task = None
        self.tasks_completed = {}
        self.tasks_table = {}
        self.schedule_thread = threading.Thread(target=self.schedule_loop)
        self.schedule_loop_flag = True
        self.progress = Progress()
        self.progress_task = None

    def schedule_loop(self):
        logger.info("Scheduler started...")
        try:
            while self.schedule_loop_flag:
                self.current_task: Task = self.tasks.get()
                if self.current_task is None:
                    continue
                self.current_task.progress_task = self.progress.add_task(f"Processing task: [{self.current_task.task_type}]...", total=self.current_task.total_progress[0])
                self.current_task.task_status = TaskStatus.Running
                self.current_task.result = self.current_task.run()
                self.current_task.task_status = TaskStatus.Finished
                self.tasks_completed[self.current_task.task_id] = self.current_task
                self.current_task = None
        except KeyboardInterrupt as e:
            logger.exception(e)
        logger.info("Scheduler stopped...")

    def start(self):
        self.schedule_thread.start()

    def stop(self):
        self.schedule_loop_flag = False
        self.tasks.put(None)
        self.schedule_thread.join()

    def add_task_txt2img(self, prompt, negative_prompt, sampler, step, width, height, n_iter, batch_size, cfg):
        task = Task(TaskType.Txt2Img, function_args={
            "prompt": prompt, "negative_prompt": negative_prompt, "step": step, "width": width, "height": height, "sampler": sampler, "n_iter": n_iter, "batch_size": batch_size, "cfg": cfg,
        }, func=self.core.sample_txt2img, total_progress=[n_iter, step])
        task.function_args["task"] = task
        self.tasks.put(task)
        self.tasks_table[task.task_id] = task
        return task.task_id

    def get_task(self, task_id):
        if task_id in self.tasks_table:
            return self.tasks_table[task_id]
        else:
            return None
