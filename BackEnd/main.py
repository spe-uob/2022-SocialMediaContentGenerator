import asyncio
import argparse

from api_server import Application
from information_provider import InformationProvider
from stable_diffusion.core import Core
from api_reg import api_register


def main(opt: argparse.Namespace):
    core = Core()
    information_provider = InformationProvider(core)
    # test = information_provider.get_info()
    app = Application(8888)
    config = {
        "core": core,
        "model_dir": opt.model_path,
        "information_provider": information_provider,
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
