# Install Tutorial

## List

- [Hardware prepare](#hardware-prepare)
- [Enviroment prepare](#enviroment-prepare)
- [Get promgram](#get-promgram)
- [Configure the config.json](#configure-the-config)
- [Run server](#run-server)
- [Download model](#download-model)
- [Nginx](#nginx)

## Hardware prepare
- Memory at least 12GB
- A Nvidia GPU with at least 8GB VRAM

## Enviroment prepare
- CUDA >= 11.3 and CUDA < 12.0
- Python 3.9.x
- Nodejs 18.x
- Cudnn 8.6(Optional, can accelerate some gpu such as 3090/4090)
- git
- proxy software(e.g. Nginx, Apache, Caddy, Only write Nginx example in this tutorial)

## Get promgram
The steps are as follows:
### Get code from github
```bash
git clone https://github.com/spe-uob/2022-SocialMediaContentGenerator.git
cd 2022-SocialMediaContentGenerator
```
### build front end
```bash
cd 2022-SocialMediaContentGenerator/web
# if use yarn
yarn install 
# if use npm
npm install 
# build quasar 
quasar build
# install for blog
cd 2022-SocialMediaContentGenerator/hexo/blog
# if use yarn
yarn install
yarn -g install hexo
# if use npm
npm install
npm -g install hexo
```
### make dir for models and install requierment for backend
```bash
cd 2022-SocialMediaContentGenerator/service
mkdir models
pip install -r requirements.txt
# run server first times, program will automaticlly generate config.json
# after server running, use ctrl+c to terminate
```
## Configure the config
Edit the config file service/config.json
following is the default config.json
```json
{
    "api_server": {
        "static_folder": "../web/dist/spa",
        "blog_path": "../hexo/blog/public"
    },
    "blog_root": "../hexo/blog",
    "blog_server_url": "http://127.0.0.1:8889",
    "model_path": "models",
    "lora_model_path": "models\\lora",
    "default_model_config": "v1-inference.yaml",
    "force_cpu": false,
    "map_location": "cpu",
    "sample_out_path": "images",
    "openai_api_key": "",
    "twitter_auth": {
        "consumer_key": "",
        "consumer_secret": ""
    },
    "linkedin_auth": {
        "application_key": "",
        "application_secret": ""
    },
    "facebook_auth": {
        "appid": ""
    }
}
```

if you exec the backend command 'python run.py' in directory `service`, the config in `"api_server"` is not nesseray to change

the `blog_server_url` is the url to access the blog page from internet

the `model_path` is the path to the folder that have the main model ckpt files.

the `lora_model_path` is the path to the folder that have the lora model files. If run on linux, please repleace \\ to /

I don't suggest use this flag `force_cpu`, I tested that use cpu only to run AI drawing, the result is it take 1 min only output 1 512x512 picture on I9-13900KF

The remaining configuration parameters do not need to be explained too much because the key already contains explanations.

## Run server
```bash
cd 2022-SocialMediaContentGenerator/service
python run.py
```
the argument `--port 8888` can change the port 

the argument `--host 0.0.0.0` can change the ip

the argument `----config config.json` can change the path to config file

## Download model

### Some link:

[https://huggingface.co/](https://huggingface.co/)

[https://civitai.com/](https://civitai.com/)

The issue of model authorization does not belong to this project, please check the introduction of each model for details.

## Nginx

```conf
# main site
server {
    listen      80;
    listen      [::]:80;
    listen      443 ssl http2;
    listen      [::]:443 ssl http2;
    server_name hostname;

    # SSL
    ssl_certificate     path_to_certificate;
    ssl_certificate_key path_to_certificate_key;

    # reverse proxy
    location / {
        proxy_pass            http://localhost:8888;
        proxy_set_header Host $host;
    }
}
# blog proxy
server {
    listen      80;
    listen      [::]:80;
    listen      443 ssl http2;
    listen      [::]:443 ssl http2;
    server_name blog_hostname; 

    # SSL
    ssl_certificate     path_to_certificate;
    ssl_certificate_key path_to_certificate_key;

    location / {
        proxy_pass            http://localhost:8889/;
        proxy_set_header Host $host;
    }
}
```
