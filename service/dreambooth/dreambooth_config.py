class DreamboothConfig(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self.working_path = kwargs.get("working_path", "")
        self.epochs = kwargs.get("epochs", 0)
        self.max_steps = kwargs.get("max_steps", 0)
        self.saving_model_frequency = kwargs.get("saving_model_frequency", 0)
        self.saving_sample_frequency = kwargs.get("saving_sample_frequency", 0)
        self.batch_size = kwargs.get("batch_size", 1)
        self.learning_rate = kwargs.get("learning_rate", 5e-5)
        self.resolutions = kwargs.get("resolutions", 512)
        self.cache_latent = kwargs.get("cache_latent", False)
        self.train_unet = kwargs.get("train_unet", True)
        self.train_clip = kwargs.get("train_clip", True)

        for key, value in kwargs.items():
            self[key] = value
