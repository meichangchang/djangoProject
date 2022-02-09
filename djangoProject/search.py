import os
import numpy as np
import random
import torch
import torch.nn as nn
import torch.utils as utils
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.autograd import Variable
from torch.utils.data import DataLoader

# 配置参数
epoch = 120
batch_size = 32
learning_rate = 0.1

# 加载数据集
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))])

trainset = ImageFolder(root="static/image/dataset/search/hua", transform=transform)
testset = ImageFolder(root="static/image/dataset/search/hua", transform=transform)
train_loader = DataLoader(dataset=trainset, batch_size=128, shuffle=True, drop_last=True)
test_loader = DataLoader(dataset=trainset, batch_size=2, shuffle=False, drop_last=True)


# Encoder和Decoder模型
## 编码网络
class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, 3, 2, 1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 32, 3, 2, 1),
            nn.ReLU(),
            nn.BatchNorm2d(32)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, 2, 1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
        )
        self.layer3 = nn.Sequential(
            nn.Linear(64 * 4 * 4, 16),
            nn.Sigmoid()
        )

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = torch.reshape(out, [out.size(0), -1])
        out = self.layer3(out)
        return out


## 解码网络
class Decoder(nn.Module):
    def __init__(self):
        super(Decoder, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(16, 64 * 4 * 4),
            nn.BatchNorm1d(64 * 4 * 4),
            nn.ReLU(inplace=True)
        )
        self.layer2 = nn.Sequential(
            nn.ConvTranspose2d(64, 32, 3, 2, 1, 1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.ConvTranspose2d(32, 32, 3, 2, 1, 1),
            nn.ReLU(),
            nn.BatchNorm2d(32)
        )
        self.layer3 = nn.Sequential(
            nn.ConvTranspose2d(32, 3, 3, 2, 1, 1),
            nn.ReLU()
        )

    def forward(self, x):
        out = self.layer1(x)
        out = torch.reshape(out, [out.size(0), 64, 4, 4])
        out = self.layer2(out)
        out = self.layer3(out)
        return out

# 自编码器训练
def sae_train():
    # 初始化模型
    encoder = Encoder()
    decoder = Decoder()
    # Loss 函数和优化器
    loss_func = nn.MSELoss()
    en_optimizer = torch.optim.Adam(encoder.parameters())
    de_optimizer = torch.optim.Adam(decoder.parameters())

    for i in range(epoch):
        for step, (image, label) in enumerate(train_loader):
            image = Variable(image)
            output = encoder(image)
            output = decoder(output)
            loss = loss_func(image, output)
            en_optimizer.zero_grad()
            de_optimizer.zero_grad()
            loss.backward()
            en_optimizer.step()
            de_optimizer.step()

            if (step + 1) % 5 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(i + 1, epoch, step + 1, len(train_loader),
                                                                         loss.item()))
    print('finish train')

    # 存储训练好的数据
    torch.save(encoder.state_dict(), "../model/en_net/hua.pth")
    torch.save(decoder.state_dict(), "../model/de_net/hua.pth")
    # 调用数据
    # encoder.load_state_dict(torch.load('./data/en_net.pth'))
    # decoder.load_state_dict(torch.load('./data/de_net.pth'))
    return encoder, decoder


#sae_train()