from core import Core


class Environment:
    def __init__(self, config, core: Core, **kwargs):
        self.config = config
        self.core = core
