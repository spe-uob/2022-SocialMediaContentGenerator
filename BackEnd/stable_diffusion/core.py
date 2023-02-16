import os
import random
from itertools import islice

import numpy as np
import torch
from loguru import logger
from PIL import Image
from rich.progress import Progress
from imwatermark import WatermarkEncoder

from stable_diffusion.model import StableDiffusionModel
from stable_diffusion.txt2img import Txt2Img

# safety_model_id = "CompVis/stable-diffusion-safety-checker"
# safety_feature_extractor = AutoFeatureExtractor.from_pretrained(safety_model_id)
# safety_checker = StableDiffusionSafetyChecker.from_pretrained(safety_model_id)


class Core:
    def __init__(self):
        self.wm_encoder = WatermarkEncoder()
        self.model_path = r"W:\work\stable-diffusion-webui-old-dreambooth\models\Stable-diffusion"
        self.default_config = r"W:\work\stable-diffusion-webui-old-dreambooth\v1-inference.yaml"
        self.save_path = "out/samples"
        self.grid_path = "out/grids"
        self.n_rows = 2
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_loader = StableDiffusionModel(self.model_path, self.default_config, self.device, half=True)
        self.txt2img: Txt2Img = None

    @staticmethod
    def check_and_create_dir(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def check_out_dir(self):
        self.check_and_create_dir(self.save_path)
        self.check_and_create_dir(self.grid_path)

    def on_load_model(self, model_name):
        logger.info(f"loading model {model_name}...")
        self.model_loader.load_model(model_name)
        self.txt2img = Txt2Img(self.model_loader.model, self.device, self.model_loader.dtype_vae)

    def on_load_vae(self, vae_name):
        pass

    def exec_sample(self, prompt, negative_prompt, sample: str, batch_size=1, step=20, cfg=7.5, width=512, height=512, seed=-1, num_samples=1):
        logger.info(f"exec sample {sample}...")
        if seed < 0:
            seed = random.randint(1000000, 1000000000)
        result = []
        for i in range(num_samples):
            result += self.txt2img.generate(prompt, negative_prompt, height, width, batch_size, seed, sample=sample, steps=step)
        return result

    def set_wm(self, wm: str = "SMCG-SD-V1"):
        self.wm_encoder.set_watermark('bytes', wm.encode('utf-8'))

    # def check_safety(self, x_image):
    #
    #     safety_checker_input = safety_feature_extractor(self.numpy_to_pil(x_image), return_tensors="pt")
    #     x_checked_image, has_nsfw_concept = safety_checker(images=x_image, clip_input=safety_checker_input.pixel_values)
    #     assert x_checked_image.shape[0] == len(has_nsfw_concept)
    #     for i in range(len(has_nsfw_concept)):
    #         if has_nsfw_concept[i]:
    #             x_checked_image[i] = self.load_replacement(x_checked_image[i])
    #     return x_checked_image, has_nsfw_concept

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
