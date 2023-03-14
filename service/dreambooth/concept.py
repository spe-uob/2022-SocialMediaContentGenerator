class Concept(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self.instance_data_dir = kwargs.get("instance_data_dir", "")
        self.class_data_dir = kwargs.get("class_data_dir", "")
        self.instance_prompt = kwargs.get("instance_prompt", "")
        self.class_prompt = kwargs.get("class_prompt", "")
        self.save_sample_prompt = kwargs.get("save_sample_prompt", "")
        self.save_sample_template = kwargs.get("save_sample_template", "")
        self.instance_token = kwargs.get("instance_token", "")
        self.class_token = kwargs.get("class_token", "")
        self.num_class_images = kwargs.get("num_class_images", 0)
        self.class_negative_prompt = kwargs.get("class_negative_prompt", "")
        self.class_guidance_scale = kwargs.get("class_guidance_scale", 7.5)
        for key, value in kwargs.items():
            self[key] = value
