import base64
import logging
import os
import random
import re
import threading
import time
import uuid
import queue

import cv2
import numpy as np
import torch
import tweepy
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS, cross_origin

from sd_rebuild.MemoryOptimizer import MemoryOptimizer, CorsAttentionOptimizationMode
from sd_rebuild.model import StableDiffusionModel
from sd_rebuild.txt2img import Txt2Img

app = Flask(__name__, static_url_path='', static_folder=r"D:\projects\2022-SocialMediaContentGenerator\FrontEndv2.0\quasar-project\dist\spa")
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
log = logging.getLogger('werkzeug')
log.disabled = True

model_path = r"S:\ckpt\source_model"
default_config = r"W:\work\stable-diffusion-webui-old-dreambooth\v1-inference.yaml"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
memory_optimizer = MemoryOptimizer()
memory_optimizer.apply_memory_optimizations(CorsAttentionOptimizationMode.DEFAULT)
model_loader = StableDiffusionModel(model_path, default_config, device, half=True, map_location="cpu" if device.type == "cpu" else None)
txt2img: Txt2Img = None
sample_queue = queue.Queue()
current_task = None
sample_result = {}
model_loading = False
stop_sample = False


def sample_worker():
    global txt2img, current_task, sample_result, model_loading, stop_sample
    while not stop_sample:
        if txt2img is None:
            time.sleep(0.1)
            continue
        if sample_queue.empty():
            time.sleep(0.1)
            continue
        uuid_str, prompt, negative_prompt, sampler, step, width, height, n_iter, batch_size, cfg = sample_queue.get()
        current_task = (uuid_str, prompt, negative_prompt, sampler, step, width, height, n_iter, batch_size, cfg)
        sample_result[uuid_str] = []
        for i in range(n_iter):
            results = txt2img.generate(prompt, negative_prompt, height, width, batch_size, random.randint(1000000, 1000000000), sample=sampler, steps=step, cfg=cfg)
            save_images(results)
            sample_result[uuid_str] += results
        current_task = None


sample_thread = threading.Thread(target=sample_worker)
sample_thread.start()


@app.route("/api/v1/sample", methods=['POST'])
def sample():
    data = request.get_json()
    prompt = data['prompts']
    negative_prompt = data['negative_prompt']
    sampler = data['sample']
    step = data['step']
    width = data['width']
    height = data['height']
    n_iter = data['n_iter']
    batch_size = data['batch_size']
    cfg = data['cfg']
    uuid_str = str(uuid.uuid4())
    sample_queue.put((uuid_str, prompt, negative_prompt, sampler, step, width, height, n_iter, batch_size, cfg))
    return {"status": 0, "uuid": uuid_str, "length": n_iter * batch_size}


@app.route("/api/v1/get_sample_result", methods=['GET'])
def get_sample_result():
    uuid_str = request.args.get('uuid')
    length = int(request.args.get('length'))
    loaded = int(request.args.get('loaded'))
    if uuid_str in sample_result.keys():
        result = sample_result[uuid_str]
        response = {"status": 0, "images": []}
        for image in result[loaded:len(result)]:
            retval, buffer = cv2.imencode('.jpg', cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            pic_str = base64.b64encode(buffer)
            pic_str = pic_str.decode()
            response["images"].append(f"data:image/jpg;base64,{pic_str}")
        if len(result) == length:
            del sample_result[uuid_str]
        return response
    else:
        return {"status": 0, "images": []}


def save_images(images):
    if not os.path.exists("images"):
        os.mkdir("images")
    existing = [x for x in os.listdir("images") if re.match(r"^[0-9]+.*\.png$", x)]
    existing.sort(key=lambda x: int(re.search(r"^[0-9]+", x)[0]))
    last = 0
    if len(existing) > 0:
        last = int(re.search(r"^[0-9]+", existing[-1])[0])
    for i, image in enumerate(images):
        image.save(f"images/{str(last + i + 1).zfill(5)}.png")


@app.route("/api/v1/get_task_info", methods=['GET'])
def get_task_info():
    queue_copy = list(sample_queue.queue)
    if current_task is not None:
        queue_copy.insert(0, current_task)
    length = len(queue_copy)
    return {"status": 0, "queue_length": length,
            "tasks": [
                {
                    "uuid": uuid_str,
                    "progress": 0 if uuid_str not in sample_result.keys() else len(sample_result[uuid_str]) / n_iter * batch_size,
                    "length": n_iter * batch_size,
                    "n_iter": n_iter,
                    "batch_size": batch_size,
                    "width": width,
                    "height": height,
                    "step": step,
                    "sampler": sampler,
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "cfg": cfg
                } for uuid_str, prompt, negative_prompt, sampler, step, width, height, n_iter, batch_size, cfg in queue_copy]}


@app.route("/api/v1/sampler_list", methods=['GET'])
def sampler_list():
    if txt2img is None:
        return {"sampler_list": ["DDIM", "PLMS"]}
    else:
        return {"sampler_list": list(txt2img.samplers.keys())}


@app.route("/api/v1/vram", methods=['GET'])
def vram():
    allocated = torch.cuda.memory_allocated(0) / (1024 ** 3)
    cached = torch.cuda.memory_reserved(0) / (1024 ** 3)
    device_total = (torch.cuda.mem_get_info()[1]) / (1024 ** 3)
    return {"allocated": allocated, "cached": cached, "device_total": device_total}


@app.route("/api/v1/model_list", methods=['GET'])
def model_list():
    model_loader.sync_checkpoint_list()
    return {"mode_list": list(model_loader.checkpoints.keys())}


@app.route("/api/v1/load_model", methods=['GET'])
def load_model():
    global txt2img
    model_name = request.args.get('ModelName')
    model_loader.load_model(model_name)
    txt2img = Txt2Img(model_loader.model, device, model_loader.dtype_vae)
    return {"status": 0}


@app.route("/api/v1/get_info", methods=['GET'])
def get_info():
    return {"current_model": model_loader.current_model}


@app.route("/api/v1/tweet", methods=['GET', 'POST'])
def twitter():
    # identify the request type
    if request.method == 'GET':
        data = request.args
    else:
        data = request.get_json()
    tweet_string = data.get('status')
    consumer_key = data.get('consumer_key')
    consumer_secret = data.get('consumer_secret')
    access_token = data.get('access_token')
    access_token_secret = data.get('access_token_secret')
    image_base = data.get('image_base', '')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    # api.update_status(tweet_string, media_data=image_base)
    try:
        if image_base == '':
            api.update_status(tweet_string)
        else:
            api.update_status(tweet_string, media_data=image_base)
        # api.update_status_with_media(tweet_string, '../assets/dkqad8ncoz871.jpg')
        # api.update_status_with_media(tweet_string, '../assets/dkqad8ncoz871.jpg')

        return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)})


@app.route("/", methods=['GET'])
def index():
    return redirect("/index.html", code=302)


if __name__ == "__main__":
    app.run(port=8888)
    stop_sample = True
    sample_thread.join()
