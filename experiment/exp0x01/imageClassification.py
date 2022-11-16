import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.datasets
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import os
import numpy as np
import glob
from torch.optim import Adam
from torch.autograd import Variable
import pathlib

# checking device

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# transforms

transformer = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),  # 0-255 to 0-1, numpy to tensor
    transforms.Normalize([0.5, 0.5, 0.5],  # 0-1 to [-1, 1] , formula x-mean/std
                         [0.5, 0.5, 0.5])
])

# Dataloader

# Path for train and test directory

train_path = '/Users/flgodd/PycharmProjects/2022-SocialMediaContentGenerator/experiment/exp0x01/dataset/scene_detection/seg_train/seg_train'
test_path = '/Users/flgodd/PycharmProjects/2022-SocialMediaContentGenerator/experiment/exp0x01/dataset/scene_detection/seg_test/seg_test'

train_loader = DataLoader(
    torchvision.datasets.ImageFolder(train_path, transform=transformer),
    batch_size=256, shuffle=True
)
test_loader = DataLoader(
    torchvision.datasets.ImageFolder(test_path, transform=transformer),
    batch_size=256, shuffle=True
)

# categories/classes

root = pathlib.Path(train_path)
classes = sorted([j.name.split('/')[-1] for j in root.iterdir()])

# print(classes)

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


model = ConvNet(num_classes=6).to(device)

# Optimizer and loss function
optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
loss_function = nn.CrossEntropyLoss()

num_epochs = 10

# calculating teh size of training and testing images
train_count = len(glob.glob(train_path+'/**/*.jpg'))
test_count = len(glob.glob(test_path+'/**/*.jpg'))

print(train_count, test_count)

# Model training and saving best model
best_accuracy = 0.0

for epoch in range(num_epochs):

    # Evaluate and training on training dataset
    model.train()
    train_accuracy = 0.0
    train_loss = 0.0

    for i, (images, labels) in enumerate(train_loader):
        if torch.cuda.is_available():
            images = Variable(images.cuda())
            labels = Variable(labels.cuda())

        optimizer.zero_grad()

        outputs = model(images)
        loss = loss_function(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.cpu().data*images.size(0)
        _, prediction = torch.max(outputs.data, 1)
        train_accuracy += int(torch.sum(prediction==labels.data))

    train_accuracy = train_accuracy/train_count
    train_loss = train_loss/train_count

    # Evaluation on testing dataset
    model.eval()

    test_accuracy = 0.0
    for i, (images, labels) in enumerate(test_loader):
        if torch.cuda.is_available():
            images = Variable(images.cuda())
            labels = Variable(labels.cuda())

        outputs = model(images)
        _, prediction = torch.max(outputs.data, 1)
        test_accuracy += int(torch.sum(prediction==labels.data))

    test_accuracy = test_accuracy/test_count

    print('Epoch: ' + str(epoch) + ' Train loss' + str(int(train_loss)) + ' Train accuracy: ' + str(int(train_accuracy)) + 'Test accuracy: '+str(int(test_accuracy)))

    # Save the best model
    if test_accuracy > best_accuracy:
        torch.save(model.state_dict(), 'best_checkpoint.model')
        best_accuracy = test_accuracy
# fin



