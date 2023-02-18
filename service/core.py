import random

import torch

from stable_diffusion import StableDiffusionModel, txt2img, MemoryOptimizer, CorsAttentionOptimizationMode


class Core:
    def __init__(self, config: dict):
        self.model_path = config.get('model_path', 'models')
        self.default_model_config = config.get('default_model_config', 'v1-inference.yaml')
        self.force_cpu = config.get('force_cpu', False)
        self.device = torch.device("cuda" if torch.cuda.is_available() and not self.force_cpu else "cpu")
        self.map_location = config.get('map_location', "cpu" if self.device.type == "cpu" else None)

        self.memory_optimizer = MemoryOptimizer()
        self.model_loader = StableDiffusionModel(self.model_path, self.default_model_config, self.device, half=True, map_location=self.map_location)
        self.txt2img: txt2img.Txt2Img = None
        self.optimize_memory()

    def optimize_memory(self):
        self.memory_optimizer.apply_memory_optimizations(CorsAttentionOptimizationMode.DEFAULT)

    def load_model(self, model_name: str, vae_name: str = None):
        self.model_loader.load_model(model_name, vae_name)
        self.txt2img: txt2img.Txt2Img = txt2img.Txt2Img(self.model_loader.model, self.device, dtype_vae=self.model_loader.dtype_vae)

    def sample_txt2img(self, prompt: str, negative_prompt: str, step: int, width: int, height: int, sampler: str = "DDIM", n_iter: int = 1, batch_size: int = 1, cfg: float = 7, seed: int = -1,
                       progress_callback=lambda x1, x2: None):
        if seed == -1:
            seed = random.randint(1000000, 1000000000)
        results = []
        for i in range(n_iter):
            temp_result = self.txt2img.generate(prompt, negative_prompt, height, width, batch_size, seed, sample=sampler, steps=step, cfg=cfg)
            seeds = [seed + i for i in range(batch_size)]
            results += zip(temp_result, seeds)
            progress_callback(i, 0)
        return results

    def refresh_model_list(self):
        self.model_loader.sync_checkpoint_list()

    def get_sampler_list(self):
        if self.txt2img is None:
            return {"sampler_list": ["DDIM", "PLMS"]}
        else:
            return {"sampler_list": list(self.txt2img.samplers.keys())}

    def get_model_list(self):
        return list(self.model_loader.checkpoint_list.keys())

    def get_vae_list(self):
        return self.model_loader.get_available_vae_list()
