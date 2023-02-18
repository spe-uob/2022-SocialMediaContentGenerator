# from service import Core
# from service import Scheduler
#
#
# class Environment:
#     def __init__(self, config, core: Core,  **kwargs):
#         self.config = config
#         self.core = core
#         self.scheduler: Scheduler = None


class Environment:
    def __init__(self, config, core,  **kwargs):
        self.config = config
        self.core = core
        self.scheduler = None
