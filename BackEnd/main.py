import asyncio
import argparse

from api_server import Application
from stable_diffusion.core import Core
from stable_diffusion.model import Model
from api_reg import api_register


def main(opt: argparse.Namespace):
    core = Core()
    app = Application(8888)
    config = {
        "core": core,
        "model_list": Model.find_model(opt.model_path)
    }
    api_register(app, config)
    app.build_app()
    asyncio.run(app.run())


def parse_agrs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-path",
        type=str,
        nargs="?",
        default="stable_diffusion/models",
        help="the model dir path"
    )
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    main(parse_agrs())
