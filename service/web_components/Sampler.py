from . import *


class SamplerList(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/sampler_list', 'SamplerList', ['GET'])
        self.env = env

    def view(self):
        return {"sampler_list": self.env.core.get_sampler_list()}
