import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, SequentialSampler


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


encoder = Encoder()
decoder = Decoder()


# 对模型进行测试
def sae_test(img, test_loader):
    # encoder, decoder = sae_train()
    with torch.no_grad():
        loss_list = []
        loss_func = nn.MSELoss()
        img = Variable(img[0])
        for i, (image, label) in enumerate(test_loader):
            image = Variable(image)
            output = encoder(image)
            output = decoder(output)
            sim1 = torch.cosine_similarity(output[0], img)
            sim2 = torch.cosine_similarity(output[1], img)
            loss1 = loss_func(output[0], img)
            loss2 = loss_func(output[1], img)
            loss_list.append((i, 0, loss1.item(), sim1, np.mean(abs(sim1.cpu().numpy())[0])))
            loss_list.append((i, 1, loss2.item(), sim2, np.mean(abs(sim2.cpu().numpy())[0])))
        print('finish test')

    # 对得到的数据进行排序，找到最像的八个
    sorted_list = sorted(loss_list, key=lambda x: x[2], reverse=False)[:5]
    sim_list = []
    for l in sorted_list:
        sim_list.append(1 - l[2])
    return sorted_list, sim_list


# 以图搜图
def search_pic(img, test_loader):
    # 对模型进行测试，获得损失率和sim
    sorted_list, sim_list = sae_test(img, test_loader)

    # 寻找相似度最高的前五个图片
    img_list = []
    for j in range(3):
        img_num = sorted_list[j][0] * 2 + sorted_list[j][1] + 1
        img_num_new = str(img_num).zfill(4)
        img_list.append(img_num_new)
    return img_list, sim_list


# 随机选择一个数
def run(variety, style, theNum):
    print(variety, theNum)
    theNum = int(theNum)
    # 加载数据集
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))])

    root1 = "static/image/dataset/commond/" + variety
    root2 = "static/image/dataset/search/" + variety + "/" + style
    trainset = ImageFolder(root=root1, transform=transform)
    testset = ImageFolder(root=root2, transform=transform)
    test_loader = DataLoader(dataset=trainset, batch_size=2, shuffle=False, drop_last=True,
                             sampler=SequentialSampler(trainset))
    encoder.load_state_dict(
        torch.load('static/model/en_net/' + variety + '.pth'))
    decoder.load_state_dict(
        torch.load('static/model/de_net/' + variety + '.pth'))

    img_list, sim_list = search_pic(testset[theNum - 1], test_loader)
    print(img_list)
    return img_list, sim_list