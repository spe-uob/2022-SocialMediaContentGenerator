import os
import random
import re

import torch

from stable_diffusion.memoryOptimizer import MemoryOptimizer, CorsAttentionOptimizationMode
from stable_diffusion.model import StableDiffusionModel
from stable_diffusion.txt2img import Txt2Img
from matplotlib import pyplot as plt

prompt = """nsfw, masterpiece, best quality, highly detailed, extremely detailed CG unity 8k wallpaper, illustration,
light and shadow,
mudrock, 1girl, large_breasts, bare_shoulders, black_choker, choker, elite_ii_(arknights), horns, long_hair, mudrock_(arknights), oripathy_lesion_(arknights), silver_hair, solo, lookat_viewer, realistic,
chinese architecture, chinese traditional buildings, chinese ancient buildings, outdoors,"""
nprompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad art, ugly, messy drawing, deformed, bad anatomy, disfigured, mutation, mutated, holding, see-through,"


def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    # model_path = r"S:\ckpt\mix_model\Mudrock768"
    # default_config = r"W:\work\stable-diffusion-webui-old-dreambooth\v1-inference.yaml"
    model_path = r"/mnt/s/ckpt/mix_model/Mudrock768"
    default_config = r"/mnt/w/work/stable-diffusion-webui-old-dreambooth/v1-inference.yaml"
    memory_optimizer = MemoryOptimizer()
    memory_optimizer.apply_memory_optimizations(CorsAttentionOptimizationMode.DEFAULT)
    model_loader = StableDiffusionModel(model_path, default_config, device, half=True)
    print("available models:")
    for checkpoint in model_loader.checkpoint_list:
        print(f"    {checkpoint[0]}")
    model_loader.load_model("Mudrock768_20000_AO-M-E6E_0.75.ckpt")
    model = model_loader.model
    txt2img = Txt2Img(model, device, model_loader.dtype_vae)
    result = []
    plt.figure(dpi=1200)
    for i in range(2):
        samples = txt2img.generate(prompt, nprompt, 512, 512, 2, random.randint(1000000, 1000000000), sample="Euler A", steps=35)
        for img in samples:
            print("show image...")
            result.append(img)
            plt.figure(dpi=600)
            plt.imshow(img)
            plt.show()

    save_images(result)


def save_images(images):
    if not os.path.exists("images"):
        os.mkdir("images")
    existing = [x for x in os.listdir("images") if re.match(r"^[0-9]+.*\.png$", x)]
    existing.sort(key=lambda x: int(re.search(r"^[0-9]+", x)[0]))
    last = 0
    if len(existing) > 0:
        last = int(re.search(r"^[0-9]+", existing[-1])[0])
    for i, image in enumerate(images):
        image.save(f"images/{str(last + i + 1).zfill(5)}.png")


if __name__ == "__main__":
    test()
