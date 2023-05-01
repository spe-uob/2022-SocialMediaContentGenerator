import logging
import os

from flask import Flask, request, jsonify, redirect, url_for, send_from_directory, render_template
from flask_autoindex import AutoIndex

from config import Config
import argparse

blog_path = "../hexo/blog/public"
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(blog_path + '/' + path) and os.path.isfile(blog_path + '/' + path):
        return send_from_directory(blog_path, path)
    else:
        return send_from_directory(os.path.join(blog_path, path), 'index.html')


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8889, help='Port to run server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='IP address to run server on')
    return parser.parse_args()


def run_blog_server(host=None, port=None):
    args = args_parser()
    if host is None:
        host = args.host
    if port is None:
        port = args.port
    from loguru import logger
    logger.info(f"Running blog server on {host}:{port}")
    app.run(host=host, port=port)


if __name__ == '__main__':
    run_blog_server()
