import torch
from ldm.models.diffusion.ddim import DDIMSampler
from ldm.models.diffusion.dpm_solver import DPMSolverSampler
from ldm.models.diffusion.plms import PLMSSampler
from omegaconf import OmegaConf

from stable_diffusion.model import Model


class Core:
    def __init__(self):
        self.model = Model()

    def on_load_model(self, model_name):
        config = OmegaConf.load(f"v1-inference.yaml")
        self.model.load_model_from_config(config, model_name, verbose=False)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model = self.model.model.to(device)
        self.model.model = model

    def exec_sample(self, sample: str, step=20):
        model = self.model.model
        sampler = DDIMSampler(model)
        if sample.lower() == "dpm":
            sampler = DPMSolverSampler(model)
        elif sample.lower() == "plms":
            sampler = PLMSSampler(model)

