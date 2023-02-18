from flask import redirect

from . import *


class Index(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/', 'Index', ['GET'])
        self.env = env

    def view(self):
        return redirect("/index.html", code=302)
