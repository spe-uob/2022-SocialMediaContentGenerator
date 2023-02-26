import inspect
from collections import deque

import k_diffusion
import torch

from stable_diffusion import prompt_parser


class TypicalStableDiffusionSampler:
    def __init__(self, init_func, model):
        self.sampler = init_func(model)
        self.is_plms = hasattr(self.sampler, 'p_sample_plms')
        self.orig_p_sample_ddim = self.sampler.p_sample_plms if self.is_plms else self.sampler.p_sample_ddim

        self.init_latent = None
        self.last_latent = None
        self.step = 0
        self.eta = 0.0

    def sample(self, x, conditioning, unconditional_conditioning, steps, cfg_scale=7.5):
        self.init_latent = None
        self.last_latent = x
        self.step = 0

        sample_results = self.sampler.sample(S=steps, conditioning=conditioning, batch_size=int(x.shape[0]), shape=x[0].shape, verbose=False, unconditional_guidance_scale=cfg_scale,
                                             unconditional_conditioning=unconditional_conditioning, x_T=x, eta=self.eta)[0]
        return sample_results

    @staticmethod
    def number_of_needed_noises(p):
        return 0


# learn from https://github.com/AUTOMATIC1111/stable-diffusion-webui/
class CFGDenoiserParams:
    def __init__(self, x, image_cond, sigma, sampling_step, total_sampling_steps):
        self.x = x
        """Latent image representation in the process of being denoised"""

        self.image_cond = image_cond
        """Conditioning image"""

        self.sigma = sigma
        """Current sigma noise step value"""

        self.sampling_step = sampling_step
        """Current Sampling step number"""

        self.total_sampling_steps = total_sampling_steps
        """Total number of sampling steps planned"""


# learn from https://github.com/AUTOMATIC1111/stable-diffusion-webui/
class CFGDenoiser(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.inner_model = model
        self.mask = None
        self.nmask = None
        self.init_latent = None
        self.step = 0

    def combine_denoised(self, x_out, conds_list, uncond, cond_scale):
        denoised_uncond = x_out[-uncond.shape[0]:]
        denoised = torch.clone(denoised_uncond)

        for i, conds in enumerate(conds_list):
            for cond_index, weight in conds:
                denoised[i] += (x_out[cond_index] - denoised_uncond[i]) * (weight * cond_scale)

        return denoised

    def forward(self, x, sigma, uncond, cond, cond_scale, image_cond):
        # if state.interrupted or state.skipped:
        #     raise InterruptedException

        conds_list, tensor = prompt_parser.reconstruct_multicond_batch(cond, self.step)
        uncond = prompt_parser.reconstruct_cond_batch(uncond, self.step)

        batch_size = len(conds_list)
        repeats = [len(conds_list[i]) for i in range(batch_size)]

        x_in = torch.cat([torch.stack([x[i] for _ in range(n)]) for i, n in enumerate(repeats)] + [x])
        image_cond_in = torch.cat([torch.stack([image_cond[i] for _ in range(n)]) for i, n in enumerate(repeats)] + [image_cond])
        sigma_in = torch.cat([torch.stack([sigma[i] for _ in range(n)]) for i, n in enumerate(repeats)] + [sigma])

        # denoiser_params = CFGDenoiserParams(x_in, image_cond_in, sigma_in, state.sampling_step, state.sampling_steps)
        denoiser_params = CFGDenoiserParams(x_in, image_cond_in, sigma_in, 0, 0)
        # cfg_denoiser_callback(denoiser_params)
        x_in = denoiser_params.x
        image_cond_in = denoiser_params.image_cond
        sigma_in = denoiser_params.sigma
        batch_cond_uncond = True
        if tensor.shape[1] == uncond.shape[1]:
            cond_in = torch.cat([tensor, uncond])

            if batch_cond_uncond:
                x_out = self.inner_model(x_in, sigma_in, cond={"c_crossattn": [cond_in], "c_concat": [image_cond_in]})
            else:
                x_out = torch.zeros_like(x_in)
                for batch_offset in range(0, x_out.shape[0], batch_size):
                    a = batch_offset
                    b = a + batch_size
                    x_out[a:b] = self.inner_model(x_in[a:b], sigma_in[a:b], cond={"c_crossattn": [cond_in[a:b]], "c_concat": [image_cond_in[a:b]]})
        else:
            x_out = torch.zeros_like(x_in)
            batch_size = batch_size * 2 if batch_cond_uncond else batch_size
            for batch_offset in range(0, tensor.shape[0], batch_size):
                a = batch_offset
                b = min(a + batch_size, tensor.shape[0])
                x_out[a:b] = self.inner_model(x_in[a:b], sigma_in[a:b], cond={"c_crossattn": [tensor[a:b]], "c_concat": [image_cond_in[a:b]]})

            x_out[-uncond.shape[0]:] = self.inner_model(x_in[-uncond.shape[0]:], sigma_in[-uncond.shape[0]:], cond={"c_crossattn": [uncond], "c_concat": [image_cond_in[-uncond.shape[0]:]]})

        denoised = self.combine_denoised(x_out, conds_list, uncond, cond_scale)

        if self.mask is not None:
            denoised = self.init_latent * self.mask + self.nmask * denoised

        self.step += 1

        return denoised


# learn from https://github.com/AUTOMATIC1111/stable-diffusion-webui/
class TorchHijack:
    def __init__(self, sampler_noises):
        # Using a deque to efficiently receive the sampler_noises in the same order as the previous index-based
        # implementation.
        self.sampler_noises = deque(sampler_noises)
        self.device = torch.device('cpu')

    def __getattr__(self, item):
        if item == 'randn_like':
            return self.randn_like

        if hasattr(torch, item):
            return getattr(torch, item)

        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, item))

    def randn_like(self, x):
        if self.sampler_noises:
            noise = self.sampler_noises.popleft()
            if noise.shape == x.shape:
                return noise

        if x.device.type == 'mps':
            return torch.randn_like(x, device=self.device).to(x.device)
        else:
            return torch.randn_like(x)


# learn from https://github.com/AUTOMATIC1111/stable-diffusion-webui/
class KDiffusionSampler:
    def __init__(self, sampler_func, model, device, enable_quantization=False):
        denoiser = k_diffusion.external.CompVisDenoiser

        self.model_wrap = denoiser(model, quantize=enable_quantization)
        self.func = sampler_func
        self.model_wrap_cfg = CFGDenoiser(self.model_wrap)
        self.device = device
        self.sampler_noises = None
        self.eta = 0

    def initialize(self):
        self.model_wrap_cfg.mask = None
        self.model_wrap_cfg.nmask = None
        self.model_wrap.step = 0
        self.eta = 0

        k_diffusion.sampling.torch = TorchHijack(self.sampler_noises if self.sampler_noises is not None else [])

        extra_params_kwargs = {}
        # for param_name in self.extra_params:
        #     if hasattr(p, param_name) and param_name in inspect.signature(self.func).parameters:
        #         extra_params_kwargs[param_name] = getattr(p, param_name)

        if 'eta' in inspect.signature(self.func).parameters:
            extra_params_kwargs['eta'] = self.eta

        return extra_params_kwargs

    @staticmethod
    def number_of_needed_noises(steps):
        return steps

    def sample(self, x, conditioning, unconditional_conditioning, steps, cfg_scale=7, image_conditioning=None):

        sigmas = k_diffusion.sampling.get_sigmas_karras(n=steps, sigma_min=0.1, sigma_max=10, device=self.device)

        x = x * sigmas[0]

        extra_params_kwargs = self.initialize()
        if 'sigma_min' in inspect.signature(self.func).parameters:
            extra_params_kwargs['sigma_min'] = self.model_wrap.sigmas[0].item()
            extra_params_kwargs['sigma_max'] = self.model_wrap.sigmas[-1].item()
            if 'n' in inspect.signature(self.func).parameters:
                extra_params_kwargs['n'] = steps
        else:
            extra_params_kwargs['sigmas'] = sigmas

        self.last_latent = x
        samples = self.func(self.model_wrap_cfg, x, extra_args={
            'cond': conditioning,
            'image_cond': image_conditioning,
            'uncond': unconditional_conditioning,
            'cond_scale': cfg_scale
        }, disable=False, callback=lambda **kwargs: None, **extra_params_kwargs)

        return samples
