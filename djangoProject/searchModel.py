import numpy as np
import random
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.autograd import Variable
from torch.utils.data import DataLoader
from djangoProject.search import Encoder
from djangoProject.search import Decoder

# 配置参数
epoch = 120
batch_size = 32
learning_rate = 0.1

# 加载数据集
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))])

trainset = ImageFolder(root="../static/image/dataset/search/hua", transform=transform)
testset = ImageFolder(root="../static/image/dataset/search/hua", transform=transform)
train_loader = DataLoader(dataset=trainset, batch_size=128, shuffle=True, drop_last=True)
test_loader = DataLoader(dataset=trainset, batch_size=2, shuffle=False, drop_last=True)


# 对模型进行测试
def sae_test(img):
    with torch.no_grad():
        loss_list = []
        loss_func = nn.MSELoss()
        img = Variable(img[0]).cuda()
        for i, (image, label) in enumerate(test_loader):
            image = Variable(image).cuda()
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
    sorted_list = sorted(loss_list, key=lambda x: x[2], reverse=False)[:8]
    sim_list = []
    for l in sorted_list:
        sim_list.append(1 - l[2])
    return sorted_list, sim_list


# 以图搜图
def search_pic(img):
    # 对模型进行测试，获得损失率和sim
    sorted_list, sim_list = sae_test(img)

    # 寻找相似度最高的前八个图片
    img_list = []
    for j in range(8):
        img_list.append(sorted_list[j][0] * 2 + sorted_list[j][1])

    return img_list


if __name__ == '__main__':
    encoder = Encoder().cuda()
    decoder = Decoder().cuda()
    encoder.load_state_dict(torch.load('../static/model/en_net_100hua.pth'))
    decoder.load_state_dict(torch.load('../static/model/de_net_100hua.pth'))
    # 随机选择一个数
    random_nums = int(random.randint(0, len(testset)))
    img_list = search_pic(testset[random_nums])