import os
import re
from copy import deepcopy
import safetensors.torch

import torch
from loguru import logger

from ldm.util import instantiate_from_config
from omegaconf import OmegaConf


class StableDiffusionModel:
    def __init__(self, path, default_config, device, half=False, vae_half=False, map_location=None, show_global_state=False, opt_channelslast=False):
        self.path = path
        self.default_config = default_config
        self.device = device
        self.half = half
        self.vae_half = vae_half
        self.map_location = map_location
        self.show_global_state = show_global_state
        self.opt_channelslast = opt_channelslast
        self.checkpoint_list = []
        self.checkpoints = {}
        self.dtype = None
        self.dtype_vae = None
        self.model = None
        self.base_vae = None
        self.current_vae_file = None
        self.current_model = None
        self.chckpoint_dict_replacements = {
            'cond_stage_model.transformer.embeddings.': 'cond_stage_model.transformer.text_model.embeddings.',
            'cond_stage_model.transformer.encoder.': 'cond_stage_model.transformer.text_model.encoder.',
            'cond_stage_model.transformer.final_layer_norm.': 'cond_stage_model.transformer.text_model.final_layer_norm.',
        }
        self.vae_ignore_keys = {"model_ema.decay", "model_ema.num_updates"}
        self.sync_checkpoint_list()

    def load_model(self, model_name):
        if model_name not in self.checkpoints:
            raise ValueError(f"Model {model_name} not found")
        config = self.checkpoints[model_name]
        if config != self.default_config:
            config = os.path.join(self.path, config)
            logger.info(f"Loading model with custom config: {os.path.join(self.path, config)}")
        model_config = OmegaConf.load(config)
        if not hasattr(model_config.model.params, "use_ema"):
            model_config.model.params.use_ema = False
        if not self.half:
            model_config.model.params.unet_config.params.use_fp16 = False
        model = instantiate_from_config(model_config.model)
        self.load_model_weights(model_name, model)
        vae_name = re.sub(r"\.ckpt", "", model_name) + ".vae.pt"
        vae_name = "Anything-V3.0.vae.pt"
        if os.path.exists(os.path.join(self.path, vae_name)):
            self.load_vae(model, vae_name)
        self.model = model
        self.model.to(self.device)
        self.model.eval()
        self.current_model = model_name

    def unload_model(self):
        del self.model
        self.model = None
        del self.base_vae
        self.base_vae = None
        self.current_vae_file = None

    def load_model_weights(self, model_name, model):
        _, extension = os.path.splitext(model_name)
        if extension.lower() == ".safetensors":
            pl_sd = safetensors.torch.load_file(os.path.join(self.path, model_name), device=self.map_location)
        else:
            pl_sd = torch.load(os.path.join(self.path, model_name), map_location=self.map_location)
        if self.show_global_state and "global_step" in pl_sd:
            print(f"Global Step: {pl_sd['global_step']}")
        pl_sd = pl_sd.pop("state_dict", pl_sd)
        pl_sd.pop("state_dict", None)
        state_dict = {}
        for k, v in pl_sd.items():
            new_key = self.transform_checkpoint_dict_key(k)
            if new_key is not None:
                state_dict[new_key] = v
        pl_sd.clear()
        pl_sd.update(state_dict)
        model.load_state_dict(pl_sd, strict=False)
        del pl_sd, state_dict

        # TODO: if want implement cache, add here

        if self.opt_channelslast:
            model.to(memory_format=torch.channels_last)
        if self.half:
            vae = model.first_stage_model
            if not self.vae_half:
                # backup vae if vae half is not enabled
                model.first_stage_model = None
            model = model.half()
            model.first_stage_model = vae
        self.dtype = torch.float16 if self.half else torch.float32
        self.dtype_vae = torch.float16 if not self.vae_half or not self.half else torch.float32
        model.first_stage_model.to(self.dtype_vae)

    def load_vae(self, model, vae):
        vae_path = os.path.join(self.path, vae)
        if vae:
            self.cache_base_vae(model)
            vae_dict = torch.load(vae_path, map_location=self.map_location)
            vae_dict_filtered = {k: v for k, v in vae_dict["state_dict"].items() if k[0:4] != "loss" and k not in self.vae_ignore_keys}
            model.first_stage_model.load_state_dict(vae_dict_filtered)
            model.first_stage_model.to(self.dtype_vae)

        self.current_vae_file = vae

    def cache_base_vae(self, model):
        self.base_vae = deepcopy(model.first_stage_model.state_dict())

    def rollback_vae(self, model):
        if self.base_vae is not None:
            model.first_stage_model.load_state_dict(self.base_vae)
            model.first_stage_model.to(self.dtype_vae)
            self.current_vae_file = None
        self.base_vae = None

    def transform_checkpoint_dict_key(self, k):
        for text, replacement in self.chckpoint_dict_replacements.items():
            if k.startswith(text):
                k = replacement + k[len(text):]
        return k

    def sync_checkpoint_list(self):
        self.checkpoint_list = []
        checkpoint_list = list(filter(lambda x: x.endswith(".ckpt") or x.endswith(".safetensors"), os.listdir(self.path)))
        config_list = list(filter(lambda x: x.endswith(".yaml"), os.listdir(self.path)))
        for checkpoint in checkpoint_list:
            basename = os.path.basename(checkpoint)
            config = f"{basename}.yaml"
            if config not in config_list:
                config = self.default_config
            self.checkpoint_list.append((checkpoint, config))
        self.checkpoints = {k: v for k, v in self.checkpoint_list}
