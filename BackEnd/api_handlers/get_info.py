from typing import Optional, Awaitable

import tornado.web


class GetInfo(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        self.information_object = {}
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, information_object):
        self.information_object = information_object

    def get(self):
        self.write(self.information_object)
