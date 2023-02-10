import os
from copy import deepcopy

import torch
from loguru import logger

from ldm.util import instantiate_from_config
from omegaconf import OmegaConf


class StableDiffusionModel:
    def __init__(self, path, default_config, half=False, vae_half=False, map_location=None, show_global_state=False, opt_channelslast=False):
        self.path = path
        self.default_config = default_config
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
            logger.info(f"Loading model with custom config: {os.path.join(self.path, config)}")
        model_config = OmegaConf.load(config)
        if not hasattr(model_config.model.params, "use_ema"):
            model_config.model.params.use_ema = False
        if not self.half:
            model_config.model.params.unet_config.params.use_fp16 = False
        model = instantiate_from_config(model_config.model)
        self.load_model_weights(model_name, model)


    def sync_checkpoint_list(self):
        self.checkpoint_list = []
        checkpoint_list = list(filter(lambda x: x.endswith(".ckpt"), os.listdir(self.path)))
        config_list = list(filter(lambda x: x.endswith(".yaml"), os.listdir(self.path)))
        for checkpoint in checkpoint_list:
            basename = os.path.basename(checkpoint)
            config = f"{basename}.yaml"
            if config not in config_list:
                config = self.default_config
            self.checkpoint_list.append((checkpoint, config))
        self.checkpoints = {k: v for k, v in self.checkpoint_list}
