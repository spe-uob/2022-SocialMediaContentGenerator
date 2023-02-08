import os
import time
from itertools import islice

import numpy as np
import torch
from loguru import logger
from PIL import Image
from rich.progress import Progress
from diffusers.pipelines.stable_diffusion import StableDiffusionSafetyChecker
from einops import rearrange
from imwatermark import WatermarkEncoder
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.models.diffusion.dpm_solver import DPMSolverSampler
from ldm.models.diffusion.plms import PLMSSampler
from omegaconf import OmegaConf
from torch import autocast
from torchvision.utils import make_grid
from tqdm import trange, tqdm
from transformers import AutoFeatureExtractor

from stable_diffusion.model import Model

safety_model_id = "CompVis/stable-diffusion-safety-checker"
safety_feature_extractor = AutoFeatureExtractor.from_pretrained(safety_model_id)
safety_checker = StableDiffusionSafetyChecker.from_pretrained(safety_model_id)


class Core:
    def __init__(self):
        self.model = Model()
        self.wm_encoder = WatermarkEncoder()
        self.model_path = "stable_diffusion/models"
        self.save_path = "out/samples"
        self.grid_path = "out/grids"
        self.n_rows = 2

    @staticmethod
    def check_and_create_dir(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def check_out_dir(self):
        self.check_and_create_dir(self.save_path)
        self.check_and_create_dir(self.grid_path)

    def on_load_model(self, model_name):
        logger.info(f"loading model {model_name}...")
        config = OmegaConf.load(f"stable_diffusion/v1-inference.yaml")
        self.model.load_model_from_config(config, os.path.join(self.model_path, model_name), verbose=False)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model = self.model.model.to(device)
        self.model.model = model

    def on_load_vae(self, vae_name):
        logger.info(f"loading vae {vae_name}...")
        self.model.load_vae(os.path.join(self.model_path, vae_name))

    def exec_sample(self, prompt, negative_prompt, sample: str, batch_size=1, step=20, cfg=7.5, width=512, height=512, f=8, channel=4, ddim_eta=0.0, skip_grid=True):
        logger.info(f"exec sample {sample}...")
        self.check_out_dir()
        model = self.model.model
        sampler = DDIMSampler(model)
        if sample.lower() == "dpm":
            sampler = DPMSolverSampler(model)
        elif sample.lower() == "plms":
            sampler = PLMSSampler(model)

        data = [batch_size * [prompt]]
        start_code = None
        base_count = len(os.listdir(self.save_path))
        grid_count = len(os.listdir(self.grid_path)) - 1
        n_rows = self.n_rows if self.n_rows > 0 else batch_size
        all_samples = list()
        images_buffer = None
        with torch.no_grad():
            with autocast("cuda"):
                with model.ema_scope():
                    with Progress() as progress:
                        task1 = progress.add_task("[red]Sampling...", total=batch_size)
                        for n in range(batch_size):
                            task2 = progress.add_task("[green]Generating...", total=len(data))
                            for prompts in data:
                                uc = None
                                if cfg != 1.0:
                                    uc = model.get_learned_conditioning(batch_size * [negative_prompt])
                                if isinstance(prompts, tuple):
                                    prompts = list(prompts)
                                c = model.get_learned_conditioning(prompts)
                                shape = [channel, height // f, width // f]
                                samples_ddim, _ = sampler.sample(S=step,
                                                                 conditioning=c,
                                                                 batch_size=batch_size,
                                                                 shape=shape,
                                                                 verbose=False,
                                                                 unconditional_guidance_scale=cfg,
                                                                 unconditional_conditioning=uc,
                                                                 eta=ddim_eta,
                                                                 x_T=start_code)

                                x_samples_ddim = model.decode_first_stage(samples_ddim)
                                x_samples_ddim = torch.clamp((x_samples_ddim + 1.0) / 2.0, min=0.0, max=1.0)
                                x_samples_ddim = x_samples_ddim.cpu().permute(0, 2, 3, 1).numpy()
                                x_checked_image, has_nsfw_concept = self.check_safety(x_samples_ddim)
                                x_checked_image = x_samples_ddim
                                x_checked_image_torch = torch.from_numpy(x_checked_image).permute(0, 3, 1, 2)

                                for x_sample in x_checked_image_torch:
                                    images_buffer = x_sample
                                    x_sample = 255. * rearrange(x_sample.cpu().numpy(), 'c h w -> h w c')
                                    img = Image.fromarray(x_sample.astype(np.uint8))
                                    # img = put_watermark(img, wm_encoder)
                                    img.save(os.path.join(self.save_path, f"{base_count:05}.png"))
                                    base_count += 1

                                if not skip_grid:
                                    all_samples.append(x_checked_image_torch)

                                progress.update(task2, advance=1)
                            progress.update(task1, advance=1)

                    if not skip_grid:
                        # additionally, save as grid
                        grid = torch.stack(all_samples, 0)
                        grid = rearrange(grid, 'n b c h w -> (n b) c h w')
                        grid = make_grid(grid, nrow=n_rows)

                        # to image
                        grid = 255. * rearrange(grid, 'c h w -> h w c').cpu().numpy()
                        img = Image.fromarray(grid.astype(np.uint8))
                        # img = put_watermark(img, wm_encoder)
                        img.save(os.path.join(self.grid_path, f'grid-{grid_count:04}.png'))
                        grid_count += 1
        result = 255. * rearrange(images_buffer.cpu().numpy(), 'c h w -> h w c')
        del samples_ddim
        del x_samples_ddim
        del x_checked_image
        del x_checked_image_torch
        del images_buffer
        return result.astype(np.uint8)

    def set_wm(self, wm: str = "SMCG-SD-V1"):
        self.wm_encoder.set_watermark('bytes', wm.encode('utf-8'))

    def check_safety(self, x_image):

        safety_checker_input = safety_feature_extractor(self.numpy_to_pil(x_image), return_tensors="pt")
        x_checked_image, has_nsfw_concept = safety_checker(images=x_image, clip_input=safety_checker_input.pixel_values)
        assert x_checked_image.shape[0] == len(has_nsfw_concept)
        for i in range(len(has_nsfw_concept)):
            if has_nsfw_concept[i]:
                x_checked_image[i] = self.load_replacement(x_checked_image[i])
        return x_checked_image, has_nsfw_concept

    @staticmethod
    def numpy_to_pil(images):
        """
        Convert a numpy image or a batch of images to a PIL image.
        """
        if images.ndim == 3:
            images = images[None, ...]
        images = (images * 255).round().astype("uint8")
        pil_images = [Image.fromarray(image) for image in images]
        return pil_images

    @staticmethod
    def chunk(it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    @staticmethod
    def load_replacement(x):
        try:
            hwc = x.shape
            y = Image.open("assets/rick.jpeg").convert("RGB").resize((hwc[1], hwc[0]))
            y = (np.array(y) / 255.0).astype(x.dtype)
            assert y.shape == x.shape
            return y
        except Exception:
            return x
