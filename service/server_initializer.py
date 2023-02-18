from web_server import ApiServer
from environment import Environment
from component import Component
from web_components import *

init_web_components: [Component] = [Index]


def initialize(environment: Environment, static_folder: str) -> [ApiServer, [Component]]:
    api_server = ApiServer(static_folder=static_folder)
    instantiated_components = []
    for component_class in init_web_components:
        component = component_class(environment)
        instantiated_components.append(component)
        api_server.register(component.url, component.view, component.methods)
    return api_server, instantiated_components
