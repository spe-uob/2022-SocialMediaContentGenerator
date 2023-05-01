import json
import logging
import os.path
import re

from bs4 import BeautifulSoup
from loguru import logger
from flask import Flask, send_from_directory, Blueprint, redirect
from flask_cors import CORS, cross_origin


class NonASCIIJSONEncoder(json.JSONEncoder):
    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(NonASCIIJSONEncoder, self).__init__(**kwargs)


class ApiServer:
    def __init__(self, static_url_path='', static_folder="web/dist/spa", blog_path="hexo/blog/public"):
        self.app = Flask(__name__,
                         static_url_path='',
                         static_folder=static_folder)
        # self.app.config['JSON_AS_ASCII'] = False
        self.app.config['RESTFUL_JSON'] = {
            'ensure_ascii': False
        }
        cors = CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        log = logging.getLogger('werkzeug')
        log.disabled = True
        logger.info("ApiServer initialized")
        logger.info("Static folder: " + static_folder)

    def run(self, host='127.0.0.1', port=5000):
        logger.info(f"server is running on http://{host}:{port}")
        self.app.run(threaded=True, host=host, port=port)

    def register(self, path, func, methods=['GET']):
        func.__func__.__name__ += path
        self.app.add_url_rule(path, view_func=func, methods=methods)
