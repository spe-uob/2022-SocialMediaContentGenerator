from api_server import Application
from api_handlers import *


def api_register(app: Application, config: dict):
    app.register_handler(r"/api/v1/get_info", GetInfo, {"information_provider": config["information_provider"]})
    app.register_handler(r"/api/v1/model_list", ModelList, {"core": config["core"]})
    app.register_handler(r"/api/v1/load_model", LoadModel, {"core": config["core"]})
    app.register_handler(r"/api/v1/load_vae", LoadVAE, {"on_load_vae": config["core"].on_load_vae})
    app.register_handler(r"/api/v1/vae_list", VAEList, {"model_dir": config["model_dir"]})
    app.register_handler(r"/api/v1/sample", Sample, {"core": config["core"]})
