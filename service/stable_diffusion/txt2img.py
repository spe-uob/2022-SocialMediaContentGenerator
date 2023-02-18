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
        with torch.autocast("cuda" if self.device.type == "cuda" else "cpu"):
            sampler = self.samplers[sample]
            x = self.create_random_tensors([self.opt_C, height // self.opt_f, width // self.opt_f], seeds=[seed + i for i in range(batch_size)], seed_resize_from_h=0, seed_resize_from_w=0,
                                           sampler=sampler)
            uc = self.model.get_learned_conditioning(batch_size * [negative_prompt])
            c = self.model.get_learned_conditioning(batch_size * [prompt])

            samples_ddim = sampler.sample(x, c, uc, steps=steps, cfg_scale=cfg)

            x_samples_ddim = [self.model.decode_first_stage(samples_ddim[i:i + 1].to(dtype=self.dtype_vae))[0].cpu() for i in range(samples_ddim.size(0))]
            x_samples_ddim = torch.stack(x_samples_ddim).float()
            x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)

        del samples_ddim
        results = []
        for i, x_sample in enumerate(x_samples_ddim):
            x_sample_cpu = 255. * np.moveaxis(x_sample.cpu().numpy(), 0, 2)
            x_sample_cpu = x_sample_cpu.astype(np.uint8)
            image = Image.fromarray(x_sample_cpu)
            results.append(image)
            del x_sample

        del x_samples_ddim
        self.torch_gc()
        return results

    def create_random_tensors(self, shape, seeds, seed_resize_from_h=0, seed_resize_from_w=0, sampler=None):
        xs = []

        if sampler is not None and (len(seeds) > 1 and self.enable_batch_seeds or self.noise_seed_delta > 0):
            sampler_noises = [[] for _ in range(sampler.number_of_needed_noises(None))]
        else:
            sampler_noises = None

        for i, seed in enumerate(seeds):
            noise_shape = shape if seed_resize_from_h <= 0 or seed_resize_from_w <= 0 else (shape[0], seed_resize_from_h // 8, seed_resize_from_w // 8)
            torch.manual_seed(seed)
            noise = torch.randn(noise_shape, device=self.device)
            if noise_shape != shape:
                torch.manual_seed(seed)
                x = torch.randn(shape, device=self.device)
                dx = (shape[2] - noise_shape[2]) // 2
                dy = (shape[1] - noise_shape[1]) // 2
                w = noise_shape[2] if dx >= 0 else noise_shape[2] + 2 * dx
                h = noise_shape[1] if dy >= 0 else noise_shape[1] + 2 * dy
                tx = 0 if dx < 0 else dx
                ty = 0 if dy < 0 else dy
                dx = max(-dx, 0)
                dy = max(-dy, 0)

                x[:, ty:ty + h, tx:tx + w] = noise[:, dy:dy + h, dx:dx + w]
                noise = x

            if sampler_noises is not None:
                cnt = sampler.number_of_needed_noises(None)
                if self.noise_seed_delta > 0:
                    torch.manual_seed(seed + self.noise_seed_delta)
                for j in range(cnt):
                    sampler_noises[j].append(torch.randn(tuple(noise_shape), device=self.device))
            xs.append(noise)

        if sampler_noises is not None:
            sampler.sampler_noises = [torch.stack(n).to(self.device) for n in sampler_noises]

        x = torch.stack(xs).to(self.device)
        return x

    @staticmethod
    def torch_gc():
        if torch.cuda.is_available():
            with torch.cuda.device("cuda:0"):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
