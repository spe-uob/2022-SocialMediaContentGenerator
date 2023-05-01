import argparse
import json
import os

from loguru import logger
from multiprocessing import Process
from config import Config
from core import Core
from scheduler import Scheduler
from utility.environment import Environment
import server_initializer


def main(args):
    config = load_config(args.config)
    logger.info(f"Loaded config from {args.config}")
    save_config(args.config, config)
    core = Core(config)
    environment = Environment(config, core)
    scheduler = Scheduler(core, environment)
    environment.scheduler = scheduler
    scheduler.start()
    api_server, components = server_initializer.initialize(environment, config['api_server']['static_folder'], config['api_server']['blog_path'])
    environment.api_server = api_server
    p = Process(target=run_blog)
    p.start()
    api_server.run(args.host, args.port)
    logger.info("Stopping scheduler...")
    p.join()
    scheduler.stop()


def run_blog():
    import blog_server
    blog_server.run_blog_server()


def load_config(path):
    if not os.path.exists(path):
        logger.info(f"Config file {path} not found")
        logger.info(f"Creating default config file {path}")
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(Config(), f, indent=4)
    with open(path, 'r', encoding="utf-8") as f:
        config = Config(**json.load(f))
    return config


def save_config(path, config):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    parser.add_argument('--port', type=int, default=8888, help='Port to run server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='IP address to run server on')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
