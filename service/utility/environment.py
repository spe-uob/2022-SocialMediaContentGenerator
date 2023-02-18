from ..core import Core
from ..scheduler import Scheduler


class Environment:
    def __init__(self, config, core: Core,  **kwargs):
        self.config = config
        self.core = core
        self.scheduler: Scheduler = None
