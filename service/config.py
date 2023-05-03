import os


class Config(dict):
    def __init__(self, **kwargs):
        api_server_config = kwargs.get("api_server", {})
        twitter_auth_config = kwargs.get("twitter_auth", {})
        linkedin_auth = kwargs.get("linkedin_auth", {})
        facebook_auth = kwargs.get("facebook_auth", {})
        dict_body = {
            "api_server": {
                "static_folder": api_server_config.get("static_folder", "../web/dist/spa"),
                "blog_path": api_server_config.get("blog_path", "../hexo/blog/public"),
            },
            "blog_root": kwargs.get("blog_root", "../hexo/blog"),
            "blog_server_url": kwargs.get("blog_server_url", "http://127.0.0.1:8889"),
            "model_path": kwargs.get("model_path", "models"),
            "lora_model_path": kwargs.get("lora_model_path", os.path.join(kwargs.get("model_path", "models"), "lora")),
            "default_model_config": kwargs.get("default_model_config", "v1-inference.yaml"),
            "force_cpu": kwargs.get("force_cpu", False),
            "map_location": kwargs.get("map_location", "cpu"),
            "sample_out_path": kwargs.get("sample_out_path", "images"),
            "openai_api_key": kwargs.get("openai_api_key", ""),
            "twitter_auth": {
                "consumer_key": twitter_auth_config.get("consumer_key", ""),
                "consumer_secret": twitter_auth_config.get("consumer_secret", ""),
            },
            "linkedin_auth": {
                "application_key": linkedin_auth.get("application_key", ""),
                "application_secret": linkedin_auth.get("application_secret", ""),
            },
            "facebook_auth": {
                "appid": facebook_auth.get("appid", ""),
            }
        }
        for key, value in dict_body.items():
            self.__setattr__(key, value)
        super().__init__(**dict_body)
