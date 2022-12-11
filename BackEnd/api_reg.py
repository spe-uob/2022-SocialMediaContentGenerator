from api_server import Application
from api_handlers import *


def api_register(app: Application, config: dict):
    app.register_handler(r"/api/v1/get_info", GetInfo, {"information_object": {}})
    app.register_handler(r"/api/v1/model_list", ModelList, {"model_dir": config["model_dir"]})
    app.register_handler(r"/api/v1/load_model", LoadModel, {"on_load_model": config["core"].on_load_model})
    app.register_handler(r"/api/v1/sample", Sample, {"core": config["core"]})
