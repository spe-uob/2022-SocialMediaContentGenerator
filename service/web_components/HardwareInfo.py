import torch

from . import *


class VRAM(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/vram', 'VRAM', ['GET'])
        self.env = env

    def view(self):
        allocated = torch.cuda.memory_allocated(0) / (1024 ** 3)
        cached = torch.cuda.memory_reserved(0) / (1024 ** 3)
        device_total = (torch.cuda.mem_get_info()[1]) / (1024 ** 3)
        return {"allocated": allocated, "cached": cached, "device_total": device_total}
