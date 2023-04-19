from service.dreambooth.concept import ConceptLoader
from service.dreambooth.dreambooth_config import DreamboothConfig


class Dreambooth:
    def __init__(self, concept_loader_args, config=None, **kwargs):
        if config is None:
            self.config = DreamboothConfig(**kwargs)
        else:
            self.config = config
        self.concept_loader = ConceptLoader(concept_loader_args)
        self.concepts = self.concept_loader.concepts

