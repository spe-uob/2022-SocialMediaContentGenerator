[![Python Test](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/python_test.yml/badge.svg)](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/python_test.yml)
[![Node.js CI Build and Lint](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/nodejs_ci_build_and_lint.yml/badge.svg)](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/nodejs_ci_build_and_lint.yml) 
[![Python Test and Deploy](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/main_python_cd.yml/badge.svg)](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/main_python_cd.yml)
[![Check Invalid Directories](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/invalid_dir_check.yml/badge.svg)](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/invalid_dir_check.yml)

# 2022-SocialMediaContentGenerator

## Working Time:

### Benjamin Aram

### David Yan

### Gene Ding

### Stephen Chen [![wakatime](https://wakatime.com/badge/user/23381c4b-372b-46eb-b687-994db38af858/project/f95e8755-5e2c-42fe-b093-687599dfb8b1.svg)](https://wakatime.com/badge/user/23381c4b-372b-46eb-b687-994db38af858/project/f95e8755-5e2c-42fe-b093-687599dfb8b1)

## Table of Contents
  - [About the project](#about-the-project)
  - [Our client](#our-client)
  - [Our group members](#our-group-members)
  - [Stakeholders and User Stories](#stakeholders-and-user-stories)
  - [Front end](#front-end)
  - [Back end](#back-end)
  - [Project Requirements](#project-requirements)
  

## About the project
An autonomous AI assistant to generate content for social media based on recent trends designed for companies that aim to extend their social media presence. 
Metrics that will be taking into consideration are key words, hashtags, geography, demography, international observances, trending topics etc. in order to keep up to date with trends using a Pytorch infrastructure.

## Our client
https://spacenxtlabs.com

## Our group members
Benjamin Aram

David Yan

Gene Ding

Stephen Chen

## Technology Stack

### Front end
- Quasar
- Vue.js
- HTML
- CSS
- JavaScript
- Node.js
- Vite
- Twitter API
- Facebook API
- LinkedIn API

### Back end
- Python
- Pytorch
- CUDA
- Twitter API
- Facebook API
- LinkedIn API
- GPT-3(OpenAI API)
- Latent Diffusion Model(Stable Diffusion)
    - [[Paper Link: https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)]
    - [[Project Link: https://github.com/CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)]
- LoRA: Low-Rank Adaptation of Large Language Models
    - [[Paper Link: https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)]
 
## Web and service

--- 
### 1. nodejs: 18.x
1.1 download the latest stable release of node.js from http://nodejs.org

### 2. quasar
2.1 install `yarn` by `npm install -g yarn` may need to use `sudo npm install -g yarn` to be an admin.

2.2 install `quasar` by `yarn add quasar`

2.3 install `quasar cli` by `yarn global add @quasar/cli`

2.4 install `vite plugin` by `yarn add quasar @quasar/extras`

2.5 use `yarn global bin` to find yarn bin path and add it to environment variables and then, goto the directory of front end. execute `quasar dev` to develop quasar projects

2.6 if using yarn doesn't work do `sudo npm i -g @quasar/cli`

### 3. python prepare
3.1 run `pip install -r requirements.txt`

### 4. cuda
4.1 install `cuda` from nvidia website https://developer.nvidia.com/cuda-downloads

## Project Requirements

- Need to have access to the internet.
- Need to have either a twitter, facebook or linkedIn account to be able to use the website.
- It is better have a at least 8GB VRAM NVIDIA GPU to accelerate the generation process.

# Stakeholders and User Stories

## Stakeholders
SpaceNXT Labs: 

Distributing the project.

SpaceNXT Labs target customers: 

Companies and organisations that strive to keep their social media presence active and up to date

General public: 

Individuals that want to keep their social media presence active and up to date.
Individuals that consume the social media trends.

Legislators:

GDPR usage of social media user data.

## User Stories
SpaceNXT Labs:
As a representative of SpaceNXT, I want to have a service that can predict social media trends.

Companies and organisations:
As a company interested in using the service, I want to be able to appeal to the younger demographic through the use of social media trends.

Member of the general public (content creator):
As a member of the general public, I want to keep up to date with social media trends to increase my follow account.

Member of the general public (consumer):
As a general consumer of social media content, I want to see the newest trends to keep up with people around me.

