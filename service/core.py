import os
import random
import re

import numpy as np
import torch
from utility import Task
from stable_diffusion import StableDiffusionModel, Txt2Img, MemoryOptimizer, CorsAttentionOptimizationMode


class Core:
    def __init__(self, config: dict):
        self.model_path = config.get('model_path', 'models')
        self.default_model_config = config.get('default_model_config', 'v1-inference.yaml')
        self.force_cpu = config.get('force_cpu', False)
        self.device = torch.device("cuda" if torch.cuda.is_available() and not self.force_cpu else "cpu")
        self.map_location = config.get('map_location', "cpu" if self.device.type == "cpu" else None)
        self.sample_out_path = config.get('sample_out_path', 'images')

        self.memory_optimizer = MemoryOptimizer()
        self.optimize_memory()
        self.model_loader = StableDiffusionModel(self.model_path, self.default_model_config, self.device, half=False, map_location=self.map_location)
        self.txt2img: Txt2Img = None

    def optimize_memory(self):
        self.memory_optimizer.apply_memory_optimizations(CorsAttentionOptimizationMode.DEFAULT)

    def load_model(self, model_name: str, vae_name: str = None):
        self.model_loader.load_model(model_name, vae_name)
        self.txt2img: Txt2Img = Txt2Img(self.model_loader.model, self.device, dtype_vae=self.model_loader.dtype_vae)

    def save_sample(self, images):
        saved_path = []
        current_images = [x for x in os.listdir(self.sample_out_path) if re.match(r"[0-9]+\.png", x.lower())]
        current_images.sort(key=lambda x: int(x.split('.')[0]))
        max_number = current_images[-1].split('.')[0] if len(current_images) > 0 else 0
        for i, image in enumerate(images):
            # get name of file and fill zero
            file_name = str(i + int(max_number) + 1).zfill(5) + ".png"
            file_path = os.path.join(self.sample_out_path, file_name)
            image.save(file_path)
            saved_path.append(file_path)
        return saved_path

    def sample_txt2img(self, prompt: str, negative_prompt: str, step: int, width: int, height: int, sampler: str = "DDIM", n_iter: int = 1, batch_size: int = 1, cfg: float = 7, seed: int = -1,
                       task: Task = None):
        if seed == -1:
            seed = random.randint(1000000, 1000000000)
        results = []
        task.result = []
        task.progress = np.array((0, 0))

        def update_progress(it):
            task.progress[1] = it

        for i in range(n_iter):
            temp_result = self.txt2img.generate(prompt, negative_prompt, height, width, batch_size, seed, sample=sampler, steps=step, cfg=cfg, update_progress=update_progress)
            seeds = [seed + i for i in range(batch_size)]
            saved_path = self.save_sample(temp_result)
            results += zip(temp_result, seeds, saved_path)
            task.progress[0] = i
            task.result += zip(temp_result, seeds, saved_path)
            seed += batch_size
        return results

    def refresh_model_list(self):
        self.model_loader.sync_checkpoint_list()

    def get_sampler_list(self):
        if self.txt2img is None:
            return ["DDIM", "PLMS"]
        else:
            return list(self.txt2img.samplers.keys())

    def get_model_list(self):
        return list(self.model_loader.checkpoints.keys())

    def get_vae_list(self):
        return self.model_loader.get_available_vae_list()
