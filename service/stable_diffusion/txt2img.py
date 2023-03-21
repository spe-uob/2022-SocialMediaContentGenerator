import numpy as np
import torch
import torch.nn.functional

from . import prompt_parser
from .sampler import TypicalStableDiffusionSampler, KDiffusionSampler
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.models.diffusion.plms import PLMSSampler
import k_diffusion.sampling
from PIL import Image
from contextlib import contextmanager, nullcontext


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
        return
        self.samplers["Euler A"] = KDiffusionSampler(k_diffusion.sampling.sample_euler_ancestral, self.model, self.device)
        self.samplers["Euler"] = KDiffusionSampler(k_diffusion.sampling.sample_euler, self.model, self.device)
        self.samplers["LMS"] = KDiffusionSampler(k_diffusion.sampling.sample_lms, self.model, self.device)
        self.samplers["Heun"] = KDiffusionSampler(k_diffusion.sampling.sample_heun, self.model, self.device)
        self.samplers["DPM2"] = KDiffusionSampler(k_diffusion.sampling.sample_dpm_2, self.model, self.device)
        self.samplers["DPM2 a"] = KDiffusionSampler(k_diffusion.sampling.sample_dpm_2_ancestral, self.model, self.device)
        self.samplers["DPM++ 2S a"] = KDiffusionSampler(k_diffusion.sampling.sample_dpmpp_2s_ancestral, self.model, self.device)
        self.samplers["DPM++ 2M"] = KDiffusionSampler(k_diffusion.sampling.sample_dpmpp_2m, self.model, self.device)
        self.samplers["DPM++ SDE"] = KDiffusionSampler(k_diffusion.sampling.sample_dpmpp_sde, self.model, self.device)
        self.samplers["DPM fast"] = KDiffusionSampler(k_diffusion.sampling.sample_dpm_fast, self.model, self.device)
        self.samplers["DPM adaptive"] = KDiffusionSampler(k_diffusion.sampling.sample_dpm_adaptive, self.model, self.device)

    def generate(self, prompt, negative_prompt, height, width, batch_size, seed, sample="DDIM", steps=20, cfg=7.5):
        with torch.autocast("cuda") if self.device.type == "cuda" else nullcontext():
            if self.device.type != "cuda":
                self.model.cond_stage_model.transformer.to(dtype=torch.float32)
            sampler = self.samplers[sample]
            x = self.create_random_tensors([self.opt_C, height // self.opt_f, width // self.opt_f], seeds=[seed + i for i in range(batch_size)], seed_resize_from_h=0, seed_resize_from_w=0,
                                           sampler=sampler)
            uc = self.model.get_learned_conditioning(batch_size * [negative_prompt])
            c = self.model.get_learned_conditioning(batch_size * [prompt])
            # uc = prompt_parser.get_learned_conditioning(self.model, batch_size * [negative_prompt], steps)
            # c = prompt_parser.get_multicond_learned_conditioning(self.model, batch_size * [prompt], steps)
            image_conditioning = self.txt2img_image_conditioning(sampler, x, width, height)

            samples_ddim = sampler.sample(x, c, uc, steps=steps, cfg_scale=cfg, image_conditioning=image_conditioning)

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

    def create_random_tensors(self, shape, seeds, seed_resize_from_h=0, seed_resize_from_w=0, sampler=None, steps=20):
        xs = []

        if sampler is not None and (len(seeds) > 1 and self.enable_batch_seeds or self.noise_seed_delta > 0):
            sampler_noises = [[] for _ in range(sampler.number_of_needed_noises(steps))]
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
                cnt = sampler.number_of_needed_noises(steps)
                if self.noise_seed_delta > 0:
                    torch.manual_seed(seed + self.noise_seed_delta)
                for j in range(cnt):
                    sampler_noises[j].append(torch.randn(tuple(noise_shape), device=self.device))
            xs.append(noise)

        if sampler_noises is not None:
            sampler.sampler_noises = [torch.stack(n).to(self.device) for n in sampler_noises]

        x = torch.stack(xs).to(self.device)
        return x

    def txt2img_image_conditioning(self, sampler, x, width, height):
        if sampler.conditioning_key not in {'hybrid', 'concat'}:
            # Dummy zero conditioning if we're not using inpainting model.
            # Still takes up a bit of memory, but no encoder call.
            # Pretty sure we can just make this a 1x1 image since its not going to be used besides its batch size.
            return x.new_zeros(x.shape[0], 5, 1, 1)

        # self.is_using_inpainting_conditioning = True

        # The "masked-image" in this case will just be all zeros since the entire image is masked.
        image_conditioning = torch.zeros(x.shape[0], 3, height, width, device=x.device)
        image_conditioning = self.model.get_first_stage_encoding(self.model.encode_first_stage(image_conditioning))

        # Add the fake full 1s mask to the first dimension.
        image_conditioning = torch.nn.functional.pad(image_conditioning, (0, 0, 0, 0, 1, 0), value=1.0)
        image_conditioning = image_conditioning.to(x.dtype)

        return image_conditioning

    @staticmethod
    def torch_gc():
        if torch.cuda.is_available():
            with torch.cuda.device("cuda:0"):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
