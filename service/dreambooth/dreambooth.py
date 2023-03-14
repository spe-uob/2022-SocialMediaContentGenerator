from service.dreambooth.dreambooth_config import DreamboothConfig


class Dreambooth:
    def __init__(self, concept_loader_args, config=None, **kwargs):
        if config is None:
            self.config = DreamboothConfig(**kwargs)
        else:
            self.config = config


