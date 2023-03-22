![python ci](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/python.yml/badge.svg) 
[![Node.js CI Build and Lint](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/nodejs_ci_build_and_lint.yml/badge.svg)](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/nodejs_ci_build_and_lint.yml) 
[![Python Test and Deploy](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/main_python_cd.yml/badge.svg)](https://github.com/spe-uob/2022-SocialMediaContentGenerator/actions/workflows/main_python_cd.yml)

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
  - [Dev env](#dev-env)
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

# Dev env

## Front end

---
### Mac:
### 1. nodejs: 18.x
  1.1 download the latest stable release of node.js from http://nodejs.org
  
### 2. quasar
  2.1 install `yarn` by `npm install -g yarn` may need to use `sudo npm install -g yarn` to be an admin.
    
  2.2 install `quasar` by `yarn add quasar`
  
  2.3 install `quasar cli` by `yarn global add @quasar/cli`
  
  2.4 install `vite plugin` by `yarn add quasar @quasar/extras`
  
  2.5 use `yarn global bin` to find yarn bin path and add it to environment variables and then, goto the directory of front end. execute `quasar dev` to develop quasar projects
    
  2.6 if using yarn doesn't work do `sudo npm i -g @quasar/cli`

### Windows:

### 1. nodejs: 18.x
  1.1 download the latest stable release of node.js from http://nodejs.org
### 2. quasar: latest
  2.1 Search `nodejs` on Google and download it, make sure use version 18.0.0 or higher
  
  2.2 install `yarn` by `npm install -g yarn`
  
  2.3 install `quasar` by `yarn add quasar`
  
  2.4 install `quasar cli` by `yarn global add @quasar/cli`
  
  2.5 install `vite plugin` by `yarn add quasar @quasar/extras`
  
  2.6 use `yarn global bin` to find yarn bin path and add it to environment variables and then, goto the directory of front end. execute `quasar dev` to develop quasar projects

## Back end

---
### Mac:
### 1. python >= 3.9 should already be installed on a mac os system but run `python --version` if not up to date do:
  1.1 `brew install python` --> install the latest Python.
    
  1.2 ls -l /usr/local/bin/python* --> List all Python versions installed on your system.
    
  1.3 `ln -s -f /usr/local/bin/python[your-latest-version-just-installed] /usr/local/bin/python` --> Change default Python version to the latest version.
        E.g: `ln -s -f /usr/local/bin/python3.9 /usr/local/bin/python`
        
  1.4 Restart terminal.
    
  1.5 `python --version` --> Check Python version default again.
    
### 2. pytorch
  2.1 run `pip3 install torch torchvision torchaudio`
   
### 3. pycharm 
  3.1 check what type of core your mac has either Intel or Apple Silicon by going to "about this mac" after clicking the apple in the top left.
    
  3.2 go to https://www.jetbrains.com/pycharm/download/#section=mac
    
      
    
### Windows:
### 1. python >= 3.9
  1.1 download the latest stable release of python from http://python.org/downloads/
### 2. pytorch
  2.1 install `pytorch` by `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116`. pip should already be installed from python
  2.2 for more information, see https://pytorch.org/get-started/locally/ for different system specifications

## training

1. deepbooru waiting for back end development implementation

jetbrain pycharm

## Project Requirements

  - Need to have access to the internet.
  - Need to have either a twitter, facebook or linkedIn account to be able to use the website.
  - It is better have a at least 4GB VRAM NVIDIA GPU to accelerate the generation process.
