from web_server import ApiServer
from web_components import *

from utility import Environment, Component

init_web_components: [Component] = [Index, GetTasks, GetTxt2ImgTasks, VRAM, ModelList, LoadModel, CurrentModel, SamplerList, Txt2Img, Txt2ImgResult, Image, ImageList, ImageInfo, VaeList, LoadLora,
                                    LoraList, CurrentVae, CurrentLora, DeleteAPI, LoginAPI, PostAPI, StatusAPI, SaveToBlog, LoadBlog, BlogList, BlogServerUrl, TextGenerator, Key]


def initialize(environment: Environment, static_folder: str, blog_path) -> [ApiServer, [Component]]:
    api_server = ApiServer(static_folder=static_folder, blog_path=blog_path)
    instantiated_components = []
    for component_class in init_web_components:
        component = component_class(environment)
        instantiated_components.append(component)
        api_server.register(component.url, component.view, component.methods)
    return api_server, instantiated_components
