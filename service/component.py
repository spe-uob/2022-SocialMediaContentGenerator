import abc


class Component:
    def __init__(self, env, url, name, methods=['GET']):
        self.env = env
        self.url = url
        self.name = name
        self.methods = methods

    @abc.abstractmethod
    def view(self):
        pass
