import json
import os

from loguru import logger

from config import Config
from core import Core
from scheduler import Scheduler
from utility.environment import Environment
import server_initializer


def load_config(path):
    if not os.path.exists(path):
        logger.info(f"Config file {path} not found")
        logger.info(f"Creating default config file {path}")
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(Config(), f, indent=4)
    with open(path, 'r', encoding="utf-8") as f:
        config = Config(**json.load(f))
    return config


def test_service():
    try:
        os.makedirs("models/lora")
        config = load_config("config.json")
        config["api_server"]["static_folder"] = "./"
        config["model_path"] = "./"
        config["default_model_config"] = "./v1-inference.yaml"
        core = Core(config)
        environment = Environment(config, core)
        scheduler = Scheduler(core, environment)
        environment.scheduler = scheduler
        api_server, components = server_initializer.initialize(environment, config['api_server']['static_folder'], config['api_server']['blog_path'])
        assert True
    except Exception as e:
        logger.error(e)
        assert False
