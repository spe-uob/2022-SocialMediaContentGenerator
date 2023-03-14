import enum


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


class ConceptLoader:
    def __init__(self, concept_loader_args):
        self.loading_mode = concept_loader_args.get("loading_mode", ConceptLoadingMode.Dict)
        self.dict_mode_dict_list = concept_loader_args.get("dict_mode_dict_list", [])
        self.loading_target_path = concept_loader_args.get("loading_target_path", "")
        self.concepts = []
        if self.loading_mode == ConceptLoadingMode.Dict:
            self.load_concept_dict_mode()

    def load_concept_dict_mode(self):
        pass

    def load_concept_path_mode(self):
        pass


class ConceptLoadingMode(enum.Enum):
    Dict = "dict"
    Path = "path"
