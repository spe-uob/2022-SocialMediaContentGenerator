from stable_diffusion.core import Core


class InformationProvider:
    def __init__(self, core: Core):
        self.core = core

    def get_info(self):
        return {
            "current_model": self.core.model.current_model_name,
        }
