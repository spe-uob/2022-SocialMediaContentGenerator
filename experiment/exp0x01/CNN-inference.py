import  torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from torchvision.models import squeezenet1_1
import torch.functional as F
from io import open
import os
from PIL import Image
import pathlib
import glob
#import cv2
from torchvision.transforms import transforms

train_path = '/Users/flgodd/PycharmProjects/2022-SocialMediaContentGenerator/experiment/exp0x01/dataset/scene_detection/seg_train/seg_train'
pred_path = '/Users/flgodd/PycharmProjects/2022-SocialMediaContentGenerator/experiment/exp0x01/dataset/scene_detection/seg_pred/seg_pred'

# categories/classes

root = pathlib.Path(train_path)
classes = sorted([j.name.split('/')[-1] for j in root.iterdir()])

# CNN


class ConvNet(nn.Module):

    def __init__(self, num_classes=6):
        super(ConvNet, self).__init__()

        # Output size after convolution filter
        # ((w-f+2P)/s)+1 w = 150 width and height, f = 3 size of filter(kernel size), p = padding s = stride

        # Input shape = (256, 3, 150, 150)

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3, stride=1, padding=1)
        # Output shape = (256, 12, 150, 150)

        self.bn1 = nn.BatchNorm2d(num_features=12)
        # shape  = (256, 12, 150, 150)

        self.relu1 = nn.ReLU()
        # shape  = (256, 12, 150, 150)

        self.pool = nn.MaxPool2d(kernel_size=2)
        # reduce the image size by a factor of 2
        # shape  = (256, 12, 75, 75)

        self.conv2 = nn.Conv2d(in_channels=12, out_channels=20, kernel_size=3, stride=1, padding=1)
        # Output shape = (256, 20, 75, 75)

        self.relu2 = nn.ReLU()
        # shape  = (256, 20, 75, 75)

        self.conv3 = nn.Conv2d(in_channels=20, out_channels=32, kernel_size=3, stride=1, padding=1)
        # Output shape = (256, 32, 75, 75)

        self.bn3 = nn.BatchNorm2d(num_features=32)
        # shape  = (256, 32, 75, 75)

        self.relu3 = nn.ReLU()
        # shape  = (256, 32, 75, 75)

        self.fc = nn.Linear(in_features=32*75*75, out_features=num_classes)

        # feed forward function

    def forward(self, inp):
        output = self.conv1(inp)
        output = self.bn1(output)
        output = self.relu1(output)

        output = self.pool(output)

        output = self.conv2(output)
        output = self.relu2(output)

        output = self.conv3(output)
        output = self.bn3(output)
        output = self.relu3(output)

        # Above output will be in the matrix form, with shape( 256, 32, 75, 75)

        output = output.view(-1, 32*75*75)

        output = self.fc(output)

        return output


checkpoint = torch.load('best_checkpoint.model')
model = ConvNet(num_classes=6)
model.load_state_dict(checkpoint)
model.eval()

# transforms

transformer = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),  # 0-255 to 0-1, numpy to tensor
    transforms.Normalize([0.5, 0.5, 0.5],  # 0-1 to [-1, 1] , formula x-mean/std
                         [0.5, 0.5, 0.5])
])

# prediction function
def prediction(img_path, transformer):

    image = Image.open(img_path)

    image_tensor = transformer(image).float()  # feed image to transformer to transfer to tensor

    image_tensor = image_tensor.unsqueeze_(0)  # since pytorch saves in batches, have to add an extra batch using unsqueeze function

    if torch.cuda.is_available():
        image_tensor.cuda()

    input = Variable(image_tensor)

    output = model(input)

    index = output.data.numpy().argmax()

    pred = classes[index]

    return pred


images_path = glob.glob(pred_path+'/*.jpq')

pred_dict = {}

for i in images_path:
    pred_dict[i[i.rfind('/')+1:]] = prediction(i, transformer)

print(pred_dict)


