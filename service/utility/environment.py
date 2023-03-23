# from service import Core
# from service import Scheduler
#
#
# class Environment:
#     def __init__(self, config, core: Core,  **kwargs):
#         self.config = config
#         self.core = core
#         self.scheduler: Scheduler = None
from web_server import ApiServer


class Environment:
    def __init__(self, config, core, **kwargs):
        self.config = config
        self.core = core
        self.api_server: ApiServer = None
        self.scheduler = None
