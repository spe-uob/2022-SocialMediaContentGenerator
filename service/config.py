class Config(dict):
    def __init__(self, **kwargs):
        api_server_config = kwargs.get("api_server", {})
        dict_body = {
            "api_server": {
                "static_folder": api_server_config.get("static_folder", "../web/dist/spa"),
            },
            "model_path": kwargs.get("model_path", "models"),
            "default_model_config": kwargs.get("default_model_config", "v1-inference.yaml"),
            "force_cpu": kwargs.get("force_cpu", False),
            "map_location": kwargs.get("map_location", "cpu"),
            "sample_out_path": kwargs.get("sample_out_path", "images"),
        }
        for key, value in dict_body.items():
            self.__setattr__(key, value)
        super().__init__(**dict_body)
