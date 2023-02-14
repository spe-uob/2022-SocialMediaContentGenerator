import random

import torch

from sd_rebuild.model import StableDiffusionModel
from sd_rebuild.txt2img import Txt2Img
from matplotlib import pyplot as plt

prompt = """nsfw, masterpiece, best quality, highly detailed, extremely detailed CG unity 8k wallpaper, illustration,
light and shadow,
mudrock, 1girl, large_breasts, bare_shoulders, black_choker, choker, elite_ii_(arknights), horns, long_hair, mudrock_(arknights), oripathy_lesion_(arknights), silver_hair, solo, lookat_viewer, realistic,
nsfw, boobs, nipples, pussy, cum, cum in pussy, cum on body, orgasm, rolling eyes, milk_breasts, torn clothes, naked,
chinese architecture, chinese traditional buildings, chinese ancient buildings, outdoors,"""
nprompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad art, ugly, messy drawing, deformed, bad anatomy, disfigured, mutation, mutated, holding, see-through,"


def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = r"W:\work\stable-diffusion-webui-old-dreambooth\models\Stable-diffusion"
    default_config = r"W:\work\stable-diffusion-webui-old-dreambooth\v1-inference.yaml"
    model_loader = StableDiffusionModel(model_path, default_config, device)
    print("available models:")
    for checkpoint in model_loader.checkpoint_list:
        print(f"    {checkpoint[0]}")
    model_loader.load_model("Mudrock768_20000_AO-M-E6E_0.75.ckpt")
    model = model_loader.model
    txt2img = Txt2Img(model, device, model_loader.dtype_vae)
    result = []
    for i in range(2):
        result += txt2img.generate(prompt, nprompt, 512, 512, 2, random.randint(0, 100000000))
    for image in result:
        plt.imshow(image)
        plt.show()


if __name__ == "__main__":
    test()
