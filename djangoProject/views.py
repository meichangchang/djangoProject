import os
import re
from djangoProject import predict
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import auth
from django import forms  # 导入表单
from django.contrib.auth.models import User  # 导入django自带的user表


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密_码', widget=forms.PasswordInput())


def index(request):
    return render(request, 'index.html')

def history(request):
    return render(request, 'history.html')

def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)  # 包含用户名和密码
        if uf.is_valid():
            # 获取表单数据
            username = uf.cleaned_data['username']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = uf.cleaned_data['password']
            # 添加到数据库
            # registAdd = User.objects.get_or_create(username=username,password=password)
            registAdd = User.objects.create_user(username=username, password=password)
            # print registAdd
            if registAdd == False:
                return render(request, 'share1.html', {'registAdd': registAdd, 'username': username})

            else:
                # return HttpResponse('ok')
                return render(request, 'share1.html', {'registAdd': registAdd})
                # return render_to_response('share.html',{'registAdd':registAdd},context_instance = RequestContext(request))
    else:
        # 如果不是post提交数据，就不传参数创建对象，并将对象返回给前台，直接生成input标签，内容为空
        uf = UserForm()
    # return render_to_response('regist.html',{'uf':uf},context_instance = RequestContext(request))
    return render(request, 'regist1.html', {'uf': uf})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        re = auth.authenticate(username=username, password=password)  # 用户认证
        if re is not None:  # 如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
            auth.login(request, re)  # 登陆成功
            return redirect('/', {'user': re})  # 跳转--redirect指从一个旧的url转到一个新的url
        else:  # 数据库里不存在与之对应的数据
            return render(request, 'login.html', {'login_error': '用户名或密码错误'})  # 注册失败
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'main.html')
def hello(request):
    return HttpResponse('“xxxx”室内智能装修系统欢迎您')


def hello_button(request):
    return render(request, 'main.html')


def hello_bikeng(request):
    return render(request, 'decoratingTips.html')


def hello_button_one(request):
    if request.POST:  # 如果数据提交
        area = request.POST.get('text', ' ')
        text1 = request.POST.get('text1', ' ')
        text2 = request.POST.get('text2', ' ')
        text3 = request.POST.get('text3', ' ')
        text4 = request.POST.get('text4', ' ')
        area1 = request.POST.get('area', ' ')

        value_rengong_jian = 5802 * int(text1) + 4800 * int(text2) + 3395 * int(text3) + 1769 * int(text4) + 8660
        value_cailiao_jian = 7050 * int(text1) + 5400 * int(text2) + 7989 * int(text3) + 13469 * int(text4) + 1320
        value_jiaju_jian = 15500 * int(text1) + 12300 * int(text2) + 900 * int(text3) + 2000 * int(text4) + 3300

        value_rengong_jing = 13936 * int(text1) + 11310 * int(text2) + 3422 * int(text3) + 1769 * int(text4) + 9697
        value_cailiao_jing = 13040 * int(text1) + 9000 * int(text2) + 12575 * int(text3) + 21868 * int(text4) + 2490
        value_jiaju_jing = 26600 * int(text1) + 31200 * int(text2) + 1600 * int(text3) + 5000 * int(text4) + 5500

        value_rengong_hao = 25456 * int(text1) + 20960 * int(text2) + 1769 * int(text3) + 1769 * int(text4) + 9697
        value_cailiao_hao = 21350 * int(text1) + 16800 * int(text2) + 21868 * int(text3) + 35048 * int(text4) + 4180
        value_jiaju_hao = 40000 * int(text1) + 54100 * int(text2) + 5000 * int(text3) + 13000 * int(text4) + 10500

        styleList = request.session['styleList']
        print(styleList[0])
        style_valve = []
        value_style = []
        for i in range(len(styleList)):
            if styleList[i] == '北欧':
                value_rengong_jian = value_rengong_jian * 1.1
                value_rengong_jing = value_rengong_jing * 1.1
                value_rengong_hao = value_rengong_hao * 1.1
            if styleList[i] == '日式':
                value_cailiao_jian = value_cailiao_jian * 1.1
                value_cailiao_jing = value_cailiao_jing * 1.1
                value_rengong_hao = value_rengong_hao * 1.1
            if styleList[i] == '地中海':
                value_rengong_jian = value_rengong_jian * 1.1
                value_rengong_jing = value_rengong_jing * 1.1
                value_cailiao_hao = value_cailiao_hao * 1.1
            if styleList[i] == '美式':
                value_rengong_jian = value_rengong_jian * 1.1
                value_cailiao_jing = value_cailiao_jing * 1.1
                value_rengong_hao = value_rengong_hao * 1.1
            if styleList[i] == '工业':
                value_cailiao_jian = value_cailiao_jian * 1.1
                value_rengong_jing = value_rengong_jing * 1.1
                value_jiaju_hao = value_jiaju_hao * 1.1
            if styleList[i] == '中式':
                value_jiaju_jian = value_jiaju_jian * 1.1
                value_rengong_jing = value_rengong_jing * 1.1
                value_rengong_hao = value_rengong_hao * 1.1
            if styleList[i] == '简约':
                value_rengong_jian = value_rengong_jian * 1.1
                value_rengong_jing = value_rengong_jing * 1.1
                value_jiaju_hao = value_jiaju_hao * 1.1
            value_list = [[value_rengong_jian,value_cailiao_jian,value_jiaju_jian],
                          [value_rengong_jing,value_cailiao_jing,value_jiaju_jing],
                          [value_rengong_hao,value_cailiao_hao,value_jiaju_hao]]
            style_valve.append(value_list)
        print(style_valve)
        pattern = re.compile('([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市|行政区))')
        print(pattern.search(area1).group(0))

        for i in range(len(style_valve)):
            if pattern.search(area1).group(0) in ['广西壮族自治区', '西藏自治区', '新疆维吾尔自治区', '宁夏回族自治区', '内蒙古自治区']:
                value = (style_valve[i][0][0] + style_valve[i][0][1] + style_valve[i][0][2]) * 0.8
                value1 = (style_valve[i][1][0] + style_valve[i][1][1] + style_valve[i][1][2]) * 0.8
                value2 = (style_valve[i][2][0] + style_valve[i][2][1] + style_valve[i][2][2]) * 0.8

            elif pattern.search(area1).group(0) in ['北京市', '上海市', '天津市', '重庆市', '香港特别行政区', '澳门特别行政区']:
                value = (style_valve[i][0][0] + style_valve[i][0][1] + style_valve[i][0][2]) * 1.2
                value1 = (style_valve[i][1][0] + style_valve[i][1][1] + style_valve[i][1][2]) * 1.2
                value2 = (style_valve[i][2][0] + style_valve[i][2][1] + style_valve[i][2][2]) * 1.2
            else:
                value = (style_valve[i][0][0] + style_valve[i][0][1] + style_valve[i][0][2])
                value1 = (style_valve[i][1][0] + style_valve[i][1][1] + style_valve[i][1][2])
                value2 = (style_valve[i][2][0] + style_valve[i][2][1] + style_valve[i][2][2])
            value_all_list = [value, value1, value2]
            value_style.append(value_all_list)

        print(value_style)
        request.session['style_value'] = style_valve
        request.session['value'] = value_style
    return render(request, 'decorateCharge.html')


def hello_button_result(request):
    value = request.session['value']
    style_value = request.session['style_value']
    styleList = request.session['styleList']
    context1 = {'new_list': []}
    for i in range(len(styleList)):
        context1['new_list'].append({})
        context1['new_list'][i].setdefault('style', styleList[i])
        context1['new_list'][i].setdefault('value', round(value[i][0] / 10000, 2))
        context1['new_list'][i].setdefault('value1', round(value[i][1] / 10000, 2))
        context1['new_list'][i].setdefault('value2', round(value[i][2] / 10000, 2))
        context1['new_list'][i].setdefault('rengong1', round(style_value[i][0][0] / 10000, 2))
        context1['new_list'][i].setdefault('rengong2', round(style_value[i][1][0] / 10000, 2))
        context1['new_list'][i].setdefault('rengong3', round(style_value[i][2][0] / 10000, 2))
        context1['new_list'][i].setdefault('cailiao1', round(style_value[i][0][1] / 10000, 2))
        context1['new_list'][i].setdefault('cailiao2', round(style_value[i][1][1] / 10000, 2))
        context1['new_list'][i].setdefault('cailiao3', round(style_value[i][2][1] / 10000, 2))
        context1['new_list'][i].setdefault('jiaju1', round(style_value[i][0][2] / 10000, 1))
        context1['new_list'][i].setdefault('jiaju2', round(style_value[i][1][2] / 10000, 1))
        context1['new_list'][i].setdefault('jiaju3', round(style_value[i][2][2] / 10000, 1))

    print(styleList)
    print(context1)
    return render(request, 'result.html', context=context1)


def hello_button_test(request):
    if request.POST:  # 如果数据提交
        likeList = request.POST.get('likeList', ' ')
        likeList = likeList.split(',')[:-1]
        styleGrade = {}
        styleList, styleIndex, styleImg = [], [], []
        styleType = {'1': '北欧', '2': '地中海', '3': '工业', '4': '简约', '5': '美式', '6': '日式', '7': '中式'}

        for ind, style in styleType.items():
            styleGrade.setdefault(style, 0)
            for i in likeList:
                i = i.split('/')[-1]
                if ind == i[0]:
                    styleGrade[style] += 1

        maxScore = max(styleGrade.values())
        for style, score in styleGrade.items():
            if int(score) == int(maxScore):
                styleList.append(style)
        for i in styleList:
            ind = [x for x in styleType.keys() if styleType[x] == i][0]
            styleIndex.append(ind)

            for imgName in os.listdir('static/image/dataset/show'):
                if int(imgName[0]) == int(ind):
                    imgPath = os.path.join('../static/image/dataset/show', imgName)
                    styleImg.append(imgPath)

        request.session['styleList'] = styleList
        request.session['styleImg'] = styleImg
        request.session['styleType'] = styleType
    return render(request, 'styleTest.html')


def hello_button_testResult(request):
    context = {
        'news_list': [
            {
                "title": "恭喜，您的测试报告已完成！",
                "result1": "您喜欢的风格包含",
                "result2": request.session['styleList'],
            },
        ]
    }

    return render(request, 'styleTestResult.html', context=context)


def hello_button_testResult2(request):
    context = {
        'news_list': [
            {
                "text": "以下关于您喜欢的装修的推荐",
                "con": request.session['styleList'],
                "img": request.session['styleImg'],
            },
        ]
    }

    return render(request, 'styleTestResult2.html', context=context)


def hello_button_predict_one(request):
    if request.POST:  # 如果数据提交
        style = request.POST.get('submit1', None)
        request.session['style_name'] = style
        print(style)

    styleList = request.session['styleList']
    context1 = {'new_list': []}
    for i in range(len(styleList)):
        context1['new_list'].append({})
        context1['new_list'][i].setdefault('style', styleList[i])

    return render(request, 'predict_result.html', context=context1)


def hello_button_predict_two(request):
    if request.POST:  # 如果数据提交
        bt = request.POST.get('submit', None)
        if bt == '窗帘':
            bt = 'lian'
        if bt == '吊灯':
            bt = 'deng'
        if bt == '床':
            bt = 'chuang'
        if bt == '地毯':
            bt = 'tan'
        if bt == '壁画':
            bt = 'hua'
        if bt == '衣柜':
            bt = 'gui'
        if bt == '书桌':
            bt = 'shu'
        if bt == '床单被套':
            bt = 'dan'
        if bt == '餐桌':
            bt = 'zhuo'
        if bt == '沙发':
            bt = 'sha'
        if bt == '摆件':
            bt = 'bai'
        if bt == '椅子':
            bt = 'yi'
        request.session['style_button'] = bt
    return render(request, 'predict_result_two.html')


def hello_button_search(request):
    if request.POST:  # 如果数据提交
        a = request.POST.get('asub', None)
        if a == 'more:one':
            a = request.session['test0']
        if a == 'more:two':
            a = request.session['test1']
        if a == 'more:three':
            a = request.session['test2']
        request.session['img'] = a

    import random
    r = random.sample(range(1, 11), 3)
    for i in range(3):
        ran = 'test' + str(i)
        request.session[ran] = str(r[i]).zfill(4)
    context = {
        'news_list': [
            {
                "text": "以下关于您喜欢的装修风格的物品推荐",
                "con": request.session['style_name'],
                "itemChoose": request.session['style_button'],
                "style": request.session['style_name'],
                "img0": request.session['test0'],
                "img1": request.session['test1'],
                "img2": request.session['test2'],
            },
        ]
    }
    return render(request, 'search.html', context=context)


def hello_button_searchResult(request):
    style = request.session['style_name']
    variety = request.session['style_button']
    img = request.session['img']
    img_list, sim_list = predict.run(variety, style, img)

    request.session['img_list'] = img_list
    request.session['sim_list'] = sim_list

    context = {
        'news_list': [
            {
                "text": "以下是相似物品推荐",
                "itemChoose": request.session['style_button'],
                "style": request.session['style_name'],
                "con": request.session['img_list'],
                "sim1": "下列图片相似度分别为：",
                "sim2": request.session['sim_list'],
                "img": request.session['img']
            },
        ]
    }

    return render(request, 'searchResult.html', context=context)


