import os.path

from . import *


class LoadLora(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/load_lora', 'LoadLora', ['POST'])
        self.env = env

    def view(self):
        data = request.get_json()
        if data is None:
            return abort(400)
        lora_networks = data['lora_networks']
        if lora_networks is None:
            return abort(400)
        self.env.core.load_lora_network(lora_networks)
        return {"status": 0}


class CurrentLora(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/current_lora', 'CurrentLora', ['GET'])
        self.env = env

    def view(self):
        lora_networks = self.env.core.model_loader.lora_networks
        lora_networks = list(map(lambda x: {"name": os.path.basename(x[1]), "weight": x[2]}, lora_networks))
        return lora_networks


class LoraList(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/lora_list', 'LoraList', ['GET'])
        self.env = env

    def view(self):
        self.env.core.model_loader.sync_checkpoint_list()
        return self.env.core.model_loader.lora_model_list
