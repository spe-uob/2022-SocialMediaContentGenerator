import os

from flask import abort, send_from_directory
from PIL import Image as PILImage
from . import *


class Image(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/cached_image', 'Image', ['GET'])
        self.env = env

    def view(self):
        path = request.args.get('path')
        if path is not None and os.path.exists(path) and os.path.isfile(path) and path.endswith('.png'):
            file_name = os.path.basename(path)
            # get path except file name
            full_path = os.path.dirname(path)
            return send_from_directory(full_path, file_name)
        else:
            return abort(404)


class ImageList(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/image_list', 'ImageList', ['GET'])
        self.env = env

    def view(self):
        image_list = [x for x in os.listdir("./images") if x.endswith('.png')]
        image_list = list(map(lambda x: f"images/{x}", image_list))
        return image_list


class ImageInfo(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/api/v1/image_info', 'ImageInfo', ['GET'])
        self.env = env

    def view(self):
        path = request.args.get('path')
        if path.endswith('.png'):
            image = PILImage.open(path)
            width, height = image.size
            return {'width': width, 'height': height}
        else:
            return abort(404)
