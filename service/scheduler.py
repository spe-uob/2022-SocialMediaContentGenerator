import queue

from core import Core
from service.utility.environment import Environment


class Scheduler:
    def __init__(self, core: Core, environment: Environment):
        self.core = core
        self.environment = environment
        self.tasks = queue.Queue()
