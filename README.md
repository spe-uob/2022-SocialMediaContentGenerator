# 2022-SocialMediaContentGenerator
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

### 1. nodejs: 18.x
  1.1 download the latest stable release of node.js from http://nodejs.org
### 2. quasar: latest
  2.1 Search `nodejs` on Google and download it, make sure use version 18.0.0 or higher
  
  2.2 install `yarn` by `npm install -g yarn`
  
  2.3 install `quasar` by `yarn add quasar`
  
  2.4 install `quasar cli` by `yarn global add @quasar/cli`
  
  2.5 install `vite plugin` by `yarn add quasar @quasar/extras`
  
  2.6 use `yarn global bin` to find yarn bin path and add it to environment variables and then, goto the directory of front end. execute `quasar dev` to develop quasar projects
### 3. nginx

## Back end

---

### 1. python >= 3.7
  1.1 download the latest stable release of python from http://python.org/downloads/
### 2. pytorch
  2.1 install `pytorch` by `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116`. pip should already be installed from python
  2.2 for more information, see https://pytorch.org/get-started/locally/ for different system specifications
### 3. stable diffusion

## training

1. deepbooru

## Software tools

jetbrain pycharm
