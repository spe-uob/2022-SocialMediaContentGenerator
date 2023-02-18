import torch

from stable_diffusion import StableDiffusionModel, txt2img


class Core:
    def __init__(self, config: dict):
        self.model_path = config.get('model_path', 'models')
        self.default_model_config = config.get('default_model_config', 'v1-inference.yaml')
        self.force_cpu = config.get('force_cpu', False)
        self.device = torch.device("cuda" if torch.cuda.is_available() and not self.force_cpu else "cpu")
        self.map_location = config.get('map_location', "cpu" if self.device.type == "cpu" else None)

        self.model_loader = StableDiffusionModel(self.model_path, self.default_model_config, self.device, half=True, map_location=self.map_location)
        self.txt2img = None

    def load_model(self, model_name: str, vae_name: str = None):
        self.model_loader.load_model(model_name, vae_name)
        self.txt2img = txt2img.Txt2Img(self.model_loader.model, self.device, dtype_vae=self.model_loader.dtype_vae)
