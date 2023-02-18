import argparse
import json
import os

from loguru import logger

from config import Config
from core import Core
from utility import Environment
import server_initializer


def main(args):
    config = load_config(args.config)
    logger.info(f"Loaded config from {args.config}")
    core = Core(config)
    environment = Environment(config, core)
    api_server, components = server_initializer.initialize(environment, config['api_server']['static_folder'])
    api_server.run(args.host, args.port)


def load_config(path):
    if not os.path.exists(path):
        logger.info(f"Config file {path} not found")
        logger.info(f"Creating default config file {path}")
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(Config(), f, indent=4)
    with open(path, 'r', encoding="utf-8") as f:
        config = Config(**json.load(f))
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    parser.add_argument('--port', type=int, default=5000, help='Port to run server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='IP address to run server on')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
