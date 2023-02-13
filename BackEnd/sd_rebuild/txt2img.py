import numpy as np
import torch

from .sampler import TypicalStableDiffusionSampler
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.models.diffusion.plms import PLMSSampler
from PIL import Image


class Txt2Img:
    def __init__(self, model, device, dtype_vae, noise_seed_delta=0.0, enable_batch_seeds=True):
        self.model = model
        self.device = device
        self.dtype_vae = dtype_vae
        self.noise_seed_delta = noise_seed_delta
        self.enable_batch_seeds = enable_batch_seeds
        self.samplers = {}
        self.opt_C = 4
        self.opt_f = 8
        self.load_sampler()

    def load_sampler(self):
        self.samplers["DDIM"] = TypicalStableDiffusionSampler(DDIMSampler, self.model)
        self.samplers["PLMS"] = TypicalStableDiffusionSampler(PLMSSampler, self.model)

    def generate(self, prompt, negative_prompt, height, width, batch_size, seed, sample="DDIM", steps=20, cfg=7.5):
        with torch.autocast("cuda"):
            sampler = self.samplers[sample]
