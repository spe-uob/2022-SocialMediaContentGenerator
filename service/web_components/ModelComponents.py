from flask import request

from . import *


class ModelList(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/model_list', 'ModelList', ['GET'])
        self.env = env

    def view(self):
        return {"mode_list": self.env.core.get_model_list()}


class VaeList(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/vae_list', 'VaeList', ['GET'])
        self.env = env

    def view(self):
        return {"mode_list": self.env.core.get_vae_list()}


class LoadModel(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/load_model', 'LoadModel', ['GET'])
        self.env = env

    def view(self):
        model_name = request.args.get('ModelName')
        vae_name = request.args.get('VAEName', None)
        self.env.core.load_model(model_name, vae_name)
        return {"status": 0}


class CurrentModel(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/current_model', 'CurrentModel', ['GET'])
        self.env = env

    def view(self):
        return {"current_model": self.env.core.model_loader.current_model}


class CurrentVae(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/current_vae', 'CurrentVae', ['GET'])
        self.env = env

    def view(self):
        return {"current_vae": self.env.core.model_loader.current_vae_file}
