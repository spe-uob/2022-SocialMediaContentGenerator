import enum
import os


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
        self.default_concept_config = concept_loader_args.get("default_concept_config", {})
        self.concepts = []
        if self.loading_mode == ConceptLoadingMode.Dict:
            self.load_concept_dict_mode()

    def load_concept_dict_mode(self):
        for concept_dict in self.dict_mode_dict_list:
            self.concepts.append(Concept(**concept_dict))

    def load_concept_path_mode(self):
        # dir structure:
        # - target_path
        #   - concept1
        #     - instance_image
        #       - 1.png
        #       - 1.txt
        #       - .....
        #     - class_image
        #       - hash.png
        #   - concept2
        #     ...
        #   - ...
        concept_dirs = [x for x in os.listdir(self.loading_target_path) if os.path.isdir(os.path.join(self.loading_target_path, x))]
        for concept_dir in concept_dirs:
            instance_image_dir = os.path.join(self.loading_target_path, concept_dir, "instance_image")
            class_image_dir = os.path.join(self.loading_target_path, concept_dir, "class_image")
            concept_config = {
                "instance_data_dir": instance_image_dir,
                "class_data_dir": class_image_dir,
                **self.default_concept_config
            }
            self.concepts.append(Concept(**concept_config))


class ConceptLoadingMode(enum.Enum):
    Dict = "dict"
    Path = "path"
