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
